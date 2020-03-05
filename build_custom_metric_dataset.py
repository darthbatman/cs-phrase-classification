import random


def get_auto_phrase_results():
    results = {}
    with open('data/auto_phrase_noun_phrases.txt', 'r') as f:
        line = f.readline()[:-1]
        while line:
            line_parts = line.split('\t')
            phrase = line_parts[1]
            score = float(line_parts[0])
            if score >= 0.9:
                score = 1
            else:
                score = 0
            results[phrase] = score
            line = f.readline()[:-1]
        f.close()
    return results


def get_wiki_scored_results():
    results = {}
    with open('data/wiki_scored_phrases.txt', 'r') as f:
        line = f.readline()
        line = f.readline()[:-1]
        while line:
            results[line.split(',')[0]] = \
                float(line.split(',')[1])
            line = f.readline()[:-1]
        f.close()
    return results


def add_freq_and_custom_scored_results(auto_phrase_results):
    results = []
    with open('data/dblp_noun_frequencies.csv', 'r') as f:
        line = f.readline()
        line = f.readline()[:-1]
        while line:
            phrase = line.split(',')[0]
            if phrase not in auto_phrase_results:
                results.append((phrase,
                                float(line.split(',')[1]) / 517756,
                                float(line.split(',')[2]),
                                0))
            else:
                results.append((phrase,
                                float(line.split(',')[1]) / 517756,
                                float(line.split(',')[2]),
                                auto_phrase_results[phrase]))
            line = f.readline()[:-1]
        f.close()
    return results


def aggregate_data(frequency_and_custom_scored_results,
                   wiki_scored_results):
    data = []
    num_zero_scores = 100
    random.shuffle(frequency_and_custom_scored_results)
    for scored_phrase in frequency_and_custom_scored_results:
        wiki_score = 0.45
        if scored_phrase[0] in wiki_scored_results:
            wiki_score = wiki_scored_results[scored_phrase[0]]
        if scored_phrase[3] == 1:
            row = ','.join([str(i) for i in list(scored_phrase)]) + '\n'
            data.append(row)
        elif num_zero_scores >= 0:
            num_zero_scores -= 1
            row = ','.join([str(i) for i in list(scored_phrase)]) + '\n'
            data.append(row)
    return data


def write_dataset_to_file(dataset, filename):
    with open(filename, 'w') as f:
        f.write('phrase,frequency,wiki_score,label\n')
        for row in dataset:
            f.write(row)
        f.close()


def build_dataset():
    auto_phrase_results = get_auto_phrase_results()
    frequency_and_custom_scored_results = \
        add_freq_and_custom_scored_results(auto_phrase_results)
    wiki_scored_results = get_wiki_scored_results()
    dataset = aggregate_data(frequency_and_custom_scored_results,
                             wiki_scored_results)
    write_dataset_to_file(dataset, 'data/custom_metric_dataset.csv')


if __name__ == '__main__':
    build_dataset()
