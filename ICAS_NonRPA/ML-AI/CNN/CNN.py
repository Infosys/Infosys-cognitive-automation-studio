'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import numpy as np
import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.utils import to_categorical

from sklearn.externals import joblib

from mlxtend.data import loadlocal_mnist

from abstract_bot import Bot


class CNN(Bot):


    def execute(self, executeContext):
        try:
            train_images_fp = executeContext['train_images_file_path']
            train_labels_fp = executeContext['train_labels_file_path']
            test_images_fp = executeContext['test_images_file_path']
            test_labels_fp = executeContext['test_labels_file_path']
            model_file_name = executeContext['model_file_name']
            model_file_path = executeContext['model_file_path']

            train_images, train_labels = loadlocal_mnist(
                        images_path=train_images_fp, 
                        labels_path=train_labels_fp)
            test_images, test_labels = loadlocal_mnist(
                        images_path=test_images_fp, 
                        labels_path=test_labels_fp)

            # --Reshaping the image to 2 dimension-- 
            train_images = train_images.reshape(train_images.shape[0], 28, 28).astype('float32')
            test_images = test_images.reshape(test_images.shape[0], 28, 28).astype('float32')

            # Normalize the images.
            train_images = (train_images / 255) - 0.5
            test_images = (test_images / 255) - 0.5

            # Reshape the images.
            train_images = np.expand_dims(train_images, axis=3)
            test_images = np.expand_dims(test_images, axis=3)

            num_filters = 8
            filter_size = 3
            pool_size = 2

            # Build the model.
            model = Sequential()
            # model = Sequential([
            # Conv2D(num_filters, filter_size, input_shape=(28, 28, 1)),
            # MaxPooling2D(pool_size=pool_size),
            # Flatten(),
            # Dense(10, activation='softmax'),
            # ])
            model.add(Conv2D(num_filters, filter_size, input_shape=(28, 28, 1)))
            model.add(MaxPooling2D(pool_size=pool_size))
            model.add(Flatten())
            model.add(Dense(10, activation='softmax'))

            # Compile the model.
            model.compile('adam',loss='categorical_crossentropy',metrics=['accuracy'],)

            # Train the model.
            model.fit(train_images,to_categorical(train_labels),epochs=3,validation_data=(test_images, to_categorical(test_labels)),)

            
            # serialize model to JSON
            model_json = model.to_json()
            with open("model.json", "w") as json_file:
                json_file.write(model_json)
            # serialize weights to HDF5
            model.save_weights(model_file_path + '\\'+ model_file_name + ".h5")
            print("Saved model to disk")
            
            # Creating directory to store model file, if it does not exist
            #if not os.path.exists(model_file_path):
            #    os.makedirs(model_file_path)

            
            
            #joblib.dump(model_file, model_file_path + '\\' +  model_file_name + '.h5')

            # Predict on the first 5 test images.
            # predictions = model.predict(test_images[:5])

            # Print our model's predictions.
            # print(np.argmax(predictions, axis=1)) # [7, 2, 1, 0, 4]

            # Check our predictions against the ground truths.
            # print(test_labels[:5]) # [7, 2, 1, 0, 4]
            return {"Status":"success"}
        except Exception as e:
            print('Exception : ',str(e))
            return {"Status":"Failure"}


if __name__ == '__main__':
    context = {}
    bot_obj = CNN()

    # --input parameters--
    # context = {'train_images_file_path':'D:\\Bot_Factory\\testedbots\\CNN\\CNN\\CNN_dataset_and_test-files\\train-images.idx3-ubyte', 
    # 'train_labels_file_path':'D:\\Bot_Factory\\testedbots\\CNN\\CNN\\CNN_dataset_and_test-files\\train-labels.idx1-ubyte', 
    # 'test_images_file_path':'D:\\Bot_Factory\\testedbots\\CNN\\CNN\\CNN_dataset_and_test-files\\t10k-images.idx3-ubyte', 
    # 'test_labels_file_path':'D:\\Bot_Factory\\testedbots\\CNN\\CNN\\CNN_dataset_and_test-files\\t10k-labels.idx1-ubyte', 
    # 'model_file_name':'CNN_model_file',  
    # 'model_file_path':'D:\\Bot_Factory\\testedbots'}

    context = {'train_images_file_path':'', 
    'train_labels_file_path':'', 
    'test_images_file_path':'', 
    'test_labels_file_path':'', 
    'model_file_name':'',  
    'model_file_path':''}

    resp = bot_obj.execute(context)
    print('response : ',resp)
