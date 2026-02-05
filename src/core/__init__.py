"""
The Judge - Core Module
========================
Componentes principais: embeddings e similaridade.
"""

from .embeddings import CLIPEncoder, get_encoder
from .similarity import (
    cosine_similarity,
    cosine_similarity_batch,
    compare_text_to_images,
    rank_targets,
    calculate_confidence
)

__all__ = [
    # Embeddings
    "CLIPEncoder",
    "get_encoder",
    # Similarity
    "cosine_similarity",
    "cosine_similarity_batch",
    "compare_text_to_images",
    "rank_targets",
    "calculate_confidence",
]
