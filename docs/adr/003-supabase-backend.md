# ADR-003: Usar Supabase como Backend de Banco de Dados

## Metadata
- **Número:** ADR-003
- **Título:** Usar Supabase como Backend de Banco de Dados
- **Data:** 2026-02-01
- **Status:** Aceito

## Contexto

O projeto The Judge precisa de:
1. Banco de dados relacional para armazenar viewers, eventos, sessões
2. Suporte a vetores (embeddings) para similaridade semântica
3. Autenticação de usuários
4. API REST automatizada
5. Storage para imagens e esboços

## Decisão

Usar **Supabase** como plataforma unificada que fornece:
- PostgreSQL com extensão **pgvector** para embeddings
- Auth integrado
- Storage para arquivos
- API REST auto-gerada
- Row Level Security (RLS)

## Consequências

### Positivas
- **One-stop-shop**: BD, Auth, Storage, API em um lugar
- **pgvector nativo**: Suporte a embeddings sem configuração extra
- **Grátis para início**: Tier gratuito suficiente para MVP
- **SDK Python oficial**: Integração simples com FastAPI
- **Tempo real**: Possibilidade de subscriptions para updates ao vivo

### Negativas
- **Vendor lock-in**: Migrar depois seria trabalhoso 
- **Limites do free tier**: 500MB de banco, 1GB storage
- **Latência**: Servidor remoto vs. local (aceitável para nosso caso)

## Alternativas Consideradas

1. **PostgreSQL local + pgvector**: Mais controle, mas mais setup e sem auth/storage integrado
2. **Firebase**: Não tem suporte nativo a vetores/embeddings
3. **MongoDB Atlas + Vector Search**: Bom para vetores, mas NoSQL menos adequado para relações complexas
4. **Pinecone + PostgreSQL separados**: Mais complexidade, dois sistemas para gerenciar

## Estrutura do Banco

```
viewers          → Perfil dos visualizadores
viewer_stats     → Métricas agregadas (hit_rate, displacement, etc.)
target_categories → Categorias (nature, urban, fire, etc.)
targets          → Pool de imagens-alvo com embeddings
events           → Eventos de predição (com par de alvos)
sessions         → Sessões de visualização
```

## Referências
- [Supabase](https://supabase.com)
- [pgvector](https://github.com/pgvector/pgvector)
- Schema: `database/schema.sql`
