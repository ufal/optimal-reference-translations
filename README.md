# Evaluating Optimal Reference Translations

> **Abstract:** The overall translation quality reached by current machine translation (MT) systems for high-resourced language pairs is remarkably good. Standard methods of evaluation are not suitable nor intended to uncover the many translation errors and quality deficiencies that still persist. Furthermore, the quality of standard reference translations is commonly questioned and comparable quality levels have been reached by MT alone in several language pairs. Navigating further research in these high-resource settings is thus difficult. In this article, we propose a methodology for creating more reliable document-level human reference translations, called "optimal reference translations," with the simple aim to raise the bar of what should be deemed "human translation quality." We evaluate the obtained document-level optimal reference translations in comparison with "standard" ones, confirming a significant quality increase and also documenting the relationship between evaluation and translation editing.

This is project at ÚFAL / Charles University. Paper to be published in Natural Language Engineering 2024.

Collected English to Czech translation evaluation human data are in [`data/annotations.json`](data/annotations.json). The rest of this repository contains data preparation and evaluation code.
The process of the data is as follows:
1. P1, P2, and P3 are independent translations from English to Czech. N1 is an expert translation by a translatologist.
2. All the human translations are evaluated (in [`data/annotations.json`](data/annotations.json)) by different types of human annotators (laypeople, translatology students, professional translators).

## Results:

![image](https://github.com/ufal/optimal-reference-translations/assets/7661193/d20d1e2e-4d08-4457-b654-961917d7b0e9)

![image](https://github.com/ufal/optimal-reference-translations/assets/7661193/190f519d-6851-4186-aac6-7fe53b59ba7f)
