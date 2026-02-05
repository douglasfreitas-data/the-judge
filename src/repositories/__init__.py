"""
The Judge - Repositories
=========================
Camada de acesso a dados.
"""

from .target_repository import TargetRepository
from .session_repository import SessionRepository

__all__ = ["TargetRepository", "SessionRepository"]
