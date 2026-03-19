# King Wen Anti-Habituation Experiment

Minimal validation of the King Wen sequence's anti-habituation properties
using Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) framework.

## Hypothesis

The King Wen sequence's surprise profile — high variance, no autocorrelation,
full-spectrum coverage — represents an optimal anti-habituation schedule.
When applied to learning rate modulation during neural network training,
it should outperform standard monotonic schedules by preventing optimizer
habituation.

## Setup

```bash
# 1. Clone autoresearch
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch

# 2. Install dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# 3. Prepare data (one-time, ~2 min)
uv run prepare.py

# 4. Copy our program.md and experiment files
cp /path/to/king-wen-agi-framework/experiment/program.md .
cp /path/to/king-wen-agi-framework/experiment/king_wen_schedules.py .

# 5. Run baseline first
uv run train.py > run.log 2>&1
grep "^val_bpb:" run.log  # record this as baseline

# 6. Start autonomous experiment loop
# Point Claude/Codex at program.md and let it run
```

## What We're Testing

The autoresearch `train.py` has a learning rate schedule (`get_lr_multiplier`)
that controls training pacing. Currently it's a standard warmup → constant → warmdown
cosine schedule. This is a monotonic, highly predictable schedule — exactly the kind
of pattern the King Wen sequence avoids.

We test whether replacing this with King Wen-inspired schedules improves val_bpb.

## Experiment Variants

See `program.md` for the full agent instructions and `king_wen_schedules.py`
for the schedule implementations.
