import pickle

model = pickle.load(open("models/diabetes_model.pkl", "rb"))

def predict_diabetes_service(data):
    input_data = [
        data.get("pregnancies", 0),
        data.get("glucose", 0),
        data.get("bloodpressure", 0),
        data.get("skinthickness", 0),
        data.get("insulin", 0),
        data.get("bmi", 0),
        data.get("dpf", 0),
        data.get("age", 0)
    ]

    prediction = model.predict([input_data])[0]

    if prediction == 1:
        return {
            "result": "Diabetic",
            "precautions": [
                "Maintain healthy diet",
                "Exercise regularly",
                "Monitor blood sugar",
                "Consult doctor"
            ]
        }
    else:
        return {
            "result": "Not Diabetic",
            "precautions": [
                "Maintain healthy lifestyle",
                "Regular checkups",
                "Balanced diet"
            ]
        }