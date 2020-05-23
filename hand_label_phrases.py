import requests


def get_suggested_queries(query):
    url = 'http://suggestqueries.google.com/complete/search?client=firefox&q='
    formatted_query = query.replace(' ', '+')
    res = requests.get(url + formatted_query)
    return res.text.split('[')[2][:-2].replace('"', '').split(',')


def hand_label():
    with open('data/model/dataset.csv', 'r') as rf:
        with open('data/model/dataset_labeled.csv', 'w') as wf:
            rf.readline()
            line = rf.readline()[:-1]
            while line:
                fields = line.split(',')
                classification = input(fields[0] + ' | (1, 0, or ?) : ')
                if classification == '0':
                    fields[-1] = 'False'
                elif classification == '?':
                    suggested_queries = get_suggested_queries(fields[0])
                    print('Suggested Queries')
                    for suggested_query in suggested_queries:
                        print(suggested_query)
                    continue
                else:
                    fields[-1] = 'True'
                wf.write(','.join(fields) + '\n')
                line = rf.readline()[:-1]
            wf.close()
        rf.close()


if __name__ == '__main__':
    hand_label()
