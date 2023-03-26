from pattern.text.de import conjugate, PAST, PRESENT, SINGULAR, PLURAL
import spacy
from spacy.symbols import NOUN

SUBJ_DEPS = {'agent', 'csubj', 'csubjpass', 'expl', 'nsubj', 'nsubjpass'}
nlp = spacy.load("de_core_news_sm")

def _get_conjuncts(tok):
    """
    Return conjunct dependents of the leftmost conjunct in a coordinated phrase,
    e.g. "Burton, [Dan], and [Josh] ...".
    """
    return [right for right in tok.rights
            if right.dep_ == 'conj']

def get_subjects_of_verb(verb):
    print(verb.dep_, list(verb.ancestors))
    if verb.dep_ == "aux" and list(verb.ancestors):
        return get_subjects_of_verb(list(verb.ancestors)[0])
    """Return all subjects of a verb according to the dependency parse."""
    subjs = [tok for tok in verb.lefts
             if tok.dep_ in SUBJ_DEPS]
    # get additional conjunct subjects
    subjs.extend(tok for subj in subjs for tok in _get_conjuncts(subj))
    if not len(subjs):
        ancestors = list(verb.ancestors)
        if len(ancestors) > 0:
            return get_subjects_of_verb(ancestors[0])
    return subjs

def change_tense(sentence, tense):
    doc = nlp(sentence)
    verb_map = {"PRESENT": "PRÄS", "PAST": "PRT", "FUTURE": "FUT"}
    new_tokens = []
    for token in doc:
        if token.pos_ == "VERB":
            print(get_subjects_of_verb(token))
            if tense == "PAST":
                token_text = token.lemma_ + "te"
                # print(token_text)
            elif tense == "FUTURE":
                token_text = "werden " + token.lemma_
                # print(token_text)
            else:
                token_text = token.text
            token_text = token_text.capitalize() if token.i == 0 else token_text
            print(token_text)
            token.tag_ = token.tag_.split("|")[0] + "|" + verb_map[tense]
            new_token = spacy.tokens.Token(doc.vocab, doc, token.i)
            new_token.tag_ = token.tag_
            new_tokens.append(new_token)
        else:
            new_tokens.append(token)
    new_doc = spacy.tokens.Doc(doc.vocab, words=[t.text for t in new_tokens])
    # new_doc.is_tagged = True
    for i, token in enumerate(new_tokens):
        new_doc[i].tag_ = token.tag_
    return new_doc.text

if __name__ == "__main__":
    sentence = "Ich spiele Fußball."
    new_sentence = change_tense(sentence, "PAST")
    print(new_sentence)
