# ADR-004: Uso da Extensão pgvector para Embeddings

## Metadata
- **Número:** ADR-004
- **Título:** Uso da Extensão pgvector para Armazenamento e Busca de Embeddings
- **Data:** 2026-02-01
- **Status:** Aceito

## O que é pgvector?

**pgvector** é uma extensão do PostgreSQL que adiciona suporte nativo a **vetores** (arrays de números com tamanho fixo) e **operações de similaridade** entre eles.

## Por que precisamos de vetores?

### O Problema
Nosso sistema precisa comparar:
- **Texto do visualizador** ("montanha com neve, céu azul")
- **Imagens-alvo** (foto da Torre Eiffel, foto de um vulcão)

Não podemos comparar texto com imagem diretamente. Precisamos convertê-los para um formato comum: **embeddings**.

### O que são Embeddings?
Embeddings são representações numéricas (vetores) que capturam o **significado semântico** de um conteúdo.

```
"cachorro" → [0.12, -0.45, 0.78, 0.33, ..., 0.21]  (512 números)
"dog"      → [0.11, -0.44, 0.77, 0.34, ..., 0.22]  (muito similar!)
"gato"     → [0.08, -0.32, 0.65, 0.28, ..., 0.19]  (diferente)
"carro"    → [-0.52, 0.13, -0.21, 0.85, ..., -0.47] (bem diferente!)
```

Conceitos **semanticamente similares** têm vetores **próximos** no espaço vetorial.

## O que o CLIP faz?

O modelo **CLIP** (OpenAI) converte tanto texto quanto imagens para o **mesmo espaço vetorial** de 512 dimensões:

```
┌─────────────────┐                    ┌─────────────────┐
│ "montanha com   │                    │  📷 Foto do     │
│  neve, azul"    │                    │  Monte Everest  │
└────────┬────────┘                    └────────┬────────┘
         │                                      │
         ▼                                      ▼
    ┌─────────┐                           ┌─────────┐
    │  CLIP   │                           │  CLIP   │
    │  Text   │                           │  Image  │
    │ Encoder │                           │ Encoder │
    └────┬────┘                           └────┬────┘
         │                                      │
         ▼                                      ▼
   [0.12, -0.45, ...]                    [0.11, -0.44, ...]
        512 números                          512 números
              │                                    │
              └──────────┬─────────────────────────┘
                         │
                         ▼
                  SIMILARIDADE = 0.94 ✓
                    (muito alta!)
```

## O que pgvector faz na prática?

### 1. Armazenar embeddings como tipo de dado
```sql
-- O tipo 'vector(512)' armazena um vetor de 512 dimensões
CREATE TABLE targets (
    id UUID PRIMARY KEY,
    name TEXT,
    embedding vector(512)  -- ← pgvector!
);
```

### 2. Calcular similaridade entre vetores
```sql
-- Distância de cosseno (quanto MENOR, mais similar)
-- Valores de 0 (idêntico) a 2 (oposto)
SELECT 
    name,
    embedding <=> query_embedding AS distance
FROM targets
ORDER BY distance
LIMIT 5;
```

### 3. Busca por similaridade em alta performance
```sql
-- Encontrar os 5 alvos mais similares ao texto do visualizador
SELECT name, 1 - (embedding <=> '[0.12, -0.45, ...]') AS similarity
FROM targets
WHERE is_active = true
ORDER BY embedding <=> '[0.12, -0.45, ...]'
LIMIT 5;
```

### 4. Indexação para buscas rápidas
```sql
-- IVFFlat: Agrupa vetores em "listas" para busca aproximada rápida
CREATE INDEX idx_targets_embedding ON targets 
    USING ivfflat (embedding vector_cosine_ops) 
    WITH (lists = 100);
```

## Operadores do pgvector

| Operador | Nome | Uso |
|----------|------|-----|
| `<->` | L2 Distance (Euclidiana) | Distância geométrica |
| `<=>` | Cosine Distance | **Mais usado para embeddings** |
| `<#>` | Inner Product | Produto interno (negativo) |

### Por que Cosine Distance?
A **distância de cosseno** mede o **ângulo** entre dois vetores, ignorando a magnitude. Isso é ideal para embeddings porque:
- Vetores normalizados têm mesma magnitude
- O ângulo captura a direção semântica

```
Cosine Similarity = cos(θ) = (A · B) / (||A|| × ||B||)

Se A e B apontam na mesma direção: cos(0°) = 1 (idênticos)
Se A e B são perpendiculares:       cos(90°) = 0 (não relacionados)
Se A e B apontam em direções opostas: cos(180°) = -1 (opostos)
```

## Fluxo no The Judge

```
1. Visualizador digita: "praia tropical, coqueiros, água azul"
                                    │
                                    ▼
2. CLIP Text Encoder: [0.32, -0.18, 0.55, ..., 0.41] (512 dims)
                                    │
                                    ▼
3. PostgreSQL + pgvector:
   
   SELECT name, 
          1 - (embedding <=> input_embedding) AS similarity
   FROM targets
   ORDER BY similarity DESC
   LIMIT 2;
   
                                    │
                                    ▼
4. Resultado:
   ┌──────────────────────┬────────────┐
   │ Alvo A: Praia Cancun │ Sim: 0.87  │ ← ALTA
   │ Alvo B: Vulcão Kilauea│ Sim: 0.23 │ ← BAIXA
   └──────────────────────┴────────────┘
   
                                    │
                                    ▼
5. Predição: Alvo A (confiança: 0.87)
```

## Alternativas Consideradas

| Solução | Prós | Contras |
|---------|------|---------|
| **pgvector** ✓ | Integrado ao PostgreSQL, SQL nativo | Menos features que Pinecone |
| Pinecone | Especializado, muito rápido | Serviço separado, custo |
| Milvus | Open source, escalável | Complexo de operar |
| FAISS (local) | Muito rápido, da Meta | Não persiste, sem SQL |

## Referências
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Supabase + pgvector](https://supabase.com/docs/guides/ai/vector-columns)
- [CLIP Paper](https://openai.com/research/clip)
