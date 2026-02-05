"""
The Judge - Register Real Targets
==================================
Script para cadastrar imagens reais no Supabase, gerando embeddings e metadados.
"""

import sys
import os
from PIL import Image
import numpy as np

# Adiciona src ao path
sys.path.insert(0, ".")

from src.database import get_supabase
from src.core import CLIPEncoder
from src.repositories import TargetRepository

# Caminhos das imagens
DATA_DIR = "data/targets"
TARGETS = [
    {
        "filename": "volcano.png",
        "source": "generated",
        "source_id": "gen_volcano_001",
        "category_name": "fire",
        "numinosity": 0.95,
        "dimensions": {
            "scale": 1.0,           
            "warm_vs_cold": 1.0,    
            "calm_vs_intense": 1.0, 
            "safe_vs_dangerous": 1.0 
        }
    },
    {
        "filename": "penguin.png",
        "source": "generated",
        "source_id": "gen_penguin_001",
        "category_name": "animals",
        "numinosity": 0.85,
        "dimensions": {
            "scale": 0.1,           
            "warm_vs_cold": 0.0,    
            "calm_vs_intense": 0.0, 
            "safe_vs_dangerous": 0.0 
        }
    }
]


def get_category_id(db, name):
    res = db.table("target_categories").select("id").eq("name", name).execute()
    if res.data:
        return res.data[0]["id"]
    return None


def setup_auth(db):
    """Autentica para permitir escrita (RLS)."""
    email = "test@example.com"
    password = "password123456"
    try:
        db.auth.sign_in_with_password({"email": email, "password": password})
        print(f"🔑 Autenticado como {email}")
        return True
    except:
        try:
            db.auth.sign_up({"email": email, "password": password})
            db.auth.sign_in_with_password({"email": email, "password": password})
            print(f"🔑 Usuário criado e autenticado: {email}")
            return True
        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            return False


def main():
    print("🚀 Iniciando cadastro de targets reais...")
    
    db = get_supabase()
    if not setup_auth(db):
        return

    print("🧠 Carregando CLIP...")
    encoder = CLIPEncoder()
    repo = TargetRepository()
    repo.db = db  

    for t in TARGETS:
        print(f"\n📸 Processando {t['filename']}...")
        
        img_path = os.path.join(DATA_DIR, t["filename"])
        if not os.path.exists(img_path):
            print(f"   ❌ Arquivo não encontrado: {img_path}")
            continue
            
        image = Image.open(img_path).convert("RGB")
        
        print("   ⚡ Gerando embedding...")
        embedding = encoder.encode_image(image)
        
        cat_id = get_category_id(db, t["category_name"])
        if not cat_id:
            cat_id = 1
            print(f"   ⚠️ Categoria '{t['category_name']}' não encontrada, usando ID 1")

        target_data = {
            "source": t["source"],
            "source_id": t["source_id"],
            "category_id": cat_id,
            "file_path": img_path,
            "numinosity": t["numinosity"],
            "dimensions": t["dimensions"]
        }

        existing = db.table("targets").select("id").eq("source_id", t["source_id"]).execute()
        
        target_id = None
        if existing.data:
            target_id = existing.data[0]["id"]
            print(f"   🔄 Target já existe ({target_id}), atualizando...")
            db.table("targets").update(target_data).eq("id", target_id).execute()
        else:
            print(f"   ✨ Criando novo target...")
            res = repo.create(target_data)
            if res:
                target_id = res["id"]
        
        if target_id:
            success = repo.save_embedding(target_id, embedding)
            if success:
                print("   ✅ Embedding salvo com sucesso!")
            else:
                print("   ❌ Falha ao salvar embedding")
        
        print(f"   🆔 {target_id}")

    print("\n✅ Cadastro concluído!")


if __name__ == "__main__":
    main()
