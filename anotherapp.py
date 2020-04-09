phrases = {}
with open('more.txt', 'r') as f:
    line = f.readline()[:-1]
    while line:
        phrase = line.split(',')[0]
        if phrase in phrases:
            if line.split(',')[1] == 'True':
                phrases[phrase] = True
        else:
            phrases[phrase] = (line.split(',')[1] == 'True')
        line = f.readline()[:-1]
    f.close()

with open('hand_weighted_metric/data/ranked_0.25_0.25_0.25_0.25.csv', 'r') as f:
    with open('something123.csv', 'w') as wf:
        line = f.readline()
        wf.write('phrase,concordance_score,frequency,uniqueness,wiki_score,label\n')
        line = f.readline()[:-1]
        while line:
            components = line.split(',')
            if components[0] in phrases:
                wf.write(components[0] + ',' + components[1] + ',' + components[2] + ',' + components[3] + ',' + components[4] + ',' + str(phrases[components[0]]) + '\n')
            line = f.readline()[:-1]
        wf.close()
    f.close()
