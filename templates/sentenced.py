import spacy
from templates.helpers import *


class sentenced:
    def __init__(self, doc: spacy.tokens.doc.Doc, verb: spacy.tokens.token.Token):
        self.__doc = doc
        self.__verb = verb
        self.__is_passive = is_passive(doc)
        self.__nn_chunk = get_noun_chunks(doc)
        self.__ners = get_ners(doc)

        self.who = None
        self.who_gave = None
        self.when = None
        self.where = None
        self.duration = None

        self.lst = ["who", "when", "where", "who_gave", "duration"]

    def __str__(self):
        dic = {}
        for key in self.lst:
            dic[key] = self.__getattribute__(key)
        return self.__class__.__name__ + dic.__str__()

    def parse(self):
        # Passive Voice
        if self.__is_passive:
            for child in self.__verb.children:
                nn_ch = ret_noun_chunk(self.__nn_chunk, child)
                # Parse Who gave sentence
                if 'agent' == child.dep_.lower() and self.who_gave is None:
                    for ch in child.children:
                        if 'obj' in ch.dep_.lower():
                            nn_child_ch = ret_noun_chunk(self.__nn_chunk, ch)
                            if nn_child_ch is not None:
                                self.who_gave = nn_child_ch.orth_
                            else:
                                self.who_gave = ch.text

                # Parse Who was sentenced
                if 'nsubjpass' == child.dep_.lower() and self.who is None:
                    if nn_ch is not None:
                        self.who = nn_ch.orth_
                    elif 'propn' in child.pos_.lower():
                        self.who = child.text

        # Active Voice
        else:
            for child in self.__verb.children:
                nn_ch = ret_noun_chunk(self.__nn_chunk, child)
                # Parse Who gave sentence
                if 'nsubj' == child.dep_.lower() and self.who_gave is None:
                    if nn_ch is not None:
                        self.who_gave = nn_ch.orth_
                    elif 'propn' in child.pos_.lower():
                        self.who_gave = child.text

                # Parse who was sentenced
                if 'dobj' == child.dep_.lower() and self.who is None:
                    if nn_ch is not None:
                        self.who = nn_ch.orth_
                    elif 'propn' in child.pos_.lower():
                        self.who = child.text

        # Extracting when and where with helper functions.
        extract_when(self, self.__ners, self.__verb)
        extract_where(self, self.__ners, self.__verb)

        for ent in self.__ners:
            if 'date' in ent.label_.lower():
                prev = ent.root.head
                while not (prev.dep_.lower() == 'root') and not (prev.pos_.lower() == 'verb'): prev = prev.head
                if prev == self.__verb:
                    if (not ('year-old' in ent.text or 'years-old' in ent.text)) and self.duration is None:
                        self.duration = ent.text
