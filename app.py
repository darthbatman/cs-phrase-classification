good_phrases = set()
with open('hand_weighted_metric/data/good_phrases.txt', 'r') as f:
    line = f.readline()[:-1]
    while line:
        good_phrases.add(line)
        line = f.readline()[:-1]
    f.close()

with open('nngp.txt', 'w') as wf:
    with open('gp.txt', 'w') as wf2:
        dataset_phrases = {}
        with open('hand_weighted_metric/data/ranked_0.25_0.25_0.25_0.25.csv', 'r') as f:
            line = f.readline()
            line = f.readline()[:-1]
            while line:
                phrase = line.split(',')[0]
                dataset_phrases[phrase] = (phrase in good_phrases)
                if phrase not in good_phrases:
                    wf.write(phrase + '\n')
                else:
                    wf2.write(phrase + '\n')
                line = f.readline()[:-1]
            f.close()
        print(dataset_phrases)
        wf2.close()
    wf.close()
