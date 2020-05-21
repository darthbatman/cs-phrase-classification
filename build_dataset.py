import requests
import wikipedia
import wikipediaapi


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
    if phrase in frequencies:
        return frequencies[phrase]
    return 0


def prefetch_concordance_scores(phrases):
    concordance_scores = {}
    phrases = set(phrases)
    with open('data/whoosh/phrase_concordances.csv', 'r') as f:
        f.readline()
        line = f.readline()[:-1].strip().lower()
        while line:
            items = line.split(',')
            phrase = items[0]
            concordance_score = float(items[-1])
            if phrase in phrases:
                concordance_scores[phrase] = concordance_score
            line = f.readline()[:-1].strip().lower()
        f.close()
    return concordance_scores


def get_concordance_score(phrase, concordance_scores):
    if phrase in concordance_scores:
        return concordance_scores[phrase]
    return 0.0


def prefetch_uniquenesses(phrases):
    uniquenesses = {}
    phrases = set(phrases)
    with open('data/noun_phrase_uniquenesses.csv', 'r') as f:
        f.readline()
        line = f.readline()[:-1].strip().lower()
        while line:
            items = line.split(',')
            phrase = items[0]
            uniqueness = float(items[-1])
            if phrase in phrases:
                uniquenesses[phrase] = uniqueness
            line = f.readline()[:-1].strip().lower()
    return uniquenesses


def get_uniqueness(phrase, uniquenesses):
    if phrase in uniquenesses:
        return uniquenesses[phrase]
    return 1.0


# Adapted from: https://github.com/harrywsh/phrase-detection
def prefetch_cs_categories():
    cs_categories = set()
    with open('data/harrywsh-phrase-detection/cs_categories.txt', 'r') as f:
        for line in f:
            cs_categories.add(line[:-1])
    return cs_categories


# Adapted from: https://github.com/harrywsh/phrase-detection
def get_wiki_score(phrase, cs_categories):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    num_results = 20
    relevant_pages = set()
    for suggested_page in wikipedia.search(phrase, results=num_results,
                                           suggestion=False):
        for word in wiki_wiki.page(suggested_page).categories:
            word = word[9:]
            if word in cs_categories:
                relevant_pages.add(suggested_page)
                break
    return (len(relevant_pages) / num_results)


def get_popularity(phrase):
    # TODO: complete implementation
    pass


def get_purity(phrase):
    # TODO: complete implementation
    pass


def get_suggested_queries(phrase):
    url = 'http://suggestqueries.google.com/complete/search?client=firefox&q='
    formatted_query = phrase.replace(' ', '+')
    res = requests.get(url + formatted_query)
    return res.text.split('[')[2][:-2].replace('"', '').split(',')


def prefetch_suggested_queries(phrases):
    suggested_queries = {}
    for phrase in phrases:
        suggestions = get_suggested_queries(phrase)
        suggested_queries[phrase] = suggestions
    return suggested_queries


def get_suggested_query_score(phrase, suggested_queries):
    if phrase not in suggested_queries:
        return 0.0

    suggested_queries = suggested_queries[phrase]

    cs_desribers = ['computer science', 'python', 'machine learning',
                    'artificial intelligence', 'ai', 'deep learning',
                    'algorithms', 'code', 'architecture', 'api',
                    'software', 'framework', 'computer security',
                    'computer system', 'computer systems']

    prefix_count = 0
    describer_score = 0
    for query in suggested_queries:
        if query[:len(phrase)] != phrase and \
           query[:len(phrase)] != phrase.replace('-', ''):
            prefix_count += 1
        for cs_desriber in cs_desribers:
            if ' ' + cs_desriber in query[len(phrase):] or ' ' + \
               cs_desriber + ' ' in query[len(phrase):] or ' ' + \
               cs_desriber + 's' in query[len(phrase):]:
                describer_score += len(cs_desribers) - \
                    cs_desribers.index(cs_desriber)
    return (describer_score / len(suggested_queries)) - \
        (prefix_count / len(suggested_queries))


def get_cs_context(phrase, suggested_queries):
    if phrase in suggested_queries:
        context = []
        cs_desribers = ['computer science', 'python', 'machine learning',
                        'artificial intelligence', 'ai', 'deep learning',
                        'algorithms', 'code', 'architecture', 'api',
                        'software', 'framework', 'computer security',
                        'computer system', 'computer systems']
        suggested_queries = suggested_queries[phrase]
        for query in suggested_queries:
            for cs_desriber in cs_desribers:
                if ' ' + cs_desriber in query[len(phrase):] or ' ' + \
                   cs_desriber + ' ' in query[len(phrase):] or ' ' + \
                   cs_desriber + 's' in query[len(phrase):]:
                    context.append(cs_desriber)
        return context
    return []


def get_phrase_features(phrase, frequencies, concordance_scores,
                        uniquenesses, cs_categories, suggested_queries):
    frequency = get_frequency(phrase, frequencies)
    concordance_score = get_concordance_score(phrase, concordance_scores)
    uniqueness = get_uniqueness(phrase, uniquenesses)
    wiki_score = get_wiki_score(phrase, cs_categories)
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
    return ','.join([str(row_item) for row_item in row_items]) + '\n'


def build_dataset():
    cs_categories = prefetch_cs_categories()

    labeled_phrases = get_labeled_phrases()

    phrases = []
    for labeled_phrase in labeled_phrases:
        phrases.append(labeled_phrase[0])
    frequencies = prefetch_frequencies(phrases)
    concordance_scores = prefetch_concordance_scores(phrases)
    uniquenesses = prefetch_uniquenesses(phrases)
    suggested_queries = prefetch_suggested_queries(phrases)

    with open('data/dataset.csv', 'w') as f:
        features = ['frequency', 'concordance_score', 'uniqueness',
                    'wiki_score', 'popularity', 'purity',
                    'suggested_query_score', 'cs_context']
        f.write(build_data_row('phrase', features, 'label'))
        for labeled_phrase in labeled_phrases:
            phrase = labeled_phrase[0]
            label = labeled_phrase[1]
            features = get_phrase_features(phrase,
                                           frequencies,
                                           concordance_scores,
                                           uniquenesses,
                                           cs_categories,
                                           suggested_queries)
            data_row = build_data_row(phrase, features, label)
            f.write(data_row)
        f.close()


if __name__ == '__main__':
    build_dataset()