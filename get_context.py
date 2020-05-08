import requests

cs_desribers = ['computer science', 'python', 'machine learning',
                'artificial intelligence', 'ai', 'deep learning',
                'algorithm', 'algorithms', 'code', 'architecture',
                'api', 'software', 'framework', 'computer security',
                'computer system', 'computer systems']


def get_suggested_queries(query):
    url = 'http://suggestqueries.google.com/complete/search?client=firefox&q='
    formatted_query = query.replace(' ', '+')
    res = requests.get(url + formatted_query)
    return res.text.split('[')[2][:-2].replace('"', '').split(',')


def get_context(phrase):
    suggested_queries = get_suggested_queries(phrase)

    context = set()

    for sq in suggested_queries:
        if phrase + ' ' in sq:
            suffix = sq.split(phrase + ' ')[1]
            for cs_desriber in cs_desribers:
                if cs_desriber in suffix:
                    context.add(cs_desriber)

    return list(context)


def get_suggested_query_scores(filename):
    contexts = {}
    with open(filename, 'r') as f:
        f.readline()
        line = f.readline()[:-1]
        while line:
            fields = line.split(',')
            context = get_context(fields[0])
            contexts[fields[0]] = context
            line = f.readline()[:-1]
        f.close()
    with open('data/noun_phrase_contexts.csv', 'w') as f:
        f.write('phrase,' + ','.join(cs_desribers) + '\n')
        for phrase in contexts:
            line = phrase + ','
            for cs_desriber in cs_desribers:
                if cs_desriber in contexts[phrase]:
                    line += '1' + ','
                else:
                    line += '0' + ','
            f.write(line[:-1] + '\n')
        f.close()


if __name__ == '__main__':
    get_suggested_query_scores('model/data/combined_metric_dataset_50_50.csv')
