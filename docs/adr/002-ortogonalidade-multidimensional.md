# ADR-002: Ortogonalidade Multidimensional para Seleção de Alvos

## Metadata
- **Número:** ADR-002
- **Título:** Ortogonalidade Multidimensional para Seleção de Alvos
- **Data:** 2026-02-01
- **Status:** Aceito

## Contexto

Na ARV (Visão Remota Associativa), a eficácia das predições depende criticamente de quão **distintos** são os dois alvos apresentados. Se os alvos são muito similares, o visualizador pode descrever características que se aplicam a ambos, tornando a predição ambígua.

O problema inicial detectado:
> Montanha vs. Arranha-céu parecem ser opostos (natureza vs. urbano), mas compartilham múltiplas características: ambos são **grandes, verticais, imponentes**.

## Decisão

Adotar um sistema de **ortogonalidade multidimensional** que avalia imagens em **22+ dimensões** independentes, agrupadas em 5 categorias:

1. **Físicas**: Escala, forma, orientação, profundidade, altitude, densidade, textura
2. **Cromáticas**: Cor dominante, brilho, saturação, contraste
3. **Temporais**: Época, movimento, velocidade, natural/artificial
4. **Emocionais**: Emoção, perigo, mistério, escala humana
5. **Ambientais**: Elemento, temperatura, umidade, bioma

O algoritmo de seleção combina:
- Score multidimensional (60%)
- Score CLIP via similaridade de cosseno (40%)
- Bonus para alta numinosidade em ambos os alvos

## Consequências

### Positivas
- Pares verdadeiramente ortogonais: Flor vs. Arranha-céu (5+ dimensões opostas)
- Reduz ambiguidade nas sessões de visualização
- Métricas explicáveis para curadoria de pool de alvos
- Algoritmo automatizado de seleção de pares

### Negativas
- Requer catalogação manual inicial das dimensões de cada imagem
- Mais complexo de implementar que simples "categorias diferentes"
- Dimensões podem ter pesos subjetivos (futuro: calibrar com dados reais)

## Alternativas Consideradas

1. **Apenas categorias diferentes**: Simples mas falha (Montanha ≈ Arranha-céu no impacto visual)
2. **Apenas CLIP embedding distance**: Não captura algumas nuances (ambos podem ter cores similares)
3. **Curadoria 100% manual**: Não escala para pools grandes

## Referências
- Documento: `docs/target_database_strategy.md` seção 3
- Insight original: discussão sobre Montanha vs. Arranha-céu
