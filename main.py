import spacy

nlp = spacy.load("de_core_news_sm")

def recognize_case(sentence):
    doc = nlp(sentence)
    verbs = []
    for token in doc:
        if token.dep_ == "ROOT":
            print('Main Verb', token.text, token.tag_)
            print(spacy.explain(token.dep_), spacy.explain(token.tag_))
            verbs.append(token)
        elif token.dep_ == "oc":
            print('Other Verb', token.text, token.tag_)
            print(spacy.explain(token.dep_), spacy.explain(token.tag_))
            verbs.append(token)
    if len(verbs) == 1:
        # Only one verb in the sentence.
        return 'present', 'simple_past'
    elif len(verbs) == 2:
        if verbs[-1].tag_ == 'VVINF': 
            # Infinitive verb.
            return 'future'
        elif verbs[-1].tag_ == 'VVPP':
            # Either past perfect or present perfect.
            if verbs[0].lemma_ in ['sein', 'haben']:
                return 'present_perfect'
            else:
                return 'past_perfect'
    return None

if __name__ == "__main__":
    sentence_case = recognize_case("Sie hatte gut gespielt.")
    print(sentence_case)
