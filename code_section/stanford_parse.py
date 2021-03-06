# '''
# A sample code usage of the python package stanfordcorenlp to access a Stanford CoreNLP server.
# Written as part of the blog post: https://www.khalidalnajjar.com/how-to-setup-and-use-stanford-corenlp-server-with-python/
# '''
from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import re

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))

    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                'word': token['word'],
                'lemma': token['lemma'],
                'pos': token['pos'],
                'ner': token['ner']
            }
        return tokens

if __name__ == '__main__':
    sNLP = StanfordNLP()
    text = "Delicious old school bar/restaurant. Love the ornate woodwork and white tablecloths. Service was absolutely excellent. I had the pot roast with the red skinned mashed potatoes and cole slaw. The meat was so tender and flavorful, and the potatoes...yum! The Cole slaw was delicious too, and I'm VERY picky about Cole slaw."

    # text = re.sub(r'[^\w\s]', '', text)
    print(text)
    print ("Annotate:", sNLP.annotate(text))
    print ("POS:", sNLP.pos(text))
    print ("Tokens:", sNLP.word_tokenize(text))
    print ("NER:", sNLP.ner(text))
    print ("Parse:", sNLP.parse(text))
    a = sNLP.dependency_parse(text)
    print ("Dep Parse:", sNLP.dependency_parse(text))