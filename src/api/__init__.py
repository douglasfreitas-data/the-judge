"""
The Judge - API Module
"""

from .main import app
from .schemas import JudgeRequest, JudgeResponse, TargetCreate, TargetResponse

__all__ = ["app", "JudgeRequest", "JudgeResponse", "TargetCreate", "TargetResponse"]
