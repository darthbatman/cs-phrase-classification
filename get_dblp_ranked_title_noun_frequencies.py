import json
import sys


def get_dblp_ranked_title_noun_frequencies():
    noun_frequencies = {}
    with open('data/dblp_nouns_517756_titles_3_words.txt', 'r') as f:
        line = f.readline()[:-1]
        while line:
            line = line.strip().lower()
            if line in noun_frequencies:
                noun_frequencies[line] += 1
            else:
                noun_frequencies[line] = 1
            line = f.readline()[:-1]
        f.close()
    with open('data/dblp_title_nouns_ranked.json', 'r') as f:
        ranked_nouns = json.load(f)
    noun_frequencies = {k: v for k, v in sorted(noun_frequencies.items(),
                        key=lambda item:
                        (0.5 * item[1] + 0.0005 * ranked_nouns[item[0]]),
                        reverse=True)}
    with open('data/dblp_noun_frequencies.csv', 'w') as f:
        f.write('noun_phrase,frequency,score\n')
        for key in noun_frequencies.keys():
            if noun_frequencies[key] > 1:
                f.write(key + ',' + str(noun_frequencies[key]) + ',' +
                        str(ranked_nouns[key]) + '\n')
        f.close()


if __name__ == '__main__':
    get_dblp_ranked_title_noun_frequencies()
