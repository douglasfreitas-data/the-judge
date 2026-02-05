"""
The Judge - API Schemas
========================
Pydantic models para request/response da API.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from uuid import UUID


# ============================================
# Request Schemas
# ============================================

class JudgeRequest(BaseModel):
    """Request para julgamento de uma sessão."""
    text: str = Field(..., description="Descrição textual do visualizador")
    target_a_id: str = Field(..., description="UUID do target A")
    target_b_id: str = Field(..., description="UUID do target B")
    viewer_id: Optional[str] = Field(None, description="UUID do viewer (opcional)")
    event_id: Optional[str] = Field(None, description="UUID do evento (opcional)")


class TargetCreate(BaseModel):
    """Request para criação de target."""
    source: str = Field(..., description="Fonte da imagem (ex: unsplash, pexels)")
    source_id: str = Field(..., description="ID na fonte original")
    category_id: int = Field(..., description="ID da categoria")
    source_url: Optional[str] = Field(None, description="URL original")
    numinosity: float = Field(0.5, ge=0.0, le=1.0, description="Score de numinosidade")
    dimensions: Optional[Dict[str, float]] = Field(None, description="Dimensões do target")


class TargetUpdateEmbedding(BaseModel):
    """Request para atualizar embedding de um target existente."""
    image_url: Optional[str] = Field(None, description="URL da imagem para gerar embedding")
    # Alternativa: upload direto (implementar depois)


# ============================================
# Response Schemas
# ============================================

class JudgeResponse(BaseModel):
    """Resultado do julgamento."""
    winner: str = Field(..., description="'A', 'B', ou 'TIE'")
    score_a: float = Field(..., description="Score de similaridade com target A")
    score_b: float = Field(..., description="Score de similaridade com target B")
    confidence: float = Field(..., description="Confiança da predição (0-1)")
    difference: float = Field(..., description="Diferença absoluta entre scores")


class TargetResponse(BaseModel):
    """Dados de um target."""
    id: str
    source: str
    source_id: str
    category_id: Optional[int]
    numinosity: Optional[float]
    has_embedding: bool = Field(..., description="Se o target tem embedding gerado")
    created_at: Optional[str]


class HealthResponse(BaseModel):
    """Status de saúde da API."""
    status: str
    version: str
    clip_loaded: bool
