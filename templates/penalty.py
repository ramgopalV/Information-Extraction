import spacy
from templates.helpers import *


class penalty:
    def __init__(self, doc: spacy.tokens.doc.Doc, verb: spacy.tokens.token.Token):
        self.__doc = doc
        self.__verb = verb
        self.__is_passive = is_passive(doc)
        self.__nn_chunk = get_noun_chunks(doc)
        self.__ners = get_ners(doc)

        self.who_was_fined = None
        self.who_fined = None
        self.amount = None
        self.reason = None

        self.lst = ["who_was_fined", "who_fined", "amount", "reason"]

    def __str__(self):
        dic = {}
        for key in self.lst:
            dic[key] = self.__getattribute__(key)
        return self.__class__.__name__ + dic.__str__()

    def parse(self):

        for child in self.__verb.children:
            nn_ch = ret_noun_chunk(self.__nn_chunk, child)
            # Passive Voice
            if not self.__is_passive:
                if 'nsubj' == child.dep_.lower() and self.who_was_fined is None:
                    if nn_ch is not None:
                        self.who_was_fined = nn_ch.orth_
                    else:
                        self.who_was_fined = child.text

                if 'agent' == child.dep_.lower() and self.who_fined is None:
                    for ch in child.children:
                        if 'obj' in ch.dep_.lower():
                            nn_child_ch = ret_noun_chunk(self.__nn_chunk, ch)
                            if nn_child_ch is not None:
                                self.who_fined = nn_child_ch.orth_
                            else:
                                self.who_fined = ch.text

            # Active Voice
            else:
                if 'obj' in child.dep_.lower() and self.who_was_fined is None:
                    if nn_ch is not None:
                        self.who_was_fined = nn_ch.orth_
                    else:
                        self.who_was_fined = child.text

                if 'nsubj' in child.dep_.lower() and self.who_fined is None:
                    if nn_ch is not None:
                        self.who_fined = nn_ch.orth_
                    else:
                        self.who_fined = child.text

            # look for attaching prep and its object....
            # look for verb attached (with prep or conj) and its subject....

        for child in self.__verb.children:
            if child.dep_.lower() in ['prep'] and self.reason is None:
                for ch in child.children:
                    if 'obj' in ch.dep_.lower():
                        self.reason = ch.text

        extract_amount(self, self.__ners, self.__verb)
