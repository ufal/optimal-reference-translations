# Evaluating Optimal Reference Translations [[paper]](https://arxiv.org/abs/2311.16787)

> **Abstract:** The overall translation quality reached by current machine translation (MT) systems for high-resourced language pairs is remarkably good. Standard methods of evaluation are not suitable nor intended to uncover the many translation errors and quality deficiencies that still persist. Furthermore, the quality of standard reference translations is commonly questioned and comparable quality levels have been reached by MT alone in several language pairs. Navigating further research in these high-resource settings is thus difficult. In this article, we propose a methodology for creating more reliable document-level human reference translations, called "optimal reference translations," with the simple aim to raise the bar of what should be deemed "human translation quality." We evaluate the obtained document-level optimal reference translations in comparison with "standard" ones, confirming a significant quality increase and also documenting the relationship between evaluation and translation editing.

This is project at ÚFAL / Charles University. [Paper](https://arxiv.org/abs/2311.16787) to be published in Natural Language Engineering 2024.
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
The process of the data is as follows:
1. P1, P2, and P3 are independent translations from English to Czech. N1 is an expert translation by a translatologist.
2. All the human translations are evaluated (in [`data/annotations.json`](data/annotations.json)) by different types of human annotators (laypeople, translatology students, professional translators).

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
```

## Results:

![image](https://github.com/ufal/optimal-reference-translations/assets/7661193/d20d1e2e-4d08-4457-b654-961917d7b0e9)

![image](https://github.com/ufal/optimal-reference-translations/assets/7661193/190f519d-6851-4186-aac6-7fe53b59ba7f)


## Data structure

Beginning of [`data/annotations.json`](data/annotations.json):

```
[
    {
        "uid": "sahara",
        "expertise": "student",
        "doc": "huffingtonpost.com.19385",
        "time": 210.0,
        "rating": {
            "2": {
                "spelling": 4.0,
                "terminology": 5.5,
                "grammar": 5.5,
                "meaning": 5.0,
                "style": 4.5,
                "pragmatics": 6.0,
                "overall": 4.5
            },
            "4": {
                "spelling": 6.0,
                "terminology": 6.0,
                "grammar": 6.0,
                "meaning": 5.0,
                "style": 5.0,
                "pragmatics": 6.0,
                "overall": 5.7
            },
            "1": {
                "spelling": 6.0,
                "terminology": 5.9,
                "grammar": 5.4,
                "meaning": 4.7,
                "style": 4.6,
                "pragmatics": 5.8,
                "overall": 5.0
            },
            "3": {
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
                "source": "Sony, Disney Back To Work On Third Spider-Man Film",
                "comment": null,
                "translations": {
                    "2": {
                        "orig": "Sony a Disney opět pracují na třetím filmu o Spider-Manovi",
                        "done": "Sony a Disney pracují na třetím filmu o Spider-Manovi",
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
