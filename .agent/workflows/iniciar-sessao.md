---
description: Iniciar nova sessão de trabalho no The Judge
---

# Workflow: Iniciar Sessão

Execute este workflow ao começar uma nova sessão de trabalho.

## 1. Ler contexto anterior

```bash
# turbo
cat docs/devlog.md | tail -50
```

Revise a última entrada do devlog para lembrar:
- O que foi feito na sessão anterior
- Quais são os próximos passos pendentes

## 2. Verificar tarefas pendentes

Olhe o arquivo de tarefas para ver o que está em progresso.

## 3. Definir foco da sessão

Antes de começar, declare:
- **Objetivo principal:** [O que quero completar hoje]
- **Tempo disponível:** [Quanto tempo tenho]

## 4. Ao finalizar

Execute o workflow `/atualizar-docs` para documentar o que foi feito.
