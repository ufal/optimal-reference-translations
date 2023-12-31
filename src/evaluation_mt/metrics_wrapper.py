"""
The expected input to each function is a list of tuples in the form of (src, tgt, ref)
"""

import tqdm
import functools


def _bleu(data):
    from sacrebleu.metrics import BLEU
    metric = BLEU(effective_order=True)
    out = [
        metric.corpus_score([x[1]], [[x[2]]],).score
        for x in tqdm.tqdm(data)
    ]
    print(metric.get_signature().format(short=True))
    return out


def _chrf(data):
    from sacrebleu.metrics import CHRF, TER
    metric = CHRF()
    out = [
        metric.corpus_score([x[1]], [[x[2]]],).score
        for x in tqdm.tqdm(data)
    ]
    print(metric.get_signature().format(short=True))
    return out


def _ter(data):
    from sacrebleu.metrics import TER
    metric = TER()
    out = [
        -metric.corpus_score([x[1]], [[x[2]]],).score
        for x in tqdm.tqdm(data)
    ]
    print(metric.get_signature().format(short=True))
    return out


def _comet(data, model):
    import torch
    from comet import download_model, load_from_checkpoint

    model = load_from_checkpoint(download_model(model))
    model.eval()
    data = [
        {
            "src": x[0],
            "mt":  x[1],
            "ref": x[2],
        }
        for x in data
    ]
    with torch.no_grad():
        out =  [x*100 for x in model.predict(data, batch_size=24, gpus=1).scores]
    del model
    return out

def _bleurt(data):
    import torch
    from bleurt_pytorch import BleurtForSequenceClassification, BleurtTokenizer

    bleurt_model = BleurtForSequenceClassification.from_pretrained(
        'lucadiliello/BLEURT-20-D12'
        ).to("cuda:0")
    bleurt_tokenizer = BleurtTokenizer.from_pretrained(
        'lucadiliello/BLEURT-20-D12', max_length=512
    )
    bleurt_model.eval()

    out = []
    with torch.no_grad():
        for line in tqdm.tqdm(data):
            inputs = bleurt_tokenizer(
                [line[1]], [line[2]], padding=True, truncation=True, return_tensors='pt'
            ).to("cuda:0")
            out.append(
                float(bleurt_model(**inputs).logits.flatten().cpu().tolist()[0])*100
            )

    del bleurt_model
    del bleurt_tokenizer

    return out


METRICS = {
    "bleu": _bleu,
    "chrf": _chrf,
    "ter": _ter,
    "comet20": functools.partial(_comet, model="Unbabel/wmt20-comet-da"),
    "comet22": functools.partial(_comet, model="Unbabel/wmt22-comet-da"),
    "bleurt": _bleurt,
}

METRIC_NAMES = {
    "bleu": "BLEU",
    "chrf": "ChrF",
    "ter": "TER",
    "comet20": "COMET$^{20}$",
    "comet22": "COMET$^{22}$",
    "bleurt": "BLEURT",
}
