# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn import svm
# from sklearn.metrics import accuracy_score

import predictor


lst = [10,115,0,0,0,35.3,0.134,29]
input_data  = [8,176,90,34,300,33.7,0.467,58]
print("////////////////////////////////////////////////////////")
print("you test_score is :" , predictor.detect_diabetes(lst))
print("////////////////////////////////////////////////////////")