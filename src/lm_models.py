from transformers import AutoTokenizer, AutoModel
from utils import get_device
import torch

DEVICE = get_device()


def mean_pooling(model_output, attention_mask, layer_i=0):
    # Mean Pooling - Take attention mask into account for correct averaging
    # first element of model_output contains all token embeddings
    token_embeddings = model_output[layer_i]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(
        token_embeddings.size()
    ).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return (sum_embeddings / sum_mask).reshape(-1)


class Czert():
    def __init__(self):
        self.model = AutoModel.from_pretrained("./models/czert-b", from_tf=True)
        self.tokenizer = AutoTokenizer.from_pretrained("./models/czert-b", from_tf=True)

    def embd(self, sentence, type_out="cls"):
        encoded_input = self.tokenizer(
            sentence, padding=True, truncation=True, max_length=128, return_tensors='pt')
        encoded_input = encoded_input.to(DEVICE)
        with torch.no_grad():
            output = self.model(**encoded_input)
        if type_out == "cls":
            return output[0][0, 0].cpu().numpy()
        elif type_out == "pooler":
            return output["pooler_output"][0].cpu().numpy()
        elif type_out == "tokens":
            sentence_embedding = mean_pooling(
                output, encoded_input['attention_mask']
            )
            return sentence_embedding.cpu().numpy()
        else:
            raise Exception("Unknown type out")


class RobeCzech():
    def __init__(self):
        self.model = AutoModel.from_pretrained("ufal/robeczech-base")
        self.tokenizer = AutoTokenizer.from_pretrained("ufal/robeczech-base")

    def embd(self, sentence, type_out="cls"):
        encoded_input = self.tokenizer(
            sentence, padding=True, truncation=True, max_length=128, return_tensors='pt')
        encoded_input = encoded_input.to(DEVICE)
        with torch.no_grad():
            output = self.model(**encoded_input)
        if type_out == "cls":
            return output[0][0, 0].cpu().numpy()
        elif type_out == "pooler":
            return output["pooler_output"][0].cpu().numpy()
        elif type_out == "tokens":
            sentence_embedding = mean_pooling(
                output, encoded_input['attention_mask']
            )
            return sentence_embedding.cpu().numpy()
        else:
            raise Exception("Unknown type out")
