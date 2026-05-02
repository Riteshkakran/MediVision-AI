import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

# -------------------- LOAD DATA --------------------

df = pd.read_csv("dataset/diabetes.csv")

print("Dataset Loaded")
print(df.head())

# -------------------- SPLIT DATA --------------------

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------- TRAIN MODEL --------------------

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# -------------------- EVALUATE --------------------

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy * 100:.2f}%")

# -------------------- SAVE MODEL --------------------

os.makedirs("models", exist_ok=True)

pickle.dump(model, open("models/diabetes_model.pkl", "wb"))

print("Model saved successfully!")
