"""
Generate comparison plots and statistical analysis for the King Wen sequence paper.

Compares the King Wen ordering against three baselines:
1. Random orderings (1,000 permutations) — null hypothesis
2. Natural binary ordering (0-63)
3. Shao Yong ordering (binary tree structure, c. 1050 AD)

Outputs:
- king_wen_metrics.pdf: King Wen sequence transition metrics
- king_wen_comparison.pdf: 4-panel comparison across all orderings
- statistical_results.txt: KS, Levene's, and Ljung-Box test results
"""

import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import ks_2samp, levene
from statsmodels.stats.diagnostic import acorr_ljungbox

# ============================================================
# Core metric functions
# ============================================================

def calculate_nuclear_distance(bin1, bin2):
    """Calculate Hamming distance between nuclear hexagrams (inner four lines)."""
    nuc1 = bin1[1:5]
    nuc2 = bin2[1:5]
    return sum(n1 != n2 for n1, n2 in zip(nuc1, nuc2))


def calculate_transition_metrics(bin1, bin2):
    """Calculate Hamming, trigram, and nuclear distances between two hexagrams."""
    d1 = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    upper1, lower1 = bin1[:3], bin1[3:]
    upper2, lower2 = bin2[:3], bin2[3:]
    d2 = sum(b1 != b2 for b1, b2 in zip(upper1, upper2)) + \
         sum(b1 != b2 for b1, b2 in zip(lower1, lower2))
    d3 = calculate_nuclear_distance(bin1, bin2)
    return d1, d2, d3


def calculate_pattern_similarity(bin1, bin2):
    """Calculate similarity incorporating I-Ching line position weights."""
    weights = [0.03, 0.07, 0.15, 0.20, 0.25, 0.30]
    line_diffs = []
    for i, (b1, b2) in enumerate(zip(bin1, bin2)):
        if b1 != b2:
            if b1 == '1' and b2 == '0':  # yang to yin
                line_diffs.append(0.7 * weights[i])
            else:
                line_diffs.append(weights[i])
    nuclear_weight = 0.4
    nuclear_diff = calculate_nuclear_distance(bin1, bin2)
    nuclear_similarity = 1 - (nuclear_diff / 4)
    raw_similarity = 1 - sum(line_diffs)
    total_similarity = (1 - nuclear_weight) * raw_similarity + nuclear_weight * nuclear_similarity
    return max(0.1, min(0.9, total_similarity))


def calculate_surprise(bin1, bin2):
    """Calculate information-theoretic surprise: -log(similarity)."""
    similarity = calculate_pattern_similarity(bin1, bin2)
    return -math.log(similarity)


def compute_sequence_metrics(sequence):
    """Compute all metrics for a given ordering of hexagram binary strings."""
    hamming = []
    similarities = []
    surprises = []
    for i in range(len(sequence) - 1):
        bin1 = sequence[i]
        bin2 = sequence[i + 1]
        d1, _, _ = calculate_transition_metrics(bin1, bin2)
        hamming.append(d1)
        similarities.append(calculate_pattern_similarity(bin1, bin2))
        surprises.append(calculate_surprise(bin1, bin2))
    return np.array(hamming), np.array(similarities), np.array(surprises)


# ============================================================
# Hexagram orderings
# ============================================================

# All 64 hexagrams as 6-bit binary strings
ALL_HEXAGRAMS = [format(i, '06b') for i in range(64)]

# King Wen sequence (traditional ordering, binary representations)
king_wen_sequence = [
    "111111", "000000", "100010", "010001", "111010", "010111",
    "010000", "000010", "111011", "110111", "111000", "000111",
    "101111", "111101", "001000", "000100", "100110", "011001",
    "110000", "000011", "100101", "101001", "000001", "100000",
    "100111", "111001", "100001", "011110", "101000", "000101",
    "100011", "110100", "111100", "001111", "110001", "100011",
    "111110", "011111", "111100", "001100", "001011", "010100",
    "010110", "011010", "101101", "110110", "110101", "101011",
    "011011", "011000", "101010", "010101", "011001", "100110",
    "100010", "010001", "010011", "110010", "110011", "001110",
    "101111", "111101", "011011", "011000"
]

