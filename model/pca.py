import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn import decomposition
from sklearn import datasets


def get_dataset():
    X = []
    y = []
    feature_names = []
    with open('data/combined_metric_dataset_50_50.csv', 'r') as f:
        line = f.readline()[:-1]
        feature_names = line.split(',')[1:-1]
        line = f.readline()[:-1]
        while line:
            fields = line.split(',')
            features = [float(x) for x in fields[1:-1]]
            if fields[-1] == 'True':
                label = 1
            else:
                label = 0
            X.append(features)
            y.append(label)
            line = f.readline()[:-1]
        f.close()
    return (np.array(X), np.array(y), feature_names)


def perform_pca():
    X, y, features = get_dataset()

    if X.shape[0] <= 0:
        return

    pca = decomposition.PCA(n_components=3)
    pca.fit(X)
    fit = pca.transform(np.identity(pca.components_.shape[1]))

    print('Feature Contribution by Component')
    for i in range(len(features)):
        sep = '\t\t'
        if i == 0:
            sep = '\t'
        print(features[i] + sep + ' '.join([f'{x:.10f}' for x in fit[i]]))

    print()
    print('Explained Variance: \t\t' + str(pca.explained_variance_))
    print('Explained Variance Ratio: \t' + str(pca.explained_variance_ratio_))


perform_pca()
