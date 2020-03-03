import nltk
from itertools import islice


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def get_concordance():
    with open('data/dblp_titles.txt', 'r') as f1:
        tokens = []
        line = f1.readline()
        while line:
            for word in line.split(' '):
                tokens.append(word.lower().strip())
            line = f1.readline()
        f1.close()
        print("Parsed Tokens")
        text = nltk.Text(tokens)
        text.concordance('information', lines=10)
        text.concordance('data', lines=10)
        # c = nltk.ConcordanceIndex(text.tokens, key = lambda s: s.lower())
        # my_list = [text.tokens[offset+1] for offset in c.offsets('information')]
        # freq = {}
        # for item in my_list:
        #     if (item in freq):
        #         freq[item] += 1
        #     else:
        #         freq[item] = 1
      
        # freq = {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)}
        # print(take(100, freq.items()))
        # with open('data/dblp_nouns_517756_titles_3_words.txt', 'r') as f2:
        #     line = f2.readline()
        #     while line:
        #         print("line: " + line)
        #         for word in line.split(' '):
        #             print("word: " + word)
        #             print(text.common_contexts([word.lower().strip()]))
        #     line = f2.readline()
        #     f2.close()


if __name__ == '__main__':
    get_concordance()
