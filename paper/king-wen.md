# Statistical Properties of the King Wen Sequence: An Anti-Habituation Structure That Does Not Improve Neural Network Training

## Abstract

The King Wen sequence of the I-Ching (c. 1000 BC) orders 64 hexagrams---states of a six-dimensional binary space---in a pattern that has puzzled scholars for three millennia. We present a rigorous statistical characterization of this ordering using Monte Carlo permutation analysis against 100,000 random baselines. We find that the sequence has four statistically significant properties: higher-than-random transition distance (98.2nd percentile), negative lag-1 autocorrelation (p=0.037), yang-balanced groups of four (p=0.002), and asymmetric within-pair vs. between-pair distances (99.2nd percentile). These properties superficially resemble principles from curriculum learning and curiosity-driven exploration, motivating the hypothesis that they might benefit neural network training. We test this hypothesis through three experiments: learning rate schedule modulation, curriculum ordering, and seed sensitivity analysis, conducted across two hardware platforms (NVIDIA RTX 2060 with PyTorch and Apple Silicon with MLX). The results are uniformly negative. King Wen LR modulation degrades performance at all tested amplitudes. As curriculum ordering, King Wen is the worst non-sequential ordering on one platform and within noise on the other. A 30-seed sweep confirms that only King Wen's degradation exceeds natural seed variance. We explain why: the sequence's high variance---the very property that makes it statistically distinctive---destabilizes gradient-based optimization. Anti-habituation in a fixed combinatorial sequence is not the same as effective training dynamics.

**Keywords:** King Wen sequence, I-Ching, curriculum learning, information-theoretic surprise, negative results, learning rate scheduling, reproducibility

## 1. Introduction

The King Wen sequence, traditionally dated to approximately 1000 BC, orders the 64 hexagrams of the I-Ching in a pattern that has long defied mathematical explanation. Unlike the Shao Yong ordering (c. 1050 AD), which follows a straightforward binary enumeration, the King Wen sequence exhibits no obvious numerical or algebraic rule. The mathematical significance of its structure was first recognized by Leibniz (1703), who discovered parallels between the binary number system and the I-Ching's hexagrams.

In recent years, the I-Ching has found applications in computational intelligence, from evolutionary algorithms (Chen et al., 2016) to neural architecture search (Zhang et al., 2021). More broadly, structured knowledge systems outside conventional machine learning have shown measurable impacts on AI system performance (Choi et al., 2023).

We begin by establishing that the King Wen sequence has genuine statistical structure. Using Monte Carlo permutation analysis against 100,000 random baselines, we confirm four properties that distinguish it from chance orderings: high transition distance, negative autocorrelation, local yang balance, and pair-level asymmetry. These properties superficially resemble principles from curriculum learning (Bengio et al., 2009; Graves et al., 2017) and curiosity-driven exploration (Schmidhuber, 2006). A natural hypothesis follows: does the sequence's anti-habituation profile translate to measurable advantages in neural network training?

We test this hypothesis rigorously and find that it does not hold. Across three experiments---learning rate schedule modulation, curriculum ordering, and seed sensitivity analysis---the King Wen sequence either degrades training performance or produces results indistinguishable from noise. We explain the mechanism: the sequence's high variance, which generates its distinctive statistical signature, is counterproductive for gradient-based optimization.

We make four contributions:

1. An enhanced statistical characterization of the King Wen sequence via 100,000-permutation Monte Carlo analysis, confirming four statistically significant combinatorial properties.
2. Learning rate schedule modulation experiments showing that the sequence's variance profile degrades training across all tested amplitudes.
3. Curriculum ordering experiments on two hardware platforms, isolating a torch.compile confound from genuine learning dynamics.
4. A mechanistic explanation of why anti-habituation statistical properties do not entail training benefit, grounded in the gap between combinatorial structure and optimization dynamics.

## 2. Related Work

### 2.1 Curriculum Learning

