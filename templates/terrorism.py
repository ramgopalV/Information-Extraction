import spacy
from templates.helpers import *


class terrorism:
    def __init__(self, doc: spacy.tokens.doc.Doc, verb: spacy.tokens.token.Token):
        self.__doc = doc
        self.__verb = verb
        self.__is_passive = is_passive(doc)
        self.__nn_chunk = get_noun_chunks(doc)
        self.__ners = get_ners(doc)

        self.type = self.__verb.text
        self.org_Name = None
        self.event = None
        self.where = None
        self.when = None

        self.lst = ["org_Name", "event", "where", "when"]

    def __str__(self):
        dic = {}
        for key in self.lst:
            dic[key] = self.__getattribute__(key)
        return self.__class__.__name__ + dic.__str__()

    def parse(self):
        for ent in self.__ners:
            if ent.label_.lower() is 'org' and self.org_Name is None:
                # prev = ent.root.head
                # # while not (prev.dep_.lower() == 'root') and not (prev.pos_.lower() == 'verb'): prev = prev.head
                # # if prev == self.__verb:
                self.org_Name = ent.text

        self.event=self.__verb.text

        # Extracting when and where with helper functions.
        extract_when(self, self.__ners, self.__verb)
        extract_where(self, self.__ners, self.__verb)
