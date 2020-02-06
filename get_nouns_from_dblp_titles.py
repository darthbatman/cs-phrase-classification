# NOTE: run with sudo

from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree
import sys

nlp = StanfordCoreNLP('data/stanford-corenlp-full-2018-10-05')


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


def get_nouns_from_dblp_titles(max_titles, max_words_in_noun_phrase):
    with open('data/dblp_nouns_' + str(max_titles) + '_titles_' +
              str(max_words_in_noun_phrase) + '_words.txt', 'w') as fw:
        with open('data/dblp_titles.txt', 'r') as fr:
            line = fr.readline()
            title_count = 0
            while line and title_count < max_titles:
                tree_str = nlp.parse(line)
                noun_phrases = extract_phrase(tree_str, 'NP')
                for noun_phrase in noun_phrases:
                    if not noun_phrase.isdigit() and \
                       len(noun_phrase) > 1 and \
                       ';' not in noun_phrase and \
                       '&' not in noun_phrase and \
                       '<' not in noun_phrase and \
                       '>' not in noun_phrase and \
                       len(noun_phrase.split(' ')) < max_words_in_noun_phrase:
                        fw.write(noun_phrase.replace(' .', '') + '\n')
                title_count += 1
                line = fr.readline()
            fr.close()
        fw.close()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        max_titles = int(sys.argv[1])
        max_words_in_noun_phrase = int(sys.argv[2])
        get_nouns_from_dblp_titles(max_titles, max_words_in_noun_phrase)
    else:
        get_nouns_from_dblp_titles(999999999, 999999999)
