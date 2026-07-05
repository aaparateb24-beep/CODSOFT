import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import streamlit as st
import numpy as np

class BlipCaptioner:
    """
    Manages loading and inference for the Salesforce/blip-image-captioning-base model.
    Includes log-probability tracking to compute caption confidence scores.
    """
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor, self.model = self._load_model()

    @st.cache_resource
    def _load_model(_self):
        """Loads processor and model from Hugging Face and caches them in Streamlit."""
        processor = BlipProcessor.from_pretrained(_self.model_name)
        model = BlipForConditionalGeneration.from_pretrained(_self.model_name).to(_self.device)
        return processor, model

    def generate_caption(self, image: Image.Image) -> tuple[str, float]:
        """
        Generates a natural language caption for the image and calculates a confidence score
        based on the average probability of the generated tokens.
        
        Args:
            image: A PIL Image object.
        Returns:
            A tuple of (caption, confidence_score) where confidence is between 0.0 and 1.0.
        """
        try:
            # Preprocess image
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            
            # Generate caption with scores enabled
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=50,
                    return_dict_in_generate=True,
                    output_scores=True,
                    num_beams=3 # standard beam search
                )
                
            # Decode the tokens to get the text
            generated_ids = outputs.sequences[0]
            caption = self.processor.decode(generated_ids, skip_special_tokens=True)
            
            # Calculate token-level confidence score
            # outputs.scores is a tuple of size (generated_tokens_count)
            # each element is a tensor of shape (num_beams * batch_size, vocab_size) or (batch_size, vocab_size)
            confidence = 0.85 # Fallback baseline
            
            if hasattr(outputs, 'scores') and len(outputs.scores) > 0:
                probs_list = []
                # Map generated token IDs back (skipping prompt/special tokens if needed)
                # For BLIP conditional generation, outputs.sequences starts with bos token (id = 30522 or similar)
                # outputs.scores contains logits for tokens starting from index 1 of outputs.sequences
                token_ids = generated_ids[1:] # Align scores with sequence tokens
                
                for i, score_tensor in enumerate(outputs.scores):
                    if i >= len(token_ids):
                        break
                    
                    # We compute softmax over the logits of the first batch element
                    # In beam search, scores shape might contain beams. We take the first row or slice.
                    logits = score_tensor[0]
                    probs = torch.softmax(logits, dim=-1)
                    
                    # Get the ID of the actual generated token
                    actual_token_id = token_ids[i].item()
                    
                    # Ensure token is in range
                    if actual_token_id < len(probs):
                        token_prob = probs[actual_token_id].item()
                        probs_list.append(token_prob)
                
                if probs_list:
                    # Arithmetic mean of the token probabilities
                    confidence = float(np.mean(probs_list))
            
            # Clean up CPU/GPU memory
            del inputs
            if self.device == "cuda":
                torch.cuda.empty_cache()
                
            return caption.strip(), round(confidence, 4)
            
        except Exception as e:
            # Fallback error handling
            print(f"Error during BLIP caption generation: {e}")
            return "Failed to generate caption due to model error.", 0.0
