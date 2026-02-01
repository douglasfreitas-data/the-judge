# The Judge - Brainstorm e Pesquisa Inicial

> **Data:** 2026-02-01  
> **Objetivo:** Consolidar pesquisa sobre tecnologias e conceitos para o sistema de julgamento automático de ARV

---

## 1. Conceito Central

### O Problema
Na Visão Remota Associativa (ARV), o **juiz humano** é o elo mais fraco:
- **Inconsistência**: O mesmo juiz pontua diferente em dias diferentes
- **Viés cognitivo**: Tendência a favorecer alvos mais complexos
- **Fadiga**: Julgar sessões é mentalmente exaustivo
- **Custo**: Não escala para múltiplos visualizadores

### A Solução Proposta: "The Judge"
Um sistema de IA que:
1. Recebe **texto descritivo** e **esboços** do visualizador
2. Converte em **vetores semânticos** (embeddings)
3. Compara com os **alvos candidatos**
4. Gera **score de probabilidade** para cada alvo
5. Emite **predição imparcial**

---

## 2. Estado da Arte: Sistemas Existentes

### 2.1 NOVA Judge (ARVcollective)
O sistema mais avançado atualmente em uso para ARV automatizado.

**Arquitetura:**
```
┌─────────────────┐     ┌─────────────────┐
│  Impressão do   │     │  Imagem Alvo    │
│   Visualizador  │     │    (A ou B)     │
└───────┬─────────┘     └───────┬─────────┘
        │                       │
        ▼                       ▼
┌─────────────────────────────────────────┐
│       Vision LLM (GPT-4V ou similar)    │
│  Gera descritores semânticos e literais │
└───────┬─────────────────────────┬───────┘
        │                         │
        ▼                         ▼
┌───────────────┐         ┌───────────────┐
│  Embeddings   │         │  Embeddings   │
│  (vetores)    │         │  (vetores)    │
└───────┬───────┘         └───────┬───────┘
        │                         │
        └──────────┬──────────────┘
                   ▼
        ┌─────────────────────┐
        │  Chamfer's Algorithm│
        │  (variante assimét.)│
        └──────────┬──────────┘
                   ▼
           ┌─────────────┐
           │  Score Final│
           └─────────────┘
```

**Resultados Reportados:**
- Redução do p-value em **4x**
- Aumento do effect size em **2-2.5%**
- Mais rápido e barato que julgamento humano

