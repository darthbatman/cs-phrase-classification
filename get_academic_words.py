def get_academic_words():
    with open('data/awl.txt', 'w') as f1:
        for i in range(1, 11):
            filename = 'data/awl_sublists/awl_sublist_' + str(i) + '.txt'
            with open(filename, 'r') as f2:
                f2.readline()  # column titles
                line = f2.readline()
                while line:
                    words = line.split(',')
                    for word in words:
                        word = word.split(' ')[0].strip()
                        if len(word) > 0 and word.isalpha():
                            f1.write(word + '\n')
                    line = f2.readline()
                f2.close()
    f1.close()


if __name__ == '__main__':
    get_academic_words()
