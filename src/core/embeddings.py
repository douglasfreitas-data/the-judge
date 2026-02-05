"""
The Judge - CLIP Embeddings Module
===================================
Gerenciamento de embeddings multimodais usando OpenCLIP.
"""

import numpy as np
import torch
from PIL import Image
from typing import Union, List
import open_clip


class CLIPEncoder:
    """
    Encoder multimodal usando CLIP (ViT-B-32).
    
    Converte texto e imagens para o mesmo espaço vetorial 512D,
    permitindo comparação semântica direta entre modalidades.
    
    Uso:
        encoder = CLIPEncoder()
        text_emb = encoder.encode_text("uma praia ensolarada")
        img_emb = encoder.encode_image_from_path("praia.jpg")
        # Ambos são vetores (512,) normalizados
    """
    
    # Modelo padrão conforme ADR-001
    DEFAULT_MODEL = "ViT-B-32"
    DEFAULT_PRETRAINED = "openai"
    
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        pretrained: str = DEFAULT_PRETRAINED,
        device: str = None
    ):
        """
        Inicializa o encoder CLIP.
        
        Args:
            model_name: Arquitetura do modelo (default: ViT-B-32)
            pretrained: Pesos pré-treinados (default: openai)
            device: Dispositivo para inferência ('cuda', 'cpu', ou None para auto)
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Carrega modelo e preprocessador
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model_name,
            pretrained=pretrained,
            device=self.device
        )
        self.tokenizer = open_clip.get_tokenizer(model_name)
        
        # Coloca em modo de avaliação (desativa dropout, etc.)
        self.model.eval()
        
        # Dimensão do embedding (para referência)
        self.embedding_dim = 512
    
    @torch.no_grad()
    def encode_text(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Converte texto para embedding vetorial.
        
        Args:
            text: String ou lista de strings para converter
            
        Returns:
            Array numpy (512,) normalizado L2, ou (N, 512) para lista
        """
        # Garante que é lista para processamento uniforme
        texts = [text] if isinstance(text, str) else text
        
        # Tokeniza e move para device
        tokens = self.tokenizer(texts).to(self.device)
        
        # Gera embeddings
        embeddings = self.model.encode_text(tokens)
        
        # Normaliza L2
        embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
        
        # Converte para numpy
        result = embeddings.cpu().numpy()
        
        # Retorna vetor 1D se input era string única
        if isinstance(text, str):
            return result[0]
        return result
    
    @torch.no_grad()
    def encode_image(self, image: Image.Image) -> np.ndarray:
        """
        Converte imagem PIL para embedding vetorial.
        
        Args:
            image: Imagem PIL.Image
            
        Returns:
            Array numpy (512,) normalizado L2
        """
        # Preprocessa imagem (resize, normalize, etc.)
        image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
        
        # Gera embedding
        embedding = self.model.encode_image(image_tensor)
        
        # Normaliza L2
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
        
        # Converte para numpy e retorna vetor 1D
        return embedding.cpu().numpy()[0]
    
    @torch.no_grad()
    def encode_image_from_path(self, path: str) -> np.ndarray:
        """
        Carrega imagem de arquivo e converte para embedding.
        
        Args:
            path: Caminho para o arquivo de imagem
            
        Returns:
            Array numpy (512,) normalizado L2
        """
        image = Image.open(path).convert("RGB")
        return self.encode_image(image)
    
    @torch.no_grad()
    def encode_images(self, images: List[Image.Image]) -> np.ndarray:
        """
        Converte múltiplas imagens para embeddings em batch.
        
        Args:
            images: Lista de imagens PIL.Image
            
        Returns:
            Array numpy (N, 512) normalizado L2
        """
        # Preprocessa todas as imagens
        batch = torch.stack([
            self.preprocess(img) for img in images
        ]).to(self.device)
        
        # Gera embeddings
        embeddings = self.model.encode_image(batch)
        
        # Normaliza L2
        embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
        
        return embeddings.cpu().numpy()


# Singleton para reutilização do encoder (carregamento é lento)
_encoder_instance = None


def get_encoder() -> CLIPEncoder:
    """
    Retorna instância singleton do CLIPEncoder.
    
    Útil para evitar recarregar o modelo a cada uso.
    """
    global _encoder_instance
    if _encoder_instance is None:
        _encoder_instance = CLIPEncoder()
    return _encoder_instance
