import pydotplus
from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def read_dataset():
    x = []
    y = []
    feature_names = []
    with open('data/combined_metric_dataset.csv', 'r') as f:
        feature_names = f.readline()[:-1].split(',')[1:-1]
        line = f.readline()[:-1]
        while line:
            x.append(line.split(',')[1:-1])
            y.append(line.split(',')[-1])
            line = f.readline()[:-1]
        f.close()
    return (x, y, feature_names)


def train_classifier(dataset):
    x = dataset[0]
    y = dataset[1]
    feature_names = dataset[2]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)
    classifier = tree.DecisionTreeClassifier(max_depth=3, min_samples_leaf=10)
    classifier.fit(x_train, y_train)
    return (classifier, x_test, y_test, feature_names)


def generate_visualization(classifier_with_feature_names):
    classifier = classifier_with_feature_names[0]
    feature_names = classifier_with_feature_names[1]
    dot_data = StringIO()
    tree.export_graphviz(
        classifier,
        out_file=dot_data,
        feature_names=feature_names,
        class_names=["Low", "Medium", "High"],
        filled=True,
        rounded=True,
        special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    output_filename = 'visualization.pdf'
    graph.write_pdf(output_filename)
    print('Visualization saved to ' + output_filename)


def evaluate_classifier(trained):
    classifier = trained[0]
    x_test = trained[1]
    y_test = trained[2]
    feature_names = trained[3]
    predictions = classifier.predict(x_test)
    print('Accuracy: ' + str(accuracy_score(y_test, predictions)))
    generate_visualization((classifier, feature_names))


def build_model():
    evaluate_classifier(train_classifier(read_dataset()))


if __name__ == '__main__':
    build_model()
