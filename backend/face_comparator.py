import numpy as np
from typing import Tuple, Dict

class FaceComparator:
    def __init__(self, threshold: float = 0.65):
        self.threshold = threshold
        self.similarity_cache = {}

    def compare_embeddings(self, embedding1: np.ndarray, embedding2: np.ndarray) -> Tuple[bool, float]:
        similarity = np.dot(embedding1, embedding2)
        return (similarity > self.threshold, similarity)

    def generate_verification_report(self, similarity: float, quality_score1: float, quality_score2: float) -> Dict:
        confidence = self._calculate_confidence(similarity, quality_score1, quality_score2)
        return {
         'match': bool(similarity > self.threshold),

         'confidence': round(float(similarity),2),  # 🔁 renamed from 'similarity'
         'quality': {
           'id_quality': round(quality_score1,2),
           'selfie_quality': round(quality_score2,2),
           'overall_quality': min(quality_score1, quality_score2)
          },
         'threshold': self.threshold
       }

    def _calculate_confidence(self, similarity: float, quality1: float, quality2: float) -> float:
        base_confidence = (similarity + 1) / 2
        quality_factor = np.sqrt(quality1 * quality2)
        return min(100.0, max(0.0, base_confidence * quality_factor * 100))
