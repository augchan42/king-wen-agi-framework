# King Wen AGI Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19199267.svg)](https://doi.org/10.5281/zenodo.19199267)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Paper

**Statistical Properties of the King Wen Sequence: An Anti-Habituation Structure That Does Not Improve Neural Network Training**

The King Wen sequence has genuine statistical properties (confirmed by Monte Carlo analysis against 100,000 random baselines) but they do not improve neural network training. This is a negative result paper reporting experiments across two platforms (NVIDIA RTX 2060 with PyTorch, Apple Silicon with MLX).

- [Paper PDF](paper/king-wen.pdf)
- [Markdown source](paper/king-wen.md)
- [LaTeX source](paper/king-wen.tex)
- [arXiv submission archive](king-wen-arxiv.tar.gz)

If you use this work in your research, please cite:

```bibtex
@article{Chan2026kingwen,
  title={Statistical Properties of the King Wen Sequence: An Anti-Habituation Structure That Does Not Improve Neural Network Training},
  author={Augustin Chan},
  year={2026},
  publisher={Zenodo},
  doi={10.5281/zenodo.19199267}
}
```

## Repository Structure

- `paper/` — Paper source (markdown, LaTeX, PDF), statistical results, figures
- `experiment/` — LR schedule implementations and experiment protocol
- `arxiv-submission/` — Flat files ready for arXiv upload
- `arxiv.sty` — arXiv preprint style file

## Build Instructions

```bash
cd paper
pdflatex king-wen.tex
bibtex king-wen
pdflatex king-wen.tex
pdflatex king-wen.tex
```

Requires TeX Live 2025+ with `libertine` and `newtxmath` packages.

## License

- Code: [MIT License](License.txt)
- Paper and Documentation: [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Citation and Reuse

If you use this template or code in your work:
1. Cite our paper using the BibTeX entry above
2. Link back to this repository
3. Check the licenses for code (MIT) and documentation (CC-BY 4.0)

## Archived Versions

This repository is archived on Zenodo for long-term preservation. You can find specific versions:
- [Latest Release](https://doi.org/10.5281/zenodo.19199267)
- [All Versions](https://zenodo.org/records/19199267)

## Contact

For questions or issues, please:
1. Open an issue in this repository
2. Contact the authors through the paper's corresponding email