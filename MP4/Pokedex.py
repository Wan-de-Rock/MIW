import pandas as pd
import matplotlib.pyplot as plt
import os
import keras as ks

from keras.preprocessing.image import ImageDataGenerator
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.compat.v1 import ConfigProto

def get_data(description_file, image_folder):
    pokedex = pd.read_csv(description_file, usecols=range(2))
    pokedex.sort_values(by=['Name'], ascending=True, inplace=True)

    images = sorted(os.listdir(image_folder))
    images = list(map(lambda image_file: os.path.join(image_folder, image_file), images))
    pokedex['Image'] = images
    return pokedex

def prepare_data_for_network(pokedex):
    data_generator = ImageDataGenerator(validation_split=0.1, rescale=1.0 / 255)
    train_generator = data_generator.flow_from_dataframe(pokedex,
                                                         x_col='Image',
                                                         y_col='Type1',
                                                         subset='training',
                                                         color_mode='rgba',
                                                         class_mode='categorical')
    return train_generator


def fix_gpu():
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
fix_gpu()

def main():
    dirname, filename = os.path.split(os.path.abspath(__file__))
    dataPath = os.path.join(dirname, 'data')
    resultPath = os.path.join(dirname, 'result')

    if not os.path.exists(resultPath):
        os.mkdir(resultPath)

    epochs = 2
    steps = 23

    pokedex = get_data(os.path.join(dataPath, 'pokemon.csv'), os.path.join(dataPath, 'images'))
    generator = prepare_data_for_network(pokedex)
    model = ks.models.Sequential()
    model.add(ks.layers.Conv2D(34, (3, 3),
                               activation='relu',
                               input_shape=(256, 256, 4)))
    model.add(ks.layers.MaxPooling2D(2, 2))
    model.add(ks.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(ks.layers.MaxPooling2D(2, 2))
    model.add(ks.layers.Flatten())
    model.add(ks.layers.Dense(128, activation='relu'))
    model.add(ks.layers.Dense(18, activation='softmax'))
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['acc'])
    print(model.summary())

    history = model.fit_generator(generator, epochs=epochs, steps_per_epoch=steps)

    plt.plot(history.history['acc'])
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.savefig(os.path.join(resultPath, 'train_history.png'))

if __name__ == '__main__':  
    main()