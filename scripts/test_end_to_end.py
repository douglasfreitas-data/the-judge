"""
The Judge - End-to-End Test
===========================
Testa o julgamento usando targets reais cadastrados no Supabase.
"""

import sys
import numpy as np
from tabulate import tabulate

# Adiciona src ao path
sys.path.insert(0, ".")

from src.database import get_supabase
from src.core import CLIPEncoder, rank_targets, calculate_confidence
from src.repositories import TargetRepository

VOLCANO_ID = "12f1d984-21bd-4ee2-88d8-90fbee0fb230"
PENGUIN_ID = "82ac4473-938b-4279-8f20-d06445c03607"

SCENARIOS = [
    {
        "name": "🔥 Descrição de Fogo",
        "text": "intense heat, red flames, explosion, smoke, dark sky, lava flowing, dangerous energy"
    },
    {
        "name": "🐧 Descrição de Gelo",
        "text": "cold ice, white snow, peaceful bird, antarctica, frozen landscape, quiet, calm"
    },
    {
        "name": "🌊 Descrição Neutra (Água)",
        "text": "water flowing, blue colors, nature scene, liquid" # Ambíguo: pinguim tem gelo (água), mas vulcão não
    },
    {
        "name": "🤔 Descrição Confusa",
        "text": "a red bird playing in the snow with fire"
    }
]


def main():
    print("🧪 Iniciando Teste End-to-End com Targets Reais")
    print("=" * 60)
    
    # Setup
    db = get_supabase()
    repo = TargetRepository()
    encoder = CLIPEncoder()
    
    # 1. Recuperar Embeddings
    print("📥 Recuperando embeddings do Supabase...")
    emb_volcano = repo.get_embedding(VOLCANO_ID)
    emb_penguin = repo.get_embedding(PENGUIN_ID)
    
    if emb_volcano is None or emb_penguin is None:
        print("❌ Falha ao recuperar embeddings. Rode register_targets.py primeiro.")
        return

    # Verificar ortogonalidade
    sim = np.dot(emb_volcano, emb_penguin)
    ortho = 1 - sim
    print(f"📉 Similaridade Visual entre Targets: {sim:.4f}")
    print(f"📐 Ortogonalidade: {ortho:.4f} (Ideal > 0.7)")
    print("-" * 60)
    
    # 2. Rodar Cenários
    results = []
    
    for scenario in SCENARIOS:
        print(f"\n🔮 Testando: {scenario['name']}")
        print(f"   📝 Texto: \"{scenario['text']}\"")
        
        # Encode texto
        text_emb = encoder.encode_text(scenario['text'])
        
        # Julgamento
        # Target A = Vulcão, Target B = Pinguim
        winner, scores = rank_targets(text_emb, emb_volcano, emb_penguin)
        confidence = calculate_confidence(scores["score_a"], scores["score_b"])
        
        # Formatar resultado
        winner_name = "VULCÃO (A)" if winner == "A" else "PINGUIM (B)"
        if winner == "TIE": winner_name = "EMPATE"
        
        results.append([
            scenario['name'],
            f"{scores['score_a']:.4f}",  # Score Vulcão
            f"{scores['score_b']:.4f}",  # Score Pinguim
            f"{scores['difference']:.4f}",
            winner_name,
            f"{confidence*100:.1f}%"
        ])
        
        print(f"   🏆 Resultado: {winner_name} (Confiança: {confidence*100:.1f}%)")

    # 3. Tabela Final
    print("\n" + "=" * 60)
    print("RESUMO DOS RESULTADOS (A=Vulcão, B=Pinguim)")
    print("=" * 60)
    headers = ["Cenário", "Score A", "Score B", "Diff", "Vencedor", "Confiança"]
    print(tabulate(results, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
