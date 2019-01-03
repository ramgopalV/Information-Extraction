import spacy
from templates.helpers import *


class assault:
    def __init__(self, doc: spacy.tokens.doc.Doc, verb: spacy.tokens.token.Token):
        self.__doc = doc
        self.__verb = verb
        self.__is_passive = is_passive(doc)
        self.__nn_chunk = get_noun_chunks(doc)
        self.__ners = get_ners(doc)

        self.type = self.__verb.text
        self.who = None
        self.whom = None
        self.when = None
        self.where = None

        self.lst = ["type", "who", "whom", "when", "where"]

    def __str__(self):
        dic = {}
        for key in self.lst:
            dic[key] = self.__getattribute__(key)
        return self.__class__.__name__ + dic.__str__()

    def parse(self):
        # Passive Voice
        if self.__is_passive:
            # Who assaulted
            for ent in self.__ners:
                if ent.label_.lower() in ['person', 'org'] and 'obj' in ent.root.dep_ and self.who is None:
                    prev = ent.root.head
                    while not (prev.dep_.lower() == 'root') and not (prev.pos_.lower() == 'verb'): prev = prev.head
                    if prev == self.__verb:
                        self.who = ent.text

            # Who was assaulted
            for child in self.__verb.children:
                nn_ch = ret_noun_chunk(self.__nn_chunk, child)
                if 'nsubjpass' == child.dep_.lower() and self.whom is None:
                    if nn_ch is not None:
                        self.whom = nn_ch.orth_
                    elif 'propn' in child.pos_.lower():
                        self.whom = child.text

        # Active Voice
        else:
            # Who assaulted
            for child in self.__verb.children:
                nn_ch = ret_noun_chunk(self.__nn_chunk, child)
                # Parse Who gave sentence
                if 'nsubj' == child.dep_.lower() and self.who is None:
                    if nn_ch is not None:
                        self.who = nn_ch.orth_
                    elif 'propn' in child.pos_.lower():
                        self.who = child.text

                # Parse who was sentenced
                if 'obj' in child.dep_.lower() and self.whom is None:
                    if nn_ch is not None:
                        self.whom = nn_ch.orth_
                    elif 'propn' in child.pos_.lower():
                        self.whom = child.text

        # Extracting when and where with helper functions.
        extract_when(self, self.__ners, self.__verb)
        extract_where(self, self.__ners, self.__verb)