Bengio et al. (2009) formalized the intuition that training machine learning models in a meaningful order---from simple to complex examples---improves convergence and generalization. Graves et al. (2017) extended this to automated curriculum learning, using multi-armed bandit algorithms to select training tasks. Wang et al. (2022) survey the field, distinguishing difficulty measurers from training schedulers. Recent work has shown that curriculum ordering interacts strongly with learning rate schedules (Agarwal et al., 2025) and that simple difficulty metrics (compression ratio, lexical diversity) are effective at scale (Jia et al., 2025).

### 2.2 I-Ching in Computational Intelligence

Chen et al. (2016) proposed the I-Ching Divination Evolutionary Algorithm (IDEA), using hexagram transformation operations as evolutionary operators. Zhang et al. (2021) extended this to neural architecture search with AS-NAS. These works use the I-Ching's transformation mechanics as algorithmic primitives. Our investigation is different: we test whether the King Wen sequence ordering itself---not the hexagram transformation rules---has optimization utility.

### 2.3 Information-Theoretic Surprise and Optimal Learning

Schmidhuber (2006) proposed that artificial curiosity should drive agents toward states of intermediate surprise. Itti and Baldi (2009) formalized Bayesian surprise as KL divergence between prior and posterior beliefs. Nielsen (2020) provides the information-geometric framework connecting these ideas. We test whether the King Wen sequence's surprise profile---which exhibits properties consistent with these frameworks---produces practical benefits when applied to neural network training.

### 2.4 Value of Negative Results

Negative results are essential for scientific progress yet remain underreported in machine learning. When a hypothesis has surface plausibility---as the King Wen sequence does, given its genuine statistical properties---rigorous negative results prevent others from pursuing similar dead ends and clarify the boundary between theoretical elegance and practical utility. Our contribution follows this tradition: we test a natural hypothesis with proper controls and report that it fails, with mechanistic explanation.

## 3. The King Wen Sequence: Statistical Characterization

### 3.1 Hexagram Space and Notation

Each hexagram is a six-bit binary vector representing six lines (yin=0 or yang=1), arranged from bottom to top. The 64 hexagrams span the complete space {0,1}^6. The King Wen sequence assigns each hexagram a position from 1 to 64 in a traditional ordering. We also consider the Shao Yong ordering (c. 1050 AD), which arranges hexagrams by binary value using a reversed-trigram convention, and the natural binary ordering (hexagrams 0--63 by integer value).

### 3.2 Transition Metrics

For consecutive hexagrams H_i and H_{i+1} in a sequence, we measure:

- **Hamming distance** d_H(H_i, H_{i+1}): the number of differing bit positions (range 0--6)
- **Trigram relationship distance**: distance between upper and lower trigram pairs
- **Nuclear hexagram distance**: Hamming distance between the inner four lines (positions 2--5)

We define information-theoretic surprise as:

S(H_i, H_{i+1}) = -log P(H_{i+1} | H_i)

where conditional probability is modeled via pattern similarity incorporating traditional line position weights [0.03, 0.07, 0.15, 0.20, 0.25, 0.30] from bottom to top, with yang-to-yin transitions weighted at 0.7x the reverse. Total similarity combines external (line-level) and internal (nuclear hexagram) components with lambda=0.4 weighting the nuclear component.

### 3.3 Monte Carlo Permutation Analysis

We compare the King Wen sequence against 100,000 random permutations of the same 64 hexagrams. Four properties are statistically significant:

**1. Higher-than-random transition distance (98.2nd percentile).** Mean Hamming distance between consecutive hexagrams: 3.35 (random mean: 3.05, sigma=0.15). The sequence deliberately maximizes change between consecutive states.

**2. Negative lag-1 autocorrelation (3.7th percentile, p=0.037).** Autocorrelation of Hamming distances at lag 1: -0.251 (random mean: -0.032, sigma=0.124). A large transition is systematically followed by a small one and vice versa. This alternation between dramatic and subtle change is actively constructed, not a property of random permutations.

