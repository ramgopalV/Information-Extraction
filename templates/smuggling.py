import spacy
from templates.helpers import *


class smuggling:
    def __init__(self, doc: spacy.tokens.doc.Doc, verb: spacy.tokens.token.Token):
        self.__doc = doc
        self.__verb = verb
        self.__is_passive = is_passive(doc)
        self.__nn_chunk = get_noun_chunks(doc)
        self.__ners = get_ners(doc)

        self.who = None
        self.what = None
        self.to_loc = None
        self.from_loc = None

        self.lst = ["what", "from_loc", "to_loc", "who"]

    def __str__(self):
        dic = {}
        for key in self.lst:
            dic[key] = self.__getattribute__(key)
        return self.__class__.__name__ + dic.__str__()

    def parse(self):

        for child in self.__verb.children:
            nn_ch = ret_noun_chunk(self.__nn_chunk, child)
            # Passive Voice
            if self.__is_passive:
                # Parse what is smuggled
                if 'nsubjpass' == child.dep_.lower() and self.what is None:
                    if nn_ch is not None:
                        self.what = nn_ch.orth_
                    elif 'propn' in child.pos_.lower():
                        self.what = child.text

                # Parse who smuggled
                if 'obj' not in child.dep_.lower():
                    for ch in child.children:
                        if 'obj' in ch.dep_.lower():
                            nn_child_ch = ret_noun_chunk(self.__nn_chunk, ch)
                            if nn_child_ch is not None:
                                self.who = nn_child_ch.orth_
                            else:
                                self.who = ch.text
                elif 'obj' in child.dep_.lower():
                    if nn_ch is not None:
                        self.who = nn_ch.orth_
                    else:
                        self.who = child.text

            # Active Voice
            else:
                # Who smuggled
                if 'nsubj' == child.dep_.lower() and self.who is None:
                    if nn_ch is not None:
                        self.who = nn_ch.orth_
                    else:
                        self.who = child.text

                # What was smuggled
                if 'dobj' == child.dep_.lower() and self.what is None:
                    if nn_ch is not None:
                        self.what = nn_ch.orth_
                    else:
                        self.what = child.text

            # look for attaching prep and its object....
            # look for verb attached (with prep or conj) and its subject....

        extract_from_loc(self, self.__ners, self.__verb)
        extract_to_loc(self, self.__ners, self.__verb)
