from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def read_dataset():
    x = []
    y = []
    feature_names = []
    with open('data/dataset.csv', 'r') as f:
        feature_names = f.readline()[:-1].split(',')[1:-1]
        line = f.readline()[:-1]
        while line:
            x.append(line.split(',')[1:-1])
            y.append(line.split(',')[-1])
            line = f.readline()[:-1]
        f.close()
    return (x, y)


def train_classifier(dataset):
    x = dataset[0]
    y = dataset[1]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    classifier = svm.SVC()
    classifier.fit(x_train, y_train)
    return (classifier, x_test, y_test)


def evaluate_classifier(trained):
    classifier = trained[0]
    x_test = trained[1]
    y_test = trained[2]
    predictions = classifier.predict(x_test)
    print('Accuracy: ' + str(accuracy_score(y_test, predictions)))


def build_model():
    evaluate_classifier(train_classifier(read_dataset()))


if __name__ == '__main__':
    build_model()
