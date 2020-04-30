import numpy as np


def scale_to_range(l):
    # Source: https://stackoverflow.com/questions/1735025/how-to-normalize-a-numpy-array-to-within-a-certain-range
    return 2 * (l - np.min(l)) / np.ptp(l) - 1


def scale_features():
    noun_phrase_popularities = {}
    noun_phrase_purities = {}
    with open('model/data/combined_metric_dataset.csv', 'r') as f:
        f.readline()
        line = f.readline()[:-1]
        while line:
            fields = line.split(',')
            noun_phrase_popularities[fields[0]] = float(fields[5])
            noun_phrase_purities[fields[0]] = float(fields[6])
            line = f.readline()[:-1]
        f.close()
    scaled_values = scale_to_range(list(noun_phrase_popularities.values()))
    idx = 0
    for key in noun_phrase_popularities:
        noun_phrase_popularities[key] = scaled_values[idx]
        idx += 1
    scaled_values = scale_to_range(list(noun_phrase_purities.values()))
    idx = 0
    for key in noun_phrase_purities:
        noun_phrase_purities[key] = scaled_values[idx]
        idx += 1
    with open('model/data/combined_metric_dataset.csv', 'r') as rf:
        with open('model/data/combined_metric_dataset_v2.csv', 'w') as wf:
            wf.write(rf.readline())
            line = rf.readline()[:-1]
            while line:
                fields = line.split(',')
                fields[5] = str(noun_phrase_popularities[fields[0]])
                fields[6] = str(noun_phrase_purities[fields[0]])
                wf.write(','.join(fields) + '\n')
                line = rf.readline()[:-1]
            wf.close()
        rf.close()


if __name__ == '__main__':
    scale_features()
