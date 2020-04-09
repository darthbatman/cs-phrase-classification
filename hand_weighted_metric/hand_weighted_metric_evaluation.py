import sys


def evaluate_hand_weighted_metric(filename):
    good_phrases = []
    with open('hand_weighted_metric/data/good_phrases.txt', 'r') as f:
        line = f.readline()[:-1]
        while line:
            if len(line.split(' ')) == 2:
                good_phrases.append(line)
            line = f.readline()[:-1]
        f.close()
    ranked_phrases = {}
    with open(filename, 'r') as f:
        line = f.readline()
        line = f.readline()[:-1]
        while line:
            components = line.split(',')
            ranked_phrases[components[0]] = float(components[-1])
            line = f.readline()[:-1]
        f.close()
    rankings_sum = 0
    for ranked_phrase in ranked_phrases:
        rankings_sum += ranked_phrases[ranked_phrase]
    avg_rank = rankings_sum / len(ranked_phrases.keys())

    num_correct = 0
    num_counted = 0
    misclassified = []
    for good_phrase in good_phrases:
        if good_phrase in ranked_phrases:
            if ranked_phrases[good_phrase] > 0.0:
                num_correct += 1
            else:
                misclassified.append(good_phrase)
            num_counted += 1
    accuracy = num_correct / num_counted

    print('Accuracy: ' + str(accuracy))
    print('Average Rank: ' + str(avg_rank))
    print('Misclassified: ' + str(misclassified))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        evaluate_hand_weighted_metric(sys.argv[1])
