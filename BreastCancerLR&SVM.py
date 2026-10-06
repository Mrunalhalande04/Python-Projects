import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


#-------------------------------------------------------------
# Function name : LoadPreserveModel
# Description : It is used to load preserved model
# Parameters : filename
# Return : model
# Date : 14/03/2026
# Author : Mrunal Halande
#-------------------------------------------------------------

def LoadPreserveModel(filename):

    loaded_model = joblib.load(filename)

    print("Model successfully loaded")

    return loaded_model


#-------------------------------------------------------------
# Function name : PreserveModel
# Description : It is used to preserve model on secondary
# Parameters : model, filename
# Return : None
# Date : 14/03/2026
# Author : Mrunal Halande
#-------------------------------------------------------------

def PreserveModel(model, filename):

    joblib.dump(model, filename)

    print("Model preserved successfully with name :", filename)


#-------------------------------------------------------------
# Function name : DisplayInfo
# Description : It displays the formatted title
# Parameters : title
# Return : None
# Date : 14/03/2026
# Author : Mrunal Halande
#-------------------------------------------------------------

def DisplayInfo(title):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


#-------------------------------------------------------------
# Function name : ShowData
# Description : It shows basic information about dataset
# Parameters : df, message
# Return : None
# Date : 14/03/2026
# Author : Mrunal Halande
#-------------------------------------------------------------

def ShowData(df, message):

    DisplayInfo(message)

    print("\nFirst 5 rows of dataset")
    print(df.head())

    print("\nShape of dataset")
    print(df.shape)

    print("\nColumn names")
    print(df.columns.tolist())

    print("\nMissing value in each column")
    print(df.isnull().sum())


#-------------------------------------------------------------
# Function name : CorrelationAnalysis
# Description : It performs correlation analysis
# Parameters : df
# Return : None
# Date : 14/03/2026
# Author : Mrunal Halande
#-------------------------------------------------------------

def CorrelationAnalysis(df):

    DisplayInfo("Correlation Analysis")

    correlation = df.corr(numeric_only=True)

    print("\nCorrelation Matrix:")
    print(correlation)

    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation, annot=True, cmap="coolwarm")
    plt.title("Breast Cancer Feature Correlation")
    plt.show()


#-------------------------------------------------------------
# Function name : BreastCancerModel
# Description : It splits data, performs feature scaling,
#               trains Logistic Regression and SVM models
#               and evaluates both models
# Parameters : df
# Return : None
# Date : 14/03/2026
# Author : Mrunal Halande
#-------------------------------------------------------------

def BreastCancerModel(df):

    # Split features and target

    X = df.drop("Target", axis=1)
    Y = df["Target"]

    print("\nFeatures :")
    print(X.head())

    print("\nLabels :")
    print(Y.head())

    print("\nShape of X :", X.shape)
    print("Shape of Y :", Y.shape)


    # Train Test Split

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

    print("\nTraining data shape :", X_train.shape)
    print("Testing data shape :", X_test.shape)


    # Feature Scaling

    DisplayInfo("Feature Scaling")

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print("Feature scaling completed successfully")


    #---------------------------------------------------------
    # Logistic Regression
    #---------------------------------------------------------

    DisplayInfo("Logistic Regression")

    lr = LogisticRegression(max_iter=10000)

    lr.fit(X_train, y_train)

    print("Model trained successfully using Logistic Regression")

    PreserveModel(lr, "LRBreastCancer.pkl")

    loaded_lr = LoadPreserveModel("LRBreastCancer.pkl")

    y_pred_lr = loaded_lr.predict(X_test)

    print("\nLogistic Regression Accuracy:")
    print(accuracy_score(y_test, y_pred_lr))

    print("\nLogistic Regression Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_lr))

    print("\nLogistic Regression Classification Report:")
    print(classification_report(y_test, y_pred_lr))


    #---------------------------------------------------------
    # SVM
    #---------------------------------------------------------

    DisplayInfo("Support Vector Machine")

    svm = SVC()

    svm.fit(X_train, y_train)

    print("Model trained successfully using SVM")

    PreserveModel(svm, "SVMBreastCancer.pkl")

    loaded_svm = LoadPreserveModel("SVMBreastCancer.pkl")

    y_pred_svm = loaded_svm.predict(X_test)

    print("\nSVM Accuracy:")
    print(accuracy_score(y_test, y_pred_svm))

    print("\nSVM Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_svm))

    print("\nSVM Classification Report:")
    print(classification_report(y_test, y_pred_svm))


#-------------------------------------------------------------
# Function name : BreastCancer
# Description : This is the main pipeline controller
# Parameters : DataPath
# Return : None
# Date : 14/03/2026
# Author : Mrunal Halande
#-------------------------------------------------------------

def BreastCancer(DataPath):

    DisplayInfo("Step 1 : Loading the DataSet")

    df = pd.read_csv(DataPath)

    print("Dataset loaded successfully")

    ShowData(df, "Initial DataSet")

    CorrelationAnalysis(df)

    DisplayInfo("Step 4 : Training Models")

    BreastCancerModel(df)


#-------------------------------------------------------------
# Function name : main
# Description : Starting point of the application
# Parameters : None
# Return : None
# Date : 06/10/2026
# Author : Mrunal Halande
#-------------------------------------------------------------

def main():

    BreastCancer("Breast_Cancer.csv")


#-------------------------------------------------------------
# Starting point
#-------------------------------------------------------------

if __name__ == "__main__":

    main()