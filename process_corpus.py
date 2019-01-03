import spacy
from nltk.corpus import wordnet as wn

model_path = r"E:\Anaconda3\lib\site-packages\spacy\data\en_core_web_lg\en_core_web_lg-2.0.0"

template_list = [('Sentenced', 0), ('Robbery', 0), ('Assault', 4), ('Smuggling', 0),
                 ('Money_laundering', 0), ('Penalty', 1), ('Suspect', 0), ('Victim', 1),
                 ('Terrorism', 0), ('Bankruptcy', 1)]

cls = spacy.util.get_lang_class('en')
nlp = cls()

component = nlp.create_pipe('tagger')
nlp.add_pipe(component)
component = nlp.create_pipe('parser')
nlp.add_pipe(component)

print("Importing SpaCy Model.")
nlp.from_disk(model_path)

print("Starting with Task 3...\nWriting to Files under results folder...")

with open('corpus.txt', 'r', encoding="utf8") as corp, \
        open('results/corpus_tokenize.txt', 'w') as corp_token, \
        open('results/corpus_lemma.txt', 'w') as corp_lemma, \
        open('results/corpus_pos.txt', 'w') as corp_pos, \
        open('results/corpus_depTree.txt', 'w') as corp_dep:
    for text in corp.readlines():
        if len(text) == 0:
            continue

        doc = nlp(text)

        corp_token.write(", ".join([t.text for t in doc]))
        corp_token.write('\n')

        corp_lemma.write(", ".join([t.lemma_ for t in doc]))
        corp_lemma.write('\n')

        corp_pos.write(", ".join([t.text + '/' + t.tag_ for t in doc]))
        corp_pos.write('\n')

        corp_dep.write(", ".join([t.head.text + "--" + t.dep_ + "->" + t.text for t in doc]))
        corp_dep.write('\n')

with open('results/templates_name_wordnet.txt', 'w') as word_net_file:
    for template in template_list:
        word = wn.synsets(template[0])[template[1]]
        word_net_file.write(template[0] + ": " + {'hypernyms': word.hypernyms(),
                                                  'hyponyms': word.hyponyms(),
                                                  'member_meronyms': word.member_meronyms(),
                                                  'member_holonyms': word.member_holonyms()}.__str__())
        word_net_file.write('\n')
print("Completed writing to File...\nTask 4 completed.")