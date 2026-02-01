# ADR-001: Usar CLIP para Embeddings Multimodais

## Metadata
- **Número:** ADR-001
- **Título:** Usar CLIP para Embeddings Multimodais
- **Data:** 2026-02-01
- **Status:** Aceito

## Contexto

O sistema The Judge precisa comparar **descrições textuais** dos visualizadores com **imagens-alvo** para determinar qual alvo tem maior correspondência semântica.

Precisamos de um modelo que:
1. Converta texto para vetores
2. Converta imagens para vetores
3. Permita comparação direta entre os dois

## Decisão

Usar **CLIP (Contrastive Language-Image Pre-training)** da OpenAI, especificamente através da biblioteca **OpenCLIP** para acesso open-source.

Modelo escolhido: `ViT-B-32` com pesos `openai` (balanceamento entre performance e velocidade).

## Consequências

### Positivas
- Espaço vetorial compartilhado texto ↔ imagem
- Zero-shot: não precisa de fine-tuning para nosso caso de uso
- Bem documentado e mantido pela comunidade
- Rápido o suficiente para uso em tempo real

### Negativas
- Fraco em tarefas abstratas (contar objetos, relações espaciais precisas)
- Não funciona bem com esboços toscos (necessário complementar com Sketchformer)
- Pode ter "acordos errôneos" - alta similaridade entre conceitos semanticamente distintos

## Alternativas Consideradas

1. **GPT-4V / Vision LLM**: Mais poderoso, mas muito lento e caro para cada comparação
2. **BLIP-2**: Similar ao CLIP mas com capacidades de caption, desnecessário para nosso caso
3. **Embeddings separados (BERT + ResNet)**: Não compartilham o mesmo espaço vetorial

## Referências
- [OpenAI CLIP Paper](https://openai.com/research/clip)
- [OpenCLIP GitHub](https://github.com/mlfoundations/open_clip)
- Documento: `docs/brainstorm_pesquisa.md` seção 3.1
