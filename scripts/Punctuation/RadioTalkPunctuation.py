import json
import sys
import DeepSegmentPunctuation as dsp
import BertPunctuation as bp


# ---------------- STATIC FUNCTIONS --------------------
def create_text(snippet_list, delimiter):
    """
    merge the snippets together so they are one string without punctuation
    """
    text = ""
    for snippet_tuple in snippet_list:
        text += snippet_tuple[1]
        text += delimiter
    return text


def create_short_texts(snippet_list, delimiter, max_length):
    """
    merge the snippets to strings that don't contain more than max_length words
    returns a list of texts
    """
    current_length = 0
    texts = []
    text = ""
    for snippet_tuple in snippet_list:
        new_length = len(snippet_tuple[1].split(" "))
        if (current_length + new_length) <= max_length:
            current_length += new_length
            text += snippet_tuple[1]
            text += delimiter
        else:
            texts.append(text)
            current_length = new_length
            text = snippet_tuple[1]
            text += delimiter

    texts.append(text)
    return texts


def write_output(data, out_file):
    with open(out_file, 'w') as outfile:
        json.dump(data, outfile, indent=2)


# ---------------- CLASS --------------------
class RadioTalkPunctuation:

    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.read_json()
        self.bare_data = {}
        self.bare_out = "../data/punctuation/bare_punct.json"
        self.simple_data = {}
        self.simple_out = "../data/punctuation/simple_punct.json"
        self.deep_data = {}
        self.deep_out = "../data/punctuation/deep_punct.json"
        self.bert = bp.BertPunctuation()
        self.bert_data = {}
        self.bert_out = "../data/punctuation/bert_punct.json"

    def read_json(self):
        """
        read in the json file containing the test data
        """
        with open(self.data_file) as file:
            return json.load(file)

    def punctuate(self, no, simple, deep, bert):
        for show in self.data:
            if no:
                self.add_no_punctuation(show, self.data[show])
            if simple:
                self.add_punctuation_simple(show, self.data[show])
            if deep:
                self.add_punctuation_deepsegemnt(show, self.data[show])
            if bert:
                self.add_punctuation_bert(show, self.data[show])

        if no:
            write_output(self.bare_data, self.bare_out)
        if simple:
            write_output(self.simple_data, self.simple_out)
        if deep:
            write_output(self.deep_data, self.deep_out)
        if bert:
            write_output(self.bert_data, self.bert_out)

    def add_no_punctuation(self, show, content):
        """
        Create a text with only whitespaces so punctuation can be added manually
        """
        text = create_text(content, " ")
        self.bare_data[show] = text

    def add_punctuation_simple(self, show, content):
        """
        simply add a full-stop after each snippet
        """
        text = create_text(content, ". ")
        self.simple_data[show] = text

    def add_punctuation_deepsegemnt(self, show, content):
        """
        add punctuation using the deepsegment module
        """
        # first put all snippets together separated by a whitespace
        text = create_text(content, " ")
        # then add punctation using deepsegment
        punct = dsp.DeepSegmentPunctuation()
        self.deep_data[show] = punct.punctuate_text(text)

    def add_punctuation_bert(self, show, content):
        """
        add punctuation using the pre-trained BERT
        """
        punctuated_text = ""
        # first put snippets together separated by [MASK]
        # but not too many as BERT can't handle more than 512 tokens at once?
        texts = create_short_texts(content, " [MASK] ", 400)
        for text in texts:
            punctuated_text += self.bert.punctuate_text(text, '[MASK]')

        self.bert_data[show] = punctuated_text


# ---------------- MAIN --------------------
def main():
    """
    Argument 1: json file that holds the snippets without punctuation (../data/punctuation/test_data.json)
    Arguemnts 2 - 5 (none = all, combinations work, order does not matter)
    "n" for no punctuation
    "s" for simple punctuation
    "d" for deepsegment
    "b" for BERT
    """

    punctuation = RadioTalkPunctuation(sys.argv[1])
    process_input(sys.argv, punctuation)


def process_input(arg, punctuation):
    n = False
    s = False
    d = False
    b = False

    if len(arg) == 2:
        punctuation.punctuate(True, True, True, True)
    elif len(arg) > 2:
        if "n" in arg:
            n = True
        if "s" in arg:
            s = True
        if "d" in arg:
            d = True
        if "b" in arg:
            b = True
        punctuation.punctuate(n, s, d, b)


if __name__ == '__main__':
    main()
