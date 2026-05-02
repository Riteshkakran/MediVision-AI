# import tensorflow as tf
# # from tensorflow.keras import layers, models
# # from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import tensorflow as tf

# layers = tf.keras.layers
# models = tf.keras.models
# ImageDataGenerator = tf.keras.preprocessing.image.ImageDataGenerator

# import os

# DATASET_PATH = "dataset/brain_tumor"
# IMG_SIZE = (150, 150)
# BATCH_SIZE = 32

# # ---------------- DATA ----------------
# datagen = ImageDataGenerator(
#     rescale=1./255,
#     validation_split=0.2
# )

# train_data = datagen.flow_from_directory(
#     DATASET_PATH,
#     target_size=IMG_SIZE,
#     batch_size=BATCH_SIZE,
#     class_mode='categorical',
#     subset='training'
# )

# val_data = datagen.flow_from_directory(
#     DATASET_PATH,
#     target_size=IMG_SIZE,
#     batch_size=BATCH_SIZE,
#     class_mode='categorical',
#     subset='validation'
# )

# # ---------------- MODEL ----------------
# model = models.Sequential([
#     layers.Input(shape=(150,150,3)),

#     layers.Conv2D(32, (3,3), activation='relu'),
#     layers.MaxPooling2D(),

#     layers.Conv2D(64, (3,3), activation='relu'),
#     layers.MaxPooling2D(),

#     layers.Conv2D(128, (3,3), activation='relu'),
#     layers.MaxPooling2D(),

#     layers.Flatten(),
#     layers.Dense(128, activation='relu'),
#     layers.Dropout(0.5),

#     # 🔥 4 classes
#     layers.Dense(4, activation='softmax')
# ])

# model.compile(
#     optimizer='adam',
#     loss='categorical_crossentropy',
#     metrics=['accuracy']
# )

# # ---------------- TRAIN ----------------
# model.fit(
#     train_data,
#     validation_data=val_data,
#     epochs=10
# )

# # ---------------- SAVE ----------------
# os.makedirs("models", exist_ok=True)
# model.save("models/brain_tumor_model.h5")

# # class labels
# print(train_data.class_indices)

# print("✅ Brain tumor model saved!")


import tensorflow as tf
# from tensorflow.keras import layers, models
# from tensorflow.keras.preprocessing.image import ImageDataGenerator

layers = tf.keras.layers
models = tf.keras.models
ImageDataGenerator = tf.keras.preprocessing.image.ImageDataGenerator
import os

print("🔥 Brain Tumor Training Started")

# ---------------- PATHS (IMPORTANT FIX) ----------------
TRAIN_PATH = "dataset/brain_tumor/train"
VAL_PATH = "dataset/brain_tumor/test"

# ---------------- IMAGE PREPROCESSING ----------------
datagen = ImageDataGenerator(
    rescale=1./255
)

train_data = datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

val_data = datagen.flow_from_directory(
    VAL_PATH,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

print("Class Mapping:", train_data.class_indices)

# ---------------- MODEL ----------------
model = models.Sequential([
    layers.Input(shape=(150, 150, 3)),

    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),

    # 4 CLASSES OUTPUT
    layers.Dense(4, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("🔥 Training Started (Epochs Running)")

# ---------------- TRAINING ----------------
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=10
)

print("🔥 Training Completed")

# ---------------- SAVE MODEL ----------------
os.makedirs("models", exist_ok=True)
model.save("models/brain_tumor_model.h5")

print("✅ Model Saved Successfully!")
