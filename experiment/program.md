# King Wen Anti-Habituation LR Schedule Experiment

This is an autoresearch experiment testing whether the King Wen sequence's
anti-habituation surprise profile improves neural network training when
applied as a learning rate schedule modulation.

## Background

The King Wen sequence (c. 1000 BC) orders the 64 I-Ching hexagrams in a
pattern with statistically unusual properties: random-like mean surprise,
significantly higher variance than all baselines, and zero autocorrelation.
We hypothesize this "anti-habituation" profile prevents optimizer habituation
when applied to learning rate scheduling.

Paper: https://github.com/augchan42/king-wen-agi-framework

## Setup

To set up this experiment:

1. **Agree on a run tag** with the user (e.g. `kingwen-mar19`).
2. **Create the branch**: `git checkout -b autoresearch/<tag>` from current master.
3. **Read the in-scope files**:
   - `README.md` — repository context
   - `prepare.py` — fixed constants, data prep, tokenizer, dataloader, evaluation. Do not modify.
   - `train.py` — the file you modify
   - `king_wen_schedules.py` — pre-built LR schedule functions (copy into repo if not present)
4. **Verify data exists**: Check `~/.cache/autoresearch/` for data shards and tokenizer.
5. **Initialize results.tsv** with header row.
6. **Confirm and go**.

## Experiment Plan

This is a STRUCTURED experiment, not free-form exploration. Run these experiments
IN ORDER. Each takes ~5 minutes.

### Phase 1: Baselines (3 runs)

**Run 1 — Standard baseline:**
Run unmodified `train.py`. Record val_bpb. This is the control.

**Run 2 — Random perturbation control:**
In `train.py`, add `from king_wen_schedules import get_random_perturbation_lr_multiplier`
and replace `get_lr_multiplier` with `get_random_perturbation_lr_multiplier` (amplitude=0.3).
This tests "does ANY perturbation help?" vs the standard schedule.

**Run 3 — Shao Yong (structured predictable) control:**
Replace with `get_shao_yong_lr_multiplier` (amplitude=0.3).
This tests "does structured perturbation help?" — the Shao Yong ordering is
highly autocorrelated (predictable), unlike King Wen.

### Phase 2: King Wen (3 runs)

**Run 4 — King Wen (amplitude=0.3):**
Replace with `get_king_wen_lr_multiplier` (amplitude=0.3).
This is the primary test.

**Run 5 — King Wen (amplitude=0.15):**
Same but with `base_amplitude=0.15`. Tests sensitivity to perturbation strength.

**Run 6 — King Wen (amplitude=0.5):**
Same but with `base_amplitude=0.5`. Tests stronger perturbation.

### Phase 3: Ablations (runs 7+)

After Phase 2, if King Wen shows improvement, run ablations:

**Run 7 — King Wen without warmdown:**
Set `warmdown_ratio=0.0` to test KW modulation without the standard cooldown.

**Run 8 — King Wen with double cycling:**
Map progress through the KW sequence twice (0→63→0→63) instead of once.
Test: `kw_idx = int((progress * 2 % 1.0) * 62)`.

**Run 9+ — Free exploration:**
If results are promising, try:
- Combining King Wen LR schedule with architectural changes
- Applying King Wen modulation to weight decay instead of LR
- Applying King Wen modulation to momentum

### Phase 4: Replication (3 runs)

Re-run the best King Wen variant and the baseline with 3 different random seeds
each (change `torch.manual_seed()` to seeds 42, 123, 456) to confirm the result
isn't seed-dependent.

## How to Modify train.py

The ONLY change for each run is the `get_lr_multiplier` function. Here's the pattern:

```python
# Add at top of train.py, after other imports:
from king_wen_schedules import get_king_wen_lr_multiplier

# Then replace the existing get_lr_multiplier function with:
def get_lr_multiplier(progress):
    return get_king_wen_lr_multiplier(
        progress,
        base_amplitude=0.3,      # ← change this per run
        warmup_ratio=WARMUP_RATIO,
        warmdown_ratio=WARMDOWN_RATIO,
        final_lr_frac=FINAL_LR_FRAC,
    )
```

For baseline/control runs, swap in the appropriate function:
- `get_random_perturbation_lr_multiplier` for random control
- `get_shao_yong_lr_multiplier` for Shao Yong control

## Logging

Use the standard autoresearch results.tsv format:

```
commit	val_bpb	memory_gb	status	description
```

Add a column or note in the description for which schedule variant was used:

```
a1b2c3d	0.997900	44.0	keep	baseline - standard LR schedule
b2c3d4e	0.995200	44.0	keep	king_wen amp=0.3
c3d4e5f	0.998100	44.0	discard	random_perturbation amp=0.3
d4e5f6g	0.999000	44.0	discard	shao_yong amp=0.3
```

## Success Criteria

The experiment supports the hypothesis if:

1. **King Wen schedule achieves lower val_bpb than standard baseline** (primary)
2. **King Wen outperforms random perturbation** (rules out "any noise helps")
3. **King Wen outperforms Shao Yong** (rules out "any structured perturbation helps")
4. **Result replicates across seeds** (rules out luck)

Even if King Wen doesn't win, the results are informative — they tell us whether
anti-habituation LR schedules are worth pursuing at all.

## The Experiment Loop

After completing the structured phases above, you may continue with free exploration.
Follow the standard autoresearch loop:

LOOP FOREVER:
1. Look at git state
2. Modify `train.py` with next experiment
3. git commit
4. Run: `uv run train.py > run.log 2>&1`
5. Read results: `grep "^val_bpb:\|^peak_vram_mb:" run.log`
6. Record in results.tsv
7. If improved: keep. If not: git reset.

**NEVER STOP** once the loop begins. The human may be away. Run until interrupted.
