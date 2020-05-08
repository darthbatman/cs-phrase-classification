import numpy as np


def scale_to_range(l):
    # Source: https://stackoverflow.com/questions/1735025/how-to-normalize-a-numpy-array-to-within-a-certain-range
    return 2 * (l - np.min(l)) / np.ptp(l) - 1


def add_scaled_feature():
    noun_phrase_sqs = {}
    with open('data/noun_phrase_suggested_query_scores.csv', 'r') as f:
        f.readline()
        line = f.readline()[:-1]
        while line:
            fields = line.split(',')
            noun_phrase_sqs[fields[0]] = float(fields[1])
            line = f.readline()[:-1]
        f.close()
    scaled_values = scale_to_range(list(noun_phrase_sqs.values()))
    idx = 0
    for key in noun_phrase_sqs:
        noun_phrase_sqs[key] = scaled_values[idx]
        idx += 1
    with open('model/data/combined_metric_dataset.csv', 'r') as rf:
        with open('model/data/combined_metric_dataset_v2.csv', 'w') as wf:
            wf.write(rf.readline())
            line = rf.readline()[:-1]
            while line:
                fields = line.split(',')
                fields.append(str(noun_phrase_sqs[fields[0]]))
                wf.write(','.join(fields[:-2]) + ',' + fields[-1] + ',' + fields[-2] + '\n')
                line = rf.readline()[:-1]
            wf.close()
        rf.close()


if __name__ == '__main__':
    add_scaled_feature()
