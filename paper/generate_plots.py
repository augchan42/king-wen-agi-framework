import matplotlib.pyplot as plt

# Function definitions
def calculate_nuclear_distance(bin1, bin2):
    """Calculate distance between nuclear hexagrams."""
    nuc1 = bin1[1:5]  # Inner four lines
    nuc2 = bin2[1:5]  # Inner four lines
    return sum(n1 != n2 for n1, n2 in zip(nuc1, nuc2))

def calculate_transition_metrics_corrected(bin1, bin2):
    """Calculate distances between two hexagrams."""
    # Hamming distance (total different lines)
    d1 = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    
    # Trigram distance (upper and lower trigrams)
    upper1, lower1 = bin1[:3], bin1[3:]  # Split into trigrams
    upper2, lower2 = bin2[:3], bin2[3:]
    d2 = sum(b1 != b2 for b1, b2 in zip(upper1, upper2)) + sum(b1 != b2 for b1, b2 in zip(lower1, lower2))
    
    # Nuclear distance
    d3 = calculate_nuclear_distance(bin1, bin2)
    
    return d1, d2, d3

def calculate_pattern_similarity(bin1, bin2):
    """Calculate similarity between hexagrams considering I-Ching principles."""
    weights = [0.03, 0.07, 0.15, 0.20, 0.25, 0.30]
    line_diffs = []
    for i, (b1, b2) in enumerate(zip(bin1, bin2)):
        if b1 != b2:
            if b1 == '1' and b2 == '0':
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
    import math
    similarity = calculate_pattern_similarity(bin1, bin2)
    return -math.log(similarity)

# King Wen sequence of hexagrams in binary
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

# Calculate metrics, similarities, and surprises
transition_metrics = []
pattern_similarities = []
surprises = []

for i in range(len(king_wen_sequence) - 1):
    bin1 = king_wen_sequence[i]
    bin2 = king_wen_sequence[i + 1]
    metrics = calculate_transition_metrics_corrected(bin1, bin2)
    similarity = calculate_pattern_similarity(bin1, bin2)
    surprise = calculate_surprise(bin1, bin2)
    transition_metrics.append(metrics)
    pattern_similarities.append(similarity)
    surprises.append(surprise)

# Unpack transition metrics for plotting
hamming_distances = [m[0] for m in transition_metrics]
trigram_distances = [m[1] for m in transition_metrics]
nuclear_distances = [m[2] for m in transition_metrics]

# Plot results
plt.figure(figsize=(12, 8))

# Hamming distance
plt.subplot(3, 1, 1)
plt.plot(hamming_distances, label='Hamming Distance')
plt.title("Hamming Distances in King Wen Sequence")
plt.xlabel("Transition Index")
plt.ylabel("Distance")
plt.legend()

# Pattern similarity
plt.subplot(3, 1, 2)
plt.plot(pattern_similarities, label='Pattern Similarity', color='orange')
plt.title("Pattern Similarities in King Wen Sequence")
plt.xlabel("Transition Index")
plt.ylabel("Similarity")
plt.legend()

# Surprise
plt.subplot(3, 1, 3)
plt.plot(surprises, label='Surprise', color='green')
plt.title("Surprises in King Wen Sequence")
plt.xlabel("Transition Index")
plt.ylabel("Surprise")
plt.legend()

plt.tight_layout()
# plt.show()

# Save to PDF
plt.savefig('king_wen_metrics.pdf', bbox_inches='tight', dpi=300)
plt.close()
