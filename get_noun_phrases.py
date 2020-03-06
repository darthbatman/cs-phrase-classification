from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree


def extract_phrase(tree_str, label):
    phrases = []
    trees = Tree.fromstring(tree_str)
    for tree in trees:
        for subtree in tree.subtrees():
            if subtree.label() == label:
                t = subtree
                t = ' '.join(t.leaves())
                phrases.append(t)
    return phrases


def get_noun_phrases():
    nlp = StanfordCoreNLP(
            'data/stanford-core-nlp/stanford-corenlp-full-2018-10-05')
    with open('data/stanford-core-nlp/dblp_titles_noun_phrases.txt',
              'w') as wf:
        with open('data/dblp-raw/dblp_titles.txt', 'r') as rf:
            line = rf.readline()
            while line:
                tree_str = nlp.parse(line)
                noun_phrases = extract_phrase(tree_str, 'NP')
                for noun_phrase in noun_phrases:
                    if not noun_phrase.isdigit() and \
                       len(noun_phrase) > 1 and \
                       ';' not in noun_phrase and \
                       '&' not in noun_phrase and \
                       '<' not in noun_phrase and \
                       '>' not in noun_phrase and \
                       len(noun_phrase.split(' ')) < 3:
                        wf.write(noun_phrase.replace(' .', '') + '\n')
                line = rf.readline()
            rf.close()
        wf.close()


if __name__ == '__main__':
    get_noun_phrases()
