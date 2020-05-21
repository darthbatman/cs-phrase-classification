from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
import numpy as np


def read_dataset():
    x = []
    y = []
    with open('../data/dataset_50_50.csv', 'r') as f:
        f.readline()
        line = f.readline()[:-1]
        while line:
            x.append(line.split(',')[0:3] + line.split(',')[4:6])
            y.append(line.split(',')[-1])
            line = f.readline()[:-1]
        f.close()
    return (x, y)


def train_classifier(dataset):
    x = dataset[0]
    y = dataset[1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    test_phrases = np.array(x_test)[:, 0]
    x_train = np.array(x_train)[:, 1:]
    x_test = np.array(x_test)[:, 1:]
    classifier = svm.SVC()
    classifier.fit(x_train, y_train)
    return (classifier, x_test, y_test, test_phrases)


def evaluate_classifier(trained):
    classifier = trained[0]
    x_test = trained[1]
    y_test = trained[2]
    test_phrases = trained[3]
    predictions = classifier.predict(x_test)
    print('Accuracy: ' + str(accuracy_score(y_test, predictions)))
    print('Precision: ' + str(precision_score(y_test, predictions, pos_label='True')))
    print('Recall: ' + str(recall_score(y_test, predictions, pos_label='True')))
    # uncomment to show misclassified terms
    # y_test = np.asarray(y_test)
    # misclassified = np.where(y_test != predictions)[0]
    # for mis in misclassified:
    #     print(test_phrases[mis] + ': ' + str(y_test[mis]))


def build_model():
    evaluate_classifier(train_classifier(read_dataset()))


if __name__ == '__main__':
    build_model()
