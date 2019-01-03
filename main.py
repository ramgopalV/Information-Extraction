import spacy

from templates.assault import assault
from templates.sentenced import sentenced
from templates.robbery import robbery
from templates.smuggling import smuggling
from templates.laundering import laundering
from templates.bankruptcy import bankruptcy
from templates.penalty import penalty
from templates.terrorism import terrorism
from templates.suspect import suspect
from templates.victim import victim

cls = spacy.util.get_lang_class('en')
nlp = cls()

component = nlp.create_pipe('tagger')
nlp.add_pipe(component)
component = nlp.create_pipe('parser')
nlp.add_pipe(component)
component = nlp.create_pipe('ner')
nlp.add_pipe(component)

nlp.from_disk(r"E:\Anaconda3\lib\site-packages\spacy\data\en_core_web_lg\en_core_web_lg-2.0.0")

templates = [("sentenced", "sentenced"), ("robbery", "robbed"), ("assault", "assaulted"),
             ("laundering", "laundering"), ("smuggling", "smuggled"), ("penalty", "fined"),
             ("bankruptcy", "bankruptcy"), ("suspect", "suspect"), ("terrorism", "terrorism"),
             ("victim", "victim")]

texts = [input("Enter the sentence: ")]

for text in texts:
    doc = nlp(text)
    template_score = {}

    for temp in templates:
        sim = 0
        for token in doc:
            if token.pos_.lower() in ["verb", "noun"]:
                sim = max(token.similarity(nlp(temp[1])), sim)
        template_score[temp] = sim
    matching_temp = [key for key in template_score.keys()
                     if template_score[key] == max(template_score.values())][0]

    sim_scores = {}
    for token in doc:
        if token.pos_.lower() in ["verb"]:
            sim_scores[token] = token.similarity(nlp(matching_temp[1]))
    verb = [key for key in sim_scores.keys()
            if sim_scores[key] == max(sim_scores.values())][0]

    template = None
    if "sentenced" == matching_temp[0]:
        template = sentenced(doc, verb)
    elif "robbery" == matching_temp[0]:
        template = robbery(doc, verb)
    elif "laundering" == matching_temp[0]:
        template = laundering(doc, verb)
    elif "smuggling" == matching_temp[0]:
        template = smuggling(doc, verb)
    elif "penalty" == matching_temp[0]:
        template = penalty(doc, verb)
    elif "suspect" == matching_temp[0]:
        template = suspect(doc, verb, nlp)
    elif "victim" == matching_temp[0]:
        template = victim(doc, verb, nlp)
    elif "bankruptcy" == matching_temp[0]:
        template = bankruptcy(doc, verb)
    elif "terrorism" == matching_temp[0]:
        template = terrorism(doc, verb)
    else:
        template = assault(doc, verb)

    template.parse()
    print(template)
