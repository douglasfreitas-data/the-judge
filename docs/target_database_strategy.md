# The Judge - Estratégia para Banco de Imagens-Alvo

> **Data:** 2026-02-01

---

## 1. O Desafio da Dupla Cegueira

Você levantou um ponto crítico: **como ter alvos sem saber quais são?**

### Soluções Possíveis

| Abordagem | Descrição | Prós | Contras |
|-----------|-----------|------|---------|
| **Admin Separado** | Outra pessoa configura os alvos | Cegueira total | Depende de terceiros |
| **Seleção Automática** | IA escolhe pares aleatórios de um pool grande | Escalável, cego | Precisa de pool inicial |
| **Modo Teste vs. Prod** | Você usa subset para testes, pool completo para real | Prático | Leve contaminação possível |
| **Banco Externo** | Usar base da IONS ou APP | Validada cientificamente | Dependência externa |

### Recomendação
**Modo Teste vs. Produção** + **Seleção Automática**:
- Você constrói um pool de 500-1000 imagens para testes
- Em produção, o sistema seleciona de um pool de 10.000+ imagens que você nunca vê diretamente

---

## 2. Fontes de Imagens

### 2.1 IONS Image Database (Em Desenvolvimento)

O **Institute of Noetic Sciences** está criando uma base especificamente para ARV:
- **2.000-3.000 imagens** normalizadas
- **18 dimensões** avaliadas: abstração, numinosidade, emocionalidade, complexidade visual
- **Open source** (quando lançado)
- Referência: [noetic.org](https://noetic.org)

> ⚠️ **Status**: Em desenvolvimento, ainda não disponível publicamente

### 2.2 Unsplash Dataset

| Versão | Imagens | Uso | Licença |
|--------|---------|-----|---------|
| **Lite** | 25.000 (natureza) | ✅ Comercial | Livre |
| **Full** | 6.5M+ | ⚠️ Não-comercial | Pesquisa |

**Vantagens:**
- Metadados ricos (keywords, EXIF, localização)
- Categorias organizadas
- Alta qualidade

**API:** https://unsplash.com/developers

### 2.3 Pexels Dataset

- **Pexels-400k**: 400.000 imagens com atributos
- Disponível no HuggingFace e Kaggle
- Uso livre

### 2.4 Outras Fontes

| Dataset | Imagens | Categorias | Uso |
|---------|---------|------------|-----|
| ImageNet | 14M+ | 21.841 | Pesquisa |
| Open Images | 9M+ | 6.000 | Livre |
| Places | 10M+ | 400 cenas | Pesquisa |

---

## 3. Categorias de Alvos Recomendadas

Para garantir **ortogonalidade** (alvos bem distintos), usar categorias contrastantes:

### Pares Ortogonais Sugeridos

```
NATUREZA vs. URBANO
┌─────────────────┐     ┌─────────────────┐
│   Montanha      │ vs. │   Arranha-céu   │
│   Floresta      │ vs. │   Fábrica       │
│   Praia         │ vs. │   Metrô         │
│   Cachoeira     │ vs. │   Estacionamento│
└─────────────────┘     └─────────────────┘

ORGÂNICO vs. MECÂNICO
┌─────────────────┐     ┌─────────────────┐
│   Árvore        │ vs. │   Engrenagem    │
│   Animal        │ vs. │   Robô          │
│   Flor          │ vs. │   Circuito      │
└─────────────────┘     └─────────────────┘

QUENTE vs. FRIO
┌─────────────────┐     ┌─────────────────┐
│   Vulcão        │ vs. │   Iceberg       │
│   Deserto       │ vs. │   Neve          │
│   Fogo          │ vs. │   Gelo          │
└─────────────────┘     └─────────────────┘

ÁGUA vs. TERRA
┌─────────────────┐     ┌─────────────────┐
│   Oceano        │ vs. │   Montanha      │
│   Rio           │ vs. │   Caverna       │
│   Aquário       │ vs. │   Deserto       │
└─────────────────┘     └─────────────────┘
```

### Categorias Principais

| Categoria | Exemplos | Características |
|-----------|----------|-----------------|
| **Natureza** | Montanhas, florestas, praias | Orgânico, curvas, verde/azul |
| **Urbano** | Cidades, prédios, ruas | Linhas retas, cinza, artificial |
| **Água** | Oceanos, rios, cachoeiras | Movimento, azul, reflexos |
| **Fogo** | Vulcões, fogueiras, lava | Vermelho/laranja, energia |
| **Animais** | Selvagens, domésticos | Vida, movimento, pelos/penas |
| **Pessoas** | Retratos, multidões | Faces, emoções |
| **Objetos** | Carros, ferramentas, comida | Específico, cores variadas |
| **Abstrato** | Arte, padrões, texturas | Formas, cores |
| **Lugares Famosos** | Torre Eiffel, Pirâmides | Reconhecível, icônico |

---

## 4. Algoritmo de Seleção de Pares

### 4.1 Cálculo de Ortogonalidade

```python
def calculate_orthogonality(image_a_embedding, image_b_embedding):
    """
    Quanto MENOR a similaridade, MAIS ortogonais são os alvos.
    Ideal: similaridade < 0.3
    """
    similarity = cosine_similarity(image_a_embedding, image_b_embedding)
    orthogonality = 1 - similarity
    return orthogonality

def select_target_pair(image_pool, min_orthogonality=0.7):
    """
    Seleciona par de imagens com máxima distinção.
    """
    best_pair = None
    best_score = 0
    
    for img_a, img_b in combinations(image_pool, 2):
        score = calculate_orthogonality(img_a.embedding, img_b.embedding)
        if score > best_score and score >= min_orthogonality:
            best_score = score
            best_pair = (img_a, img_b)
    
    return best_pair
```

### 4.2 Filtros Adicionais

- **Categorias diferentes**: Não usar duas imagens da mesma categoria
- **Cores dominantes diferentes**: Evitar dois alvos azuis, por exemplo
- **Sem repetição recente**: Não reutilizar imagens usadas nos últimos N dias

---

## 5. Estrutura do Banco de Dados

### Schema Proposto

```sql
-- Categorias de imagens
CREATE TABLE target_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE,  -- 'nature', 'urban', 'water', etc.
    description TEXT
);

-- Pool de imagens-alvo
CREATE TABLE targets (
    id UUID PRIMARY KEY,
    category_id INT REFERENCES target_categories(id),
    source VARCHAR(50),       -- 'unsplash', 'pexels', 'custom'
    source_id VARCHAR(255),   -- ID original na fonte
    file_path VARCHAR(500),
    thumbnail_path VARCHAR(500),
    
    -- Metadados visuais
    dominant_color VARCHAR(7),  -- Hex color
    brightness FLOAT,           -- 0-1
    complexity FLOAT,           -- 0-1 (entropia visual)
    
    -- Embedding pré-calculado
    embedding VECTOR(512),      -- pgvector
    
    -- Controle
    times_used INT DEFAULT 0,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Pares utilizados (histórico)
CREATE TABLE target_pairs (
    id UUID PRIMARY KEY,
    event_id UUID,
    target_a_id UUID REFERENCES targets(id),
    target_b_id UUID REFERENCES targets(id),
    orthogonality_score FLOAT,
    result CHAR(1),  -- 'A', 'B', ou NULL
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 6. Plano de Coleta Inicial

### Fase 1: Pool de Desenvolvimento (100 imagens)

```bash
# Estrutura de pastas
data/targets/
├── nature/          # 20 imagens
├── urban/           # 20 imagens  
├── water/           # 15 imagens
├── fire/            # 10 imagens
├── animals/         # 15 imagens
├── famous_places/   # 10 imagens
└── abstract/        # 10 imagens
```

**Fonte recomendada:** Unsplash Lite (gratuito, comercial)

### Fase 2: Pool de Produção (1000+ imagens)

- Download via API Unsplash/Pexels
- Script automatizado para:
  1. Baixar imagens por categoria
  2. Gerar embeddings CLIP
  3. Calcular metadados (cor, complexidade)
  4. Validar ortogonalidade mínima

### Fase 3: Pool Expandido (10.000+ imagens)

- Integração contínua com APIs
- Crowdsourcing de imagens
- Curadoria comunitária

---

## 7. Script de Coleta (Sugerido)

```python
# scripts/collect_targets.py

import requests
from PIL import Image
import torch
import open_clip

class TargetCollector:
    def __init__(self, unsplash_key: str):
        self.unsplash_key = unsplash_key
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            'ViT-B-32', pretrained='openai'
        )
    
    def fetch_from_unsplash(self, query: str, count: int = 30):
        """Busca imagens do Unsplash por categoria."""
        url = f"https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": count,
            "orientation": "landscape"
        }
        headers = {"Authorization": f"Client-ID {self.unsplash_key}"}
        
        response = requests.get(url, params=params, headers=headers)
        return response.json()["results"]
    
    def generate_embedding(self, image_path: str):
        """Gera embedding CLIP para uma imagem."""
        image = Image.open(image_path)
        image_input = self.preprocess(image).unsqueeze(0)
        
        with torch.no_grad():
            embedding = self.model.encode_image(image_input)
        
        return embedding.numpy().flatten()
    
    def calculate_complexity(self, image_path: str):
        """Calcula entropia visual (complexidade)."""
        # Implementar usando histograma de cores
        pass
```

---

## 8. Considerações de Segurança (Cegueira)

### Para Testes (Você pode ver)
- Use subset de ~100 imagens conhecidas
- Foco em validar o algoritmo de similaridade
- Resultados não contam para estatísticas reais

### Para Produção (Você NÃO deve ver)
- Pool de 1000+ imagens nunca visualizadas
- Seleção 100% automatizada
- Apenas vê a imagem APÓS o feedback do evento
- Considerar: admin separado para curadoria inicial

---

## Próximos Passos

1. [ ] Registrar conta na API do Unsplash
2. [ ] Criar script de coleta inicial (100 imagens)
3. [ ] Implementar geração de embeddings
4. [ ] Testar algoritmo de ortogonalidade
