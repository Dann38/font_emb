import tensorflow as tf
from tensorflow.keras import layers, models


def mini_cnn():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28,28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='softmax'))
    return model


conv_models = []
for i in range(33):
    conv_models.append(mini_cnn())

merged_outputs = []
for model in conv_models:
    merged_outputs += model.outputs

dropout_layer = layers.Dropout(0.5)(merged_outputs)