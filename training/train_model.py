import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# -------------------- LOAD DATA --------------------

df = pd.read_csv("dataset/disease_symptoms.csv")
df.fillna("none", inplace=True)

print("Dataset Loaded Successfully!")
print("Shape:", df.shape)

# -------------------- CHECK DUPLICATES --------------------

duplicates = df.duplicated().sum()
print("Duplicate rows:", duplicates)

# -------------------- PREPARE SYMPTOMS --------------------

symptoms = set()

for col in df.columns[1:]:
    symptoms.update(df[col].unique())

symptoms.discard("none")
symptoms = sorted(symptoms)

print("Total unique symptoms:", len(symptoms))

# Create symptom index
symptom_index = {symptom: i for i, symptom in enumerate(symptoms)}

# -------------------- CONVERT TO VECTORS --------------------

X = []
y = []

for _, row in df.iterrows():
    vector = [0] * len(symptoms)

    for col in df.columns[1:]:
        if row[col] != "none":
            vector[symptom_index[row[col]]] = 1

    X.append(vector)
    y.append(row["Disease"])

# -------------------- TRAIN TEST SPLIT --------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)

# -------------------- MODEL TRAINING --------------------

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# -------------------- EVALUATION --------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -------------------- SAVE MODEL --------------------

os.makedirs("models", exist_ok=True)

pickle.dump(model, open("models/disease_model.pkl", "wb"))
pickle.dump(symptom_index, open("models/symptom_index.pkl", "wb"))

print("\nModel and symptom index saved successfully!")
