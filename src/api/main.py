"""
The Judge - FastAPI Application
================================
API REST para julgamento de sessões de Visão Remota.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import numpy as np

from .schemas import (
    JudgeRequest, JudgeResponse,
    TargetCreate, TargetResponse, TargetUpdateEmbedding,
    HealthResponse
)
from ..core import CLIPEncoder, rank_targets, calculate_confidence
from ..repositories import TargetRepository, SessionRepository
from ..database import get_supabase

# ============================================
# App Lifespan (carrega modelo CLIP no startup)
# ============================================

encoder: CLIPEncoder = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carrega o modelo CLIP no startup."""
    global encoder
    print("🚀 Carregando modelo CLIP...")
    encoder = CLIPEncoder()
    print("✅ CLIP carregado!")
    yield
    print("👋 Shutting down...")


# ============================================
# FastAPI App
# ============================================

app = FastAPI(
    title="The Judge API",
    description="Sistema de julgamento automatizado para Visão Remota Associativa (ARV)",
    version="0.1.0",
    lifespan=lifespan
)

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Dependencies
# ============================================

def get_target_repo() -> TargetRepository:
    return TargetRepository()


def get_session_repo() -> SessionRepository:
    return SessionRepository()


def get_encoder() -> CLIPEncoder:
    if encoder is None:
        raise HTTPException(status_code=503, detail="CLIP encoder not loaded")
    return encoder


# ============================================
# Endpoints
# ============================================

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Verifica status da API."""
    return HealthResponse(
        status="ok",
        version="0.1.0",
        clip_loaded=(encoder is not None)
    )


@app.post("/judge", response_model=JudgeResponse)
async def judge_session(
    request: JudgeRequest,
    target_repo: TargetRepository = Depends(get_target_repo),
    clip: CLIPEncoder = Depends(get_encoder)
):
    """
    Julga uma descrição textual contra dois targets.
    
    Compara o embedding do texto com os embeddings dos targets A e B,
    retornando qual tem maior similaridade.
    """
    # Busca embeddings dos targets
    emb_a = target_repo.get_embedding(request.target_a_id)
    emb_b = target_repo.get_embedding(request.target_b_id)
    
    if emb_a is None:
        raise HTTPException(status_code=404, detail=f"Target A ({request.target_a_id}) não encontrado ou sem embedding")
    
    if emb_b is None:
        raise HTTPException(status_code=404, detail=f"Target B ({request.target_b_id}) não encontrado ou sem embedding")
    
    # Gera embedding do texto
    text_emb = clip.encode_text(request.text)
    
    # Faz o julgamento
    winner, scores = rank_targets(text_emb, emb_a, emb_b)
    confidence = calculate_confidence(scores["score_a"], scores["score_b"])
    
    return JudgeResponse(
        winner=winner,
        score_a=scores["score_a"],
        score_b=scores["score_b"],
        confidence=confidence,
        difference=scores["difference"]
    )


@app.post("/targets", response_model=TargetResponse)
async def create_target(
    request: TargetCreate,
    target_repo: TargetRepository = Depends(get_target_repo)
):
    """Cria um novo target."""
    data = request.model_dump(exclude_none=True)
    
    result = target_repo.create(data)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Falha ao criar target")
    
    return TargetResponse(
        id=result["id"],
        source=result["source"],
        source_id=result["source_id"],
        category_id=result.get("category_id"),
        numinosity=result.get("numinosity"),
        has_embedding=result.get("embedding") is not None,
        created_at=str(result.get("created_at"))
    )


@app.get("/targets/{target_id}", response_model=TargetResponse)
async def get_target(
    target_id: str,
    target_repo: TargetRepository = Depends(get_target_repo)
):
    """Busca um target por ID."""
    result = target_repo.get_by_id(target_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Target não encontrado")
    
    return TargetResponse(
        id=result["id"],
        source=result["source"],
        source_id=result["source_id"],
        category_id=result.get("category_id"),
        numinosity=result.get("numinosity"),
        has_embedding=result.get("embedding") is not None,
        created_at=str(result.get("created_at"))
    )


@app.post("/targets/{target_id}/embedding")
async def generate_target_embedding(
    target_id: str,
    request: TargetUpdateEmbedding,
    target_repo: TargetRepository = Depends(get_target_repo),
    clip: CLIPEncoder = Depends(get_encoder)
):
    """
    Gera e salva embedding para um target.
    
    Por enquanto, aceita apenas URL de imagem.
    """
    import httpx
    from PIL import Image
    from io import BytesIO
    
    if not request.image_url:
        raise HTTPException(status_code=400, detail="image_url é obrigatório")
    
    # Baixa imagem
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(request.image_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao baixar imagem: {e}")
    
    # Gera embedding
    embedding = clip.encode_image(image)
    
    # Salva no banco
    success = target_repo.save_embedding(target_id, embedding)
    
    if not success:
        raise HTTPException(status_code=400, detail="Falha ao salvar embedding")
    
    return {"status": "ok", "message": "Embedding gerado e salvo"}


@app.get("/targets")
async def list_targets(
    limit: int = 50,
    target_repo: TargetRepository = Depends(get_target_repo)
):
    """Lista targets ativos."""
    targets = target_repo.list_active(limit=limit)
    
    return {
        "count": len(targets),
        "targets": [
            {
                "id": t["id"],
                "source_id": t["source_id"],
                "category_id": t.get("category_id"),
                "has_embedding": t.get("embedding") is not None
            }
            for t in targets
        ]
    }
