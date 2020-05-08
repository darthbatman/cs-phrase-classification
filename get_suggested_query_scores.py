import requests


def get_suggested_queries(query):
    url = 'http://suggestqueries.google.com/complete/search?client=firefox&q='
    formatted_query = query.replace(' ', '+')
    res = requests.get(url + formatted_query)
    return res.text.split('[')[2][:-2].replace('"', '').split(',')


def get_suggested_query_score(phrase):
    suggested_queries = get_suggested_queries(phrase)

    cs_desribers = ['computer science', 'python', 'machine learning',
                    'artificial intelligence', 'ai', 'deep learning',
                    'algorithms', 'code', 'architecture', 'api',
                    'software', 'framework', 'computer security',
                    'computer system', 'computer systems']

    prefix_count = 0
    describer_score = 0
    for query in suggested_queries:
        if query[:len(phrase)] != phrase and query[:len(phrase)] != phrase.replace('-', ''):
            prefix_count += 1
        for cs_desriber in cs_desribers:
            if ' ' + cs_desriber in query[len(phrase):] or ' ' + cs_desriber + ' ' in query[len(phrase):] or ' ' + cs_desriber + 's' in query[len(phrase):]:
                describer_score += len(cs_desribers) - cs_desribers.index(cs_desriber)
    return (describer_score / len(suggested_queries)) - (prefix_count / len(suggested_queries))


def get_suggested_query_scores(filename):
    suggested_query_scores = {}
    with open(filename, 'r') as f:
        f.readline()
        line = f.readline()[:-1]
        while line:
            fields = line.split(',')
            score = get_suggested_query_score(fields[0])
            suggested_query_scores[fields[0]] = score
            line = f.readline()[:-1]
        f.close()
    with open('data/noun_phrase_suggested_query_scores.csv', 'w') as f:
        f.write('phrase,suggested_query_score\n')
        for phrase in suggested_query_scores:
            f.write(phrase + ',' + str(suggested_query_scores[phrase]) + '\n')
        f.close()


if __name__ == '__main__':
    get_suggested_query_scores('model/data/combined_metric_dataset.csv')
