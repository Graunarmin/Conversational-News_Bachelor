import sys
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM


class BertPunctuation:
    """
    add punctuation to a text using BERT
    https://stackoverflow.com/questions/54978443/predicting-missing-words-in-a-sentence-natural-language-processing-model
    """

    def __init__(self):
        # Load pre-trained model tokenizer (vocabulary)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        # Load pre-trained model (weights)
        self.model = BertForMaskedLM.from_pretrained('bert-base-uncased')
        self.model.eval()

    def punctuate_text(self, string):
        tokenized_text = self.tokenizer.tokenize(string)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)

        segments_ids = [0] * len(tokenized_text)

        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensor = torch.tensor([segments_ids])

        with torch.no_grad():
            predictions = self.model(tokens_tensor, segments_tensor)

        masked_index = tokenized_text.index('[MASK]')
        predicted_index = torch.argmax(predictions[0][0][masked_index]).items()
        predicted_token = self.tokenizer.convert_ids_to_tokens([predicted_index])[0]
