import tensorflow as tf
model= tf.keras.models.load_model("Flag48.h5")
model.summary()
converter = tf.lite.TFLiteConverter.from_keras_model(model) # path to the SavedModel directory
tflite_model = converter.convert()

# Save the model.
with open('FAF48.tflite', 'wb') as f:
  f.write(tflite_model)