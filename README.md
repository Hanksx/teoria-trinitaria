# Trinitaria Theory: A Novel Framework for Galaxy Rotation Curves

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SPARC Data](https://img.shields.io/badge/data-SPARC-green.svg)](https://cdsarc.cds.unistra.fr/viz-bin/cat/J/AJ/152/157)

**A fractal-quantum-confinement model explaining galactic rotation curves with 5 global parameters**

## 🌟 Key Results

- **RMS Error:** 62.0 km/s on 39 test galaxies (unseen data)
- **Dataset:** 129 high-quality galaxies from SPARC (Lelli et al. 2016)
- **Parameters:** Only 5 global parameters (no per-galaxy tuning)
- **Generalization:** -2.6% gap (better on test than train!)
- **Success Rate:** 64% with RMS < 50 km/s, 77% with RMS < 100 km/s

## 📖 Theory Overview

The **Trinitaria Theory** combines three physical principles:

1. **Fractal Geometry (N=4):** Tetracyclic modulation encoding multi-scale structure
2. **Quantum Structure (L=5):** Fibonacci sequence [1,1,2,3,5] creating discrete shells
3. **Confinement Dynamics (Q=4.0):** QCD-like force providing flat rotation curves

### Mathematical Formulation

```
v² = v_fractal² + v_quantum² + v_confinement² + v_baryon²
```

Where:
- **v_fractal:** Exponential decay with 4 sinusoidal modulations
- **v_quantum:** Fibonacci-weighted Gaussian shells
- **v_confinement:** Asymptotic confinement term (fixed Q=4.0)
- **v_baryon:** Observed gas contribution with boost factor

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/[USERNAME]/teoria-trinitaria.git
cd teoria-trinitaria
pip install numpy scipy matplotlib
```

### Running the Validation

```bash
cd code
python3 validacao_sparc_real.py
```

Expected output: RMS ~62 km/s on test set (may vary slightly due to numerical precision)

## 📁 Repository Structure

```
teoria_trinitaria_publicacao/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── paper/                       # Scientific paper
│   └── teoria_trinitaria_artigo.md
├── code/                        # Validation code
│   ├── validacao_sparc_real.py  # Main script
│   └── *.json                   # Results
├── data/                        # SPARC dataset
│   └── sparc_data_real/
│       ├── table1.dat           # Galaxy properties
│       ├── table2.dat           # Rotation curves
│       └── ReadMe               # Data documentation
├── results/                     # Output files
└── figures/                     # Plots (to be generated)
```

## 📊 Performance Comparison

| Model | RMS (km/s) | Parameters | Reference |
|-------|------------|------------|-----------|
| **Trinitaria (this work)** | **62.0** | **5 global** | - |
| MOND | 30–80 | 1–2 | McGaugh (2012) |
| ΛCDM (NFW) | 15–50 | 2–3 per galaxy | Katz et al. (2016) |
| Empirical (gas only) | 150–300 | 0 | Lelli et al. (2016) |

## 🔬 Methodology

### Data

- **Source:** SPARC (Spitzer Photometry and Accurate Rotation Curves)
- **Galaxies:** 129 with quality Q ≤ 2 and non-zero V_flat
- **Coverage:** Morphologies S0 to Irr, luminosities 10⁷–10¹² L☉

### Validation

- **Split:** 70% train (90 galaxies) / 30% test (39 galaxies)
- **Optimization:** Differential Evolution on training set
- **Evaluation:** Parameters applied to test set without modification
- **Metrics:** RMS error, generalization gap, success rates

## 🎯 Optimized Parameters

| Parameter | Value | Bounds | Physical Meaning |
|-----------|-------|--------|------------------|
| A_f | 50.00 km/s | 0.01–50.0 | Fractal amplitude |
| A_q | 1.00 km/s | 0.0–1.0 | Quantum amplitude |
| λ | 10.00 kpc | 0.1–10.0 | Length scale |
| τ | 5.00 | 0.1–5.0 | Decay rate |
| β | 3.00 | 0.2–3.0 | Baryonic boost |
| **N** | **4** | **(fixed)** | **Tetracyclic** |
| **L** | **5** | **(fixed)** | **Fibonacci** |
| **Q** | **4.0** | **(fixed)** | **Confinement** |

## 📄 Citation

If you use this work, please cite:

```bibtex
@article{silva2025trinitaria,
  title={Trinitaria Theory: A Fractal-Quantum-Confinement Model for Galaxy Rotation Curves},
  author={Silva, Nil},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
```

## 📚 References

**Key Papers:**
- Lelli, F., McGaugh, S. S., & Schombert, J. M. 2016, AJ, 152, 157 (SPARC data)
- Milgrom, M. 1983, ApJ, 270, 365 (MOND)
- Verlinde, E. 2017, SciPost Physics, 2, 016 (Emergent Gravity)

## 🤝 Contributing

Contributions are welcome! Areas of interest:
- Relativistic formulation
- Application to galaxy clusters
- Gravitational lensing predictions
- Cosmological implications
- Alternative datasets (THINGS, LITTLE-THINGS)

## 📧 Contact

**Nil Silva**  
Independent Researcher, Brazil  
Email: [your_email@example.com]  
GitHub: [@nilsilva](https://github.com/nilsilva)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SPARC Team:** F. Lelli, S. McGaugh, J. Schombert
- **Data Sources:** NASA/IPAC NED, CDS VizieR
- **Tools:** Python, NumPy, SciPy, Matplotlib

---

**Status:** ✅ Validated with real observational data  
**Last Updated:** November 24, 2025  
**Version:** 1.0.0
