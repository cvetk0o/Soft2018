# 3. Import libraries and modules
import numpy as np
np.random.seed(123)  # for reproducibility
 
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from keras.optimizers import SGD



def pripremiY(podaci):
    pomocni=np.zeros((len(podaci),10))
    for i in range(len(podaci)):
        pomocni1=pomocni[i]
        pomocni1[podaci[i]]=1
        pomocni[i]=pomocni1
    return pomocni
        

    
def display_result(outputs, alphabet):
    '''za svaki rezultat pronaći indeks pobedničkog
        regiona koji ujedno predstavlja i indeks u alfabetu.
        Dodati karakter iz alfabet u result'''
    result = []
    for output in outputs:
        result.append(alphabet[winner(output)])
    return result

def winner(output): # output je vektor sa izlaza neuronske mreze
    '''pronaći i vratiti indeks neurona koji je najviše pobuđen'''
    return max(enumerate(output), key=lambda x: x[1])[0]

    
# 4. Load pre-shuffled MNIST data into train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()
 

X_train = X_train.reshape((X_train.shape[0], 784))
X_train = X_train.astype('float32') / 255
X_test = X_test.reshape((X_test.shape[0], 784))
X_test = X_test.astype('float32') / 255

y_train=pripremiY(y_train)
y_test=pripremiY(y_test)





#pravljenje neuronske

ann = Sequential()
ann.add(Dense(128, input_dim=784, activation='sigmoid'))
ann.add(Dense(10, activation='sigmoid'))


 # definisanje parametra algoritma za obucavanje
sgd = SGD(lr=0.01, momentum=0.9)
ann.compile(loss='mean_squared_error', optimizer=sgd,metrics=['accuracy'])

    # obucavanje neuronske mreze
ann.fit(X_train, y_train, epochs=25, batch_size=10, validation_data=(X_test, y_test)) 


result = ann.predict(np.array(X_test[2:10], np.float32))
print(result)

ann.save("neuronskaMreza.h5")


def loadModel():
    model = None
    try:
        model = load_model('neuronskaMreza.h5')
        if model is None:
            (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
            model = cnn_model(x_train,x_test,y_train,y_test)
            return model
    except NameError:
        print('Cant find model')
    
    return model 