# Natural binary ordering (0-63)
binary_ordering = ALL_HEXAGRAMS[:]

# Shao Yong ordering (Xiantian / Fu Xi sequence)
# This follows the binary tree pattern where hexagrams are ordered
# by reversing the bit order of their index (reflecting the top-down
# construction of the Xiantian diagram)
def shao_yong_order():
    """Generate Shao Yong (Xiantian) ordering.

    The Shao Yong sequence arranges hexagrams in a binary tree structure.
    Each hexagram's position is determined by reading its lines from top
    to bottom as a binary number (opposite of the natural binary reading
    which goes bottom to top).
    """
    hexagrams = []
    for i in range(64):
        # Reverse the 6-bit binary representation
        bits = format(i, '06b')
        reversed_bits = bits[::-1]
        hexagrams.append(reversed_bits)
    return hexagrams

shao_yong_sequence = shao_yong_order()


# ============================================================
# Generate random orderings
# ============================================================

N_RANDOM = 1000
random.seed(42)
np.random.seed(42)

random_surprises_all = []
random_hamming_all = []
random_similarity_all = []

for _ in range(N_RANDOM):
    perm = ALL_HEXAGRAMS[:]
    random.shuffle(perm)
    h, s, surp = compute_sequence_metrics(perm)
    random_hamming_all.append(h)
    random_similarity_all.append(s)
    random_surprises_all.append(surp)


# ============================================================
# Compute metrics for each ordering
# ============================================================

kw_hamming, kw_similarity, kw_surprise = compute_sequence_metrics(king_wen_sequence)
bin_hamming, bin_similarity, bin_surprise = compute_sequence_metrics(binary_ordering)
sy_hamming, sy_similarity, sy_surprise = compute_sequence_metrics(shao_yong_sequence)

# Random: mean and 95% CI
random_surprise_mean = np.mean(random_surprises_all, axis=0)
random_surprise_std = np.std(random_surprises_all, axis=0)
random_surprise_lo = np.percentile(random_surprises_all, 2.5, axis=0)
random_surprise_hi = np.percentile(random_surprises_all, 97.5, axis=0)

random_hamming_mean = np.mean(random_hamming_all, axis=0)
random_similarity_mean = np.mean(random_similarity_all, axis=0)


# ============================================================
# Figure 1: King Wen metrics (existing figure, improved)
# ============================================================

fig1, axes1 = plt.subplots(3, 1, figsize=(12, 8))

axes1[0].plot(kw_hamming, color='#2c3e50', linewidth=1.2)
axes1[0].set_title("Hamming Distances in King Wen Sequence", fontsize=11)
axes1[0].set_ylabel("Distance")
axes1[0].set_ylim(-0.5, 6.5)

axes1[1].plot(kw_similarity, color='#e67e22', linewidth=1.2)
axes1[1].set_title("Pattern Similarities in King Wen Sequence", fontsize=11)
axes1[1].set_ylabel("Similarity")

axes1[2].plot(kw_surprise, color='#27ae60', linewidth=1.2)
axes1[2].set_title("Information-Theoretic Surprise in King Wen Sequence", fontsize=11)
axes1[2].set_xlabel("Transition Index")
axes1[2].set_ylabel("Surprise")

fig1.tight_layout()
fig1.savefig('king_wen_metrics.pdf', bbox_inches='tight', dpi=300)
plt.close(fig1)
print("Saved king_wen_metrics.pdf")


# ============================================================
# Figure 2: 4-panel comparison
# ============================================================

fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))
transition_x = np.arange(63)

