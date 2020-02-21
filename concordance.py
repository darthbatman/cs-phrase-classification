import nltk


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
        print("Got Text")
        print(text.concordance('information'))
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
