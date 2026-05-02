
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


# Service imports
from services.disease import predict_disease_service
from services.diabetes import predict_diabetes_service
from services.pneumonia import predict_pneumonia_service
from services.brain import predict_brain_service
from services.doctors import get_doctors_service

app = Flask(__name__)
CORS(app)

# -------------------- PAGE ROUTES --------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/disease')
def disease():
    return render_template('disease.html')


@app.route('/doctors')
def doctors():
    return render_template('doctors.html')


@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


@app.route('/pneumonia')
def pneumonia():
    return render_template('pneumonia.html')


@app.route('/brain')
def brain():
    return render_template('brain.html')


# -------------------- API ROUTES --------------------

@app.route('/api/predict/disease', methods=['POST'])
def api_predict_disease():
    try:
        symptoms = request.json.get('symptoms', [])
        prediction = predict_disease_service(symptoms)
        return jsonify({"success": True, "prediction": prediction})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/predict/diabetes', methods=['POST'])
def api_predict_diabetes():
    try:
        data = request.json
        prediction = predict_diabetes_service(data)
        return jsonify({"success": True, "prediction": prediction})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/predict/pneumonia', methods=['POST'])
def api_predict_pneumonia():
    try:
        file = request.files.get('file')
        prediction = predict_pneumonia_service(file)
        return jsonify({"success": True, "prediction": prediction})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/predict/brain', methods=['POST'])
def api_predict_brain():
    try:
        file = request.files.get('file')
        prediction = predict_brain_service(file)
        return jsonify({"success": True, "prediction": prediction})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/doctors', methods=['POST'])
def api_doctors():
    try:
        data = request.json
        city = data.get('city')
        disease = data.get('disease')

        result = get_doctors_service(city, disease)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')


# @app.route('/api/nutrition', methods=['POST'])
# def nutrition_api():
#     data = request.json
#     symptoms = data.get("symptoms", [])

#     # simple logic (you can improve later)
#     if "fatigue" in symptoms and "pale_skin" in symptoms:
#         result = {
#             "deficiency": "Iron Deficiency",
#             "foods": ["Spinach", "Red Meat", "Lentils", "Dates"]
#         }

#     elif "bone_pain" in symptoms:
#         result = {
#             "deficiency": "Vitamin D Deficiency",
#             "foods": ["Milk", "Eggs", "Sunlight", "Fish"]
#         }

#     elif "bleeding_gums" in symptoms:
#         result = {
#             "deficiency": "Vitamin C Deficiency",
#             "foods": ["Oranges", "Lemon", "Tomatoes"]
#         }

#     else:
#         result = {
#             "deficiency": "General Nutrient Deficiency",
#             "foods": ["Balanced Diet", "Fruits", "Vegetables"]
#         }

#     return jsonify({"success": True, "result": result})


@app.route('/api/nutrition', methods=['POST'])
def nutrition_api():
    data = request.json
    symptoms = data.get("symptoms", [])

    # Convert to set for faster matching
    symptoms = set(symptoms)

    # ---------------- VITAMINS ---------------- #

    if {"night_blindness", "dry_eyes"} & symptoms:
        result = {
            "deficiency": "Vitamin A Deficiency",
            "foods": ["Carrots", "Spinach", "Sweet Potato", "Mango"]
        }

    elif {"fatigue", "weakness"} <= symptoms:
        result = {
            "deficiency": "Vitamin B12 Deficiency",
            "foods": ["Eggs", "Fish", "Dairy Products"]
        }

    elif {"bleeding_gums", "slow_healing"} & symptoms:
        result = {
            "deficiency": "Vitamin C Deficiency",
            "foods": ["Oranges", "Lemon", "Amla", "Guava"]
        }

    elif {"bone_pain", "muscle_weakness"} & symptoms:
        result = {
            "deficiency": "Vitamin D Deficiency",
            "foods": ["Milk", "Egg Yolks", "Fish", "Sunlight"]
        }

    elif {"easy_bruising", "bleeding"} & symptoms:
        result = {
            "deficiency": "Vitamin K Deficiency",
            "foods": ["Spinach", "Broccoli", "Cabbage"]
        }

    elif {"hair_loss", "brittle_nails"} & symptoms:
        result = {
            "deficiency": "Vitamin B7 (Biotin) Deficiency",
            "foods": ["Eggs", "Nuts", "Seeds"]
        }

    # ---------------- MINERALS ---------------- #

    elif {"fatigue", "pale_skin"} <= symptoms:
        result = {
            "deficiency": "Iron Deficiency",
            "foods": ["Spinach", "Jaggery", "Red Meat", "Lentils"]
        }

    elif {"weak_bones", "muscle_cramps"} & symptoms:
        result = {
            "deficiency": "Calcium Deficiency",
            "foods": ["Milk", "Cheese", "Almonds", "Yogurt"]
        }

    elif {"muscle_cramps", "irregular_heartbeat"} & symptoms:
        result = {
            "deficiency": "Magnesium Deficiency",
            "foods": ["Nuts", "Seeds", "Whole Grains"]
        }

    elif {"hair_loss", "weak_immunity"} & symptoms:
        result = {
            "deficiency": "Zinc Deficiency",
            "foods": ["Pumpkin Seeds", "Meat", "Legumes"]
        }

    elif {"weight_gain", "fatigue"} & symptoms:
        result = {
            "deficiency": "Iodine Deficiency",
            "foods": ["Iodized Salt", "Seafood"]
        }

    elif {"muscle_weakness", "cramps"} & symptoms:
        result = {
            "deficiency": "Potassium Deficiency",
            "foods": ["Banana", "Potatoes", "Coconut Water"]
        }

    elif {"confusion", "nausea"} & symptoms:
        result = {
            "deficiency": "Sodium Deficiency",
            "foods": ["Salted Foods", "Electrolytes"]
        }

    elif {"weakness", "bone_pain"} & symptoms:
        result = {
            "deficiency": "Phosphorus Deficiency",
            "foods": ["Dairy", "Meat", "Nuts"]
        }

    # ---------------- DEFAULT ---------------- #

    else:
        result = {
            "deficiency": "General Nutrient Deficiency",
            "foods": ["Balanced Diet", "Fruits", "Vegetables"]
        }

    return jsonify({"success": True, "result": result})
# -------------------- MAIN --------------------

if __name__ == '__main__':
    app.run(debug=True)

