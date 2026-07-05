import os
import json
import logging
from typing import Dict, Any, List, Tuple
from PIL import Image
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Manages communication with Google's Gemini 1.5 Flash API to perform
    multimodal image reasoning, detailed accessibility descriptions, and VQA.
    """
    def __init__(self, api_key: str = None):
        # Resolve API Key: passed parameter -> environment variable
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.warning("Gemini API Key not set. Gemini features will be unavailable.")
            
        self.model_name = "gemini-2.5-flash"
        self.model = genai.GenerativeModel(self.model_name)

    def is_configured(self) -> bool:
        """Checks if the API key is set."""
        return bool(self.api_key)

    def set_api_key(self, api_key: str):
        """Allows dynamically setting the API key at runtime."""
        self.api_key = api_key
        genai.configure(api_key=api_key)

    def get_scene_understanding(self, image: Image.Image) -> Dict[str, Any]:
        """
        Categorizes the image setting and provides a textual explanation.
        """
        if not self.is_configured():
            return {"category": "N/A", "explanation": "Gemini API key is missing."}
            
        prompt = (
            "Analyze this image and identify which category best describes it. "
            "Choose from: Indoor, Outdoor, Urban, Nature, Office, Classroom, Beach, Forest, Street, or a custom specific setting. "
            "Provide a brief, detailed explanation of why. "
            "You must return your response in JSON format with exactly two keys: "
            "'category' (string) and 'explanation' (string)."
        )
        
        try:
            # We request JSON using generation_config
            response = self.model.generate_content(
                [image, prompt],
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            return {
                "category": data.get("category", "Unknown"),
                "explanation": data.get("explanation", "No explanation provided.")
            }
        except Exception as e:
            logger.error(f"Error in Gemini Scene Understanding: {e}")
            # Fallback parsing in case JSON config fails
            try:
                # Direct generation without JSON format enforcement
                response = self.model.generate_content([image, "Classify this image into Indoor, Outdoor, Urban, Nature, Office, Classroom, Beach, Forest, Street. Then explain why."])
                text = response.text
                return {"category": "Undetermined", "explanation": text}
            except Exception as inner_e:
                return {"category": "Error", "explanation": f"API Error: {str(inner_e)}"}

    def get_accessibility_description(self, image: Image.Image) -> str:
        """
        Generates a highly detailed description tailored for visually impaired users.
        """
        if not self.is_configured():
            return "Gemini API key is missing. Cannot generate detailed description."
            
        prompt = (
            "You are an expert accessibility assistant. Generate a highly detailed description of this image "
            "specifically designed for a visually impaired user. "
            "Describe the overall setting, lighting, main subjects (objects/people), their relative positions "
            "(foreground, background, left, right), colors, emotions/expressions of people if visible, and "
            "any readable text or signage. Do not use vague words. Provide a structured, cohesive paragraph."
        )
        
        try:
            response = self.model.generate_content([image, prompt])
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error in Gemini Accessibility Description: {e}")
            return f"Failed to generate description. Error: {str(e)}"

    def get_ai_summary(self, image: Image.Image, caption: str, objects: List[str], scene_category: str) -> str:
        """
        Generates a cohesive human-friendly summary of the image by combining
        YOLO predictions, BLIP captions, and Gemini vision reasoning.
        """
        if not self.is_configured():
            return "Gemini API key is missing. Cannot generate AI Summary."
            
        objects_str = ", ".join(objects) if objects else "none detected"
        prompt = (
            f"Generate a concise, human-friendly summary of this image in 1 or 2 sentences. "
            f"Here is some preliminary metadata we detected:\n"
            f"- Preliminary Caption: {caption}\n"
            f"- Objects detected by computer vision: {objects_str}\n"
            f"- Scene Setting: {scene_category}\n\n"
            f"Combine these findings with your visual analysis to output a clean, descriptive summary sentence."
        )
        
        try:
            response = self.model.generate_content([image, prompt])
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error in Gemini AI Summary: {e}")
            return f"Failed to generate AI Summary. Error: {str(e)}"

    def get_ai_insights(self, image: Image.Image) -> Dict[str, str]:
        """
        Extracts structural insights about the subject, activity, environment, and situational context.
        """
        default_insights = {
            "main_subject": "N/A",
            "activity": "N/A",
            "environment": "N/A",
            "context": "N/A",
            "use_case": "N/A"
        }
        
        if not self.is_configured():
            return default_insights
            
        prompt = (
            "Analyze this image and extract structural insights. "
            "You must return your response in JSON format with exactly these keys:\n"
            "- 'main_subject': The primary focal object, animal, or person.\n"
            "- 'activity': The main action or event occurring.\n"
            "- 'environment': The specific setting or background details.\n"
            "- 'context': The overall situational or emotional context.\n"
            "- 'use_case': A practical way a visually impaired user could use this information in daily life.\n"
        )
        
        try:
            response = self.model.generate_content(
                [image, prompt],
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            return {
                "main_subject": data.get("main_subject", "Unknown"),
                "activity": data.get("activity", "Unknown"),
                "environment": data.get("environment", "Unknown"),
                "context": data.get("context", "Unknown"),
                "use_case": data.get("use_case", "Unknown")
            }
        except Exception as e:
            logger.error(f"Error in Gemini AI Insights: {e}")
            return default_insights

    def answer_question(self, image: Image.Image, question: str, chat_history: List[Tuple[str, str]]) -> str:
        """
        Answers a specific question about the image, considering the chat history.
        
        Args:
            image: PIL Image object.
            question: The user's new question.
            chat_history: List of tuples (user_message, assistant_response).
        """
        if not self.is_configured():
            return "Gemini API key is missing. Cannot perform visual question answering."
            
        # Format the chat history for context
        history_formatted = ""
        for user_msg, assist_msg in chat_history:
            history_formatted += f"User: {user_msg}\nAssistant: {assist_msg}\n\n"
            
        prompt = (
            f"You are an AI Accessibility Assistant helping a visually impaired user understand an image.\n"
            f"Answer the user's question politely and accurately based on the visual contents of the image.\n\n"
            f"Here is the dialogue history of your conversation so far:\n"
            f"{history_formatted}"
            f"Current User Question: {question}\n\n"
            f"Please respond directly and concisely to the question."
        )
        
        try:
            response = self.model.generate_content([image, prompt])
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error in Gemini VQA: {e}")
            return f"Could not generate an answer. Error: {str(e)}"
