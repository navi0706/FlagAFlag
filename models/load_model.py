import tensorflow as tf
from tensorflow import lite
from tensorflow import keras


class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if (logs.get("val_accuracy")>0.97):
            #print("accuracy reached over 97% stopping training")
            self.model.stop_training= True
callbacks=myCallback()



model =  tf.keras.models.load_model("Flag48.h5")

model.summary()


training_dir="data/flags/training"
#testing_dir="data/flags/testing"
datagen = tf.keras.preprocessing.image.ImageDataGenerator(validation_split=0.20, rescale=1./255,
rotation_range=30, brightness_range=[0.4,1.6],
width_shift_range=0.1, height_shift_range=0.1)
#testing_datagen = ImageDataGenerator(rescale = 1./255)
      #width_shift_range=0.2, 
      #height_shift_range=0.2)



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

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(train_generator, epochs=200, validation_data = validation_generator, verbose = 1, callbacks=[callbacks])
model.save("Flag48.h5")

labels = '\n'.join(sorted(train_generator.class_indices.keys()))
with open('labels48.txt', 'w') as f:
    f.write(labels)
