import numpy as np


def scale_to_range(l):
    # Source: https://stackoverflow.com/questions/1735025/how-to-normalize-a-numpy-array-to-within-a-certain-range
    return 2 * (l - np.min(l)) / np.ptp(l) - 1


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
    scaled_values = scale_to_range(list(noun_phrase_concordance_scores.values()))
    idx = 0
    for key in noun_phrase_concordance_scores:
        noun_phrase_concordance_scores[key] = scaled_values[idx]
        idx += 1
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
    scaled_values = scale_to_range(list(noun_phrase_frequencies.values()))
    idx = 0
    for key in noun_phrase_frequencies:
        noun_phrase_frequencies[key] = scaled_values[idx]
        idx += 1
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
    scaled_values = scale_to_range(list(noun_phrase_uniquenesses.values()))
    idx = 0
    for key in noun_phrase_uniquenesses:
        noun_phrase_uniquenesses[key] = scaled_values[idx]
        idx += 1
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
    scaled_values = scale_to_range(list(noun_phrase_wiki_scores.values()))
    idx = 0
    for key in noun_phrase_wiki_scores:
        noun_phrase_wiki_scores[key] = scaled_values[idx]
        idx += 1
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
    weights = [0.20, 0.05, 0.25, 0.5]
    for item in dataset:
        ranked_phrases[item[0]] = (
                weights[0] * item[1] +
                weights[1] * item[2] +
                weights[2] * item[3] +
                weights[3] * item[4],
                item[1], item[2], item[3], item[4])
    ranked_phrases = {k: v for k, v in sorted(ranked_phrases.items(),
                                              key=lambda item: item[1],
                                              reverse=True)}
    weights = [str(weight) for weight in weights]
    with open('ranked_' + '_'.join(weights) + '.csv', 'w') as f:
        features = ['concordance_score', 'frequency',
                    'uniqueness', 'wiki_score']
        f.write('phrase,' + ','.join(features) + ',total\n')
        for phrase in ranked_phrases:
            f.write(phrase + ',')
            f.write(str(ranked_phrases[phrase][1]) + ',')
            f.write(str(ranked_phrases[phrase][2]) + ',')
            f.write(str(ranked_phrases[phrase][3]) + ',')
            f.write(str(ranked_phrases[phrase][4]) + ',')
            f.write(str(ranked_phrases[phrase][0]) + '\n')
        f.close()


if __name__ == '__main__':
    get_hand_weighted_metric_ranking()
