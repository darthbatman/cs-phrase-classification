import requests

from credentials import api_key, search_engine_id


def get_num_google_results(query):
    url = 'https://www.googleapis.com/customsearch/v1?'
    params = {'key': api_key, 'cx': search_engine_id, 'q': query}
    r = requests.get(url=url, params=params)
    data = r.json()
    if 'searchInformation' in data:
        if 'totalResults' in data['searchInformation']:
            return int(data['searchInformation']['totalResults'])
    return -1


def format_query(noun_phrase, domain):
    return '"{}" AND "{}"'.format(noun_phrase, domain)


def get_popularity(noun_phrase, domain, num_domain_results):
    query = format_query(noun_phrase, domain)
    num_results = get_num_google_results(query)
    if num_results == -1:
        print('Error: Query: \'{}\' failed.'.format(query))
    return num_results / num_domain_results


def get_noun_phrases(filename):
    phrases = []
    with open(filename, 'r') as f:
        line = f.readline()
        line = f.readline()[:-1]
        while line:
            phrases.append(line.split(',')[0])
            line = f.readline()[:-1]
        f.close()
    return phrases


def get_noun_phrase_popularities(filename, domain):
    phrases = get_noun_phrases(filename)
    num_domain_results = get_num_google_results('\"{}\"'.format(domain))
    with open('popularity_purity/data/noun_phrase_popularities.csv', 'w') as f:
        f.write('phrase,popularity\n')
        for phrase in phrases:
            popularity = get_popularity(phrase, domain, num_domain_results)
            f.write('{},{:f}\n'.format(phrase, popularity))
        f.close()


if __name__ == '__main__':
    get_noun_phrase_popularities('model/data/combined_metric_dataset.csv',
                                 'computer science')
