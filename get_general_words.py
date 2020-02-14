def get_general_words():
    with open('data/gsl.txt', 'w') as f1:
        with open('data/gsl_raw.txt', 'r') as f2:
            f2.readline()  # column titles
            line = f2.readline()
            while line:
                words = line.split(',')
                for i in range(4, len(words)):
                    word = words[i].strip()
                    if len(word) > 0:
                        f1.write(word + '\n')
                line = f2.readline()
            f2.close()
        f1.close()


if __name__ == '__main__':
    get_general_words()
