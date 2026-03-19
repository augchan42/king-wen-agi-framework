"""
King Wen anti-habituation learning rate schedules.

Drop this file into the autoresearch repo alongside train.py.
Import and use in train.py's get_lr_multiplier function.

Usage in train.py:
    from king_wen_schedules import get_king_wen_lr_multiplier
    # Replace get_lr_multiplier with get_king_wen_lr_multiplier
"""

import math

# King Wen sequence surprise values (pre-computed from the paper's analysis).
# These are the information-theoretic surprise values for each of the 63
# transitions in the King Wen sequence, normalized to [0, 1].
KING_WEN_SURPRISE_RAW = [
    2.3026, 1.0498, 0.7133, 0.6539, 0.9676, 1.1874, 0.1625, 0.5798,
    0.2963, 0.4155, 0.6539, 0.4463, 0.1532, 0.9293, 0.3285, 0.8675,
    0.4463, 0.7985, 0.1625, 0.5390, 0.2744, 0.7560, 0.1985, 0.4155,
    0.2231, 0.7985, 0.7985, 0.7133, 0.5390, 0.7560, 0.3567, 0.2744,
    0.9293, 0.7133, 0.4463, 1.1874, 0.1532, 0.2744, 1.5141, 0.7560,
    0.5390, 0.2744, 0.2744, 0.7133, 0.2231, 0.1985, 0.4463, 0.9676,
    0.3567, 0.4463, 0.4463, 0.9676, 0.4463, 0.7133, 0.7133, 0.7560,
    0.5390, 0.2744, 0.9293, 0.4463, 0.1532, 0.7985, 0.3567,
]

# Normalize to [0, 1]
_min_s = min(KING_WEN_SURPRISE_RAW)
_max_s = max(KING_WEN_SURPRISE_RAW)
KING_WEN_SURPRISE = [(s - _min_s) / (_max_s - _min_s) for s in KING_WEN_SURPRISE_RAW]


def get_king_wen_lr_multiplier(progress, base_amplitude=0.3, warmup_ratio=0.0,
                                warmdown_ratio=0.5, final_lr_frac=0.0):
    """
    King Wen anti-habituation LR schedule.

    Uses the King Wen sequence's surprise profile to modulate learning rate.
    The surprise values provide high-variance, non-autocorrelated perturbation
    on top of a standard warmup/warmdown envelope.

    Args:
        progress: float in [0, 1], fraction of training time elapsed
        base_amplitude: how much the KW modulation affects LR (0.3 = ±30%)
        warmup_ratio: fraction of time for warmup
        warmdown_ratio: fraction of time for warmdown
        final_lr_frac: final LR as fraction of peak
    """
    # Standard envelope (warmup → constant → warmdown)
    if progress < warmup_ratio:
        envelope = progress / warmup_ratio if warmup_ratio > 0 else 1.0
    elif progress < 1.0 - warmdown_ratio:
        envelope = 1.0
    else:
        cooldown = (1.0 - progress) / warmdown_ratio
        envelope = cooldown * 1.0 + (1 - cooldown) * final_lr_frac

    # King Wen modulation: map progress to a position in the 63-transition sequence
    kw_idx = int(progress * (len(KING_WEN_SURPRISE) - 1))
    kw_idx = min(kw_idx, len(KING_WEN_SURPRISE) - 1)
    kw_value = KING_WEN_SURPRISE[kw_idx]  # in [0, 1]

    # Convert to modulation: center at 1.0, range determined by amplitude
    # kw_value=0 → (1 - amplitude), kw_value=1 → (1 + amplitude)
    modulation = 1.0 + base_amplitude * (2 * kw_value - 1)

    return envelope * modulation


def get_random_perturbation_lr_multiplier(progress, seed=42, base_amplitude=0.3,
                                           warmup_ratio=0.0, warmdown_ratio=0.5,
                                           final_lr_frac=0.0):
    """
    Random perturbation LR schedule (control for King Wen).

    Same envelope and amplitude as King Wen schedule, but with deterministic
    pseudo-random perturbation instead of King Wen surprise values.
    This controls for "any perturbation helps" vs "King Wen specifically helps."
    """
    if progress < warmup_ratio:
        envelope = progress / warmup_ratio if warmup_ratio > 0 else 1.0
    elif progress < 1.0 - warmdown_ratio:
        envelope = 1.0
    else:
        cooldown = (1.0 - progress) / warmdown_ratio
        envelope = cooldown * 1.0 + (1 - cooldown) * final_lr_frac

    # Deterministic pseudo-random using sin hash (no imports needed, reproducible)
    idx = int(progress * 63)
    rand_value = (math.sin(seed * 1000 + idx * 7.919) + 1) / 2  # in [0, 1]
    modulation = 1.0 + base_amplitude * (2 * rand_value - 1)

    return envelope * modulation


def get_shao_yong_lr_multiplier(progress, base_amplitude=0.3, warmup_ratio=0.0,
                                 warmdown_ratio=0.5, final_lr_frac=0.0):
    """
    Shao Yong ordering LR schedule (structured but predictable control).

    Uses a repeating sawtooth pattern that mimics the highly autocorrelated
    surprise profile of the Shao Yong sequence.
    """
    if progress < warmup_ratio:
        envelope = progress / warmup_ratio if warmup_ratio > 0 else 1.0
    elif progress < 1.0 - warmdown_ratio:
        envelope = 1.0
    else:
        cooldown = (1.0 - progress) / warmdown_ratio
        envelope = cooldown * 1.0 + (1 - cooldown) * final_lr_frac

    # Highly autocorrelated sawtooth (mimics Shao Yong's binary tree pattern)
    idx = int(progress * 63)
    # Shao Yong pattern: repeating rise-fall with period 8
    cycle_pos = (idx % 8) / 7  # 0 to 1 within each cycle
    modulation = 1.0 + base_amplitude * (2 * cycle_pos - 1)

    return envelope * modulation
