import tensorflow as tf


class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get("val_acc")>0.94):
            self.model.stop_training= True
callbacks=myCallback()





model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Conv2D(32, (3,3), activation="relu"),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(32, (3,3), activation="relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Conv2D(32, (3,3), activation="relu"),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(32, (3,3), activation="relu"),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Conv2D(32, (3,3), activation="relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation="relu"),
    tf.keras.layers.Dropout(0.35),
    tf.keras.layers.Dense(48, activation='softmax')
 ])

model.summary()


training_dir="data/flags/training"

datagen = tf.keras.preprocessing.image.ImageDataGenerator(validation_split=0.20, rescale=1./255,
rotation_range=30, brightness_range=[0.2,1.8],
width_shift_range=0.2, height_shift_range=0.2)



train_generator = datagen.flow_from_directory(
	training_dir,
    subset='training',
	target_size=(224,224),
	class_mode="categorical",
    shuffle=True,
    batch_size=64
)

validation_generator = datagen.flow_from_directory(
	training_dir,
    subset='validation',
	target_size=(224,224),
	class_mode="categorical",
    shuffle=True,
    batch_size=64
)
#optimizer = keras.optimizers.Adam(lr=0.01)

model.compile(optimizer="Adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(train_generator, epochs=100, validation_data = validation_generator,
 verbose = 1, callbacks=[callbacks],)
model.save("Flag48.h5")


labels = '\n'.join(sorted(train_generator.class_indices.keys()))
with open('labels48TEST.txt', 'w') as f:
    f.write(labels)
