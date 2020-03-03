def rank_with_wiki():
    with open('data/dblp_noun_frequencies_3.csv', 'r') as f:
        line = f.readline()
        line = f.readline()
        phrase_qualities = []
        while line:
            line_words = line.split(',')
            freq = float(line_words[1])
            c = float(line_words[2])
            w = float(line_words[3])
            # phrase, frequency, custom_metric_score, wiki_score
            phrase_qualities.append((line_words[0], freq, c, w, 1.0 * freq + 0.1 * c + 100.0 * w))
            line = f.readline()
        f.close()
        phrase_qualities = sorted(phrase_qualities, key=lambda x: x[4])
        with open('data/scored_with_wiki.csv', 'w') as f:
            f.write('phrase,frequency,custom_metric_score,wiki_score,final_score\n')
            for phrase_quality in phrase_qualities:
                if phrase_quality[1] > 1:
                    f.write(str(phrase_quality[0]) + ',' + str(phrase_quality[1]) + ',' + str(phrase_quality[2]) + ',' + str(str(phrase_quality[3])) + ',' + str(phrase_quality[4]) + '\n')
            f.close()


if __name__ == '__main__':
    rank_with_wiki()
