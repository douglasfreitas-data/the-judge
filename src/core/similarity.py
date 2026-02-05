"""
The Judge - Similarity Module
==============================
Funções para cálculo de similaridade entre embeddings.
"""

import numpy as np
from typing import List, Tuple, Dict, Union


def cosine_similarity(embedding_a: np.ndarray, embedding_b: np.ndarray) -> float:
    """
    Calcula similaridade de cosseno entre dois embeddings.
    
    Como os embeddings do CLIPEncoder já são normalizados L2,
    o produto escalar é equivalente à similaridade de cosseno.
    
    Args:
        embedding_a: Vetor numpy (D,)
        embedding_b: Vetor numpy (D,)
        
    Returns:
        Float entre -1 e 1 (1 = idênticos, 0 = ortogonais, -1 = opostos)
    """
    return float(np.dot(embedding_a, embedding_b))


def cosine_similarity_batch(
    query: np.ndarray,
    candidates: np.ndarray
) -> np.ndarray:
    """
    Calcula similaridade entre um query e múltiplos candidatos.
    
    Args:
        query: Vetor numpy (D,)
        candidates: Matriz numpy (N, D)
        
    Returns:
        Array numpy (N,) com scores de similaridade
    """
    return candidates @ query


def compare_text_to_images(
    text_embedding: np.ndarray,
    image_embeddings: List[np.ndarray]
) -> List[Tuple[int, float]]:
    """
    Compara um embedding de texto com múltiplos embeddings de imagem.
    
    Args:
        text_embedding: Vetor (512,) do texto
        image_embeddings: Lista de vetores (512,) das imagens
        
    Returns:
        Lista de tuplas (índice, score) ordenada por score decrescente
    """
    scores = []
    for idx, img_emb in enumerate(image_embeddings):
        score = cosine_similarity(text_embedding, img_emb)
        scores.append((idx, score))
    
    # Ordena por score (maior primeiro)
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


def rank_targets(
    session_embedding: np.ndarray,
    target_a_embedding: np.ndarray,
    target_b_embedding: np.ndarray
) -> Tuple[str, Dict[str, float]]:
    """
    Determina qual alvo (A ou B) melhor corresponde à sessão.
    
    Esta é a função principal de julgamento do The Judge.
    
    Args:
        session_embedding: Embedding da descrição/esboço do visualizador
        target_a_embedding: Embedding da imagem alvo A
        target_b_embedding: Embedding da imagem alvo B
        
    Returns:
        Tupla com:
        - winner: 'A' ou 'B' (ou 'TIE' se diferença < threshold)
        - scores: Dict com scores detalhados
    """
    score_a = cosine_similarity(session_embedding, target_a_embedding)
    score_b = cosine_similarity(session_embedding, target_b_embedding)
    
    # Calcula diferença e margem de confiança
    difference = abs(score_a - score_b)
    
    # Threshold para considerar empate (muito próximos)
    TIE_THRESHOLD = 0.02
    
    if difference < TIE_THRESHOLD:
        winner = "TIE"
    elif score_a > score_b:
        winner = "A"
    else:
        winner = "B"
    
    return winner, {
        "score_a": score_a,
        "score_b": score_b,
        "difference": difference,
        "winner": winner
    }


def calculate_confidence(score_a: float, score_b: float) -> float:
    """
    Calcula nível de confiança da predição baseado na diferença de scores.
    
    Quanto maior a diferença entre os scores, maior a confiança.
    
    Args:
        score_a: Score do alvo A
        score_b: Score do alvo B
        
    Returns:
        Float entre 0 e 1 indicando confiança (1 = muito confiante)
    """
    difference = abs(score_a - score_b)
    
    # Escala logarítmica para confiança
    # Diferença de 0.1 → ~50% confiança
    # Diferença de 0.3 → ~90% confiança
    confidence = 1 - np.exp(-difference * 10)
    
    return float(min(1.0, max(0.0, confidence)))
