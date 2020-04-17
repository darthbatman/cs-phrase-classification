def get_popularity():
    all_popularities = {}
    all_purities = {}
    with open('data/rohansuresh/popularities_and_purities.csv', 'r') as f:
        line = f.readline()
        line = f.readline()[:-1]
        phrase = ''
        while line:
            if phrase:
                all_popularities[phrase] = float(line[1:].strip().split()[0])
                all_purities[phrase] = float(line[1:].strip().split()[1])
                phrase = ''
            else:
                phrase = line[1:].strip().lower()
            line = f.readline()[:-1]
        f.close()
    with open('data/stanford-core-nlp/dblp_titles_noun_phrases.txt',
              'r') as rf:
        with open('data/noun_phrase_popularities.csv', 'w') as wf1:
            with open('data/noun_phrase_purities.csv', 'w') as wf2:
                wf1.write('phrase,popularity\n')
                wf2.write('phrase,purity\n')
                line = rf.readline()[:-1].lower()
                while line:
                    if line in all_popularities:
                        wf1.write(line + ',' + str(all_popularities[line]) + '\n')
                    if line in all_purities:
                        wf2.write(line + ',' + str(all_purities[line]) + '\n')
                    line = rf.readline()[:-1].lower()
                wf2.close()
            wf1.close()
        rf.close()


if __name__ == '__main__':
    get_popularity()