**3. Yang-balanced groups of four (99.8th percentile, p=0.002).** Seven out of 16 groups of four consecutive hexagrams have exactly 12 yang lines (perfect yin-yang balance). Random expectation: 2.6 (sigma=1.5). The sequence maintains energetic equilibrium at the 4-hexagram scale.

**4. Within-pair vs. between-pair asymmetry (99.2nd percentile).** Within-pair mean Hamming distance: 3.56. Between-pair: 2.94. Asymmetry: 0.63. Paired hexagrams are maximally different from each other (complement/inverse), while transitions between pairs are smoother---creating tension within pairs and resolution between them.

### 3.4 Comparison with Systematic Orderings

We compare the surprise distributions of four orderings across all 63 consecutive transitions:

| Ordering | Mean Surprise | Std | Variance | Range |
|---|---|---|---|---|
| King Wen | 0.842 | 0.624 | 0.390 | 0.16--2.30 |
| Random (mean of 1000) | 0.711 | 0.453 | 0.202 | 0.11--2.30 |
| Binary | 0.482 | 0.403 | 0.162 | 0.20--1.75 |
| Shao Yong | 0.270 | 0.348 | 0.121 | 0.11--2.07 |

**Distribution shape (Kolmogorov-Smirnov test):** King Wen is not significantly different from random (D=0.11, p=0.44), but is highly significantly different from binary (D=0.46, p<0.001) and Shao Yong (D=0.73, p<0.001).

