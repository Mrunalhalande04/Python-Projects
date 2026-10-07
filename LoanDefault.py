import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


#-------------------------------------------------------------
# Function name : LoadPreserveModel
# Description : It is used to load preserved model
# Parameters : filename
# Return : model
# Date : 07/10/2026
# Author : Mrunal Halande
#-------------------------------------------------------------

def LoadPreserveModel(filename):

    loaded_model = joblib.load(filename)

    print("Model successfully loaded")

    return loaded_model


#-------------------------------------------------------------
# Function name : PreserveModel
# Description : It is used to preserve model
# Parameters : model, filename
# Return : None
# Date : 07/10/2026
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
#-------------------------------------------------------------

def ShowData(df, message):

    DisplayInfo(message)

    print("\nFirst 5 rows of dataset")
    print(df.head())

    print("\nShape of dataset")
    print(df.shape)

    print("\nColumn names")
    print(df.columns.tolist())

    print("\nMissing values in each column")
    print(df.isnull().sum())


#-------------------------------------------------------------
# Function name : FeatureEngineering
# Description : It converts categorical data into numerical
#               data and creates useful financial features
# Parameters : df
# Return : df
#-------------------------------------------------------------

def FeatureEngineering(df):

    DisplayInfo("Feature Engineering")

    # Convert PreviousDefault into numerical value

    df["PreviousDefault"] = df["PreviousDefault"].map({"Yes": 1, "No": 0})

    # Convert HomeOwn into numerical dummy columns

    df = pd.get_dummies(df, columns=["HomeOwnership"], drop_first=True)

    # Create Loan to Income ratio

    df["LoanIncomeRatio"] = df["LoanAmount"] / df["Income"]

    # Create Monthly Debt to Income ratio

    df["DebtIncomeRatio"] = df["MonthlyDebt"] / df["Income"]

    print("\nFeature engineering completed")

    print("\nNew columns:")
    print(df.columns.tolist())

    return df



#-------------------------------------------------------------
# Function name : RandomForestModel
# Description : It trains and evaluates Random Forest
# Parameters : X_train, X_test, y_train, y_test
# Return : None
#-------------------------------------------------------------

def RandomForestModel(X_train, X_test, y_train, y_test):

    DisplayInfo("Random Forest Classifier")

    rf = RandomForestClassifier(n_estimators=100, random_state=42,max_depth=9)

    rf.fit(X_train, y_train)

    print("Model trained successfully using Random Forest")

    # Preserve model

    PreserveModel(rf, "RandomForestLoan.pkl")

    # Load model

    loaded_rf = LoadPreserveModel("RandomForestLoan.pkl")

    # Prediction

    y_pred_rf = loaded_rf.predict(X_test)

    # Evaluation

    print("\nRandom Forest Accuracy:")
    print(accuracy_score(y_test, y_pred_rf))

    print("\nRandom Forest Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_rf))

    print("\nRandom Forest Classification Report:")
    print(classification_report(y_test, y_pred_rf))


#-------------------------------------------------------------
# Function name : GradientBoostingModel
# Description : It trains and evaluates Gradient Boosting
# Parameters : X_train, X_test, y_train, y_test
# Return : None
#-------------------------------------------------------------

def GradientBoostingModel(X_train, X_test, y_train, y_test):

    DisplayInfo("Gradient Boosting Classifier")

    gb = GradientBoostingClassifier(random_state=42)

    gb.fit(X_train, y_train)

    print("Model trained successfully using Gradient Boosting")

    # Preserve model

    PreserveModel(gb, "GradientBoostingLoan.pkl")

    # Load model

    loaded_gb = LoadPreserveModel("GradientBoostingLoan.pkl")

    # Prediction

    y_pred_gb = loaded_gb.predict(X_test)

    # Evaluation

    print("\nGradient Boosting Accuracy:")
    print(accuracy_score(y_test, y_pred_gb))

    print("\nGradient Boosting Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_gb))

    print("\nGradient Boosting Classification Report:")
    print(classification_report(y_test, y_pred_gb))


#-------------------------------------------------------------
# Function name : LoanRiskModel
# Description : It prepares data, splits data and trains
#               Random Forest and Gradient Boosting
# Parameters : df
# Return : None
#-------------------------------------------------------------

def LoanRiskModel(df):

    # Separate features and target

    X = df.drop("Default", axis=1)

    Y = df["Default"]

    print("\nFeatures:")
    print(X.head())

    print("\nTarget:")
    print(Y.head())

    print("\nShape of X:", X.shape)
    print("Shape of Y:", Y.shape)


    #---------------------------------------------------------
    # Train Test Split
    #---------------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        Y,
        test_size=0.2,
        random_state=42,
        stratify=Y
    )

    print("\nTraining data shape:", X_train.shape)
    print("Testing data shape:", X_test.shape)


    #---------------------------------------------------------
    # Random Forest
    #---------------------------------------------------------

    RandomForestModel(X_train, X_test, y_train, y_test)


    #---------------------------------------------------------
    # Gradient Boosting
    #---------------------------------------------------------

    GradientBoostingModel(X_train, X_test, y_train, y_test)


#-------------------------------------------------------------
# Function name : LoanRisk
# Description : Main pipeline controller
# Parameters : DataPath
# Return : None
#-------------------------------------------------------------

def LoanRisk(DataPath):

    DisplayInfo("Step 1 : Loading the Dataset")

    df = pd.read_csv(DataPath)

    print("Dataset loaded successfully")

    # Show original dataset

    ShowData(df, "Initial Dataset")

    # Feature Engineering

    df = FeatureEngineering(df)


    # Train models

    DisplayInfo("Step 4 : Training Models")

    LoanRiskModel(df)


#-------------------------------------------------------------
# Function name : main
# Description : Starting point of the application
# Parameters : None
# Return : None
#-------------------------------------------------------------

def main():

    LoanRisk("Loan_Default.csv")


#-------------------------------------------------------------
# Starting point
#-------------------------------------------------------------

if __name__ == "__main__":

    main()