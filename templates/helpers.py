def is_passive(doc):
    for token in doc:
        if ('pass' in token.dep_):
            return True
    return False


def get_noun_chunks(doc):
    nn_chunk = []
    for chunk in doc.noun_chunks:
        nn_chunk.append(chunk)
    return nn_chunk


def get_ners(doc):
    ners = []
    for ent in doc.ents:
        ners.append(ent)
    return ners


def ret_noun_chunk(chunks, token):
    for ch in chunks:
        if token.text in ch.orth_:
            return ch
    return None


def extract_when(template, ners, verb):
    for ent in ners:
        if ent.label_.lower() in ['date', 'time']:
            if ent.root.head.text.lower() in ['in', 'on', 'since'] and template.when is None:
                prev = ent.root.head
                while not (prev.dep_.lower() == 'root') and not (prev.pos_.lower() == 'verb'): prev = prev.head
                # if prev == verb:
                template.when = ent.text
                return


def extract_where(template, ners, verb):
    for ent in ners:
        # and ent.root.head.pos_.lower() == 'adp'
        if ent.label_.lower() in ['gpe', 'loc'] and template.where is None:
            prev = ent.root.head
            while not (prev.dep_.lower() == 'root') and not (prev.pos_.lower() == 'verb'): prev = prev.head
            # if prev == verb:
            template.where = ent.text
            return


def extract_to_loc(template, ners, verb):
    for ent in ners:
        if ent.label_.lower() in ['gpe', 'loc'] and \
                ent.root.head.text.lower() in ['to', 'into'] and \
                template.to_loc is None:
            template.to_loc = ent.text
            return


def extract_from_loc(template, ners, verb):
    for ent in ners:
        if ent.label_.lower() in ['gpe', 'loc'] and \
                ent.root.head.text.lower() in ['from'] and \
                template.from_loc is None:
            template.from_loc = ent.text
            return


def extract_amount(template, ners, verb):
    if template.amount is None:
        for ent in ners:
            if 'money' in ent.label_.lower():
                prev = ent.root.head
                while not (prev.dep_.lower() == 'root') and not (prev.pos_.lower() == 'verb'): prev = prev.head
                # if prev == verb:
                template.amount = ent.text
                return
