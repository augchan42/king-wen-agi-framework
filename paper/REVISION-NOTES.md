# Revision Notes for Next Version

Feedback collected during arXiv v1 submission (2026-04-10).

## Priority Changes

### 1. Title reframing (editorial, high impact)

Current:
> Statistical Properties of the King Wen Sequence: An Anti-Habituation Structure That Does Not Improve Neural Network Training

Suggested:
> Statistical Structure in the King Wen Sequence: A Negative Result for Neural Training Utility

Rationale: The more novel contribution is the statistical characterization, not the ML experiments. Lead with the unique part. Many papers do ML experiments; very few make original mathematical claims about a 3,000-year-old sequence.

### 2. Add sinology / mathematical humanities citations (historical credibility)

The historical bridge currently jumps from Leibniz to modern ML. Add classical academic references to anchor the King Wen discussion:

- Richard Rutt — *Zhouyi: The Book of Changes* (historical/philological analysis)
- Edward Shaughnessy — *Unearthing the Changes* (archaeological/textual scholarship)
- Joseph Needham — *Science and Civilisation in China* (mathematical/scientific context)
- Richard Wilhelm — *I Ching* translation (historical discussion only)

Even one or two prevents the paper from looking like "modern ML project with ancient branding."

### 3. Strengthen scale limitation defense (reviewer anticipation)

Current wording is too soft:
> "It is possible that King Wen's anti-habituation properties could help at larger scale..."

Replace with something firmer:
> "While larger-scale effects cannot be excluded, the monotonic degradation under LR modulation suggests the mechanism is unlikely to reverse purely with scale."

This is the first thing reviewers will attack. The monotonic degradation argument is the strongest defense — make it explicit.

### 4. Soften historical claim tone (defensibility)

Change:
> "puzzled scholars for three millennia"

To something like:
> "has long attracted mathematical and philosophical analysis"

The current phrasing is elegant but broad. A reviewer may ask "which scholars? what tradition?"

## Lower Priority

### 5. Consider computational humanities venue

The statistical characterization section (Monte Carlo, four significant properties) stands on its own even without the ML experiments. Could be submitted separately to a computational humanities or digital sinology venue.

### 6. Cross-framework curriculum finding

The torch.compile confound is a useful methodological contribution that could be expanded. Curriculum ordering experiments validated across frameworks (not just seeds) is an underappreciated point.

## Submission Record

- arXiv submitted: 2026-04-10
- Primary category: cs.LG (Machine Learning)
- Cross-lists: cs.AI, cs.NE
- License: CC BY 4.0
- Zenodo concept DOI: 10.5281/zenodo.14679537
- GitHub release: v2.1.1
