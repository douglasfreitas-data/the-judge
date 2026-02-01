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
- [ ] Configurar Supabase
- [ ] Criar primeiro ADR completo
- [ ] Iniciar implementação do MVP (Fase 1)

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
