import datetime

import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras.layers import Dense, Flatten, MaxPooling2D, Dropout, Conv2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator


generator = ImageDataGenerator(rescale=1. / 255, width_shift_range=0.1, height_shift_range=0.1)
train_generator = generator.flow_from_directory('data/train', target_size=(28, 28), batch_size=1,
                                                class_mode='categorical')

validation_generator = generator.flow_from_directory('data/val', target_size=(28, 28), class_mode='categorical')

model = Sequential()
model.add(Conv2D(32, (24, 24), input_shape=(28, 28, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.4))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(36, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(lr=0.00001), metrics=['accuracy'])

batch_size = 1

model.fit_generator(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size,
    epochs=60)
