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
