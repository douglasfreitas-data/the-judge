"""
The Judge - Session Repository
===============================
Operações de banco de dados para Sessions (visualizações).
"""

import numpy as np
from typing import Optional, Dict, Any, List
from uuid import UUID

from ..database import get_supabase


class SessionRepository:
    """
    Repositório para operações com sessões de visualização no Supabase.
    
    Uso:
        repo = SessionRepository()
        session = repo.create({
            "viewer_id": "uuid",
            "event_id": "uuid",
            "text_input": "descrição do viewer"
        })
    """
    
    TABLE = "sessions"
    
    def __init__(self):
        self.db = get_supabase()
    
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Cria uma nova sessão.
        
        Args:
            data: Dados da sessão (viewer_id, event_id, text_input, etc.)
            
        Returns:
            Sessão criada ou None
        """
        response = self.db.table(self.TABLE).insert(data).execute()
        
        if response.data:
            return response.data[0]
        return None
    
    def get_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Busca sessão por ID."""
        response = self.db.table(self.TABLE).select("*").eq("id", session_id).execute()
        
        if response.data:
            return response.data[0]
        return None
    
    def save_judgment(
        self,
        session_id: str,
        text_embedding: np.ndarray,
        score_a: float,
        score_b: float,
        prediction: str,
        confidence: float
    ) -> bool:
        """
        Salva o resultado do julgamento em uma sessão.
        
        Args:
            session_id: UUID da sessão
            text_embedding: Embedding do texto do viewer
            score_a: Score de similaridade com target A
            score_b: Score de similaridade com target B
            prediction: 'A' ou 'B'
            confidence: Confiança da predição (0-1)
            
        Returns:
            True se salvo com sucesso
        """
        data = {
            "text_embedding": text_embedding.tolist(),
            "score_target_a": score_a,
            "score_target_b": score_b,
            "prediction": prediction,
            "confidence": confidence
        }
        
        response = self.db.table(self.TABLE).update(data).eq("id", session_id).execute()
        
        return len(response.data) > 0
    
    def mark_result(
        self,
        session_id: str,
        is_correct: bool,
        is_displacement: bool = False
    ) -> bool:
        """
        Marca o resultado real da sessão (após revelação do target).
        
        Args:
            session_id: UUID da sessão
            is_correct: Se a predição estava correta
            is_displacement: Se foi um displacement (oposto do esperado)
            
        Returns:
            True se atualizado com sucesso
        """
        data = {
            "is_correct": is_correct,
            "is_displacement": is_displacement
        }
        
        response = self.db.table(self.TABLE).update(data).eq("id", session_id).execute()
        
        return len(response.data) > 0
    
    def get_viewer_sessions(
        self, 
        viewer_id: str, 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Lista sessões de um viewer."""
        response = (
            self.db.table(self.TABLE)
            .select("*")
            .eq("viewer_id", viewer_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        
        return response.data
    
    def get_event_sessions(self, event_id: str) -> List[Dict[str, Any]]:
        """Lista todas as sessões de um evento."""
        response = (
            self.db.table(self.TABLE)
            .select("*, viewers(username)")
            .eq("event_id", event_id)
            .execute()
        )
        
        return response.data
