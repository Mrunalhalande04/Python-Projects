import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier,plot_tree

from sklearn.metrics import (accuracy_score,confusion_matrix,classification_report,ConfusionMatrixDisplay)

def MarvellousClassifier(DatasetPath):

    Border="-"*40
    ################################################################################
    # Step 1: Load the dataset
    ################################################################################

    print(Border)
    print("Step 1: Load the DataSet ")
    print(Border)

    df = pd.read_csv(DatasetPath)

    print("DataSet gets loaded Succesfully :")
    print("Initial Entry from DataSet :")
    print(df.head())



    ################################################################################
    # Step 2: Data Analysis (EDA)
    ################################################################################

    print(Border)
    print("Step 2: Data Analysis ")
    print(Border)


    print("Shape of DataSet :",df.shape) #Shape is feature not method shape is attribute
    print("Column Name :",list(df.columns)) #columns is also a attribute

    print("Missing value (Per Column)")
    print(df.isnull().sum())
    print("Class Distribution (Species count)")
    print(df["species"].value_counts())
    print("Statistical report of Dataset")
    print(df.describe())

    ################################################################################
    # Step 3: Decide Independent and Dependent Variable
    ################################################################################

    print(Border)
    print("Step 3: Decide Independent and Dependent Variable ")
    print(Border)

    #X: Independent Variables / Features
    #Y: Dependent Variables / Labels

    feature_cols=["sepal length (cm)","sepal width (cm)","petal length (cm)","petal width (cm)"]

    X=df[feature_cols]
    Y=df["species"]

    print("X shape :",X.shape)
    print("Y shape :",Y.shape)


    ################################################################################
    # Step 4: visualization of dataset
    ################################################################################

    print(Border)
    print("Step 4: visualization of dataset ")
    print(Border)

    #scatter plot

    plt.figure(figsize=(7,5))

    for sp in df["species"].unique():
        temp=df[df["species"]==sp]
        plt.scatter(temp["petal length (cm)"], temp["petal width (cm)"],label=sp)

    plt.title("Iris : Petal length vs Petal widht")
    plt.xlabel("petal length (cm)")
    plt.ylabel("petal width  (cm)")
    plt.legend()
    plt.grid(True)
    plt.show()


    ################################################################################
    # Step 5: Split the dataset for training and testing
    ################################################################################

    print(Border)
    print("Step 5: Split the dataset for training and testing ")
    print(Border)

    #test size = 20%
    #train size=80%

    X_train, X_test, Y_train, Y_test=train_test_split(
    X,
    Y,
    test_size=0.5,
    random_state=42   #mix the iris
    )

    print("X - Independent :",X.shape) #150,4
    print("Y - Depenedent :",Y.shape)#150,

    print("Data spliting activity done :")

    print("X_train :",X_train.shape) #120,4
    print("X_test :",X_test.shape)#30,4

    print("Y_train :",Y_train.shape) #120,
    print("Y_test :",Y_test.shape)  #30,


    ################################################################################
    # Step 6: Build the Model
    ################################################################################

    print(Border)
    print("Step 6: Build the Model ")
    print(Border)

    print("We are going to use DecisionTreeClassifier")

    model=DecisionTreeClassifier(
        criterion="gini",
        max_depth=5, #hyper parameter
        random_state=42 
    )

    print("Model successfully created :",model)


    ################################################################################
    # Step 7: train the Model
    ################################################################################

    print(Border)
    print("Step 7: Train the Model ")
    print(Border)

    model.fit(X_train,Y_train)
    print("Model training completed ")


    ################################################################################
    # Step 8: test the Model
    ################################################################################

    print(Border)
    print("Step 8: Test /Evaluate the Model ")
    print(Border)

    Y_pred=model.predict(X_test)
    print("Model Evaluation (testing)Complete ")
    print(Y_pred.shape)

    print("Expected answer :")
    print(Y_test)

    print("Predicted answer")
    print(Y_pred)

    ################################################################################
    # Step 9: Evaluate the model performance
    ################################################################################

    print(Border)
    print("Step 9: Evaluate the model performance ")
    print(Border)

    accuracy= accuracy_score(Y_test,Y_pred)
    print("Accuracy of model is :",accuracy*100)

    cm=confusion_matrix(Y_test,Y_pred)
    print("Confusion matrix : ")
    print(cm)

    print("Classification report :")
    print(classification_report(Y_test,Y_pred))

    ################################################################################
    # Step 10: Plot Confusion matrix
    ################################################################################

    print(Border)
    print("Step 10: Plot confusion matrix ")
    print(Border)

    data=ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=model.classes_)
    data.plot()
    plt.title("Confusion matrix of Iris DataSet")
    plt.show()


def main():
    border="-"*40
    print(border)
    print("Iris Classification using Decision Tree Classifier :")
    print(border)

    MarvellousClassifier("iris.csv")







if __name__=="__main__":
    main()