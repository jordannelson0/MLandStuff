import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

# loads the data set
data = pd.read_csv("antimalware_test.csv")
print(data)

# classifiers
mlp = MLPClassifier(hidden_layer_sizes=(200,), activation='relu', solver='sgd', alpha=0.0005,
                    learning_rate='adaptive', max_iter=2000)

# mlp1 = MLPClassifier(max_iter=6000)
#  parameter_space = {'hidden_layer_sizes': [(64, 16), (64, 32), (50, 50, 50), (100,), (100, 100, 50), (200,)],
#                   'activation': ['tanh', 'relu', 'logistic', 'identity'], 'solver': ['sgd', 'adam'],
#                   'alpha': [0.0001, 0.05, 0.01, 0.003, 0.08, 0.0005],
#                   'learning_rate': ['constant', 'adaptive']}
# gsclf = GridSearchCV(mlp1, parameter_space, n_jobs=-1, cv=10)

# columns in the data
X = data.values[:, 0:204]
Y = data.values[:, 204]

# splits the data set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
# gsclf.fit(X_train, Y_train)
mlp.fit(X_train, Y_train)

# does the calculation for the evaluation metrics
# default metric is accuracy
accuracy = cross_val_score(mlp, X, Y, cv=10)
precision = cross_val_score(mlp, X, Y, cv=10, scoring='precision_macro')
recall = cross_val_score(mlp, X, Y, cv=10, scoring='recall_macro')
f1 = cross_val_score(mlp, X, Y, cv=10, scoring='f1_macro')


# output
print("------------- MLP -------------")
print("MLP Accuracy: %0.2f (+/- %0.2f)" % (accuracy.mean(), accuracy.std()))
print("MLP Precision: %0.2f (+/- %0.2f)" % (precision.mean(), precision.std()))
print("MLP Recall: %0.2f (+/- %0.2f)" % (recall.mean(), recall.std()))
print("MLP F1: %0.2f (+/- %0.2f)" % (f1.mean(), f1.std()))
# print(gsclf.best_params_)