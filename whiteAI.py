from tensorflow import keras
import tensorflow as tf
from tensorflow.keras import layers,models
import os
import numpy as np
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
import time
from sklearn.utils import class_weight

#Getting images from our pieces folders


labels = ['wRook', 'wQueen','wPawn','wKnight','wKing','wBishop']

img_size = 50
def get_data(data_dir):
    data = [] 
    for label in labels: 
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img))[...,::-1] #convert BGR to RGB format
                resized_arr = cv2.resize(img_arr, (img_size, img_size)) # Reshaping images to preferred size
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)

train = get_data('pieces/')

#putting it into array for our model

x_train = []
y_train = []

for feature, label in train:
  x_train.append(feature)
  y_train.append(label)

# Normalize the data
x_train = np.array(x_train) / 255
x_train.reshape(-1, img_size, img_size, 1)
y_train = np.array(y_train)

class_weights = class_weight.compute_class_weight('balanced',
                                                 np.unique(y_train),
                                                 y_train)


model = keras.Sequential(
    [
        keras.Input(shape=(50,50,3)),
        layers.Conv2D(50, kernel_size=(5, 5), activation="relu", padding="valid"),
        layers.Conv2D(100, kernel_size=(3, 3), activation="relu",padding='valid'),
        layers.Flatten(),
        layers.Dense(6, activation="softmax"),
    ]
)


model.summary()

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=keras.optimizers.SGD(lr=0.0003,momentum=0.9,nesterov=True),
    metrics=["accuracy"],
)

history = model.fit(x_train, y_train, batch_size=500, epochs=100, shuffle = True,class_weight=dict(zip(np.unique(y_train), class_weight.compute_class_weight('balanced', np.unique(y_train), 
                y_train))) )

model.save("whitePieces")

while True:

    choice = np.random.randint(0,4000)

    convertor = (dict(enumerate(labels))) 

    model = keras.models.load_model("whitePieces")

    eval = model.predict(x_train[choice].reshape(1,50,50,3))

    eval = eval[0].tolist()
    maxValue = max(eval)

    print(convertor[eval.index(maxValue)])

    plt.imshow(x_train[choice])
    plt.show()
