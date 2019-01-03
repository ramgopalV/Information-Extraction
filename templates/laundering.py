import spacy
from templates.helpers import *


class laundering:
    def __init__(self, doc: spacy.tokens.doc.Doc, verb: spacy.tokens.token.Token):
        self.__doc = doc
        self.__verb = verb
        self.__is_passive = is_passive(doc)
        self.__nn_chunk = get_noun_chunks(doc)
        self.__ners = get_ners(doc)

        self.who = None
        self.when = None
        self.amount = None

        self.lst = ["who", "when", "amount"]

    def __str__(self):
        dic = {}
        for key in self.lst:
            dic[key] = self.__getattribute__(key)
        return self.__class__.__name__ + dic.__str__()

    def parse(self):
        # Parse for NSUBJ, who laundered
        for chunk in self.__nn_chunk:
            if 'nsubj' in chunk.root.dep_:
                self.who = chunk.text
                break
        if self.who is None:
            for ent in self.__ners:
                if 'nsubj' in ent.root.dep_:
                    self.who = ent.text
                    break

        if self.who is None:
            for child in self.__verb.children:
                nn_ch = ret_noun_chunk(self.__nn_chunk, child)
                if 'nsubj' == child.dep_.lower() and self.who is None:
                    if nn_ch is not None:
                        self.who = nn_ch.orth_
                    else:
                        self.who = child.text

        if self.who is None:
            root = None
            for token in self.__doc:
                if token.dep_.lower() == 'root':
                    root = token
                    break

            for child in root.children:
                nn_ch = ret_noun_chunk(self.__nn_chunk, child)
                if 'nsubj' == child.dep_.lower() and self.who is None:
                    if nn_ch is not None:
                        self.who = nn_ch.orth_
                    else:
                        self.who = child.text

        # When laundering happened
        extract_when(self, self.__ners, self.__verb)
        extract_amount(self, self.__ners, self.__verb)
