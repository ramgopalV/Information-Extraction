import spacy
from templates.helpers import *


class suspect:
    def __init__(self, doc: spacy.tokens.doc.Doc, verb: spacy.tokens.token.Token, nlp):
        self.__doc = doc
        self.__verb = verb
        self.__nlp = nlp
        self.__is_passive = is_passive(doc)
        self.__nn_chunk = get_noun_chunks(doc)
        self.__ners = get_ners(doc)

        self.Name = None
        self.age = None
        self.activity = self.__verb.text

        self.lst = ["Name", "age", "activity"]

    def __str__(self):
        dic = {}
        for key in self.lst:
            dic[key] = self.__getattribute__(key)
        return self.__class__.__name__ + dic.__str__()

    def parse(self):
        for ent in self.__doc.ents:
            if ent.label_.lower() == 'person' and self.Name is None:
                prev = ent.root
                while prev.dep_.lower() != 'root':
                    if prev.head.dep_.lower() == 'verb' and \
                            prev.head.similarity(self.__nlp('suspect')[0]) > 0.5:
                        self.Name = ent.text
                    prev = prev.head

            if ('year-old' in ent.text or ent.label_.lower() in ['date', 'time']) \
                    and 'day' not in ent.text and ' a.m' not in ent.text and ' p.m' not in ent.text\
                    and self.age is None:
                self.age = ent.text

        # Extracting when and where with helper functions.
        # extract_when(self, self.__ners, self.__verb)
        # extract_where(self, self.__ners, self.__verb)