**Referência:** [Reddit - AI Judge Breakthrough](https://www.reddit.com/r/remoteviewing/comments/1q3yqwm/ai_judge_breakthrough_its_public/)

---

## 3. Tecnologias-Chave

### 3.1 CLIP (OpenAI) - Embeddings Multimodais

**O que é:** Modelo que mapeia texto e imagens para o mesmo espaço vetorial.

**Capacidades:**
- Zero-shot image classification
- Cross-modal search (texto → imagem, imagem → texto)
- Similaridade semântica entre modalidades

**Limitações:**
- Fraco em tarefas abstratas (contar objetos, proximidade exata)
- Pode ter "acordos errôneos" com imagens semanticamente distintas

**Evolução (2024-2025):**
- OpenCLIP ViT-G/H
- EVA-CLIP
- SigLIP 2
- Llava-Next

**Aplicação no The Judge:**
- Converter descrições textuais em embeddings
- Converter imagens-alvo em embeddings
- Calcular similaridade de cosseno

### 3.2 Sketchformer - Processamento de Esboços

**O que é:** Arquitetura Transformer para representação de esboços.

**Por que é necessário:**
> Modelos treinados em fotos (CLIP, ImageNet) **falham** em interpretar desenhos toscos.
> Os esboços de ARV são frequentemente ideogramas abstratos ou fragmentos visuais.

**Características:**
- Processa esboços como **sequências de traços vetoriais**
- Classificação de esboços
- Sketch-Based Image Retrieval (SBIR)
- Reconstrução e interpolação

**Performance:**
- mAP de 56.96% em Sketch2Image retrieval (Stock10M dataset)
- Supera arquiteturas LSTM anteriores (SketchRNN)

**Evolução:**
- **Sketchformer++**: Arquitetura hierárquica (sketch → stroke → segment)
- **TASK-former**: Combina texto + esboço para retrieval

**Aplicação no The Judge:**
- Processar desenhos do visualizador
- Extrair "conceito" do desenho vs. comparação de pixels
- Gerar embedding do esboço para comparação com alvos

### 3.3 Fuzzy String Matching - Correção de Erros

**Problema:** Visualizadores escrevem com erros (ex: "Condilhatoa" → "Cordilheira")

**Algoritmos Fonéticos:**
| Algoritmo | Descrição | Quando usar |
|-----------|-----------|-------------|
| **Soundex** | Código de 4 caracteres baseado em pronúncia | Nomes, palavras simples |
| **Metaphone** | Regras para inconsistências do inglês | Melhor que Soundex |
| **Double Metaphone** | Dois códigos (primário/secundário) | Origens linguísticas diversas |
| **NYSIIS** | Otimizado para sobrenomes europeus/hispânicos | Nomes específicos |

**Algoritmos de Distância:**
| Biblioteca | Método | Uso |
|------------|--------|-----|
| `difflib` | Ratcliff/Obershelp | Standard library Python |
| `fuzzywuzzy` | Levenshtein + variantes | Mais robusto, word order |

**Aplicação no The Judge:**
- Pré-processar texto do visualizador
- Mapear palavras com erros para termos corretos
- Aumentar recall semântico

---

## 4. Arquitetura Proposta para The Judge

### 4.1 Pipeline de Processamento

```
ENTRADA
   │
   ├─► Texto (palavras-chave, descrições)
   │      │
   │      ├─► Fuzzy Matching (correção de erros)
   │      ├─► Normalização (lowercase, stopwords)
   │      └─► CLIP Text Encoder → Embedding texto
   │
   └─► Esboço (desenho digitalizado)
          │
          ├─► Pré-processamento (binarização, resize)
          ├─► Sketchformer → Embedding esboço
          └─► CLIP Image Encoder (backup) → Embedding imagem

PROCESSAMENTO
   │
   ├─► Fusão de Embeddings (texto + esboço)
   │      │
   │      └─► Weighted Average ou Attention-Based Fusion
   │
   └─► Comparação com Alvos
          │
          ├─► Alvo A: Embedding da imagem A
          └─► Alvo B: Embedding da imagem B

SAÍDA
   │
   ├─► Similaridade(sessão, Alvo A): 72%
   ├─► Similaridade(sessão, Alvo B): 34%
   └─► PREDIÇÃO: Alvo A (confiança: alta)
```

### 4.2 Componentes do Sistema

| Módulo | Tecnologia | Função |
|--------|------------|--------|
| **Text Encoder** | CLIP / OpenCLIP | Embeddings de texto |
| **Sketch Encoder** | Sketchformer | Embeddings de esboços |
| **Image Encoder** | CLIP / ViT | Embeddings de imagens-alvo |
| **Fuzzy Matcher** | fuzzywuzzy + Metaphone | Correção de erros |
| **Similarity Engine** | Cosine Distance + Chamfer | Cálculo de scores |
| **Target Selector** | Algoritmo de Ortogonalidade | Escolha de pares de alvos |

---

## 5. Diferenciais vs. NOVA Judge

| Aspecto | NOVA Judge | The Judge (proposta) |
|---------|------------|---------------------|
| Processamento de esboços | Vision LLM genérico | Sketchformer especializado |
| Correção de erros | Não mencionado | Fuzzy matching fonético |
| Seleção de alvos | Manual/externo | Algoritmo de ortogonalidade integrado |
| Código | Proprietário | Open source |
| Custo | Depende de API LLM | Modelos locais possíveis |

---

## 6. Desafios Técnicos a Resolver

### 6.1 Ruído Semântico
**Problema:** Se o visualizador escreve "vermelho, redondo" e ambos os alvos têm vermelho → confusão.

**Soluções:**
- Ponderar descritores por especificidade (TF-IDF-like)
- Ontologia de RV para pesos diferenciados
- Penalizar termos genéricos

### 6.2 Deslocamento (Displacement)
**Problema:** Visualizador descreve perfeitamente o alvo errado.

**Soluções:**
- Tracking histórico por visualizador
- Inversão automática se padrão de displacement detectado
- Flag de "sessão ambígua" quando scores são próximos

### 6.3 Ortogonalidade dos Alvos
**Problema:** Se alvos são similares (Mar vs. Lago), predição falha.

**Soluções:**
- Algoritmo de seleção que garante distância mínima
- Banco de alvos vetorizados com métricas pré-calculadas
- Rejeição automática de pares com similaridade > threshold

### 6.4 Qualidade dos Esboços
**Problema:** Desenhos muito abstratos ou minimalistas.

**Soluções:**
- Múltiplos encoders (Sketchformer + CLIP)
- Fallback para análise apenas textual
- Pedir redesenho se confiança muito baixa

---

## 7. Stack Tecnológico Proposto

### Backend
- **Python 3.11+** - Linguagem principal
- **FastAPI** - API REST
- **PyTorch** - Framework ML
- **Transformers (HuggingFace)** - Modelos pré-treinados
- **OpenCLIP** - Embeddings multimodais
- **fuzzywuzzy** - Fuzzy matching

### Frontend
- **Next.js / React** - Interface web
- **Canvas API** - Captura de esboços
- **TailwindCSS** - Estilização

### Banco de Dados
- **PostgreSQL** - Dados relacionais
- **pgvector** - Armazenamento de embeddings
- **Redis** - Cache de sessões

### Infraestrutura
- **Docker** - Containerização
- **GitHub Actions** - CI/CD

---

## 8. Próximos Passos

1. [ ] **Prova de Conceito**: Testar CLIP + texto em cenário ARV simples
2. [ ] **Integrar Sketchformer**: Adicionar processamento de esboços
3. [ ] **Banco de Alvos**: Criar base de imagens vetorizadas
4. [ ] **Interface Web**: MVP para captura de sessões
5. [ ] **Validação**: Comparar com julgamento humano em dados históricos

---

## 9. Referências

### Artigos e Pesquisas
- [Sketchformer: Transformer-Based Representation for Sketched Structure (CVPR 2020)](https://openaccess.thecvf.com/content_CVPR_2020/papers/Ribeiro_Sketchformer_Transformer-Based_Representation_for_Sketched_Structure_CVPR_2020_paper.pdf)
- [CLIP: Learning Transferable Visual Models (OpenAI)](https://openai.com/research/clip)
- [An Ethnographical Assessment of Project Firefly (ResearchGate)](https://www.researchgate.net/publication/324526120)
- [Stock Market Prediction Using ARV (ResearchGate)](https://www.researchgate.net/publication/272151807)

### Ferramentas e Bibliotecas
- [OpenCLIP (GitHub)](https://github.com/mlfoundations/open_clip)
- [Sketchformer (GitHub)](https://github.com/leosampaio/sketchformer)
- [fuzzywuzzy (PyPI)](https://pypi.org/project/fuzzywuzzy/)
- [metaphone (PyPI)](https://pypi.org/project/metaphone/)

### Comunidades
- [Applied Precognition Project](https://www.appliedprecog.com/)
- [r/remoteviewing (Reddit)](https://www.reddit.com/r/remoteviewing/)
