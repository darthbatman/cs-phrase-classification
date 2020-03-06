# Adapted from: https://github.com/harrywsh/phrase-detection
import wikipedia
import wikipediaapi


def get_cs_categories():
    cs_categories = set()
    with open('data/harrywsh-phrase-detection/cs_categories.txt', 'r') as f:
        for line in f:
            cs_categories.add(line[:-1])
    return cs_categories


def get_wiki_score(candidate, cs_categories, num_results=20):
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


if __name__ == '__main__':
    print(get_wiki_score('database system', get_cs_categories()))
