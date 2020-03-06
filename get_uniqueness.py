import json


def get_uniqueness():
    common_word_uniquenesses = {}
    with open('data/google-trillion-words/most_common_words_20k.txt') as f:
        common_words = f.readlines()
    common_word_uniquenesses = {v.strip().lower():
                                (len(common_words) - i) / len(common_words)
                                for i, v in enumerate(common_words)}
    with open('data/stanford-core-nlp/dblp_titles_noun_phrases.txt',
              'r') as rf:
        with open('data/noun_phrase_uniquenesses.csv', 'w') as wf:
            wf.write('phrase,uniqueness\n')
            line = rf.readline().strip().lower()
            while line:
                phrase_word_count = 0
                total_uniqueness = 0
                for word in line.split(' '):
                    if len(word) > 0:
                        phrase_word_count += 1
                        if word in common_word_uniquenesses:
                            total_uniqueness += common_word_uniquenesses[word]
                        else:
                            total_uniqueness += 1
                wf.write(line + ',' +
                         str(total_uniqueness / phrase_word_count) + '\n')
                line = rf.readline().strip().lower()
            wf.close()
        rf.close()


if __name__ == '__main__':
    get_uniqueness()
