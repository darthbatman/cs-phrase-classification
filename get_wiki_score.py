# Adapted from: https://github.com/harrywsh/phrase-detection
import wikipedia
import wikipediaapi

cs_categories = set()


def get_cs_categories():
    with open('data/harrywsh-phrase-detection/cs_categories.txt', 'r') as f:
        for line in f:
            cs_categories.add(line[:-1])


def wiki_score(candidate, num_results=20):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    relevant_pages = set()
    for suggested_page in wikipedia.search(candidate, results=num_results,
                                           suggestion=False):
        for word in wiki_wiki.page(suggested_page).categories:
            word = word[9:]
            if word in cs_categories:
                relevant_pages.add(suggested_page)
                break
    return (len(relevant_pages) / num_results)


def get_wiki_score():
    get_cs_categories()
    with open('data/stanford-core-nlp/dblp_titles_noun_phrases.txt',
              'r') as rf:
        with open('data/noun_phrase_wiki_scores.csv', 'w') as wf:
            wf.write('phrase,wiki_score\n')
            noun_phrase = rf.readline().strip().lower()
            while noun_phrase:
                wf.write(noun_phrase + ',' +
                         str(wiki_score(noun_phrase)) + '\n')
                noun_phrase = rf.readline().strip().lower()
            wf.close()
        rf.close()


if __name__ == '__main__':
    get_wiki_score()
