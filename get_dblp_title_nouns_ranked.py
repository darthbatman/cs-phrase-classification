import json


def get_dblp_title_nouns_ranked():
    with open('data/gsl.txt') as f:
        general_words = f.readlines()
    general_words_scored = {v.strip().lower(): (len(general_words) - i)
                            for i, v in enumerate(general_words)}
    with open('data/awl.txt') as f:
        academic_words = f.readlines()
    academic_words_scored = {v.strip().lower(): (len(academic_words) - i)
                             for i, v in enumerate(academic_words)}
    words_ranked = {}
    count = 0
    with open('data/dblp_nouns_517756_titles_3_words.txt', 'r') as f1:
        line = f1.readline().strip().lower()
        while line:
            for word in line.split(' '):
                word = word.strip()
                if len(word) > 0:
                    if line not in words_ranked:
                        words_ranked[line] = 0
                    if word in general_words_scored:
                        words_ranked[line] -= general_words_scored[word]
                    if word in academic_words_scored:
                        words_ranked[line] -= \
                            int(0.5 * academic_words_scored[word])
                    count += 1
            line = f1.readline().strip().lower()
        f1.close()
    words_ranked = {k: v for k, v in sorted(words_ranked.items(), key=lambda
                                            item: item[1], reverse=True)}
    with open('data/dblp_title_nouns_ranked.json', 'w') as f:
        f.write(json.dumps(words_ranked, indent=4))
        f.close()


if __name__ == '__main__':
    get_dblp_title_nouns_ranked()
