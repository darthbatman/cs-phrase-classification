import numpy as np


def build_dataset():
    noun_phrase_concordance_scores = {}
    with open('data/noun_phrase_concordance_scores.csv', 'r') as f:
        line = f.readline()
        line = f.readline()[:-1]
        while line:
            components = line.split(',')
            if components[-1].strip():
                noun_phrase_concordance_scores[components[0]] = \
                    float(components[-1])
            line = f.readline()[:-1]
        f.close()
    mean = np.mean(list(noun_phrase_concordance_scores.values()))
    std = np.std(list(noun_phrase_concordance_scores.values()))
    for key in noun_phrase_concordance_scores:
        noun_phrase_concordance_scores[key] -= mean
        noun_phrase_concordance_scores[key] /= std
    noun_phrase_frequencies = {}
    with open('data/noun_phrase_frequencies.csv', 'r') as f:
        line = f.readline()
        line = f.readline()[:-1]
        while line:
            components = line.split(',')
            if components[-1].strip():
                noun_phrase_frequencies[components[0]] = \
                    float(components[-1])
            line = f.readline()[:-1]
        f.close()
    mean = np.mean(list(noun_phrase_frequencies.values()))
    std = np.std(list(noun_phrase_frequencies.values()))
    for key in noun_phrase_frequencies:
        noun_phrase_frequencies[key] -= mean
        noun_phrase_frequencies[key] /= std
    noun_phrase_uniquenesses = {}
    with open('data/noun_phrase_uniquenesses.csv', 'r') as f:
        line = f.readline()
        line = f.readline()[:-1]
        while line:
            components = line.split(',')
            if components[-1].strip():
                noun_phrase_uniquenesses[components[0]] = \
                    float(components[-1])
            line = f.readline()[:-1]
        f.close()
    mean = np.mean(list(noun_phrase_uniquenesses.values()))
    std = np.std(list(noun_phrase_uniquenesses.values()))
    for key in noun_phrase_uniquenesses:
        noun_phrase_uniquenesses[key] -= mean
        noun_phrase_uniquenesses[key] /= std
    noun_phrase_wiki_scores = {}
    with open('data/noun_phrase_wiki_scores.csv', 'r') as f:
        line = f.readline()
        line = f.readline()[:-1]
        while line:
            components = line.split(',')
            if components[-1].strip():
                noun_phrase_wiki_scores[components[0]] = \
                    float(components[-1])
            line = f.readline()[:-1]
        f.close()
    mean = np.mean(list(noun_phrase_wiki_scores.values()))
    std = np.std(list(noun_phrase_wiki_scores.values()))
    for key in noun_phrase_wiki_scores:
        noun_phrase_wiki_scores[key] -= mean
        noun_phrase_wiki_scores[key] /= std
    common_keys = set(noun_phrase_concordance_scores.keys()) \
        .intersection(set(noun_phrase_frequencies.keys())) \
        .intersection(set(noun_phrase_uniquenesses.keys())) \
        .intersection(set(noun_phrase_wiki_scores.keys()))
    data = []
    for key in common_keys:
        data.append((key,
                     noun_phrase_concordance_scores[key],
                     noun_phrase_frequencies[key],
                     noun_phrase_uniquenesses[key],
                     noun_phrase_wiki_scores[key]))
    return data


def get_hand_weighted_metric_ranking():
    dataset = build_dataset()
    ranked_phrases = {}
    for item in dataset:
        ranked_phrases[item[0]] = \
            0.1 * item[1] + \
            0.01 * item[2] + \
            0.4 * item[3] + \
            0.4 * item[4]
    ranked_phrases = {k: v for k, v in sorted(ranked_phrases.items(),
                                              key=lambda item: item[1],
                                              reverse=True)}
    print(ranked_phrases)


if __name__ == '__main__':
    get_hand_weighted_metric_ranking()
