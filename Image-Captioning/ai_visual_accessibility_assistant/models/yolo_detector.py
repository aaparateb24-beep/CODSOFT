import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
import streamlit as st
from typing import List, Dict, Any, Tuple

class YoloDetector:
    """
    Manages loading and running the YOLOv8 object detection model.
    Handles drawing bounding boxes and returning metadata of detected objects.
    """
    def __init__(self, model_name: str = "yolov8n.pt"):
        self.model_name = model_name
        self.model = self._load_model()

    @st.cache_resource
    def _load_model(_self):
        """Loads and caches the YOLOv8 model weights."""
        model = YOLO(_self.model_name)
        return model

    def detect_objects(self, image: Image.Image) -> Tuple[Image.Image, List[Dict[str, Any]]]:
        """
        Runs object detection on the provided PIL Image.
        
        Args:
            image: A PIL Image object.
        Returns:
            A tuple of (annotated_image, detections_list)
            where detections_list is a list of dicts:
            [{"name": "dog", "confidence": 0.92, "bbox": [x1, y1, x2, y2]}, ...]
        """
        try:
            # Convert PIL Image to OpenCV (numpy array, RGB)
            img_np = np.array(image.convert("RGB"))
            
            # Run inference
            # We pass verbose=False to keep terminal logs clean
            results = self.model(img_np, verbose=False)
            
            detections = []
            
            # If no results returned
            if not results or len(results) == 0:
                return image, []
            
            result = results[0]
            
            # Extract detections for database and display
            for box in result.boxes:
                # Bbox coordinates
                coords = box.xyxy[0].cpu().numpy().tolist()  # [x1, y1, x2, y2]
                conf = float(box.conf[0].cpu().numpy())
                cls_id = int(box.cls[0].cpu().numpy())
                class_name = self.model.names[cls_id]
                
                detections.append({
                    "name": class_name,
                    "confidence": round(conf, 4),
                    "bbox": [round(c, 2) for c in coords]
                })
            
            # Generate annotated image
            # result.plot() returns a numpy array of the image with bounding boxes drawn (BGR format)
            annotated_bgr = result.plot()
            
            # Convert BGR back to RGB for PIL/Streamlit compatibility
            annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
            annotated_image = Image.fromarray(annotated_rgb)
            
            return annotated_image, detections
            
        except Exception as e:
            print(f"Error during YOLOv8 detection: {e}")
            return image, []
