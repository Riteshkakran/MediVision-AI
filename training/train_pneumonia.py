
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os

# -------------------- PATH --------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "chest_xray")

# -------------------- DATA GENERATOR --------------------

train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = train_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, "train"),
    target_size=(150,150),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

val_data = train_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, "train"),
    target_size=(150,150),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

# -------------------- MODEL --------------------

model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# -------------------- TRAIN --------------------

model.fit(
    train_data,
    validation_data=val_data,
    epochs=5
)

# -------------------- SAVE MODEL --------------------

os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

model.save(os.path.join(BASE_DIR, "models", "pneumonia_model.h5"))

print("Model saved successfully!")

