
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import os

# -------------------- LOAD MODEL --------------------
model = tf.keras.models.load_model("models/pneumonia_model.h5")

# 🔥 IMPORTANT: Initialize model (fixes Grad-CAM error)
model.predict(np.zeros((1, 150, 150, 3)))


# -------------------- FIND LAST CONV LAYER --------------------
def get_last_conv_layer(model):
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer
    return None


# -------------------- GRAD-CAM --------------------
def get_heatmap(img_array):
    last_conv_layer = get_last_conv_layer(model)

    grad_model = tf.keras.models.Model(
        inputs=model.input,
        outputs=[last_conv_layer.output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        loss = predictions[:, 0]   # binary model

    grads = tape.gradient(loss, conv_outputs)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = np.maximum(heatmap, 0)

    if np.max(heatmap) != 0:
        heatmap /= np.max(heatmap)

    return heatmap.numpy()


# -------------------- MAIN FUNCTION --------------------
def predict_pneumonia_service(file):

    if file is None:
        return {"result": "❌ No file uploaded"}

    # ✅ File validation
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return {"result": "❌ Please upload a valid image"}

    try:
        img = Image.open(file).convert("RGB")
    except:
        return {"result": "❌ Invalid image file"}

    # Preprocess
    img = img.resize((150, 150))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # -------------------- PREDICTION FIRST --------------------
    pred = model.predict(img_array)[0][0]
    print("Prediction:", pred)

    confidence = float(pred if pred > 0.5 else 1 - pred)

    # ❌ Reject unclear images
    if confidence < 0.60:
        return {
            "result": "⚠️ Please upload a clear chest X-ray",
            "confidence": round(confidence * 100, 2)
        }

    # -------------------- GRAD-CAM (SAFE) --------------------
    try:
        heatmap = get_heatmap(img_array)

        heatmap = cv2.resize(heatmap, (150, 150))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        original = np.array(img)
        overlay = cv2.addWeighted(original, 0.6, heatmap, 0.4, 0)

        os.makedirs("static/results", exist_ok=True)
        path = "static/results/result.jpg"
        cv2.imwrite(path, overlay)

    except Exception as e:
        print("Grad-CAM error:", e)
        path = None

    # -------------------- RESULT --------------------
    if pred > 0.5:
        if confidence < 0.70:
            severity = "Mild"
        elif confidence < 0.85:
            severity = "Moderate"
        else:
            severity = "Severe"

        precautions = [
            "Consult a doctor immediately",
            "Take proper rest",
            "Stay hydrated",
            "Avoid cold exposure",
            "Complete medications as prescribed"
        ]

        return {
            "result": "🫁 Pneumonia Detected",
            "confidence": round(confidence * 100, 2),
            "severity": severity,
            "image": "/" + path if path else None,
            "precautions": precautions
        }

    else:
        return {
            "result": "✅ Normal",
            "confidence": round(confidence * 100, 2),
            "severity": "None",
            "image": "/" + path if path else None,
            "precautions": ["Maintain healthy lifestyle"]
        }

