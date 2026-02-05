# Devlog - The Judge

> Registro cronológico do desenvolvimento do projeto

---

## 2026-02-01 - Sessão 1: Fundação do Projeto

### O que foi feito
- ✅ Inicializado repositório Git
- ✅ Criado README.md com visão geral do projeto
- ✅ Pesquisado tecnologias: CLIP, Sketchformer, Fuzzy Matching
- ✅ Analisado sistema existente: NOVA Judge (ARVcollective)
- ✅ Criado documento de brainstorm consolidado

### Insights importantes
- **NOVA Judge** já faz algo similar usando Vision LLM + embeddings
- CLIP é fraco para esboços abstratos → precisamos do Sketchformer
- Fuzzy matching necessário para corrigir erros de digitação dos visualizadores

### Decisões tomadas
- ADR-001: Usar CLIP para embeddings multimodais
- ADR-002: Ortogonalidade multidimensional (não apenas por categoria)

---

## 2026-02-01 - Sessão 2: Planejamento e Alvos

### O que foi feito
- ✅ Criado plano de implementação em 5 fases
- ✅ Definida estratégia para banco de imagens-alvo
- ✅ Expandido conceito de ortogonalidade para 22+ dimensões
- ✅ Criado catálogo de landmarks icônicos

### Insights importantes
- **Categoria ≠ Ortogonalidade!** Montanha vs. Arranha-céu parecem opostos mas ambos são grandes, verticais, imponentes
- Bons pares: Flor vs. Arranha-céu (5 dimensões opostas!)
- Landmarks icônicos (Pirâmides, Torre Eiffel, Estação Espacial) têm alta numinosidade

### Decisões tomadas
- Supabase para banco de dados (a documentar)
- Sistema de scoring por visualizador com pesos dinâmicos

### Próximos passos
- [x] Configurar Supabase
- [x] Criar schema do banco de dados
- [ ] Testar conexão Python → Supabase
- [ ] Iniciar implementação do MVP (Fase 1)

---

## 2026-02-01 - Sessão 3: Banco de Dados Supabase

### O que foi feito
- ✅ Configurado projeto no Supabase
- ✅ Criado schema completo do banco (`database/schema.sql`)
- ✅ Extensão pgvector ativada para embeddings
- ✅ Tabelas criadas: viewers, viewer_stats, target_categories, targets, events, sessions
- ✅ Funções SQL: `calculate_orthogonality()`, `find_best_target_pair()`
- ✅ Indexes IVFFlat para busca vetorial rápida
- ✅ Row Level Security (RLS) configurado

### Decisões tomadas
- ADR-003: Supabase como backend unificado
- ADR-004: pgvector para armazenamento de embeddings

### Próximos passos
- [x] Configurar Supabase
- [x] Criar schema do banco de dados
- [x] Testar conexão Python → Supabase (Sucesso!)
- [ ] Inserir primeiros dados de teste (Automático via script)
- [ ] Implementar core de embeddings (CLIP)

> **📌 META PARA PRÓXIMA SESSÃO:**
> Começar imediatamente pela **Implementação do Core de Embeddings**.
> 1. Criar `src/core/embeddings.py`
> 2. Implementar classe `CLIPEncoder`
> 3. Integrar com FastAPI básico

---

## 2026-02-05 - Sessão 4: Core de Embeddings CLIP

### O que foi feito
- ✅ Criado `src/core/embeddings.py` com classe `CLIPEncoder`
  - Métodos: `encode_text()`, `encode_image()`, `encode_image_from_path()`
  - Modelo: ViT-B-32 via OpenCLIP
- ✅ Criado `src/core/similarity.py` com funções de comparação
  - `cosine_similarity()`, `rank_targets()`, `calculate_confidence()`
- ✅ Criado `tests/test_embeddings.py` com 8 testes unitários (todos ✓)
- ✅ Adicionado pytest ao `requirements.txt`

### Insights importantes
- Importar diretamente do módulo (não via `__init__.py`) para testes rápidos sem carregar open_clip
- Função `rank_targets()` retorna TIE quando scores diferem < 0.02

### Próximos passos
- [x] Instalar dependências ML (open-clip-torch)
- [x] Executar testes de integração com modelo real (6/6 ✓)
- [ ] Integrar com Supabase para persistência

> **📌 INSIGHT:** CLIP tem similaridade base alta (~0.76) mesmo entre conceitos diferentes.
> O que importa é a *diferença relativa* entre targets, não o valor absoluto.

### Integração Supabase (continuação)
- ✅ Criado `src/database.py` - cliente singleton
- ✅ Criado `src/repositories/target_repository.py` - save/load embeddings
- ✅ Criado `src/repositories/session_repository.py` - save judgments
- ✅ Testes save/load funcionando (similaridade = 1.0)

> **📌 META PARA PRÓXIMA SESSÃO:**
> 1. Criar **FastAPI endpoints** básicos
> 2. Testar com imagens reais de targets

### FastAPI Endpoints ✅
- ✅ Criado `src/api/main.py` - app FastAPI com CLIP carregando no startup
- ✅ Criado `src/api/schemas.py` - Pydantic models
- ✅ Endpoints funcionando: `/`, `/judge`, `/targets`
- ✅ Testado: `POST /judge` retorna scores e winner corretamente

### Teste com Dados Reais ✅
- Cadastrados targets de alta ortogonalidade:
  - 🌋 **Vulcão** (Fogo, Quente, Caos)
  - 🐧 **Pinguim** (Gelo, Frio, Calma)
- **Resultados do Teste End-to-End**:
  - Prompt "Fogo/Explosão" → Venceu Vulcão (Confiança 62%)
  - Prompt "Gelo/Calmo" → Venceu Pinguim (Confiança 61%)
  - Prompt "Água" → Venceu Pinguim (Confiança 27% - correto, pois gelo=água)

> **🎉 CONCLUSÃO DA SESSÃO 4:**
> O sistema core está completo e validado. CLIP funciona, Supabase persiste, API serve, e a lógica de julgamento "pensa" corretamente.

---

## Template para novas entradas

```markdown
## YYYY-MM-DD - Sessão N: [Título]

### O que foi feito
- ✅ Item completado
- 🔄 Item em progresso

### Insights importantes
- Descoberta ou aprendizado relevante

### Decisões tomadas
- ADR-XXX: Breve descrição

### Próximos passos
- [ ] Tarefa pendente
```
