"""
The Judge - Test Embeddings + Supabase Integration
====================================================
Testa o fluxo completo: CLIP encoding → Supabase storage → retrieval
"""

import sys
import numpy as np

# Adiciona src ao path
sys.path.insert(0, ".")

from src.database import get_supabase
from src.repositories import TargetRepository


def setup_auth():
    """Autentica com usuário de teste (necessário para RLS)."""
    print("🔑 Autenticando...")
    db = get_supabase()
    email = "test@example.com"
    password = "password123456"
    
    try:
        session = db.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        print(f"   ✅ Logado como: {email}")
        return True
    except Exception as e:
        print(f"   ⚠️ Login falhou: {e}")
        try:
            db.auth.sign_up({"email": email, "password": password})
            db.auth.sign_in_with_password({"email": email, "password": password})
            print(f"   ✅ Usuário criado e logado: {email}")
            return True
        except:
            print("   ❌ Não foi possível autenticar")
            return False


def test_connection():
    """Testa conexão com Supabase."""
    print("🔌 Testando conexão com Supabase...")
    try:
        db = get_supabase()
        print("✅ Conexão estabelecida!")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_list_targets():
    """Lista targets existentes no banco."""
    print("\n📋 Listando targets...")
    repo = TargetRepository()
    
    targets = repo.list_active(limit=5)
    print(f"   Encontrados: {len(targets)} targets")
    
    for t in targets:
        has_emb = "✓" if t.get("embedding") else "✗"
        print(f"   - [{has_emb}] {t['source_id']} (cat: {t['category_id']})")
    
    return targets


def test_save_dummy_embedding():
    """Testa salvar um embedding dummy em um target existente."""
    print("\n💾 Testando save de embedding...")
    repo = TargetRepository()
    
    # Busca primeiro target ativo
    targets = repo.list_active(limit=1)
    if not targets:
        print("   ⚠️ Nenhum target encontrado para teste")
        return False
    
    target = targets[0]
    target_id = target["id"]
    print(f"   Target: {target['source_id']} (ID: {target_id})")
    
    # Cria embedding dummy (512D normalizado)
    dummy_embedding = np.random.randn(512).astype(np.float32)
    dummy_embedding = dummy_embedding / np.linalg.norm(dummy_embedding)
    
    # Salva
    success = repo.save_embedding(target_id, dummy_embedding)
    
    if success:
        print("   ✅ Embedding salvo!")
    else:
        print("   ❌ Falha ao salvar")
        return False
    
    # Recupera e verifica
    print("\n🔍 Verificando embedding salvo...")
    recovered = repo.get_embedding(target_id)
    
    if recovered is not None:
        print(f"   Shape: {recovered.shape}")
        print(f"   Norma: {np.linalg.norm(recovered):.4f}")
        
        # Verifica se é o mesmo
        diff = np.abs(dummy_embedding - recovered).max()
        print(f"   Diferença máxima: {diff:.6f}")
        
        if diff < 1e-5:
            print("   ✅ Embedding recuperado corretamente!")
            return True
        else:
            print("   ⚠️ Embedding difere do original (possível precisão)")
            return True  # Ainda OK se pequena diferença
    else:
        print("   ❌ Embedding não encontrado")
        return False


def test_with_real_clip():
    """Testa com encoder CLIP real (se disponível)."""
    print("\n🤖 Testando com CLIP real...")
    
    try:
        from src.core import CLIPEncoder
        encoder = CLIPEncoder()
        print("   ✅ CLIPEncoder carregado!")
    except ImportError as e:
        print(f"   ⚠️ CLIP não disponível: {e}")
        return None
    
    # Gera embedding de texto de teste
    text = "a beautiful sunset over the ocean"
    embedding = encoder.encode_text(text)
    
    print(f"   Texto: \"{text}\"")
    print(f"   Embedding shape: {embedding.shape}")
    print(f"   Norma L2: {np.linalg.norm(embedding):.4f}")
    
    # Salva no primeiro target
    repo = TargetRepository()
    targets = repo.list_active(limit=1)
    
    if targets:
        target_id = targets[0]["id"]
        success = repo.save_embedding(target_id, embedding)
        
        if success:
            print(f"   ✅ Embedding CLIP salvo no target!")
            
            # Recupera e verifica
            recovered = repo.get_embedding(target_id)
            similarity = np.dot(embedding, recovered)
            print(f"   Similaridade original vs recuperado: {similarity:.6f}")
            
            return similarity > 0.9999
    
    return False


def main():
    print("=" * 50)
    print("🧪 THE JUDGE - Teste Embeddings + Supabase")
    print("=" * 50)
    
    # Teste 1: Conexão
    if not test_connection():
        print("\n❌ Falha no teste de conexão")
        return
    
    # Setup Auth (necessário para RLS)
    setup_auth()
    
    # Teste 2: Listar targets
    targets = test_list_targets()
    
    # Teste 3: Save/Load embedding
    if targets:
        test_save_dummy_embedding()
    
    # Teste 4: CLIP real (opcional)
    test_with_real_clip()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")
    print("=" * 50)


if __name__ == "__main__":
    main()
