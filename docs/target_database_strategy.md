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

## 3. Ortogonalidade Multidimensional

> ⚠️ **Insight crucial:** Categoria ≠ Ortogonalidade!
> 
> Montanha vs. Arranha-céu parecem opostos (natureza vs. urbano), mas compartilham:
> - **Escala:** Ambos são grandes/altos
> - **Forma:** Verticais, triangulares/retangulares
> - **Emoção:** Grandiosidade, imponência

### 3.1 Dimensões de Análise

Para garantir alvos verdadeiramente distintos, cada imagem deve ser avaliada em **múltiplas dimensões**:

| Dimensão | Escala | Exemplos de Opostos |
|----------|--------|---------------------|
| **Escala** | Minúsculo ↔ Gigante | Formiga vs. Montanha |
| **Forma** | Orgânico ↔ Geométrico | Nuvem vs. Cubo de Rubik |
| **Cor Dominante** | Cores quentes ↔ Cores frias | Vulcão vs. Iceberg |
| **Brilho** | Escuro ↔ Claro | Caverna vs. Praia ensolarada |
| **Textura** | Liso ↔ Rugoso | Espelho vs. Casca de árvore |
| **Movimento** | Estático ↔ Dinâmico | Pedra vs. Cachoeira |
| **Densidade** | Vazio ↔ Cheio | Deserto vs. Floresta densa |
| **Emoção** | Calma ↔ Intensidade | Lago sereno vs. Tempestade |
| **Orientação** | Horizontal ↔ Vertical | Horizon vs. Arranha-céu |
| **Natureza** | Natural ↔ Artificial | Floresta vs. Circuito eletrônico |

### 3.2 Exemplos de Pares BONS (Alta Ortogonalidade)

```
✅ ALTA ORTOGONALIDADE (Oposto em múltiplas dimensões)

┌─────────────────────┐     ┌─────────────────────┐
│   🌸 FLOR           │ vs. │   🏢 ARRANHA-CÉU    │
├─────────────────────┤     ├─────────────────────┤
│ Escala: Pequeno     │     │ Escala: Gigante     │
│ Forma: Orgânico     │     │ Forma: Geométrico   │
│ Orientação: Baixo   │     │ Orientação: Alto    │
│ Textura: Delicado   │     │ Textura: Duro       │
│ Emoção: Suave       │     │ Emoção: Imponente   │
└─────────────────────┘     └─────────────────────┘
Dimensões opostas: 5/5 ✓

┌─────────────────────┐     ┌─────────────────────┐
│   🔥 FOGUEIRA       │ vs. │   🐧 PINGUIM        │
├─────────────────────┤     ├─────────────────────┤
│ Temperatura: Quente │     │ Temperatura: Frio   │
│ Cor: Laranja/vermelho│    │ Cor: Preto/branco   │
│ Movimento: Caótico  │     │ Movimento: Calmo    │
│ Textura: Etéreo     │     │ Textura: Penas      │
│ Emoção: Perigo      │     │ Emoção: Fofura      │
└─────────────────────┘     └─────────────────────┘
Dimensões opostas: 5/5 ✓

┌─────────────────────┐     ┌─────────────────────┐
│   🌊 ONDA GIGANTE   │ vs. │   🏜️ DESERTO       │
├─────────────────────┤     ├─────────────────────┤
│ Elemento: Água      │     │ Elemento: Terra/Areia│
│ Cor: Azul           │     │ Cor: Bege/Dourado   │
│ Movimento: Intenso  │     │ Movimento: Estático │
│ Densidade: Cheio    │     │ Densidade: Vazio    │
│ Umidade: Molhado    │     │ Umidade: Seco       │
└─────────────────────┘     └─────────────────────┘
Dimensões opostas: 5/5 ✓
```

### 3.3 Exemplos de Pares RUINS (Baixa Ortogonalidade)

```
❌ BAIXA ORTOGONALIDADE (Parecem opostos, mas não são)

┌─────────────────────┐     ┌─────────────────────┐
│   🏔️ MONTANHA      │ vs. │   🏢 ARRANHA-CÉU    │
├─────────────────────┤     ├─────────────────────┤
│ Escala: GIGANTE     │     │ Escala: GIGANTE     │ ← Igual!
│ Orientação: VERTICAL│     │ Orientação: VERTICAL│ ← Igual!
│ Emoção: IMPONENTE   │     │ Emoção: IMPONENTE   │ ← Igual!
│ Forma: Triangular   │     │ Forma: Retangular   │
│ Natureza: Natural   │     │ Natureza: Artificial│
└─────────────────────┘     └─────────────────────┘
Dimensões opostas: 2/5 ✗ (RUIM!)

┌─────────────────────┐     ┌─────────────────────┐
│   🌊 OCEANO         │ vs. │   🏞️ LAGO          │
├─────────────────────┤     ├─────────────────────┤
│ Elemento: ÁGUA      │     │ Elemento: ÁGUA      │ ← Igual!
│ Cor: AZUL           │     │ Cor: AZUL           │ ← Igual!
│ Textura: LÍQUIDO    │     │ Textura: LÍQUIDO    │ ← Igual!
│ Emoção: Força       │     │ Emoção: Calma       │
│ Escala: Grande      │     │ Escala: Médio       │
└─────────────────────┘     └─────────────────────┘
Dimensões opostas: 2/5 ✗ (RUIM!)
```

