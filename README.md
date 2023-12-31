This is a repository for two papers: **Quality and Quantity of Machine Translation References for Automated Metrics [paper WIP]** - effect of reference quality and quantity on automatic metric performance, and **Evaluating Optimal Reference Translations [[paper]](https://arxiv.org/abs/2311.16787)** - creation of the data and human aspects of annotation and translation.

# Quality and Quantity of Machine Translation References for Automated Metrics [paper WIP]

> **Abstract:** Automatic machine translation metrics often use _human_ translations to determine the quality _system_ translations. Common wisdom in the field dictates that the human references should be of very high quality. However, there are no cost-benefit analyses that could be used to guide practitioners who plan to collect references for machine translation evaluation. We find that higher-quality references lead to better metric correlations with humans at the segment-level. Having up to 7 references per segment and taking their average helps. Interestingly, the references from vendors of different qualities can be mixed together and improve metric success. Higher quality references, however, cost more to create and we frame this as an optimization problem: given a specific budget, what types of references should be collected to maximize metric success. These findings can be used by evaluators of shared tasks when references need to be created under a certain budget.

Cite [this work][TODO] as:
```
@misc{TODO}
```

## Results

Higher quality translation lead to better segment-level correlations. Very high quality translations (R4, which come from translatologists) contain translation shifts and are not the best as references.
Using up to 7 references per segment helps.

<img src="https://github.com/ufal/optimal-reference-translations/assets/7661193/d4cf2669-b2d8-40a3-9193-b1e8811090f2" width="48%">
<img src="https://github.com/ufal/optimal-reference-translations/assets/7661193/c660daaa-ffd2-4229-8084-309e4db2b89f" width="48%">

A heuristic-based algorithm can select which references to invest in. It is controlled by a hyperparameter which balances between quality and quantity.

<img src="https://github.com/ufal/optimal-reference-translations/assets/7661193/53e27e2e-57b6-4aa8-ae52-74f6adc649de" width="48%">
<img src="https://github.com/ufal/optimal-reference-translations/assets/7661193/d5579fea-946c-4056-b4d6-ccdb8cefa3cb" width="48%">

# Evaluating Optimal Reference Translations [[paper]](https://arxiv.org/abs/2311.16787)

> **Abstract:** The overall translation quality reached by current machine translation (MT) systems for high-resourced language pairs is remarkably good. Standard methods of evaluation are not suitable nor intended to uncover the many translation errors and quality deficiencies that still persist. Furthermore, the quality of standard reference translations is commonly questioned and comparable quality levels have been reached by MT alone in several language pairs. Navigating further research in these high-resource settings is thus difficult. In this article, we propose a methodology for creating more reliable document-level human reference translations, called "optimal reference translations," with the simple aim to raise the bar of what should be deemed "human translation quality." We evaluate the obtained document-level optimal reference translations in comparison with "standard" ones, confirming a significant quality increase and also documenting the relationship between evaluation and translation editing.

This is project at ETH Zürich and ÚFAL Charles University. [Paper](https://arxiv.org/abs/2311.16787) to be published in Natural Language Engineering 2024.
For now cite as:
```
@misc{zouhar2023evaluating,
      title={Evaluating Optimal Reference Translations}, 
      author={Vilém Zouhar and Věra Kloudová and Martin Popel and Ondřej Bojar},
      year={2023},
      eprint={2311.16787},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

Collected English to Czech translation evaluation human data are in [`data/annotations.json`](data/annotations.json). The rest of this repository contains data preparation and evaluation code.
Our data is based on WMT2020 data and can thus be also used to e.g. evaluate the quality of various translations as references.
The process of the data is as follows:
1. P1, P2, and P3 are independent translations from English to Czech. N1 is an expert translation by a translatologist.
2. All the human translations are evaluated on document and segment level with detail (in [`data/annotations.json`](data/annotations.json)) by different types of human annotators (laypeople, translatology students, professional translators). If the translation is not perfect, the annotators provide a post-edited version for which they would assign the highest grade (6).

## Example usage

```bash
# fetch data
curl "https://raw.githubusercontent.com/ufal/optimal-reference-translations/main/data/annotations.json" > annotations.json
```

```python3
# in Python
import json
data = json.load(open("annotations.json"))

# 220 annotated documents
len(data)

# 1760 annotated source lines
sum([len(doc["lines"]) for doc in data])

# 7040 annotated translations
sum([sum([len(line["translations"]) for line in doc["lines"]]) for doc in data])

# 11 annotators
len(set(doc["uid"] for doc in data))

import numpy as np
# Average document-level for N1: 5.865
np.average([doc["rating"]["4"]["overall"] for doc in data])

# Average document-level for P3: 4.810
np.average([doc["rating"]["3"]["overall"] for doc in data])
```

## Results

It make sense to have multiple rounds of translation post-editing.
![image](https://github.com/ufal/optimal-reference-translations/assets/7661193/d20d1e2e-4d08-4457-b654-961917d7b0e9)

Translatology students, professionals and laypeople perceive quality differently.
![image](https://github.com/ufal/optimal-reference-translations/assets/7661193/190f519d-6851-4186-aac6-7fe53b59ba7f)


## Data structure

Beginning of [`data/annotations.json`](data/annotations.json):

```
[
    {
        "uid": "sahara",
        "expertise": "student",
        "doc": "huffingtonpost.com.19385",
        "time": 210.0,                             # self-reported in minutes
        "rating": {
            "2": {                                 # 2 = P2
                "spelling": 4.0,                   # ranges from 0 to 6
                "terminology": 5.5,
                "grammar": 5.5,
                "meaning": 5.0,
                "style": 4.5,
                "pragmatics": 6.0,
                "overall": 4.5
            },
            "4": {                                 # 4 = N1
                "spelling": 6.0,
                "terminology": 6.0,
                "grammar": 6.0,
                "meaning": 5.0,
                "style": 5.0,
                "pragmatics": 6.0,
                "overall": 5.7
            },
            "1": {                                 # 1 = P1
                "spelling": 6.0,
                "terminology": 5.9,
                "grammar": 5.4,
                "meaning": 4.7,
                "style": 4.6,
                "pragmatics": 5.8,
                "overall": 5.0
            },
            "3": {                                 # 3 = P3
                "spelling": 4.5,
                "terminology": 4.7,
                "grammar": 5.0,
                "meaning": 4.5,
                "style": 5.0,
                "pragmatics": 6.0,
                "overall": 4.6
            }
        },
        "lines": [
            {
                "source": "Sony, Disney Back To Work On Third Spider-Man Film",               # source sentence
                "comment": null,
                "translations": {
                    "2": {
                        "orig": "Sony a Disney opět pracují na třetím filmu o Spider-Manovi", # original translation
                        "done": "Sony a Disney pracují na třetím filmu o Spider-Manovi",      # post-edited translation
                        "rating": {
                            "spelling": 6.0,
                            "terminology": 6.0,
                            "grammar": 6.0,
                            "meaning": 5.0,
                            "style": 6.0,
                            "pragmatics": 6.0,
                            "overall": 5.0
                        }
                    },
                    "4": {
                        "orig": "Sony a Disney opět spolupracují na třetím filmu o Spider-Manovi",
                        "done": "Sony a Disney opět spolupracují na třetím filmu o Spider-Manovi",
                        "rating": {
                            "spelling": 6.0,
                            "terminology": 6.0,
                            "grammar": 6.0,
                            "meaning": 6.0,
                            "style": 6.0,
                            "pragmatics": 6.0,
                            "overall": 6.0
                        }
                    },
...
```
