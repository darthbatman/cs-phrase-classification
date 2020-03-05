import json
import sys
import wikipedia
import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')
cs_categories = set()
with open('data/cs_categories.txt', 'r') as f:
    for line in f:
        cs_categories.add(line[:-1])


def get_wiki_score(candidate, num_results=10):
    relevant_pages = set()
    for suggested_page in wikipedia.search(candidate, results=num_results,
                                           suggestion=False):
        for word in wiki_wiki.page(suggested_page).categories:
            word = word[9:]
            if word in cs_categories:
                relevant_pages.add(suggested_page)
                break
    return (len(relevant_pages)/num_results)


def get_dblp_ranked_title_noun_frequencies():
    noun_frequencies = {}
    with open('data/dblp_nouns_517756_titles_3_words.txt', 'r') as f:
        line = f.readline()[:-1]
        while line:
            line = line.strip().lower()
            if line in noun_frequencies:
                noun_frequencies[line] += 1
            else:
                noun_frequencies[line] = 1
            line = f.readline()[:-1]
        f.close()
    with open('data/dblp_title_nouns_ranked_2.json', 'r') as f:
        ranked_nouns = json.load(f)
    noun_frequencies = {k: v for k, v in sorted(noun_frequencies.items(),
                        key=lambda item:
                        (1.0 * item[1] + 0.01 * ranked_nouns[item[0]]),
                        reverse=True)}
    with open('data/dblp_noun_frequencies_4.csv', 'w') as f:
        f.write('noun_phrase,frequency,custom_score,wiki_score\n')
        count = 0
        for key in noun_frequencies.keys():
            if count % 10 == 0:
                print('count: ' + str(count))
            count += 1
            if noun_frequencies[key] > 1:
                f.write(key + ',' + str(noun_frequencies[key]) + ',' +
                        str(ranked_nouns[key]) + ',' + str(get_wiki_score(key)) + '\n')
        f.close()


if __name__ == '__main__':
    get_dblp_ranked_title_noun_frequencies()
