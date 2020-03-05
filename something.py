import random
scored_phrases = []
autophrase_phrases = {}
with open('data/something.txt', 'r') as f:
    line = f.readline()[:-1]
    while line:
        line_parts = line.split('\t')
        phrase = line_parts[1]
        score = float(line_parts[0])
        if score >= 0.9:
            score = 2
        else:
            score = 1
        autophrase_phrases[phrase] = score
        line = f.readline()[:-1]
    f.close()
wiki_scored_phrases = {}
with open('data/something_else.txt', 'r') as f:
    line = f.readline()
    for scored_phrase in line.split('),'):
        wiki_scored_phrases[scored_phrase[2:-1].split(', ')[0]] = float(scored_phrase[2:-1].split(', ')[1])
    f.close()
with open('data/dblp_noun_frequencies.csv', 'r') as f:
    line = f.readline()
    line = f.readline()[:-1]
    while line:
        phrase = line.split(',')[0]
        if phrase not in autophrase_phrases:
            scored_phrases.append((phrase, float(line.split(',')[1]) / 517756, float(line.split(',')[2]), 0))
        else:
            scored_phrases.append((phrase, float(line.split(',')[1]) / 517756, float(line.split(',')[2]), autophrase_phrases[phrase]))
        line = f.readline()[:-1]
    f.close()

one_count = 120
zero_count = 120
random.shuffle(scored_phrases)
with open('data/dataset.csv', 'w') as f:
    f.write('phrase,frequency,wiki_score,label\n')
    for scored_phrase in scored_phrases:
        wiki_score = 0.45
        if scored_phrase[0] in wiki_scored_phrases:
            wiki_score = wiki_scored_phrases[scored_phrase[0]]
        if scored_phrase[3] == 2:
            f.write(scored_phrase[0] + ',' + str(scored_phrase[1]) + ',' + str(wiki_score) + ',' + str(scored_phrase[3]) + '\n')
        elif scored_phrase[3] == 1 and one_count >= 0:
            one_count -= 1
            f.write(scored_phrase[0] + ',' + str(scored_phrase[1]) + ',' + str(wiki_score) + ',' + str(scored_phrase[3]) + '\n')
        elif zero_count >= 0:
            zero_count -= 1
            f.write(scored_phrase[0] + ',' + str(scored_phrase[1]) + ',' + str(wiki_score) + ',' + str(scored_phrase[3]) + '\n')
    f.close()
