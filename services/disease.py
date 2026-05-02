import pickle
import pandas as pd

# -------------------- LOAD MODEL --------------------

model = pickle.load(open("models/disease_model.pkl", "rb"))
symptom_index = pickle.load(open("models/symptom_index.pkl", "rb"))

# -------------------- LOAD PRECAUTIONS --------------------

precautions_df = pd.read_csv("dataset/disease_precaution.csv")

# -------------------- 🔥 ADD THIS HERE --------------------

SYMPTOM_MAP = {
    "fever": "high_fever",
    "cold": "runny_nose",
    "cough": "cough",
    "headache": "headache",
    "breathing problem": "breathlessness",
    "chest pain": "chest_pain",
    "stomach pain": "abdominal_pain",
    "vomiting": "vomiting",
    "fatigue": "fatigue"
}

# -------------------- FUNCTIONS --------------------

def get_precautions(disease):
    row = precautions_df[precautions_df['Disease'] == disease]
    if row.empty:
        return ["No precautions available"]
    return row.iloc[0][1:].dropna().tolist()


def predict_disease_service(symptoms):
    vector = [0] * len(symptom_index)

    for s in symptoms:
        s = s.lower().strip()

        # 🔥 FIX: use mapping
        s = SYMPTOM_MAP.get(s, s.replace(" ", "_"))

        if s in symptom_index:
            vector[symptom_index[s]] = 1

    print("User input:", symptoms)
    print("Vector sum:", sum(vector))

    prediction = model.predict([vector])[0]
    precautions = get_precautions(prediction)

    return {
        "disease": prediction,
        "precautions": precautions
    }