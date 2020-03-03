def compare_results():
    autophrase_terms = {}
    with open('AutoPhrase-master/models/DBLP-Titles/AutoPhrase.txt') as f1:
        lines = f1.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            autophrase_terms[line.split('\t')[1]] = 1.0 - ((i + 1) / len(lines))
        f1.close()
    my_terms = {}
    with open('data/scored_with_wiki.csv') as f2:
        lines = f2.readlines()
        for i, line in enumerate(lines):
            line = line.strip()
            if i == 0:
                continue
            my_terms[line.split(',')[0]] = 1.0 - (i / len(autophrase_terms.keys()))
            if i == len(autophrase_terms.keys()):
                break
        f2.close()
    with open('comparison_wiki.csv', 'w') as f:
        f.write('term,autophrase_rank,my_rank\n')
        for a_term in autophrase_terms.keys():
            if a_term in my_terms:
                f.write(a_term + ',' + str(autophrase_terms[a_term]) + ',' + str(my_terms[a_term]) + '\n')
                my_terms[a_term] = -1
            else:
                f.write(a_term + ',' + str(autophrase_terms[a_term]) + '\n')
        for m_term in my_terms:
            if my_terms[m_term] != -1:
                f.write(m_term + ',,' + str(my_terms[m_term]) + '\n')
        f.close()


if __name__ == '__main__':
    compare_results()
