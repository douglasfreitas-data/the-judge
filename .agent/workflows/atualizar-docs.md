---
description: Atualizar documentação do projeto The Judge após cada sessão
---

# Workflow: Atualizar Documentação

Execute este workflow ao final de cada sessão de trabalho no projeto The Judge.

## Checklist de Atualização

### 1. Devlog (docs/devlog.md)
Adicione uma nova entrada com:
- Data e número da sessão
- O que foi feito (itens completados)
- Insights importantes descobertos
- Decisões tomadas (referenciando ADRs se houver)
- Próximos passos

### 2. ADRs (docs/adr/)
Se uma decisão técnica importante foi tomada:
- Copie `docs/adr/000-template.md`
- Renomeie para `NNN-titulo-da-decisao.md`
- Preencha: Contexto, Decisão, Consequências, Alternativas

### 3. Task.md (brain/task.md)
Atualize o status das tarefas:
- `[ ]` → `[/]` para em progresso
- `[/]` → `[x]` para completado
- Adicione novas tarefas se surgirem

### 4. Documentos específicos
Se houve discussão sobre:
- **Alvos/Ortogonalidade** → Atualizar `docs/target_database_strategy.md`
- **Arquitetura/Tech** → Atualizar `docs/brainstorm_pesquisa.md`
- **Plano de fases** → Atualizar `docs/implementation_plan.md`

### 5. Commit e Push
```bash
# turbo
git add -A && git commit -m "docs: Update documentation after session [N]"
git push
```

## Quando criar um novo ADR?

Crie um ADR quando:
- Escolher uma tecnologia/biblioteca específica
- Decidir uma abordagem de arquitetura
- Fazer tradeoff significativo
- Reverter uma decisão anterior

## Perguntas de reflexão

Antes de finalizar, pergunte-se:
1. Descobri algo hoje que mudou minha visão do problema?
2. Tomei alguma decisão que deveria documentar?
3. O próximo "eu" vai entender o que foi feito hoje?
