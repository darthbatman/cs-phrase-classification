import nltk
from nltk.corpus import stopwords
import string


def get_concordance_score():
    all_concordances = {}
    with open('data/whoosh/phrase_concordances.csv', 'r') as rf:
        line = rf.readline()
        line = rf.readline()[:-1]
        while line:
            components = line.split(',')
            all_concordances[components[0]] = float(components[-1])
            line = rf.readline()[:-1]
        rf.close()
    with open('data/stanford-core-nlp/dblp_titles_noun_phrases.txt',
              'r') as rf:
        with open('data/noun_phrase_concordance_scores.csv', 'w') as wf:
            wf.write('phrase,concordance_score\n')
            line = rf.readline()[:-1].lower()
            while line:
                if line in all_concordances:
                    wf.write(line + ',' + str(all_concordances[line]) + '\n')
                line = rf.readline()[:-1].lower()
            wf.close()
        rf.close()


if __name__ == '__main__':
    get_concordance_score()
