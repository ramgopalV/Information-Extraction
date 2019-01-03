import spacy
from templates.helpers import *


class bankruptcy:
    def __init__(self, doc: spacy.tokens.doc.Doc, verb: spacy.tokens.token.Token):
        self.__doc = doc
        self.__verb = verb

        if verb.pos_.lower() == 'noun':
            prev = verb
            while(prev.dep_.lower() not in ['root','verb']): prev = prev.head
            self.__verb = prev

        self.__is_passive = is_passive(doc)
        self.__nn_chunk = get_noun_chunks(doc)
        self.__ners = get_ners(doc)

        print(self.__nn_chunk)
        print(self.__ners)

        self.company = None
        self.amount = None
        self.when = None
        self.who_bailed = None

        self.lst = ["company", "amount", "when", "who_bailed"]

    def __str__(self):
        dic = {}
        for key in self.lst:
            dic[key] = self.__getattribute__(key)
        return self.__class__.__name__ + dic.__str__()

    def parse(self):

        for child in self.__verb.children:
            nn_ch = ret_noun_chunk(self.__nn_chunk, child)
            #if bailed is present
            if 'bailed' in self.__verb.text.lower():
                # Parse Who robbed
                if self.__is_passive:

                    if 'agent'==child.dep_.lower() and self.who_bailed is None:
                        for ch in child.children:
                            if 'obj' in ch.dep_.lower():
                                nn_child_ch = ret_noun_chunk(self.__nn_chunk, ch)
                                if nn_child_ch is not None:
                                    self.who_bailed = nn_child_ch.orth_
                                else:
                                    self.who_bailed = ch.text

                    if 'nsubjpass'==child.dep_.lower() and self.company is None:
                        self.company=child.text


                else:

                    if 'obj' in child.dep_.lower():
                        self.company=child.text

                    if 'nsubj'==child.dep_.lower() and self.who_bailed is None:
                        self.who_bailed=child.text


            #if bankrupted is there
            else:
                if self.__is_passive:
                    if 'agent'==child.dep_.lower() and self.company is None:
                        for ch in child.children:
                            if 'obj' in ch.dep_.lower():
                                nn_child_ch = ret_noun_chunk(self.__nn_chunk, ch)
                                if nn_child_ch is not None:
                                    self.company = nn_child_ch.orth_
                                else:
                                    self.company = ch.text

                else:
                    if 'nsubj'==child.dep_.lower() and self.company is None:
                        self.company=child.text


        extract_amount(self, self.__ners, self.__verb)
        extract_when(self, self.__ners, self.__verb)
