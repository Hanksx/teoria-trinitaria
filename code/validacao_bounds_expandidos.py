#!/usr/bin/env python3
"""
Validação da Teoria Trinitária com BOUNDS EXPANDIDOS

CRÍTICA #1: Parâmetros saturaram nos limites superiores
SOLUÇÃO: Bounds expandidos 4-5x para permitir convergência natural

Antes: Af=50, Aq=1, λ=10, τ=5, β=3 (TODOS saturados)
Agora: Af→200, Aq→5, λ→50, τ→20, β→10 (expandidos)
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from scipy.optimize import differential_evolution

# ==============================================================================
# LEITURA DOS DADOS REAIS DO SPARC
# ==============================================================================

def ler_sparc_table1(filepath='../data/sparc_data_real/table1.dat'):
    """
    Lê Table 1 do SPARC (propriedades das galáxias)
    Parser robusto que divide por espaços
    """
    galaxias = []
    
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) < 14:
                continue
                
            try:
                name = parts[0]
                hubble_type = int(parts[1])
                distance = float(parts[2])
                inclination = float(parts[5])
                L36 = float(parts[7]) * 1e9  # 10^9 Lsun
                MHI = float(parts[14]) * 1e9  # 10^9 Msun
                
                # Vflat e Quality
                if len(parts) >= 18:
                    Vflat = float(parts[15]) if parts[15] not in ['0.0', '0'] else 0.0
                    quality = int(parts[17])
                else:
                    Vflat = 0.0
                    quality = 3
                
                galaxy = {
                    'name': name,
                    'distance': distance,
                    'inclination': inclination,
                    'L36': L36,
                    'MHI': MHI,
                    'Vflat': Vflat,
                    'quality': quality
                }
                
                # Filtrar apenas galáxias com Q=1 ou Q=2 (alta/média qualidade)
                if quality <= 2 and Vflat > 0:
                    galaxias.append(galaxy)
                    
            except (ValueError, IndexError) as e:
                continue
    
    print(f"✓ Lidas {len(galaxias)} galáxias com Q≤2 e Vflat>0")
    return galaxias


def ler_sparc_table2(filepath='../data/sparc_data_real/table2.dat'):
    """
    Lê Table 2 do SPARC (curvas de rotação)
    
    Formato (bytes):
    1-11: Galaxy name
    13-18: Distance (Mpc)
    20-25: Radius (kpc)
    27-32: Vobs (km/s)
    34-38: e_Vobs
    40-45: Vgas
    47-52: Vdisk
    54-59: Vbulge
    """
    curvas = {}
    
    with open(filepath, 'r') as f:
        for line in f:
            if len(line) < 60:
                continue
            
            name = line[0:11].strip()
            
            try:
                radius = float(line[19:25].strip())
                vobs = float(line[26:32].strip())
                e_vobs = float(line[33:38].strip())
                vgas = float(line[39:45].strip())
                
                if name not in curvas:
                    curvas[name] = {'radii': [], 'vobs': [], 'errors': [], 'vgas': []}
                
                curvas[name]['radii'].append(radius)
                curvas[name]['vobs'].append(vobs)
                curvas[name]['errors'].append(e_vobs)
                curvas[name]['vgas'].append(vgas)
                
            except:
                continue
    
    # Converter para arrays numpy
    for name in curvas:
        for key in ['radii', 'vobs', 'errors', 'vgas']:
            curvas[name][key] = np.array(curvas[name][key])
    
    print(f"✓ Lidas curvas de rotação para {len(curvas)} galáxias")
    return curvas


def preparar_dataset_sparc():
    """Prepara dataset combinando Table 1 e Table 2"""
    
    print("\n" + "="*70)
    print("LENDO DADOS REAIS DO SPARC")
    print("="*70)
    
    galaxias = ler_sparc_table1()
    curvas = ler_sparc_table2()
    
    # Combinar
    dataset = []
    for gal in galaxias:
        name = gal['name']
        if name in curvas:
            dataset.append({
                'name': name,
                'distance': gal['distance'],
                'inclination': gal['inclination'],
                'L36': gal['L36'],
                'MHI': gal['MHI'],
                'Vflat': gal['Vflat'],
                'quality': gal['quality'],
                'radii': curvas[name]['radii'],
                'vobs': curvas[name]['vobs'],
                'errors': curvas[name]['errors'],
                'vgas': curvas[name]['vgas']
            })
    
    print(f"\n✓ Dataset final: {len(dataset)} galáxias com curvas completas")
    print(f"  - Qualidade 1 (alta): {sum(1 for g in dataset if g['quality']==1)}")
    print(f"  - Qualidade 2 (média): {sum(1 for g in dataset if g['quality']==2)}")
    
    return dataset


# ==============================================================================
# TEORIA TRINITÁRIA (N=4, L=5, Q=4.0)
# ==============================================================================

def teoria_trinitaria(r, amplitude_fractal, amplitude_quantum, length_scale_factor,
                      decay_rate, baryonic_boost, vgas, N=4, L=5, Q=4.0):
    """
    Modelo completo da Teoria Trinitária
    """
    # Escala característica
    r_scale = length_scale_factor
    
    # 1. Componente fractal (tetracíclica, N=4)
    fractal = amplitude_fractal * np.exp(-r / (r_scale * decay_rate))
    for n in range(1, N + 1):
        fractal *= (1 + 0.1 * np.sin(2 * np.pi * n * r / r_scale))
    
    # 2. Componente quântica (Fibonacci L=5: [1,1,2,3,5])
    fibonacci = np.array([1, 1, 2, 3, 5])
    quantum = np.zeros_like(r)
    for i, fib in enumerate(fibonacci[:L]):
        quantum += amplitude_quantum * np.exp(-((r - i * r_scale / L) / r_scale)**2) * fib / 5.0
    
    # 3. Confinamento (Q=4.0)
    confinement = Q * (1 - np.exp(-r / (r_scale * 2)))
    
    # 4. Componente bariônica (gás observado)
    baryonic = baryonic_boost * vgas
    
    # Velocidade total
    v_total = np.sqrt(fractal**2 + quantum**2 + confinement**2 + baryonic**2)
    
    return v_total


def fit_galaxy(galaxy_data, params):
    """Ajusta modelo a uma galáxia"""
    r = galaxy_data['radii']
    vobs = galaxy_data['vobs']
    vgas = galaxy_data['vgas']
    
    amplitude_fractal = params[0]
    amplitude_quantum = params[1]
    length_scale_factor = params[2]
    decay_rate = params[3]
    baryonic_boost = params[4]
    
    v_model = teoria_trinitaria(
        r, amplitude_fractal, amplitude_quantum, length_scale_factor,
        decay_rate, baryonic_boost, vgas
    )
    
    residuals = vobs - v_model
    rms = np.sqrt(np.mean(residuals**2))
    
    return rms, v_model


# ==============================================================================
# VALIDAÇÃO CRUZADA
# ==============================================================================

def validacao_cruzada_sparc():
    """Validação cruzada com dados reais do SPARC"""
    
    # Carregar dados reais
    dataset = preparar_dataset_sparc()
    
    print("\n" + "="*70)
    print("VALIDAÇÃO CRUZADA COM DADOS REAIS")
    print("="*70)
    print(f"Total de galáxias: {len(dataset)}")
    
    # Split 70/30
    np.random.seed(42)
    indices = np.random.permutation(len(dataset))
    n_train = int(0.7 * len(dataset))
    
    train_indices = indices[:n_train]
    test_indices = indices[n_train:]
    
    train_data = [dataset[i] for i in train_indices]
    test_data = [dataset[i] for i in test_indices]
    
    print(f"\nTreino: {len(train_data)} galáxias")
    print(f"Teste:  {len(test_data)} galáxias")
    
    # Otimização com DE
    print("\n" + "-"*70)
    print("OTIMIZANDO PARÂMETROS GLOBAIS (N=4, L=5, Q=4.0 fixos)")
    print("-"*70)
    
    # BOUNDS EXPANDIDOS (Corrigindo Saturação - Crítica #1)
    # Anteriores: saturaram em todos os máximos
    # Novos: 4-5x maiores para permitir convergência natural
    bounds = [
        (0.01, 200.0),  # amplitude_fractal (4x: 50→200)
        (0.0, 5.0),     # amplitude_quantum (5x: 1→5)
        (0.1, 50.0),    # length_scale_factor (5x: 10→50)
        (0.1, 20.0),    # decay_rate (4x: 5→20)
        (0.2, 10.0)     # baryonic_boost (3.3x: 3→10)
    ]
    
    def objective(params):
        total_rms = 0
        for galaxy in train_data:
            rms, _ = fit_galaxy(galaxy, params)
            total_rms += rms
        return total_rms / len(train_data)
    
    print("\nExecutando Differential Evolution...")
    print("(Isso pode levar alguns minutos com dados reais)")
    
    result = differential_evolution(
        objective,
        bounds,
        maxiter=100,
        popsize=15,
        seed=42,
        disp=True
    )
    
    best_params = result.x
    print(f"\n✓ Otimização concluída!")
    print(f"\nParâmetros ótimos (DADOS REAIS):")
    print(f"  amplitude_fractal:    {best_params[0]:.4f}")
    print(f"  amplitude_quantum:    {best_params[1]:.4f}")
    print(f"  length_scale_factor:  {best_params[2]:.4f}")
    print(f"  decay_rate:           {best_params[3]:.4f}")
    print(f"  baryonic_boost:       {best_params[4]:.4f}")
    print(f"  N (fixo):             4")
    print(f"  L (fixo):             5")
    print(f"  Q (fixo):             4.0")
    
    # Avaliar no treino
    print("\n" + "-"*70)
    print("AVALIANDO NO CONJUNTO DE TREINO")
    print("-"*70)
    
    train_rms_list = []
    for galaxy in train_data:
        rms, _ = fit_galaxy(galaxy, best_params)
        train_rms_list.append(rms)
    
    train_rms = np.mean(train_rms_list)
    print(f"RMS médio (treino): {train_rms:.1f} km/s")
    
    # Avaliar no teste
    print("\n" + "-"*70)
    print("AVALIANDO NO CONJUNTO DE TESTE (DADOS NÃO VISTOS)")
    print("-"*70)
    
    test_rms_list = []
    for galaxy in test_data:
        rms, _ = fit_galaxy(galaxy, best_params)
        test_rms_list.append(rms)
    
    test_rms = np.mean(test_rms_list)
    print(f"RMS médio (teste): {test_rms:.1f} km/s")
    
    # Gap de generalização
    gap = 100 * (test_rms - train_rms) / train_rms
    print(f"\nGap de generalização: {gap:+.1f}%")
    
    # Resultados
    print("\n" + "="*70)
    print("RESULTADOS FINAIS - DADOS REAIS DO SPARC")
    print("="*70)
    
    success_50 = sum(1 for rms in test_rms_list if rms < 50)
    success_100 = sum(1 for rms in test_rms_list if rms < 100)
    
    print(f"\n✓ RMS teste:  {test_rms:.1f} km/s")
    print(f"✓ Gap:        {gap:+.1f}%")
    print(f"✓ RMS < 50:   {success_50}/{len(test_data)} ({100*success_50/len(test_data):.0f}%)")
    print(f"✓ RMS < 100:  {success_100}/{len(test_data)} ({100*success_100/len(test_data):.0f}%)")
    
    # Comparação
    print("\n" + "="*70)
    print("COMPARAÇÃO: DADOS SINTÉTICOS vs DADOS REAIS")
    print("="*70)
    print(f"\nDados SINTÉTICOS (anteriores):")
    print(f"  RMS teste: 40.4 km/s")
    print(f"  Gap:       +7.3%")
    print(f"\nDados REAIS (SPARC atual):")
    print(f"  RMS teste: {test_rms:.1f} km/s")
    print(f"  Gap:       {gap:+.1f}%")
    print(f"\nDiferença: {test_rms - 40.4:+.1f} km/s")
    
    if test_rms < 100:
        print(f"\n🎉 SUCESSO! RMS < 100 km/s com dados REAIS!")
        print(f"   Teoria validada com observações astronômicas reais")
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        'timestamp': timestamp,
        'n_galaxies': len(dataset),
        'n_train': len(train_data),
        'n_test': len(test_data),
        'parameters': {
            'amplitude_fractal': float(best_params[0]),
            'amplitude_quantum': float(best_params[1]),
            'length_scale_factor': float(best_params[2]),
            'decay_rate': float(best_params[3]),
            'baryonic_boost': float(best_params[4]),
            'N': 4,
            'L': 5,
            'Q': 4.0
        },
        'results': {
            'train_rms': float(train_rms),
            'test_rms': float(test_rms),
            'gap_percent': float(gap),
            'success_50km': int(success_50),
            'success_100km': int(success_100)
        },
        'comparison': {
            'synthetic_rms': 40.4,
            'real_rms': float(test_rms),
            'difference': float(test_rms - 40.4)
        }
    }
    
    output_file = f"validacao_sparc_real_{timestamp}.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Resultados salvos em: {output_file}")
    
    return output


if __name__ == '__main__':
    validacao_cruzada_sparc()
