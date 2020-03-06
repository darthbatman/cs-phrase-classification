import sys


def get_frequency():
    noun_frequencies = {}
    with open('data/stanford-core-nlp/dblp_titles_noun_phrases.txt', 'r') as f:
        line = f.readline()[:-1]
        while line:
            if line in noun_frequencies:
                noun_frequencies[line] += 1
            else:
                noun_frequencies[line] = 1
            line = f.readline()[:-1]
        f.close()
    with open('data/noun_phrase_frequencies.csv', 'w') as f:
        f.write('phrase,frequency\n')
        for key in noun_frequencies.keys():
            f.write(key + ',' + str(noun_frequencies[key]) + '\n')
        f.close()


if __name__ == '__main__':
    get_frequency()
