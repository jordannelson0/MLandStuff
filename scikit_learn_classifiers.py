import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import cross_val_score

# loads the data set
data = pd.read_csv("antimalware_test.csv")
print(data)

# classifiers
clf = KNeighborsClassifier(n_neighbors=8)
DTclf = DecisionTreeClassifier()
RFclf = RandomForestClassifier()
mlp = MLPClassifier(hidden_layer_sizes=(200,), activation='relu', solver='sgd', alpha=0.0005,
                    learning_rate='adaptive', max_iter=2000)
ehclf = VotingClassifier(estimators=[('knn', clf), ('rf', RFclf), ('dt', DTclf), ('mlp', mlp)], voting='hard')
esclf = VotingClassifier(estimators=[('knn', clf), ('rf', RFclf), ('dt', DTclf), ('mlp', mlp)], voting='soft')

# columns in the data
X = data.values[:, 0:204]
Y = data.values[:, 204]

# splits the data set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
clf.fit(X_train, Y_train)
DTclf.fit(X_train, Y_train)
RFclf.fit(X_train, Y_train)
mlp.fit(X_train, Y_train)

# stores predicted values of testing
# then compared to actual values for accuracy
Y_prediction = clf.predict(X_test)
print("Train/test accuracy (knn):", accuracy_score(Y_test, Y_prediction))

# splits the data set into 10 parts for cross-field validation
cv = 10

# does the calculation for the evaluation metrics
# default metric is accuracy
knnA = cross_val_score(clf, X, Y, cv=cv)
DTScoresA = cross_val_score(DTclf, X, Y, cv=cv)
RFScoresA = cross_val_score(RFclf, X, Y, cv=cv)

for clf, label in zip([clf, RFclf, DTclf, ehclf, mlp],
                      ['KNN', 'Random Forest', 'Decision Tree', 'Ensemble', 'MLP']):
    ehScores = cross_val_score(clf, X, Y, cv=cv)
for clf, label in zip([clf, RFclf, DTclf, esclf, mlp], ['KNN', 'Random Forest', 'Decision Tree', 'Ensemble', 'MLP']):
    esScores = cross_val_score(clf, X, Y, cv=cv)

# output
print("------------- KNN -------------")
print("KNN Accuracy: %0.3f (+/- %0.2f)" % (knnA.mean(), knnA.std()))
print()
print("------------- Trees -------------")
print("Decision Tree Accuracy: %0.2f (+/- %0.2f)" % (DTScoresA.mean(), DTScoresA.std()))
print("Random Forest Accuracy: %0.2f (+/- %0.2f)" % (RFScoresA.mean(), RFScoresA.std()))
print()
print("------------- Ensemble -------------")
print("Ensemble HV Accuracy: %0.2f (+/- %0.2f) [%s]" % (ehScores.mean(), ehScores.std(), label))
print("Ensemble SV Accuracy: %0.2f (+/- %0.2f) [%s]" % (esScores.mean(), ehScores.std(), label))