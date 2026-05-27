# import tensorflow as tf
# import numpy as np
# from PIL import Image

# model = tf.keras.models.load_model("models/brain_tumor_model.h5")

# # class labels (IMPORTANT)
# classes = ['glioma', 'meningioma', 'no_tumor', 'pituitary']

# model.predict(np.zeros((1,150,150,3)))  # init

# def predict_brain_service(file):

#     if file is None:
#         return {"result": "❌ No file uploaded"}

#     img = Image.open(file).convert("RGB")
#     img = img.resize((150,150))

#     img_array = np.array(img) / 255.0
#     img_array = np.expand_dims(img_array, axis=0)

#     preds = model.predict(img_array)[0]

#     class_index = np.argmax(preds)
#     confidence = float(np.max(preds))

#     if confidence < 0.60:
#         return {
#             "result": "⚠️ Upload a clear MRI scan",
#             "confidence": round(confidence * 100, 2)
#         }

#     return {
#         "result": f"🧠 {classes[class_index].replace('_',' ').title()} Detected",
#         "confidence": round(confidence * 100, 2),
#         "type": classes[class_index]
#     }