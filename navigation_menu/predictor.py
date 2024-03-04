import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
import warnings

def detect_diabetes(patient_data):
    diabetes_dataset = pd.read_csv('diabetes.csv')
    x = diabetes_dataset.drop(['Outcome'] , axis = 1)
    y = diabetes_dataset['Outcome']

    #scaling and transforming the x values
    scaler = StandardScaler()
    scaler.fit(x)
    standardized_data = scaler.transform(x)
    
    #passing the standardized value to the x
    x = standardized_data 

    #splitting of the dataset:
    x_train , x_test , y_train , y_test = train_test_split(x , y ,test_size = 0.2 , random_state = 2 , stratify = y)

   #Training the support vector Machine classifier:
    classifier = svm.SVC(kernel = 'linear')
    classifier.fit(x_train , y_train)

    #Making the predictive system:
    data_in_array = np.array(patient_data , ndmin=2)

    #scaling the patient data:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        standardized_data_of_patient = scaler.transform(data_in_array)

    #prediction statement:
    prediction = classifier.predict(standardized_data_of_patient)
    if prediction[0]==0:
        return 0
    else:
        return 1
    





    

