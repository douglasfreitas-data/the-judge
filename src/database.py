"""
The Judge - Database Client
============================
Cliente Supabase singleton para conexão com o banco de dados.
"""

import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Singleton
_supabase_client: Optional[Client] = None


def get_supabase() -> Client:
    """
    Retorna cliente Supabase singleton.
    
    Configura automaticamente usando variáveis de ambiente:
    - SUPABASE_URL
    - SUPABASE_ANON_KEY
    
    Raises:
        ValueError: Se as variáveis não estiverem configuradas
    """
    global _supabase_client
    
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise ValueError(
                "SUPABASE_URL e SUPABASE_ANON_KEY devem estar definidos no .env"
            )
        
        _supabase_client = create_client(url, key)
    
    return _supabase_client


def reset_client():
    """Reset do singleton (útil para testes)."""
    global _supabase_client
    _supabase_client = None
