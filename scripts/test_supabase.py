"""
The Judge - Test Supabase Connection
=====================================
Script para testar a conexão com o Supabase e operações básicas do banco de dados.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")


def get_supabase_client() -> Client:
    """Cria e retorna um cliente Supabase."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_URL e SUPABASE_ANON_KEY devem estar definidos no .env"
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def test_connection():
    """Testa a conexão básica com o Supabase."""
    print("🔌 Testando conexão com Supabase...")
    print(f"   URL: {SUPABASE_URL}")
    
    try:
        supabase = get_supabase_client()
        print("✅ Cliente Supabase criado com sucesso!")
        return supabase
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None


def test_read_categories(supabase: Client):
    """Testa leitura das categorias de alvos."""
    print("\n📂 Lendo categorias de alvos...")
    
    try:
        response = supabase.table("target_categories").select("*").execute()
        categories = response.data
        
        print(f"✅ {len(categories)} categorias encontradas:")
        for cat in categories:
            print(f"   - {cat['name']}: {cat['description']}")
        
        return categories
    except Exception as e:
        print(f"❌ Erro ao ler categorias: {e}")
        return None


def setup_auth(supabase: Client):
    """Cria um usuário de teste e retorna o cliente autenticado."""
    print("\n🔑 Configurando autenticação...")
    email = "test_user@thejudge.dev"
    password = "password123456"
    
    try:
        # Tenta logar
        print("   Tentando login...")
        session = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        print(f"   ✅ Login realizado! UID: {session.user.id}")
        return session.user.id
        
    except Exception as e:
        print(f"   Login falhou ({e}), tentando cadastro...")
        try:
            # Tenta criar
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            if response.user:
                print(f"   ✅ Usuário criado! UID: {response.user.id}")
                return response.user.id
            else:
                print("   ❌ Falha ao criar usuário (sem dados retornados)")
                return None
        except Exception as signup_error:
            print(f"   ❌ Falha crítica na auth: {signup_error}")
            return None


def test_insert_viewer(supabase: Client, user_id: str):
    """Testa inserção de um visualizador de teste."""
    print("\n👤 Inserindo visualizador de teste...")
    
    if not user_id:
        print("   ❌ Pulei: Sem User ID autenticado")
        return None
        
    try:
        # Verifica se já existe
        existing = supabase.table("viewers").select("*").eq("id", user_id).execute()
        
        if existing.data:
            print(f"   Visualizador de teste já existe (ID: {existing.data[0]['id']})")
            return existing.data[0]
        
        # Insere novo usando o ID do auth (obrigatório pelo RLS)
        response = supabase.table("viewers").insert({
            "id": user_id,  # Linka com auth.users
            "username": "test_viewer",
            "email": "test_user@thejudge.dev"
        }).execute()
        
        if response.data:
            viewer = response.data[0]
            print(f"✅ Visualizador criado com ID: {viewer['id']}")
            return viewer
        else:
            print("   ❌ Falha: Nenhum dado retornado na inserção")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao inserir visualizador: {e}")
        return None


def test_insert_target(supabase: Client, category_id: int):
    """Testa inserção de um alvo de teste."""
    print("\n🎯 Inserindo alvo de teste...")
    
    try:
        # Verifica se já existe
        existing = supabase.table("targets").select("*").eq(
            "source_id", "test_target_001"
        ).execute()
        
        if existing.data:
            print(f"   Alvo de teste já existe (ID: {existing.data[0]['id']})")
            return existing.data[0]
        
        # Insere novo alvo com dimensões
        data = {
            "source": "test",
            "source_id": "test_target_001",
            "category_id": category_id,
            "numinosity": 0.85,
            "dimensions": {
                "scale": 0.8,
                "horizontal_vs_vertical": 0.6
                # Outros campos usarão default do JSONB
            },
            # Dummy embedding para teste (512 zeros)
            "embedding": [0.0] * 512
        }
        
        response = supabase.table("targets").insert(data).execute()
        
        if response.data:
            target = response.data[0]
            print(f"✅ Alvo criado com ID: {target['id']}")
            return target
        else:
            print("   ❌ Falha: Nenhum dado retornado")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao inserir alvo: {e}")
        print("   (Verifique se a política 'Authenticated users can insert targets' foi aplicada)")
        return None


def test_orthogonality_function(supabase: Client):
    """Testa a função de cálculo de ortogonalidade."""
    print("\n📐 Testando função calculate_orthogonality...")
    
    try:
        # Dimensões de teste (muito diferentes)
        dims_a = {
            "scale": 0.1, "warm_vs_cold": 0.9, "calm_vs_intense": 0.2
        }
        dims_b = {
            "scale": 0.9, "warm_vs_cold": 0.1, "calm_vs_intense": 0.8
        }
        
        response = supabase.rpc("calculate_orthogonality", {
            "dims_a": dims_a,
            "dims_b": dims_b
        }).execute()
        
        orthogonality = response.data
        print(f"✅ Ortogonalidade calculada: {orthogonality:.4f}")
        print(f"   (Esperado ~0.57 para dimensões bem diferentes)")
        return orthogonality
    except Exception as e:
        print(f"❌ Erro ao calcular ortogonalidade: {e}")
        print("   (Isso pode ser normal se a função não aceitar RPC)")
        return None


def main():
    """Executa todos os testes."""
    print("=" * 50)
    print("🧪 THE JUDGE - Testes de Conexão Supabase")
    print("=" * 50)
    
    # Teste 1: Conexão
    supabase = test_connection()
    if not supabase:
        print("\n❌ Falha na conexão. Verifique as credenciais no .env")
        return
    
    # Teste 2: Leitura de Metadados (Público)
    categories = test_read_categories(supabase)
    
    # Configuração de Auth (Necessário para inserts)
    user_id = setup_auth(supabase)
    
    # Teste 3: Inserção de visualizador (Autenticado)
    if user_id:
        viewer = test_insert_viewer(supabase, user_id)
    else:
        print("\n⚠️ Pulando testes de insert (sem auth)")
    
    # Teste 4: Inserção de alvo (Autenticado)
    if user_id and categories:
        # Usa a primeira categoria (nature)
        target = test_insert_target(supabase, categories[0]['id'])
    
    # Teste 5: Função de ortogonalidade (RPC)
    test_orthogonality_function(supabase)
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")
    print("=" * 50)


if __name__ == "__main__":
    main()