# Panel 1: King Wen
ax = axes2[0, 0]
ax.plot(transition_x, kw_surprise, color='#c0392b', linewidth=1.2, label='King Wen')
ax.set_title("King Wen Sequence", fontsize=12, fontweight='bold')
ax.set_ylabel("Surprise")
ax.set_ylim(0, np.max(kw_surprise) * 1.3)
ax.axhline(y=np.mean(kw_surprise), color='#c0392b', linestyle='--', alpha=0.5,
           label=f'Mean: {np.mean(kw_surprise):.3f}')
ax.axhline(y=np.mean(kw_surprise) + np.std(kw_surprise), color='gray',
           linestyle=':', alpha=0.4)
ax.axhline(y=np.mean(kw_surprise) - np.std(kw_surprise), color='gray',
           linestyle=':', alpha=0.4)
ax.legend(fontsize=8)

# Panel 2: Random (mean + 95% CI)
ax = axes2[0, 1]
ax.plot(transition_x, random_surprise_mean, color='#7f8c8d', linewidth=1.2,
        label='Random Mean')
ax.fill_between(transition_x, random_surprise_lo, random_surprise_hi,
                color='#bdc3c7', alpha=0.4, label='95% CI')
ax.set_title(f"Random Orderings (n={N_RANDOM})", fontsize=12, fontweight='bold')
ax.set_ylabel("Surprise")
ax.set_ylim(0, np.max(kw_surprise) * 1.3)
ax.legend(fontsize=8)

# Panel 3: Natural binary
ax = axes2[1, 0]
ax.plot(transition_x, bin_surprise, color='#2980b9', linewidth=1.2,
        label='Binary')
ax.set_title("Natural Binary Ordering (0-63)", fontsize=12, fontweight='bold')
ax.set_xlabel("Transition Index")
ax.set_ylabel("Surprise")
ax.set_ylim(0, np.max(kw_surprise) * 1.3)
ax.axhline(y=np.mean(bin_surprise), color='#2980b9', linestyle='--', alpha=0.5,
           label=f'Mean: {np.mean(bin_surprise):.3f}')
ax.legend(fontsize=8)

# Panel 4: Shao Yong
ax = axes2[1, 1]
ax.plot(transition_x, sy_surprise, color='#8e44ad', linewidth=1.2,
        label='Shao Yong')
ax.set_title("Shao Yong Ordering (c. 1050 AD)", fontsize=12, fontweight='bold')
ax.set_xlabel("Transition Index")
ax.set_ylabel("Surprise")
ax.set_ylim(0, np.max(kw_surprise) * 1.3)
ax.axhline(y=np.mean(sy_surprise), color='#8e44ad', linestyle='--', alpha=0.5,
           label=f'Mean: {np.mean(sy_surprise):.3f}')
ax.legend(fontsize=8)

fig2.suptitle("Surprise Profile Comparison Across Orderings", fontsize=14,
              fontweight='bold', y=1.02)
fig2.tight_layout()
fig2.savefig('king_wen_comparison.pdf', bbox_inches='tight', dpi=300)
plt.close(fig2)
print("Saved king_wen_comparison.pdf")


# ============================================================
# Statistical tests
# ============================================================

results = []
results.append("=" * 70)
results.append("STATISTICAL ANALYSIS: King Wen Sequence vs. Baselines")
results.append("=" * 70)

# Summary statistics
results.append("\n--- Summary Statistics (Surprise) ---\n")
results.append(f"{'Ordering':<20} {'Mean':>8} {'Std':>8} {'Min':>8} {'Max':>8} {'Variance':>10}")
results.append("-" * 64)

for name, data in [("King Wen", kw_surprise),
                   ("Binary", bin_surprise),
                   ("Shao Yong", sy_surprise)]:
    results.append(f"{name:<20} {np.mean(data):>8.4f} {np.std(data):>8.4f} "
                   f"{np.min(data):>8.4f} {np.max(data):>8.4f} {np.var(data):>10.6f}")

# Random aggregate
rand_all_flat = np.concatenate(random_surprises_all)
rand_variances = [np.var(s) for s in random_surprises_all]
results.append(f"{'Random (mean)':<20} {np.mean(rand_all_flat):>8.4f} "
               f"{np.std(rand_all_flat):>8.4f} {np.min(rand_all_flat):>8.4f} "
               f"{np.max(rand_all_flat):>8.4f} {np.mean(rand_variances):>10.6f}")

