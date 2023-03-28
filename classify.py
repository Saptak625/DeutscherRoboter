import spacy

nlp = spacy.load("de_core_news_sm")

cases = ['present', 'simple_past', 'present_perfect', 'past_perfect', 'future']
for case in cases:
    with open(f'sentences/{case}.txt', 'r') as f:
        for i, line in enumerate(f):
            with open(f'results/{case}/{i}.txt', 'w') as g:
                doc = nlp(line)
                g.write(doc.text+'\n')
                for token in doc:
                    g.write(', '.join((token.text, token.pos_, token.dep_, token.tag_, '\n')))
                    g.write(', '.join((spacy.explain(token.pos_), spacy.explain(token.dep_), spacy.explain(token.tag_), '\n')))
                    g.write('\n')