### 3.4 Pares Sugeridos de Alta Qualidade

| Alvo A | Alvo B | Por que funciona? |
|--------|--------|-------------------|
| Flor close-up | Arranha-céu distante | Pequeno/grande, orgânico/geométrico, horizontal/vertical |
| Fogueira | Iceberg | Quente/frio, vermelho/azul, movimento/estático |
| Borboleta | Tanque de guerra | Delicado/pesado, colorido/monocromático, leve/massivo |
| Bebê dormindo | Vulcão em erupção | Calma/caos, pequeno/grande, seguro/perigoso |
| Praia tropical | Sala de cirurgia | Natural/artificial, relaxante/tenso, cores quentes/frias |
| Galaxia (foto do Hubble) | Formiga close-up | Imenso/minúsculo, distante/próximo, cósmico/terrestre |
| Balão colorido | Submarino | Leve/pesado, ar/água, alegre/sério, colorido/escuro |
| Relâmpago | Tartaruga | Rápido/lento, energia/calma, caótico/sereno |
| Cubo de gelo | Dançarina de fogo | Sólido/movimento, frio/quente, transparente/brilhante |

### 3.5 Características Marcantes (Alta Numinosidade)

Imagens que funcionam melhor na ARV têm **alta numinosidade** (impacto emocional/visual):

| ✅ USAR | ❌ EVITAR |
|---------|-----------|
| Torre Eiffel à noite | Prédio genérico |
| Vulcão em erupção | Montanha comum |
| Aurora Boreal | Céu nublado |
| Tigre rugindo | Gato dormindo |
| Cachoeira imensa | Riacho pequeno |
| Astronauta no espaço | Pessoa andando |
| Relâmpago atingindo torre | Chuva comum |

### 3.6 Perfil de Imagem (Schema Atualizado)

```json
{
  "id": "uuid",
  "source": "unsplash",
  "url": "...",
  
  "dimensions": {
    "scale": 0.9,           // 0=minúsculo, 1=gigante
    "organic_vs_geometric": 0.2,  // 0=orgânico, 1=geométrico
    "warm_vs_cold": 0.8,    // 0=frio, 1=quente
    "static_vs_dynamic": 0.7,  // 0=estático, 1=dinâmico
    "empty_vs_dense": 0.4,  // 0=vazio, 1=cheio
    "calm_vs_intense": 0.9, // 0=calma, 1=intenso
    "horizontal_vs_vertical": 0.6, // 0=horizontal, 1=vertical
    "natural_vs_artificial": 0.1,  // 0=natural, 1=artificial
    "light_vs_dark": 0.7,   // 0=escuro, 1=claro
    "smooth_vs_textured": 0.3      // 0=liso, 1=rugoso
  },
  
  "numinosity": 0.85,  // Impacto visual/emocional (0-1)
  "embedding": [...]   // Vetor CLIP
}
```

### 3.7 Algoritmo de Ortogonalidade Multidimensional

```python
def calculate_multidimensional_orthogonality(img_a: dict, img_b: dict) -> float:
    """
    Calcula ortogonalidade baseada em diferença em múltiplas dimensões.
    
    Retorna valor entre 0 (idêntico) e 1 (totalmente oposto).
    """
    dimensions = [
        'scale', 'organic_vs_geometric', 'warm_vs_cold', 
        'static_vs_dynamic', 'empty_vs_dense', 'calm_vs_intense',
        'horizontal_vs_vertical', 'natural_vs_artificial',
        'light_vs_dark', 'smooth_vs_textured'
    ]
    
    total_difference = 0
    for dim in dimensions:
        diff = abs(img_a['dimensions'][dim] - img_b['dimensions'][dim])
        total_difference += diff
    
    # Normaliza para 0-1
    orthogonality = total_difference / len(dimensions)
    
    return orthogonality

def select_optimal_pair(pool: list, min_orthogonality: float = 0.6) -> tuple:
    """
    Seleciona par com maior ortogonalidade multidimensional.
    """
    best_pair = None
    best_score = 0
    
    for img_a, img_b in combinations(pool, 2):
        # Ortogonalidade multidimensional
        multi_score = calculate_multidimensional_orthogonality(img_a, img_b)
        
        # Ortogonalidade via CLIP (embedding)
        clip_score = 1 - cosine_similarity(img_a['embedding'], img_b['embedding'])
        
        # Score combinado (média ponderada)
        combined = 0.6 * multi_score + 0.4 * clip_score
        
        # Bonus para alta numinosidade em ambos
        numinosity_bonus = (img_a['numinosity'] + img_b['numinosity']) / 4
        final_score = combined + numinosity_bonus
        
        if final_score > best_score and multi_score >= min_orthogonality:
            best_score = final_score
            best_pair = (img_a, img_b)
    
    return best_pair
```

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
