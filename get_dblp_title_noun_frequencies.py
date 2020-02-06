import sys


def get_dblp_title_noun_frequencies(filename):
    noun_frequencies = {}
    with open(filename, 'r') as f:
        line = f.readline()[:-1]
        while line:
            if line in noun_frequencies:
                noun_frequencies[line] += 1
            else:
                noun_frequencies[line] = 1
            line = f.readline()[:-1]
        f.close()
    noun_frequencies = {k: v for k, v in
                        sorted(noun_frequencies.items(),
                               key=lambda item: item[1], reverse=True)}
    with open('data/dblp_noun_frequencies.csv', 'w') as f:
        f.write('noun_phrase,frequency\n')
        for key in noun_frequencies.keys():
            f.write(key + ',' + str(noun_frequencies[key]) + '\n')
        f.close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        get_dblp_title_noun_frequencies(sys.argv[1])
