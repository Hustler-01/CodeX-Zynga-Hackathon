import cv2
import numpy as np
from typing import Optional, Tuple

class FaceDetector:
    def __init__(self, prototxt_path: str, model_path: str):
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        self.min_confidence = 0.5
    
    def detect_largest_face(self, image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)),
            1.0, (300, 300), (104.0, 177.0, 123.0)
        )
        self.net.setInput(blob)
        detections = self.net.forward()
        
        best_face = None
        max_area = 0
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.min_confidence:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                area = (endX - startX) * (endY - startY)
                if area > max_area:
                    max_area = area
                    best_face = (startX, startY, endX, endY)
        
        return best_face

    def get_face_quality(self, image: np.ndarray, face_coords: Tuple[int, int, int, int]) -> float:
        (startX, startY, endX, endY) = face_coords
        face = image[startY:endY, startX:endX]
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        return min(1.0, max(0.0, (fm - 10) / 200))
