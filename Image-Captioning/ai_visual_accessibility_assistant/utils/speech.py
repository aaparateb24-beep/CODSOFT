import os
import threading
import logging
from gtts import gTTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lock for pyttsx3 to prevent thread-safety issues in Streamlit
pyttsx3_lock = threading.Lock()

def generate_speech(text: str, output_path: str, prefer_gtts: bool = True) -> bool:
    """
    Generates an audio file from text.
    First tries preferred option, then falls back to the other option if errors occur.
    
    Args:
        text: The text to narrate.
        output_path: Target filepath for the audio (typically .mp3 or .wav).
        prefer_gtts: If True, uses gTTS first; if False, uses pyttsx3 first.
    Returns:
        True if speech generation succeeded, False otherwise.
    """
    # Ensure parent directory exists
    dir_name = os.path.dirname(output_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    if prefer_gtts:
        logger.info("Attempting speech generation with gTTS...")
        success = _generate_with_gtts(text, output_path)
        if not success:
            logger.warning("gTTS failed. Falling back to pyttsx3...")
            success = _generate_with_pyttsx3(text, output_path)
        return success
    else:
        logger.info("Attempting speech generation with pyttsx3...")
        success = _generate_with_pyttsx3(text, output_path)
        if not success:
            logger.warning("pyttsx3 failed. Falling back to gTTS...")
            success = _generate_with_gtts(text, output_path)
        return success

def _generate_with_gtts(text: str, output_path: str) -> bool:
    """Generates audio file using gTTS (Google Text-To-Speech)."""
    try:
        # Enforce .mp3 extension for gTTS
        if not output_path.endswith('.mp3'):
            base, _ = os.path.splitext(output_path)
            output_path = base + '.mp3'
            
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        logger.info(f"Successfully saved gTTS audio to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error during gTTS generation: {e}")
        return False

def _generate_with_pyttsx3(text: str, output_path: str) -> bool:
    """Generates audio file using pyttsx3 (SAPI5 offline engine)."""
    # Import inside function to prevent loading issues if the library isn't working
    try:
        import pyttsx3
    except ImportError:
        logger.error("pyttsx3 is not installed.")
        return False

    # We wrap the engine operations in a lock because pyttsx3 is not thread-safe.
    with pyttsx3_lock:
        engine = None
        try:
            # We initialize and use it in a local scope to avoid global loop issues
            engine = pyttsx3.init()
            
            # Adjust properties
            engine.setProperty('rate', 150)  # Speed (words per minute)
            engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            
            # SAPI5 supports .wav natively. If saving with pyttsx3, it's safer to save as .wav
            # and let the Streamlit audio player handle it.
            if output_path.endswith('.mp3'):
                # Note: Windows SAPI5 may complain when writing to .mp3 directly, so we can save to .wav
                # and return it. But we'll try output_path first.
                pass
                
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            
            # Clean up the engine immediately
            del engine
            
            # Verify file was written and is not empty
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"Successfully saved pyttsx3 audio to {output_path}")
                return True
            else:
                logger.error("pyttsx3 output file is empty or missing.")
                return False
        except Exception as e:
            logger.error(f"Error during pyttsx3 generation: {e}")
            if engine:
                try:
                    del engine
                except:
                    pass
            return False