**Variance (Levene's test):** King Wen has significantly higher variance than random (p=0.009) and Shao Yong (p<0.001). The difference versus binary is marginal (p=0.053).

**Autocorrelation (Ljung-Box, lag 5):** King Wen shows no significant autocorrelation (p=0.45), while binary (p<0.001) and Shao Yong (p=0.002) are highly autocorrelated. Only 3.9% of random permutations show significant autocorrelation.

### 3.5 Summary

The King Wen sequence is neither random nor algebraically systematic. It occupies a distinctive position: random-like mean surprise, significantly higher variance, negative lag-1 autocorrelation, and local yang balance. These properties are real and confirmed against rigorous baselines. Whether they are useful for optimization is a separate, empirical question---addressed in the next section.

## 4. Experimental Evaluation

We test the hypothesis that the King Wen sequence's anti-habituation properties improve neural network training. We conduct three experiments using Karpathy's autoresearch framework, which runs fixed-duration (5-minute) training experiments on a small GPT language model and evaluates using validation bits per byte (val_bpb; lower is better).

### 4.1 Experimental Setup

**Model.** GPT with rotary position embeddings (RoPE), sliding window attention, and a hybrid optimizer (Muon for matrix parameters, AdamW for embeddings and scalars). Default configuration: DEPTH=4 (~11.5M parameters), MAX_SEQ_LEN=2048, vocabulary size 8192.

**Dataset.** ClimbMix-400B, prepared with best-fit packing and BPE tokenization.

**Platforms.** (1) NVIDIA RTX 2060 (6 GB VRAM) with PyTorch and torch.compile. (2) MacBook Pro with 96 GB unified memory, Apple Silicon, MLX framework.

**Metric.** Validation bits per byte (val_bpb), vocabulary-size-independent and architecture-independent (lower is better). All experiments use the same evaluation shard and token count.

**Time budget.** Fixed 300-second training budget per run. Curriculum overhead (difficulty scoring, buffer sorting, refill) counts against this budget.

### 4.2 Experiment 1: Learning Rate Schedule Modulation

We apply the King Wen sequence's surprise profile as a multiplicative modulation on the learning rate schedule. The 63 inter-hexagram surprise values (Section 3.2) are cycled across training steps, scaling the base learning rate by (1 + amplitude * surprise_value). We test three amplitudes (0.15, 0.3, 0.5) against two controls: random perturbation (pseudo-random values at the same amplitude) and Shao Yong ordering (highly autocorrelated sawtooth pattern).

All runs use identical configuration: 4-layer GPT, standard warmup/warmdown LR envelope, RTX 2060, seed 42.

| Schedule | val_bpb | vs. Baseline |
|---|---|---|
| Baseline (no modulation) | 1.753 | --- |
| Random perturbation (amp=0.3) | 1.731 | -0.023 |
| Shao Yong (amp=0.3) | 1.732 | -0.021 |
| King Wen (amp=0.15) | 1.777 | +0.024 |
| King Wen (amp=0.3) | 1.785 | +0.032 |
| King Wen (amp=0.5) | 1.790 | +0.036 |

**Finding.** King Wen LR modulation degrades performance at all amplitudes tested. The degradation increases monotonically with amplitude. Both control perturbations (random and Shao Yong) show marginal improvements at the same amplitude, though as Section 4.4 shows, these fall within natural seed variance.

### 4.3 Experiment 2: Curriculum Ordering

We reframe King Wen as a data ordering strategy rather than an LR modulator. Training batches are buffered (64 micro-batches), scored by a difficulty metric, and reordered according to various orderings. For the King Wen ordering, batches are mapped by rank: the batch at difficulty rank k is placed at the King Wen position with surprise rank k.

Two difficulty metrics were used across platforms: token diversity (ratio of unique tokens to total tokens per batch) for initial CUDA experiments, and compression ratio (gzip compressed size / original size) for MLX and CUDA replication experiments. Both produce consistent ordinal rankings of batch difficulty.

#### CUDA Results (RTX 2060, DEPTH=4, token diversity metric)

| Ordering | val_bpb | vs. Sequential |
|---|---|---|
| Sequential (no buffer) | 1.719 | --- |
| Buffered passthrough | 1.680 | -0.039 |
| **Random shuffle** | **1.614** | **-0.106** |
| Easy-to-hard | 1.632 | -0.087 |
| Hard-to-easy | 1.627 | -0.092 |
| Shao Yong | 1.638 | -0.081 |
| King Wen | 1.662 | -0.057 |

All reorderings beat sequential, but random shuffle wins. King Wen is the worst non-sequential ordering. The buffered passthrough control (buffering without reordering) itself improves performance by 0.039 bpb, suggesting that the dataloader's best-fit packing creates sequential correlation that any disruption helps break.

#### MLX Results (Apple Silicon, DEPTH=4, compression ratio metric)

We repeat the experiment on MLX with five orderings (Shao Yong is dropped as it performed identically to random perturbation in the LR experiments and is structurally similar to easy-to-hard). Two LR regimes are tested: standard warmdown and constant LR, following the finding that LR decay can suppress curriculum benefits (Agarwal et al., 2025).

| Ordering | Standard Warmdown | Constant LR |
|---|---|---|
| Sequential | 1.732 | 1.722 |
| Random | 1.713 | 1.697 |
| Easy-to-hard | 1.695 | 1.731 |
| Hard-to-easy | 1.709 | 1.707 |
| King Wen | 1.724 | 1.729 |

Noise floor (3-seed range at DEPTH=4): +/-0.060 bpb. **No ordering achieves a statistically significant improvement over sequential on MLX.** All differences fall within the measured noise floor.

#### MLX Results (Apple Silicon, DEPTH=6)

| Ordering | Standard Warmdown | Constant LR |
|---|---|---|
| Sequential | 2.056 | 2.039 |
| Random | 2.047 | 2.056 |
| Easy-to-hard | 2.099 | 2.079 |
| Hard-to-easy | 2.084 | 2.095 |
| King Wen | 2.074 | 2.030 |

Noise floor at DEPTH=6: +/-0.043. King Wen achieves 2.030 under constant LR (a delta of -0.044, marginally outside noise), but this is a single run and does not replicate the CUDA pattern.

#### Cross-Platform Analysis

The large curriculum effect observed on CUDA (~0.04--0.11 bpb) does not replicate on MLX. The most likely explanation is that torch.compile creates kernel-level optimization patterns that overfit to sequential data ordering. Buffering disrupts this optimization, and random shuffling maximizes the disruption. This is a framework-specific artifact, not a property of the learning dynamics. The decorrelation benefit (breaking best-fit packing correlation) is real (~0.038 bpb from buffered passthrough) but is not King Wen-specific.

### 4.4 Experiment 3: Seed Sensitivity Analysis

To establish whether any of the above results exceed natural variance, we train 30 models with different random seeds (0--29) on the identical baseline configuration (4-layer GPT, standard LR schedule, RTX 2060, 5-minute budget).

| Statistic | Value |
|---|---|
| Range | 1.732--1.773 |
| Mean | 1.756 |
| Std | 0.009 |
| CV | 0.51% |

The seed sweep reveals that the "improvements" from random perturbation (-0.023) and Shao Yong (-0.021) in Experiment 1 fall within the natural seed variance range of 0.041 bpb. Only King Wen's degradation (+0.032) is statistically meaningful---it exceeds the upper bound of observed seed variation.

Behavioral analysis of generated text across all 30 seeds (150 samples per seed, 4,500 total) shows that between-seed variance ratios are below 0.21 on all 12 metrics measured. PCA reveals a single "verbosity axis" (PC1 = 66.4% of between-seed variance), not multi-dimensional behavioral traits. Seeds produce quantitatively similar models at this scale.

### 4.5 Discussion: Why Anti-Habituation Does Not Help

The King Wen sequence's statistically significant properties---high transition distance, negative autocorrelation, full-spectrum variance---are precisely what make it harmful for gradient-based optimization:

**Excessive variance destabilizes gradient updates.** The sequence's defining statistical feature is higher variance than random permutations (Section 3.4). When applied as LR modulation, this means larger effective perturbation magnitude than random noise at the same nominal amplitude. The optimizer is whiplashed by surprise spikes exceeding 2.0 interspersed with drops below 0.2.

**Negative autocorrelation prevents optimization momentum.** Shao Yong's highly autocorrelated pattern allows the optimizer to make consistent progress at a stable effective learning rate for several steps. Random noise has some statistical clustering. King Wen is constructed to never repeat---each step reverses the previous step's intensity. This actively disrupts the temporal coherence that optimizers rely on.

**Anti-habituation is premature at small scale.** A 4-layer model trained for 5 minutes is in rapid early learning, far from the convergence plateau where habituation-breaking interventions might help. Disrupting a learner that hasn't plateaued simply slows it down.

**Fixed sequences cannot adapt.** Effective curriculum learning requires adaptation to learner state (Graves et al., 2017). The King Wen sequence is a 3,000-year-old fixed ordering that cannot respond to the model's current loss landscape. Simple adaptive approaches---even random shuffling---outperform any fixed ordering because they do not impose incorrect assumptions about the learning trajectory.

**Framework artifacts confound curriculum evaluation.** The large CUDA curriculum effect (~0.11 bpb for random shuffle) disappears on MLX, revealing that torch.compile's kernel optimization interacts with data ordering in ways that masquerade as learning dynamics. This is an important methodological finding: curriculum ordering experiments must be validated across frameworks, not just seeds.

## 5. Implications

**For I-Ching studies.** The King Wen sequence has genuine combinatorial structure confirmed by Monte Carlo analysis. The four statistically significant properties---especially the yang-balanced groups (p=0.002) and negative autocorrelation (p=0.037)---are mathematical findings about a historically important object, independent of any ML application.

**For curriculum learning.** Fixed ordering curricula, even those with theoretically appealing statistical properties, do not substitute for adaptive curricula at the scales tested. The gap between combinatorial elegance and optimization utility is wide. Anti-habituation and anti-correlation in a fixed sequence are not equivalent to effective training dynamics.

**For experimental methodology.** The torch.compile confound demonstrates that curriculum ordering experiments must be validated across frameworks. The 30-seed sweep (Section 4.4) provides a reusable template for distinguishing genuine effects from seed noise.

**For reproducibility.** All experiments use a fixed 5-minute time budget with val_bpb as the single metric, making results directly comparable. The autoresearch framework's edit-train-evaluate loop provides a lightweight, reproducible experimental pipeline for testing training hypotheses.

## 6. Limitations

Our experiments are conducted at small scale: ~11.5M parameter models trained for 5 minutes on a single GPU. Curriculum learning effects in the literature are typically demonstrated at 1B+ parameter scale with longer training. It is possible that King Wen's anti-habituation properties could help at larger scale, where models are more likely to reach convergence plateaus where habituation-breaking is relevant. However, the LR modulation results (Section 4.2) show degradation that increases with amplitude, not a marginal effect that might reverse at scale. The mechanistic explanation---excessive variance and negative autocorrelation disrupting gradient coherence---applies at any scale.

The torch.compile confound (Section 4.3) means our CUDA curriculum results reflect framework behavior, not pure learning dynamics. We address this by reporting both platforms, but the MLX null result means we lack a platform where curriculum ordering shows large, genuine effects against which to test King Wen.

## 7. Conclusion

The King Wen sequence has statistically significant combinatorial properties. Monte Carlo analysis against 100,000 random permutations confirms four distinctive features: high transition distance, negative lag-1 autocorrelation, local yang balance, and pair-level asymmetry. These are not artifacts---they reflect genuine structure in a 3,000-year-old ordering of 64 binary states.

These properties do not translate to neural network training benefit. Learning rate modulation with the King Wen surprise profile degrades performance at all tested amplitudes. Curriculum ordering using the sequence is the worst non-sequential ordering on one platform and indistinguishable from noise on another. A 30-seed sweep confirms that only King Wen's degradation exceeds natural variance.

The central lesson is the gap between "statistically interesting" and "useful for optimization." The King Wen sequence's high variance and negative autocorrelation---the properties that make it combinatorially distinctive---are counterproductive for gradient-based learning, which benefits from temporal coherence and moderate perturbation. Anti-habituation in a fixed sequence is not the same as adaptive curriculum design. We publish these negative results to close off a speculative research direction with data and to provide a methodological template for testing similar hypotheses.

## References

[1] Agarwal, A. et al. (2025). "How LR Decay Wastes Your Best Data in Curriculum-Based Pretraining." arXiv:2511.18903.

[2] Bengio, Y., Louradour, J., Collobert, R., & Weston, J. (2009). "Curriculum Learning." ICML.

[3] Chen, C. L. P., Zhang, T., Chen, L., & Tam, S. C. (2016). "I-Ching Divination Evolutionary Algorithm and its Convergence Analysis." IEEE Transactions on Cybernetics, 47(1), 1-12.

[4] Choi, S., Gazeley, W., Wong, S. H., & Li, T. (2023). "Conversational Factor Information Retrieval Model (ConFIRM)." arXiv:2310.13001.

[5] Graves, A., Bellemare, M. G., Menick, J., Munos, R., & Kavukcuoglu, K. (2017). "Automated Curriculum Learning for Neural Networks." ICML.

[6] Itti, L. & Baldi, P. (2009). "Bayesian Surprise Attracts Human Attention." Vision Research, 49(10), 1295-1306.

[7] Jia, Z. et al. (2025). "Beyond Random Sampling: Curriculum Learning for LM Pretraining." arXiv:2506.11300.

[8] Leibniz, G. W. (1703). "Explication de l'Arithmetique Binaire." Memoires de l'Academie Royale des Sciences.

[9] Nielsen, F. (2020). "An Elementary Introduction to Information Geometry." Entropy, 22(10), 1100.

[10] Schmidhuber, J. (2006). "Developmental robotics, optimal artificial curiosity, creativity, music, and the fine arts." Connection Science, 18(2), 173-187.

[11] Wang, X., Chen, Y., & Zhu, W. (2022). "A Survey on Curriculum Learning." IEEE TPAMI, 44(9), 4555-4576.

[12] Zhang, T., Lei, C., Zhang, Z., Meng, X., & Chen, C. L. P. (2021). "AS-NAS: Adaptive Scalable Neural Architecture Search." IEEE Transactions on Evolutionary Computation, 25(5), 840-854.

## Appendix A: Full Experimental Results

### A.1 LR Schedule Modulation (RTX 2060, DEPTH=4, seed 42)

| Run | Schedule | Amplitude | val_bpb | Memory (GB) |
|---|---|---|---|---|
| 1 | Baseline | --- | 1.753 | 4.3 |
| 2 | Random perturbation | 0.3 | 1.731 | 4.3 |
| 3 | Shao Yong | 0.3 | 1.732 | 4.3 |
| 4 | King Wen | 0.3 | 1.785 | 4.3 |
| 5 | King Wen | 0.15 | 1.777 | 4.3 |
| 6 | King Wen | 0.5 | 1.790 | 4.3 |

### A.2 Seed Sweep Summary (RTX 2060, DEPTH=4, 30 seeds)

Mean val_bpb across 30 seeds: 1.756 (range 1.732--1.773, std 0.009, CV 0.51%).

### A.3 Curriculum Ordering: CUDA with Compression Ratio (RTX 2060, DEPTH=4)

| Ordering | val_bpb | vs. Sequential |
|---|---|---|
| Sequential | 1.778 | --- |
| Random | 1.627 | -0.151 |
| Easy-to-hard | 1.634 | -0.144 |
| Hard-to-easy | 1.634 | -0.144 |
| King Wen | 1.638 | -0.140 |

### A.4 Curriculum Ordering: MLX DEPTH=4, Standard Warmdown

| Ordering | val_bpb |
|---|---|
| Sequential | 1.732 |
| Random | 1.713 |
| Easy-to-hard | 1.695 |
| Hard-to-easy | 1.709 |
| King Wen | 1.724 |

### A.5 Curriculum Ordering: MLX DEPTH=4, Constant LR

| Ordering | val_bpb |
|---|---|
| Sequential | 1.722 |
| Random | 1.697 |
| Easy-to-hard | 1.731 |
| Hard-to-easy | 1.707 |
| King Wen | 1.729 |

### A.6 Curriculum Ordering: MLX DEPTH=6, Standard Warmdown

| Ordering | val_bpb |
|---|---|
| Sequential | 2.056 |
| Random | 2.047 |
| Easy-to-hard | 2.099 |
| Hard-to-easy | 2.084 |
| King Wen | 2.074 |

### A.7 Curriculum Ordering: MLX DEPTH=6, Constant LR

| Ordering | val_bpb |
|---|---|
| Sequential | 2.039 |
| Random | 2.056 |
| Easy-to-hard | 2.079 |
| Hard-to-easy | 2.095 |
| King Wen | 2.030 |

### A.8 Hardware Specifications

| Platform | GPU | VRAM | Framework | Precision |
|---|---|---|---|---|
| CUDA | NVIDIA RTX 2060 | 6 GB | PyTorch + torch.compile | fp32 |
| MLX | Apple M-series | 96 GB unified | MLX | fp32 |

## Appendix B: Code and Data Availability

Experimental code, ADR documents, and raw results are available at:

- King Wen AGI Framework: https://github.com/augchan42/king-wen-agi-framework
- Autoresearch experiments: documented in ADR-001 through ADR-008

The autoresearch framework by Andrej Karpathy provides the experimental infrastructure. All experiments use a fixed 5-minute training budget with val_bpb as the single evaluation metric.
