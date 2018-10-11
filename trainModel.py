import numpy as np
import os
import keras
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping, ModelCheckpoint, CSVLogger
from keras.optimizers import *
from keras import regularizers



def get_labels(path):
    labels = [file.replace('.npy', '') for file in os.listdir(path) if file.endswith('.npy')]
    label_indices = np.arange(0, len(labels))
    return labels, label_indices, to_categorical(label_indices)

def get_train_test(train_ratio, pathData):
    labels, _, _ = get_labels(pathData)
    classNumber = 0
    X = data = np.load(pathData + '\\' + labels[0] + '.npy')
    Y = np.zeros(X.shape[0])
    dimension = X[0].shape
    for i, label in enumerate(labels[1:]):
        data = np.load(pathData + '\\' + label + '.npy')
        X = np.vstack((X, data))
        Y = np.append(Y, np.full(data.shape[0], fill_value=(i)))
        classNumber += 1

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=train_ratio)

    te = np.asarray(X_train)
    te2 = np.asarray(X_test)

    te3 = np.asarray(Y_train)
    te4 = np.asarray(Y_test)

    print('DIMENSION X TRAIN ' + str(te.shape))
    print('DIMENSION X TEST ' + str(te2.shape))
    print('DIMENSION Y TRAIN ' + str(te3.shape))
    print('DIMENSION Y TEST ' + str(te4.shape))

    return X_train, X_test, to_categorical(Y_train), to_categorical(Y_test), classNumber, dimension


def main():
    pathData = '.\\numpy'
    trainRatio = 0.8
    epochs = 1000
    batch_size = 16
    earlyStopPatience = 2
    model_name = 'AlexNet'

    csv_logger = CSVLogger('.\\logs\\log.csv', append=True, separator=',')
    early = EarlyStopping(monitor='val_loss', min_delta=0, patience=earlyStopPatience, verbose=0, mode='auto')
    check = ModelCheckpoint('.\\trainedModel\\model_{}.hdf5'.format(model_name), monitor='val_loss', verbose=0,
                            save_best_only=True, save_weights_only=False, mode='auto')


    x_train, x_test, y_train, y_test, classNumber, dimension = get_train_test(trainRatio, pathData)

    #x_train = x_train.astype(np.float32).reshape(x_train.shape[0], dimension[0], dimension[1], dimension[2])
    #x_test = x_test.astype(np.float32).reshape(x_test.shape[0], dimension[0], dimension[1], dimension[2])
    print('DIMENSION X TRAIN ' + str(x_train.shape))
    print('DIMENSION X TEST ' + str(x_test.shape))
    print('DIMENSION Y TRAIN ' + str(y_train.shape))
    print('DIMENSION Y TEST ' + str(y_test.shape))



    model = Sequential()


    
    
    model.add(
        Conv2D(96, padding='same', kernel_size=(11, 11), strides=3, kernel_initializer='glorot_uniform',
               activation='elu',
               input_shape=(dimension[0], dimension[1], dimension[2])))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=2))

    #model.add(Conv2D(256, padding='same', kernel_size=(5, 5), strides=1, kernel_initializer='glorot_uniform',
#                     activation='elu'))
    #model.add(MaxPooling2D(pool_size=(3, 3), strides=2))

    #model.add(Conv2D(384, padding='same', kernel_size=(3, 3), strides=1, kernel_initializer='glorot_uniform',
       #              activation='elu'))
    #model.add(Conv2D(384, padding='same', kernel_size=(3, 3), strides=1, kernel_initializer='glorot_uniform',
      #               activation='elu'))
    #model.add(Conv2D(256, padding='same', kernel_size=(3, 3), strides=1, kernel_initializer='glorot_uniform',
     #                activation='elu'))
    #model.add(MaxPooling2D(pool_size=(3, 3), strides=2))


    # Flatten layer -> matrix to vector
    model.add(Flatten())
    model.add(Dropout(0.5))

    model.add(Dense(4096, kernel_initializer='glorot_uniform', activation='elu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, kernel_initializer='glorot_uniform', activation='elu'))
    model.add(Dense(classNumber, kernel_initializer='glorot_uniform', activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adamax(lr=0.001, beta_1=0.9, beta_2=0.999, decay=0.0),
                  metrics=['accuracy'])

    trainning = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
					validation_data=(x_test, y_test), callbacks=[early, check,csv_logger])

# MAIN
if __name__ == "__main__":
    main()