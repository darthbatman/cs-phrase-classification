def get_labeled_phrases():
    labeled_phrases = []
    with open('data/labeled_phrases.csv', 'r') as f:
        f.readline()
        line = f.readline()[:-1]
        while line:
            items = line.split(',')
            phrase = items[0]
            label = items[1]
            labeled_phrases.append((phrase, label))
            line = f.readline()[:-1]
        f.close()
    return labeled_phrases


def prefetch_frequencies(phrases):
    frequencies = {}
    phrases = set(phrases)
    with open('data/stanford-core-nlp/dblp_titles_noun_phrases.txt', 'r') as f:
        line = f.readline()[:-1].strip().lower()
        while line:
            if line in phrases:
                if line in frequencies:
                    frequencies[line] += 1
                else:
                    frequencies[line] = 1
            line = f.readline()[:-1].strip().lower()
        f.close()
    return frequencies


def get_frequency(phrase, frequencies):
    noun_frequencies = {}
    with open('data/stanford-core-nlp/dblp_titles_noun_phrases.txt', 'r') as f:
        line = f.readline()[:-1].strip().lower()
        while line:
            if line in noun_frequencies:
                noun_frequencies[line] += 1
            else:
                noun_frequencies[line] = 1
            line = f.readline()[:-1].strip().lower()
        f.close()
    with open('data/noun_phrase_frequencies.csv', 'w') as f:
        f.write('phrase,frequency\n')
        for key in noun_frequencies.keys():
            f.write(key + ',' + str(noun_frequencies[key]) + '\n')
        f.close()


def get_concordance_score(phrase):
    # TODO: complete implementation
    pass


def get_uniqueness(phrase):
    # TODO: complete implementation
    pass


def get_wiki_score(phrase):
    # TODO: complete implementation
    pass


def get_popularity(phrase):
    # TODO: complete implementation
    pass


def get_purity(phrase):
    # TODO: complete implementation
    pass


def get_suggested_query_score(phrase, suggested_queries):
    # TODO: complete implementation
    pass


def get_cs_context(phrase, suggested_queries):
    # TODO: complete implementation
    pass


def get_phrase_features(phrase, frequencies, suggested_queries):
    frequency = get_frequency(phrase, frequencies)
    concordance_score = get_concordance_score(phrase)
    uniqueness = get_uniqueness(phrase)
    wiki_score = get_wiki_score(phrase)
    # TODO: get popularity
    popularity = 0.0
    # TODO: get purity
    purity = 0.0
    suggested_query_score = get_suggested_query_score(phrase,
                                                      suggested_queries)
    cs_context = get_cs_context(phrase, suggested_queries)
    return [frequency, concordance_score, uniqueness, wiki_score,
            popularity, purity, suggested_query_score, cs_context]


def build_data_row(phrase, features, label):
    row_items = [phrase]
    row_items.extend(features)
    row_items.append(label)
    return ','.join(row_items) + '\n'


def build_dataset():
    labeled_phrases = get_labeled_phrases()

    phrases = []
    for labeled_phrase in labeled_phrases:
        phrases.append(labeled_phrase[0])
    frequencies = prefetch_frequencies(phrases)
    suggested_queries = prefetch_frequencies(phrases)

    with open('data/dataset.csv', 'w') as f:
        for labeled_phrase in labeled_phrases:
            phrase = labeled_phrase[0]
            label = labeled_phrase[1]
            features = get_phrase_features(phrase,
                                           frequencies,
                                           suggested_queries)
            data_row = build_data_row(phrase, features, label)
            f.write(data_row)
        f.close()

    # TODO: scale dataset features and write to file
    # IDEA: scale features individually (in each get_FEATURE function)


if __name__ == '__main__':
    build_dataset()
