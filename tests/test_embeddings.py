"""
The Judge - Embeddings Tests
=============================
Testes unitários para o módulo de embeddings CLIP.
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock

# Para testes unitários, importamos diretamente do módulo sem passar pelo __init__.py
# Isso evita carregar open_clip que é pesado e pode não estar instalado
import sys
import importlib.util


def import_similarity_directly():
    """Importa similarity.py diretamente sem passar pelo __init__.py"""
    spec = importlib.util.spec_from_file_location(
        "similarity",
        "src/core/similarity.py"
    )
    similarity = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(similarity)
    return similarity


class TestCLIPEncoderUnit:
    """Testes unitários que não carregam o modelo real (rápidos)."""
    
    @pytest.fixture(autouse=True)
    def setup_similarity(self):
        """Carrega o módulo similarity diretamente."""
        self.similarity = import_similarity_directly()
    
    def test_cosine_similarity_identical(self):
        """Vetores idênticos devem ter similaridade 1."""
        vec = np.array([1, 0, 0, 0], dtype=np.float32)
        vec = vec / np.linalg.norm(vec)
        
        assert abs(self.similarity.cosine_similarity(vec, vec) - 1.0) < 1e-6
    
    def test_cosine_similarity_orthogonal(self):
        """Vetores ortogonais devem ter similaridade 0."""
        vec_a = np.array([1, 0, 0, 0], dtype=np.float32)
        vec_b = np.array([0, 1, 0, 0], dtype=np.float32)
        
        assert abs(self.similarity.cosine_similarity(vec_a, vec_b)) < 1e-6
    
    def test_cosine_similarity_opposite(self):
        """Vetores opostos devem ter similaridade -1."""
        vec_a = np.array([1, 0, 0, 0], dtype=np.float32)
        vec_b = np.array([-1, 0, 0, 0], dtype=np.float32)
        
        assert abs(self.similarity.cosine_similarity(vec_a, vec_b) + 1.0) < 1e-6
    
    def test_rank_targets_winner_a(self):
        """Deve retornar A quando score_a > score_b."""
        session = np.array([1, 0, 0, 0], dtype=np.float32)
        target_a = np.array([0.9, 0.1, 0, 0], dtype=np.float32)
        target_b = np.array([0.1, 0.9, 0, 0], dtype=np.float32)
        
        # Normaliza
        target_a = target_a / np.linalg.norm(target_a)
        target_b = target_b / np.linalg.norm(target_b)
        
        winner, scores = self.similarity.rank_targets(session, target_a, target_b)
        
        assert winner == "A"
        assert scores["score_a"] > scores["score_b"]
    
    def test_rank_targets_winner_b(self):
        """Deve retornar B quando score_b > score_a."""
        session = np.array([0, 1, 0, 0], dtype=np.float32)
        target_a = np.array([1, 0, 0, 0], dtype=np.float32)
        target_b = np.array([0, 1, 0, 0], dtype=np.float32)
        
        winner, scores = self.similarity.rank_targets(session, target_a, target_b)
        
        assert winner == "B"
        assert scores["score_b"] > scores["score_a"]
    
    def test_rank_targets_tie(self):
        """Deve retornar TIE quando scores são muito próximos."""
        session = np.array([0.5, 0.5, 0, 0], dtype=np.float32)
        session = session / np.linalg.norm(session)
        
        target_a = np.array([0.51, 0.49, 0, 0], dtype=np.float32)
        target_a = target_a / np.linalg.norm(target_a)
        
        target_b = np.array([0.49, 0.51, 0, 0], dtype=np.float32)
        target_b = target_b / np.linalg.norm(target_b)
        
        winner, scores = self.similarity.rank_targets(session, target_a, target_b)
        
        assert winner == "TIE"
    
    def test_calculate_confidence_high(self):
        """Diferença grande deve gerar alta confiança."""
        conf = self.similarity.calculate_confidence(0.8, 0.3)
        assert conf > 0.9
    
    def test_calculate_confidence_low(self):
        """Diferença pequena deve gerar baixa confiança."""
        conf = self.similarity.calculate_confidence(0.51, 0.49)
        assert conf < 0.3


@pytest.mark.integration
class TestCLIPEncoderIntegration:
    """
    Testes de integração que carregam o modelo real.
    
    Estes testes são mais lentos (carregam ~400MB de modelo).
    Execute com: pytest -m integration
    """
    
    @pytest.fixture(scope="class")
    def encoder(self):
        """Fixture que cria encoder uma vez para toda a classe."""
        from src.core.embeddings import CLIPEncoder
        return CLIPEncoder()
    
    def test_encode_text_returns_correct_shape(self, encoder):
        """Embedding de texto deve ter shape (512,)."""
        embedding = encoder.encode_text("hello world")
        assert embedding.shape == (512,)
    
    def test_encode_text_is_normalized(self, encoder):
        """Embedding deve ter norma L2 = 1."""
        embedding = encoder.encode_text("uma praia ensolarada")
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 1e-5
    
    def test_similar_texts_have_high_similarity(self, encoder):
        """Textos similares devem ter alta similaridade."""
        similarity = import_similarity_directly()
        
        emb_a = encoder.encode_text("a dog running in the park")
        emb_b = encoder.encode_text("a puppy playing in the garden")
        
        sim = similarity.cosine_similarity(emb_a, emb_b)
        assert sim > 0.6
    
    def test_different_concepts_have_lower_similarity(self, encoder):
        """Conceitos diferentes devem ter similaridade MENOR que conceitos relacionados."""
        similarity = import_similarity_directly()
        
        # Conceitos relacionados
        emb_dog = encoder.encode_text("a cute puppy")
        emb_pet = encoder.encode_text("a friendly pet dog")
        sim_related = similarity.cosine_similarity(emb_dog, emb_pet)
        
        # Conceitos não relacionados
        emb_puppy = encoder.encode_text("a cute puppy")
        emb_building = encoder.encode_text("a modern skyscraper in the city")
        sim_unrelated = similarity.cosine_similarity(emb_puppy, emb_building)
        
        # CLIP pode ter alta similaridade base, mas relacionados > não relacionados
        assert sim_related > sim_unrelated
    
    def test_encode_multiple_texts(self, encoder):
        """Batch de textos deve retornar matriz (N, 512)."""
        texts = ["hello", "world", "test"]
        embeddings = encoder.encode_text(texts)
        
        assert embeddings.shape == (3, 512)
    
    def test_embedding_consistency(self, encoder):
        """Mesmo texto deve gerar mesmo embedding."""
        text = "consistency test"
        
        emb_1 = encoder.encode_text(text)
        emb_2 = encoder.encode_text(text)
        
        # Embeddings devem ser idênticos
        assert np.allclose(emb_1, emb_2)
