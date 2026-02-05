"""
The Judge - Target Repository
==============================
Operações de banco de dados para Targets (imagens-alvo).
"""

import numpy as np
from typing import Optional, List, Dict, Any
from uuid import UUID

from ..database import get_supabase


class TargetRepository:
    """
    Repositório para operações com targets no Supabase.
    
    Uso:
        repo = TargetRepository()
        target = repo.get_by_id("uuid-do-target")
        embedding = repo.get_embedding("uuid-do-target")
    """
    
    TABLE = "targets"
    
    def __init__(self):
        self.db = get_supabase()
    
    def get_by_id(self, target_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca um target por ID.
        
        Args:
            target_id: UUID do target
            
        Returns:
            Dict com dados do target ou None se não encontrado
        """
        response = self.db.table(self.TABLE).select("*").eq("id", target_id).execute()
        
        if response.data:
            return response.data[0]
        return None
    
    def get_embedding(self, target_id: str) -> Optional[np.ndarray]:
        """
        Retorna o embedding de um target como numpy array.
        
        Args:
            target_id: UUID do target
            
        Returns:
            Array numpy (512,) ou None se não existir
        """
        response = self.db.table(self.TABLE).select("embedding").eq("id", target_id).execute()
        
        if response.data and response.data[0].get("embedding"):
            embedding_data = response.data[0]["embedding"]
            
            # pgvector pode retornar como string "[0.1,0.2,...]" ou como lista
            if isinstance(embedding_data, str):
                # Remove colchetes e converte para lista de floats
                embedding_data = embedding_data.strip("[]")
                embedding_data = [float(x) for x in embedding_data.split(",")]
            
            return np.array(embedding_data, dtype=np.float32)
        return None
    
    def save_embedding(
        self, 
        target_id: str, 
        embedding: np.ndarray,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Salva ou atualiza o embedding de um target.
        
        Args:
            target_id: UUID do target
            embedding: Array numpy (512,) normalizado
            metadata: Dados adicionais para atualizar (opcional)
            
        Returns:
            True se salvo com sucesso
        """
        data = {"embedding": embedding.tolist()}
        
        if metadata:
            data.update(metadata)
        
        response = self.db.table(self.TABLE).update(data).eq("id", target_id).execute()
        
        return len(response.data) > 0
    
    def list_active(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Lista targets ativos.
        
        Args:
            limit: Máximo de resultados
            
        Returns:
            Lista de dicts com dados dos targets
        """
        response = (
            self.db.table(self.TABLE)
            .select("id, source, source_id, category_id, numinosity, embedding")
            .eq("is_active", True)
            .limit(limit)
            .execute()
        )
        
        return response.data
    
    def list_without_embedding(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Lista targets que ainda não têm embedding.
        
        Útil para processar em batch.
        """
        response = (
            self.db.table(self.TABLE)
            .select("id, source, source_id, file_path, storage_url")
            .eq("is_active", True)
            .is_("embedding", "null")
            .limit(limit)
            .execute()
        )
        
        return response.data
    
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Cria um novo target.
        
        Args:
            data: Dados do target (source, source_id, category_id, etc.)
            
        Returns:
            Target criado ou None
        """
        response = self.db.table(self.TABLE).insert(data).execute()
        
        if response.data:
            return response.data[0]
        return None
    
    def find_similar(
        self, 
        embedding: np.ndarray, 
        limit: int = 5,
        exclude_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Encontra targets mais similares usando busca vetorial.
        
        Nota: Requer RPC call para busca vetorial eficiente.
        """
        # TODO: Implementar via RPC com pgvector
        raise NotImplementedError("Busca vetorial será implementada via RPC")
