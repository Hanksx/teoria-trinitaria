#!/usr/bin/env python3
"""
VALIDAÇÃO SPARC COM BOUNDS MAIORES - Corrigindo Saturação de Parâmetros

CRÍTICA #1: Parâmetros saturaram nos limites superiores
SOLUÇÃO: Aumentar bounds por 4-5x e reotimizar

Bounds ANTIGOS (saturados):
- Af: 0.01-50.0  → saturou em 50.0
- Aq: 0.0-1.0    → saturou em 1.0
- λ:  0.1-10.0   → saturou em 10.0
- τ:  0.1-5.0    → saturou em 5.0
- β:  0.2-3.0    → saturou em 3.0

Bounds NOVOS (expandidos):
- Af: 0.01-200.0  (4x)
- Aq: 0.0-5.0     (5x)
- λ:  0.1-50.0    (5x)
- τ:  0.1-20.0    (4x)
- β:  0.2-10.0    (3.3x)
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from scipy.optimize import differential_evolution

# Importar funções do código original
import sys
sys.path.append('/Users/nilsilva/Desktop/espiral_fractal')

try:
    from sparc_downloader import SPARCDatasetManager
except ImportError:
    print("⚠️  Não foi possível importar sparc_downloader")
    print("Execute este script de dentro do diretório espiral_fractal")
    sys.exit(1)


def velocidade_trinitaria_simples(r_kpc, params):
    """
    Modelo Trinitária simplificado para otimização rápida
    
    Parâmetros:
    - params[0]: Af (amplitude fractal)
    - params[1]: Aq (amplitude quântica)
    - params[2]: λ (length scale)
    - params[3]: τ (decay rate)
    - params[4]: β (baryonic boost)
    
    Fixos: N=4, L=5, Q=4.0
    """
    Af, Aq, lambda_scale, tau, beta = params
    
    # Componente Fractal (N=4)
    v_fractal = Af * np.exp(-r_kpc / (lambda_scale * tau))
    for n in range(1, 5):  # N=4
        v_fractal *= (1 + 0.1 * np.sin(2 * np.pi * n * r_kpc / lambda_scale))
    
    # Componente Quântico (L=5, Fibonacci [1,1,2,3,5])
    fibonacci = [1, 1, 2, 3, 5]
    v_quantum = 0
    for i, fib in enumerate(fibonacci):
        r_center = i * lambda_scale / 5
        v_quantum += Aq * (fib / 5) * np.exp(-((r_kpc - r_center) / lambda_scale) ** 2)
    
    # Componente Confinamento (Q=4.0 fixo)
    v_confinement = 4.0 * (1 - np.exp(-r_kpc / (2 * lambda_scale)))
    
    # Combinação quadrática
    v_total = np.sqrt(v_fractal**2 + v_quantum**2 + v_confinement**2)
    
    return v_total


def avaliar_modelo(params, galaxias_treino):
    """Avaliar RMS médio no conjunto de treinamento"""
    rms_values = []
    
    for galaxy in galaxias_treino:
        r_kpc = galaxy['r_kpc']
        v_obs = galaxy['v_kms']
        
        # Calcular velocidade do modelo
        v_model = velocidade_trinitaria_simples(r_kpc, params)
        
        # Boost bariônico simples (se disponível)
        if 'v_gas' in galaxy and galaxy['v_gas'] is not None:
            v_gas = galaxy['v_gas']
            beta = params[4]
            v_model = np.sqrt(v_model**2 + (beta * v_gas)**2)
        
        # RMS
        rms = np.sqrt(np.mean((v_model - v_obs)**2))
        rms_values.append(rms)
    
    return np.mean(rms_values)


def otimizar_com_bounds_maiores():
    """
    Otimização completa com bounds expandidos
    """
    print("=" * 80)
    print("VALIDAÇÃO SPARC - BOUNDS MAIORES (Corrigindo Saturação)")
    print("=" * 80)
    
    start_time = datetime.now()
    
    # 1. Carregar dados SPARC
    print("\n📊 Carregando dados SPARC...")
    
    data_dir = Path("/Users/nilsilva/Desktop/teoria_trinitaria_publicacao/data/sparc_data_real")
    if not data_dir.exists():
        data_dir = Path("/Users/nilsilva/Desktop/espiral_fractal/sparc_data_real")
    
    manager = SPARCDatasetManager(str(data_dir))
    
    try:
        sparc_galaxies = manager.load_sparc_dataset()
        print(f"✅ Carregadas {len(sparc_galaxies)} galáxias SPARC")
    except Exception as e:
        print(f"❌ Erro ao carregar SPARC: {e}")
        return None
    
    # 2. Filtrar galáxias de qualidade
    galaxias_validas = []
    for galaxy in sparc_galaxies:
        if galaxy.quality <= 2 and galaxy.v_flat > 0:
            galaxias_validas.append({
                'name': galaxy.name,
                'r_kpc': galaxy.r_kpc,
                'v_kms': galaxy.v_kms,
                'v_err_kms': galaxy.v_err_kms,
                'v_gas': getattr(galaxy, 'v_gas', None)
            })
    
    print(f"✅ Selecionadas {len(galaxias_validas)} galáxias (Q≤2, Vflat>0)")
    
    # 3. Split treino/teste (70/30, seed=42)
    np.random.seed(42)
    indices = np.random.permutation(len(galaxias_validas))
    n_train = int(0.7 * len(galaxias_validas))
    
    galaxias_treino = [galaxias_validas[i] for i in indices[:n_train]]
    galaxias_teste = [galaxias_validas[i] for i in indices[n_train:]]
    
    print(f"\n📈 Split: {len(galaxias_treino)} treino / {len(galaxias_teste)} teste")
    
    # 4. BOUNDS MAIORES (corrigindo saturação)
    print("\n🔧 BOUNDS EXPANDIDOS:")
    print("   Af: 0.01 → 200.0 km/s (4x)")
    print("   Aq: 0.0  → 5.0 km/s   (5x)")
    print("   λ:  0.1  → 50.0 kpc   (5x)")
    print("   τ:  0.1  → 20.0       (4x)")
    print("   β:  0.2  → 10.0       (3.3x)")
    
    bounds = [
        (0.01, 200.0),  # Af - fractal amplitude
        (0.0, 5.0),     # Aq - quantum amplitude
        (0.1, 50.0),    # λ  - length scale
        (0.1, 20.0),    # τ  - decay rate
        (0.2, 10.0)     # β  - baryonic boost
    ]
    
    # 5. Otimização com Differential Evolution
    print("\n🚀 Iniciando otimização (Differential Evolution)...")
    print("   Gerações máximas: 20")
    print("   População: 15 x 5 parâmetros = 75 indivíduos")
    
    resultado = differential_evolution(
        lambda params: avaliar_modelo(params, galaxias_treino),
        bounds,
        maxiter=20,
        popsize=15,
        seed=42,
        atol=0.01,
        tol=0.01,
        workers=1,
        updating='deferred',
        disp=True
    )
    
    params_otimizados = resultado.x
    rms_treino = resultado.fun
    
    print(f"\n✅ Otimização concluída!")
    print(f"   RMS treino: {rms_treino:.2f} km/s")
    
    # 6. Avaliar no conjunto de teste
    print("\n🧪 Avaliando no conjunto de teste...")
    rms_teste = avaliar_modelo(params_otimizados, galaxias_teste)
    
    print(f"   RMS teste: {rms_teste:.2f} km/s")
    
    # 7. Análise de saturação
    print("\n📊 ANÁLISE DE SATURAÇÃO:")
    param_names = ['Af', 'Aq', 'λ', 'τ', 'β']
    saturated = []
    
    for i, (name, value, (low, high)) in enumerate(zip(param_names, params_otimizados, bounds)):
        margin_low = (value - low) / (high - low)
        margin_high = (high - value) / (high - low)
        
        is_saturated_low = margin_low < 0.05
        is_saturated_high = margin_high < 0.05
        
        status = "✅ OK"
        if is_saturated_low:
            status = "🔴 SATURADO (mínimo)"
            saturated.append(name)
        elif is_saturated_high:
            status = "🔴 SATURADO (máximo)"
            saturated.append(name)
        elif margin_low < 0.15 or margin_high < 0.15:
            status = "⚠️  PRÓXIMO"
        
        print(f"   {name}: {value:.4f} [{low:.2f}, {high:.2f}] {status}")
    
    # 8. Resultados detalhados
    gap = ((rms_teste - rms_treino) / rms_treino) * 100
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'n_galaxies_total': len(galaxias_validas),
        'n_train': len(galaxias_treino),
        'n_test': len(galaxias_teste),
        'bounds_old': {
            'Af': [0.01, 50.0],
            'Aq': [0.0, 1.0],
            'lambda': [0.1, 10.0],
            'tau': [0.1, 5.0],
            'beta': [0.2, 3.0]
        },
        'bounds_new': {
            'Af': [0.01, 200.0],
            'Aq': [0.0, 5.0],
            'lambda': [0.1, 50.0],
            'tau': [0.1, 20.0],
            'beta': [0.2, 10.0]
        },
        'parameters_optimized': {
            'Af': float(params_otimizados[0]),
            'Aq': float(params_otimizados[1]),
            'lambda': float(params_otimizados[2]),
            'tau': float(params_otimizados[3]),
            'beta': float(params_otimizados[4]),
            'N': 4,
            'L': 5,
            'Q': 4.0
        },
        'performance': {
            'train_rms': float(rms_treino),
            'test_rms': float(rms_teste),
            'gap_percent': float(gap)
        },
        'saturation_analysis': {
            'saturated_parameters': saturated,
            'status': 'RESOLVED' if len(saturated) == 0 else 'STILL_SATURATED'
        },
        'execution_time_seconds': (datetime.now() - start_time).total_seconds()
    }
    
    # 9. Salvar resultados
    output_file = Path("code/validacao_sparc_bounds_maiores.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Resultados salvos em: {output_file}")
    
    # 10. Resumo final
    print("\n" + "=" * 80)
    print("RESUMO FINAL")
    print("=" * 80)
    
    print(f"\n📊 PARÂMETROS OTIMIZADOS (BOUNDS MAIORES):")
    for name, value in zip(param_names, params_otimizados):
        print(f"   {name}: {value:.4f}")
    
    print(f"\n📈 PERFORMANCE:")
    print(f"   RMS Treino: {rms_treino:.2f} km/s")
    print(f"   RMS Teste:  {rms_teste:.2f} km/s")
    print(f"   Gap:        {gap:+.2f}%")
    
    if len(saturated) == 0:
        print(f"\n🎉 SUCESSO! Nenhum parâmetro saturado!")
        print(f"   ✅ Crítica #1 RESOLVIDA")
    else:
        print(f"\n⚠️  ATENÇÃO: {len(saturated)} parâmetro(s) ainda saturado(s):")
        for param in saturated:
            print(f"   - {param}")
        print(f"   Considere aumentar bounds ainda mais.")
    
    print(f"\n⏱️  Tempo total: {results['execution_time_seconds']:.1f}s")
    
    return results


if __name__ == "__main__":
    try:
        results = otimizar_com_bounds_maiores()
        
        if results is None:
            print("\n❌ Otimização falhou!")
            sys.exit(1)
        
        print("\n✅ Script concluído com sucesso!")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
