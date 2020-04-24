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


def get_purity(noun_phrase, domain):
    first_query = format_query(noun_phrase, domain)
    first_num_results = get_num_google_results(first_query)
    if first_num_results == -1:
        print('Error: Query: \'{}\' failed.'.format(first_query))
    second_query = '\"{}\"'.format(noun_phrase)
    second_num_results = get_num_google_results(first_query)
    if second_num_results == -1:
        print('Error: Query: \'{}\' failed.'.format(second_query))
    return first_num_results / second_num_results


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


def get_noun_phrase_purities(filename, domain):
    phrases = get_noun_phrases(filename)
    with open('popularity_purity/data/noun_phrase_purities.csv', 'w') as f:
        f.write('phrase,purity\n')
        for phrase in phrases[950:]:
            purity = get_purity(phrase, domain)
            f.write('{},{:f}\n'.format(phrase, purity))
        f.close()


if __name__ == '__main__':
    get_noun_phrase_purities('model/data/combined_metric_dataset.csv',
                             'computer science')
