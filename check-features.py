# check_feature_names.py

import joblib

feature_names = joblib.load("models/feature_names.pkl")
print("Feature names expected by the model:")
for name in feature_names:
    print(name)