# Kolmogorov-Smirnov tests
results.append("\n--- Kolmogorov-Smirnov Tests (Surprise Distribution) ---\n")
results.append(f"{'Comparison':<35} {'KS Statistic':>14} {'p-value':>12} {'Significant':>12}")
results.append("-" * 75)

# KW vs each random permutation — use the pooled random distribution
ks_rand = ks_2samp(kw_surprise, rand_all_flat)
ks_bin = ks_2samp(kw_surprise, bin_surprise)
ks_sy = ks_2samp(kw_surprise, sy_surprise)

for name, result in [("King Wen vs. Random (pooled)", ks_rand),
                     ("King Wen vs. Binary", ks_bin),
                     ("King Wen vs. Shao Yong", ks_sy)]:
    sig = "YES" if result.pvalue < 0.05 else "no"
    results.append(f"{name:<35} {result.statistic:>14.4f} {result.pvalue:>12.6f} {sig:>12}")

# Levene's test (variance equality)
results.append("\n--- Levene's Test (Variance Equality) ---\n")
results.append(f"{'Comparison':<35} {'Statistic':>14} {'p-value':>12} {'KW Lower Var':>14}")
results.append("-" * 77)

# Compare King Wen variance against each baseline
for name, baseline in [("King Wen vs. Random (pooled)", rand_all_flat),
                       ("King Wen vs. Binary", bin_surprise),
                       ("King Wen vs. Shao Yong", sy_surprise)]:
    stat, p = levene(kw_surprise, baseline)
    kw_lower = "YES" if np.var(kw_surprise) < np.var(baseline) else "no"
    results.append(f"{name:<35} {stat:>14.4f} {p:>12.6f} {kw_lower:>14}")

# Ljung-Box test (autocorrelation)
results.append("\n--- Ljung-Box Test (Autocorrelation, lag=5) ---\n")
results.append(f"{'Ordering':<20} {'LB Statistic':>14} {'p-value':>12} {'Significant':>12}")
results.append("-" * 60)

for name, data in [("King Wen", kw_surprise),
                   ("Binary", bin_surprise),
                   ("Shao Yong", sy_surprise)]:
    lb_result = acorr_ljungbox(data, lags=[5], return_df=True)
    lb_stat = lb_result['lb_stat'].values[0]
    lb_p = lb_result['lb_pvalue'].values[0]
    sig = "YES" if lb_p < 0.05 else "no"
    results.append(f"{name:<20} {lb_stat:>14.4f} {lb_p:>12.6f} {sig:>12}")

# Random: what fraction show significant autocorrelation?
rand_sig_count = 0
for surp in random_surprises_all:
    lb = acorr_ljungbox(surp, lags=[5], return_df=True)
    if lb['lb_pvalue'].values[0] < 0.05:
        rand_sig_count += 1
results.append(f"{'Random':<20} {rand_sig_count}/{N_RANDOM} permutations show significant autocorrelation")

# Autocorrelation values
results.append("\n--- Autocorrelation (lags 1-5) ---\n")
results.append(f"{'Ordering':<20} {'Lag 1':>8} {'Lag 2':>8} {'Lag 3':>8} {'Lag 4':>8} {'Lag 5':>8}")
results.append("-" * 62)

for name, data in [("King Wen", kw_surprise),
                   ("Binary", bin_surprise),
                   ("Shao Yong", sy_surprise)]:
    acf = [np.corrcoef(data[:-lag], data[lag:])[0, 1] for lag in range(1, 6)]
    results.append(f"{name:<20} " + " ".join(f"{a:>8.4f}" for a in acf))

# Print and save
output = "\n".join(results)
print(output)

with open('statistical_results.txt', 'w') as f:
    f.write(output)
print("\nSaved statistical_results.txt")
