import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.preprocessing import StandardScaler

def MarvellousClassifier(DataPath):
    border="-"*40

    #Step 1: Load the dataset from CSV file
    print(border)
    print("Step 1: Load the dataset from CSV file")
    print(border)

    df=pd.read_csv(DataPath)
    print(border)
    print("Some entries from dataset")
    print(df.head())
    print(border)

    #Step 2: clean the dataset by removing empty rows
    print(border)
    print("Step 2: clean the dataset by removing empty rows")
    print(border)

    df.dropna(inplace=True) #remove empty row
    print("Total records ",df.shape[0])
    print("Total columns :",df.shape[1])
    print(border)

    #Step 3: Seperate independent and dependent variable
    print(border)
    print("Step 3: Seperate independent and dependent variable")
    print(border)

    X=df.drop(columns=['Class'])
    Y=df['Class']

    print("Shape of X :",X.shape)
    print("Shape of Y :",Y.shape)

    print(border)
    print("Input columns :",X.columns.tolist())
    print("Output columns : Class")

    #Step 4: split the dataset for training and testing
    print(border)
    print("Step 4:split the dataset for training and testing ")
    print(border)

    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=42,stratify=Y)

    print(border)
    print("Information of training and testing data")
    print("X_train shape ",X_train.shape)
    print("X_test shape ",X_test.shape)
    print("Y_train shape ",Y_train.shape)
    print("Y_test shape ",Y_test.shape)
    print(border)

    #Step 5: Feature scaling
    print(border)
    print("Step 5: Feature scaling")
    print(border)
    
    scalar=StandardScaler()
    #Independent variable scaling
    X_train_scaled=scalar.fit_transform(X_train)
    X_test_scaled=scalar.fit_transform(X_test)
    print("Feature scaling is done")

    #Step 6: Explore the multiple values of k
    #Hyperparameter tuning (K)
    print(border)
    print("Step 6: Explore the multiple values of k")
    print(border)

    accuracy_scores=[]
    K_value=range(1,21)

    for k in K_value:
        model=KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train_scaled,Y_train)
        Y_pred=model.predict(X_test_scaled)
        accuracy=accuracy_score(Y_test,Y_pred)
        accuracy_scores.append(accuracy)

    print(border)
    print("Accuracy report of all k values from 1 to 20")

    for value in accuracy_scores:
        print(value)

    print(border)


    #Step 7: Plot graph of K vs accuracy
    print(border)
    print("Step 7: Plot graph of K vs accuracy")
    print(border)

    plt.figure(figsize=(8,5))
    plt.plot(K_value,accuracy_scores,marker= 'o')
    plt.title("K values vs accuracy")
    plt.xlabel("Value of K")
    plt.ylabel("Accuracy")
    plt.grid(True)
    plt.xticks(list(K_value))
    plt.show()

    #Step 8: find best value of K
    print(border)
    print("Step 8: find best value of K")
    print(border)

    best_k=list(K_value)[accuracy_scores.index(max(accuracy_scores))]

    print("Best value of K is :",best_k)

    #Step 9: build final model using best value of K
    print(border)
    print("Step 9: build final model using best value of K")
    print(border)

    final_model=KNeighborsClassifier(n_neighbors=best_k)
    final_model.fit(X_train_scaled,Y_train)
    Y_pred=final_model.predict(X_test_scaled)

    #Step 10: calculate final accuracy
    print(border)
    print("Step 10: calculate final accuracy")
    print(border)

    accuracy=accuracy_score(Y_test,Y_pred)
    print("Accuracy of model is :",accuracy*100)


    #Step 11: Display confusion matrix
    print(border)
    print("Step 11: Display confusion matrix")
    print(border)

    cm=confusion_matrix(Y_test,Y_pred)
    print(cm)


    #Step 12: Display classification report
    print(border)
    print("Step 12: Display classification report")
    print(border)

    print(classification_report(Y_test,Y_pred))



def main():
    border="-"*40
    print(border)
    print("Wine Classifier using KNN")
    print(border)

    MarvellousClassifier("WinePredictor.csv")




if __name__ =="__main__":
    main()