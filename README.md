# King Wen AGI Framework

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14679538.svg)](https://doi.org/10.5281/zenodo.14679538)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Paper

This repository contains the LaTeX source for our paper "King Wen Sequence of the I-Ching as a Proto-AGI Learning Framework". You can find:

- The compiled PDF in the `paper` directory
- LaTeX source files in the `paper` directory
- Supporting materials and code in the `src` directory

If you use this work in your research, please cite:

```bibtex
@article{AugustinChan2025kingwen,
  title={King Wen Sequence of the I-Ching as a Proto-AGI Learning Framework},
  author={Augustin Chan},
  year={2025},
  publisher={Zenodo},
  doi={10.5281/zenodo.14679538}
}
```

## LaTeX Template

This project uses a modified arXiv-style LaTeX template based on the NeurIPS 2018 style. The template provides a clean, single-column format optimized for preprint submissions.

### Usage

1. Use document class **article**
2. Copy **arxiv.sty** to your tex file's directory
3. Add `\usepackage{arxiv}` after `\documentclass{article}`
4. Required packages (included in style): **geometry** and **fancyheader**

### Build Instructions

The repository includes VSCode LaTeX Workshop settings. To build:

1. Install required LaTeX packages
2. Use the provided `settings.json` configuration
3. Build will trigger automatically on save, or:
   ```bash
   xelatex -shell-escape paper
   bibtex paper
   xelatex -shell-escape paper
   xelatex -shell-escape paper
   ```

### arXiv Submission

When submitting to arXiv:

1. Run `latex paper && bibtex paper`
2. Copy contents of generated `.bbl` file into your tex file
3. Comment out `\bibliography{references}`
4. Submit the self-contained tex file

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
- [Latest Release](https://doi.org/10.5281/zenodo.14679538)
- [All Versions](https://zenodo.org/records/14679538)

## Contact

For questions or issues, please:
1. Open an issue in this repository
2. Contact the authors through the paper's corresponding email