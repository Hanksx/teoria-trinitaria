# Figures for Trinitaria Theory Publication

This directory contains 6 key figures demonstrating the performance and validation of the Trinitaria Theory.

## Figure List

### Figure 1: Train vs Test Performance Comparison
**File:** `fig1_train_test_comparison.png`  
**Description:** Comparison of training and test set performance showing minimal generalization gap (-2.6%). Demonstrates that the model does not overfit and generalizes robustly to unseen data.

**Key metrics shown:**
- Training RMS: 63.7 km/s (90 galaxies)
- Test RMS: 62.0 km/s (39 galaxies)
- Gap: -2.6% (negative = better on test!)

---

### Figure 2: RMS Error Distribution
**File:** `fig2_rms_histogram.png`  
**Description:** Histogram showing the distribution of RMS errors across all 129 SPARC galaxies.

**Success rates:**
- RMS < 50 km/s: 64% (25/39 test galaxies)
- RMS < 100 km/s: 77% (30/39 test galaxies)

---

### Figure 3: Model Comparison (Trinitaria vs MOND vs ΛCDM)
**File:** `fig3_model_comparison.png`  
**Description:** Systematic comparison of Trinitaria Theory performance against established theories (MOND and ΛCDM) across different galaxy types.

**Comparison:**
- Trinitaria: RMS = 62.0 km/s (5 global parameters)
- MOND: RMS = 30-80 km/s (1-2 parameters)
- ΛCDM: RMS = 15-50 km/s (2-3 parameters per galaxy)

---

### Figure 4: Rotation Curve - NGC 3198
**File:** `fig4_rotation_curve_ngc3198.png`  
**Description:** Example rotation curve fit for NGC 3198, a classic disk galaxy. Shows observed data points, model fit, and individual velocity components.

**Galaxy properties:**
- Type: Sc spiral
- Distance: ~13.8 Mpc
- Classic flat rotation curve

**Components shown:**
- Total velocity (model)
- Baryonic contribution
- Trinitaria components (fractal + quantum + confinement)

---

### Figure 5: Rotation Curve - NGC 2403
**File:** `fig5_rotation_curve_ngc2403.png`  
**Description:** Example rotation curve fit for NGC 2403, demonstrating excellent agreement across all radii with individual component decomposition.

**Galaxy properties:**
- Type: Sc spiral
- Distance: ~3.2 Mpc
- Well-studied nearby galaxy

**Components shown:**
- Observed velocity
- Model total velocity
- Fractal component (N=4)
- Quantum component (L=5, Fibonacci)
- Confinement component (Q=4.0)

---

### Figure 6: Systematic Theory Comparison
**File:** `fig6_theory_comparison.png`  
**Description:** Comprehensive comparison of Trinitaria Theory with established dark matter models across the full SPARC sample, showing performance across different mass ranges.

**Analysis includes:**
- Light galaxies (M < 2×10¹⁰ M☉)
- Medium galaxies (2×10¹⁰ < M < 8×10¹⁰ M☉)
- Heavy galaxies (M > 8×10¹⁰ M☉)

---

## Usage in Articles

These figures are referenced in both the English (`teoria_trinitaria_artigo.md`) and Portuguese (`teoria_trinitaria_artigo_PT.md`) versions of the paper.

### Reference format in articles:
```markdown
![Figure 1: Train vs Test Performance](../figures/fig1_train_test_comparison.png)
*Figure 1: Training vs test set performance showing minimal generalization gap.*
```

---

## Source

All figures were generated from tests and validations in:
`/Users/nilsilva/Desktop/espiral_fractal/`

Selected based on:
1. Scientific relevance
2. Visual clarity
3. Demonstration of key results
4. Comparison with established theories

---

## File Sizes

| Figure | Size | Type |
|--------|------|------|
| fig1 | 174 KB | PNG |
| fig2 | 1.1 MB | PNG |
| fig3 | 426 KB | PNG |
| fig4 | 84 KB | PNG |
| fig5 | 81 KB | PNG |
| fig6 | 278 KB | PNG |

**Total:** ~2.1 MB

---

## Notes for Publication

- All figures are publication-ready (300 DPI or vector)
- Color schemes are colorblind-friendly where possible
- Axis labels and legends are clear and readable
- Figures follow standard astrophysics journal formatting

---

**Date:** 2025-11-24  
**Author:** Nil Silva  
**Repository:** https://github.com/Hanksx/teoria-trinitaria
