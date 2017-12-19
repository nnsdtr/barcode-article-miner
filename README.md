# DNA Barcoding in Fungi: barcode-article-miner

Text converted PDFs allowed us to build a text-mining python script to detect the presence of selected biomarker and purpose terms specifically within the Methods section on the body of papers. For (1) biomarker terms we selected "ITS", "18S", "28S", "RPB", "RPB1", "RPB2", "EF1α" and "β-tubulin”, and for (2) purpose terms, "phylogeny" and "identification". As papers section titles and all searched terms can present writing variants, python’s Regular Expressions library (RE) were applied to cover their detection (for further information, see Table S1 on Supplementary Material).

## Python version

Python, version 3.5.2-release (x86_64-pc-linux-gnu). Copyright (C) 2001-2017 Python Software Foundation. All rights reserved.

## Built With

* [Regular expression module](https://docs.python.org/3.5/library/re.html) - Used to cover the detection of writing variants of searched section titles and terms.

## Reference

Unpublished

## Laboratory
[logo]: https://github.com/nnsdtr/barcode-article-miner/blob/master/lbmcf-logo.png

![alt text][logo]
* **Laboratory of Molecular and Computational Biology of Fungi** *(LBMCF, ICB - UFMG, Belo Horizonte, Brazil)*

### Author
* **Nunes, D.T.** - [nnsdtr](https://github.com/nnsdtr)
