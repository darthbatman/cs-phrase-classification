from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.externals.six import StringIO
import pydotplus

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

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

my_classifier = tree.DecisionTreeClassifier(max_depth=3, min_samples_leaf=10)

# training decision tree classifier

my_classifier.fit(x_train, y_train)

# classifying entries using decision tree classifier

predictions = my_classifier.predict(x_test)

# # showing test values and corresponding predictions

# print x_test
# print predictions

# showing measure of decision tree classifier's performance for test

print(accuracy_score(y_test, predictions))

# generating visualization of decision tree classifier

dot_data = StringIO()

tree.export_graphviz(my_classifier, out_file=dot_data, feature_names=feature_names, class_names=["Low", "Medium", "High"], filled=True, rounded=True, special_characters=True)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())

graph.write_pdf("visualization.pdf")