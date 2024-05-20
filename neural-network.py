import numpy as np
from os.path  import join
from math import sqrt

def sigmoid(x):
    x = np.clip(x, -500, 500) # limit range of x to avoid overflow
    return 1.0 / (1.0 + np.exp(-x))

def relu(x):
    return max(x, 0)


def softmax(inputs):
    print('softmax inputs', inputs)
    exp_scores = np.exp(inputs)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    #print('numpy sum', sum(np.sum(exp_scores, axis=1, keepdims=True)))
    #print('probs:', probs)
    return probs

def relu_derivative(self, dA, Z):
    dZ = np.array(dA, copy = True)
    dZ[Z <= 0] = 0
    return dZ


def CategoricalCrossEntropyLoss(prediction, desired) -> float:
    if len(prediction[0])!= len(desired[0]):
        raise ValueError('Unequal output shape')
    
    loss = 0.
    #print('prediction initial', prediction)
    print('desired', desired)
    for i, output in enumerate(prediction[0]):
        output = float(output)
        #print('output', output)
        #print('np.log(output):', np.log(output))
        tempLoss = np.log(output) * desired[0][i]
        if tempLoss != [np.nan]:
            #print('temploss not nan:', tempLoss)
            loss -= tempLoss
    
    print('CategoricalCrossEntropyLoss loss:', loss)
    return loss



class Perceptron:
    def __init__(self, weightShape: tuple):
    
        # number of nodes in the previous layer
        n = weightShape[0] * weightShape[1]
        # calculate the range for the weights
        std = sqrt(2.0 / n)
        # generate random numbers
        numbers = np.random.randn(weightShape[0], weightShape[1])
        # scale to the desired range
        self.weights = numbers * std
        self.bias = 0



        #print('rand weights test:', self.weights)

class DenseLayer:
    def __init__(self, width, height, weightShape, activation):
        self.activation  = activation
        self.neurons = []
        self.shape = (width, height)
        for i in range(width):
            tempArray = []
            for j in range(height):
                tempArray.append(Perceptron(weightShape))
            self.neurons.append(tempArray)
        
        #for row in self.neurons:
            #for neuron in row:
                #print(neuron.weights, neuron.bias)

    def calculateOutputs(self, inputs):
        output = np.zeros(self.shape)
    
        if self.activation == 'sigmoid' or self.activation == 'relu':
            for i, row in enumerate(self.neurons):
                for j, neuron in enumerate(row):
                    temp = np.sum(np.dot(inputs, neuron.weights)) + neuron.bias
                    match self.activation:
                        case 'sigmoid':
                            output[i][j] = sigmoid(temp)

                        case 'relu':
                            output[i][j] = relu(temp)

        elif self.activation == 'softmax':
            for i, row in enumerate(self.neurons):
                for j, neuron in enumerate(row):
                    temp = np.sum(np.dot(inputs, neuron.weights)) + neuron.bias
                    output[i][j] = temp

            output = softmax(output)

        else:
            raise KeyError('Invalid Activation Function')

        return output

    def shape(self) -> tuple:
        return (len(self.neurons), len(self.neurons[0]))
    
    def print(self) -> None:
        for row in self.neurons:
            for neuron in row:
                print(f'Neuron Weight: {neuron.weights}')
                print(f'Neuron Bias: {neuron.bias}')

class NeuralNetwork:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.learningRate = None

    def addLayer(self, layer):
        self.layers.append(layer)

    def forwardPropagate(self, input):
        for i, layer in enumerate(self.layers):
            print('i', i)
            if i == len(self.layers) - 1:
                print('layer input:', input)
            input = layer.calculateOutputs(input)

        return input

    def backpropagate(self, result, desired):
        loss = CategoricalCrossEntropyLoss(result, desired)

        return loss


def main():

    input_path = 'data/mnist/'
    training_images_filepath = join(input_path, 'train-images-idx3-ubyte/train-images-idx3-ubyte')
    training_labels_filepath = join(input_path, 'train-labels-idx1-ubyte/train-labels-idx1-ubyte')
    test_images_filepath = join(input_path, 't10k-images-idx3-ubyte/t10k-images-idx3-ubyte')
    test_labels_filepath = join(input_path, 't10k-labels-idx1-ubyte/t10k-labels-idx1-ubyte')


    mnistDataloader = MnistDataloader(training_images_filepath, training_labels_filepath, test_images_filepath, test_labels_filepath)
    (x_train, y_train), (x_test, y_test) = mnistDataloader.load_data()

    tempList = np.array(x_train[0])

    print(tempList.shape)

    testNet = NeuralNetwork()
    inputs = tempList
    testNet.addLayer(DenseLayer(28, 28, weightShape=(28, 28), activation='sigmoid'))
    testNet.addLayer(DenseLayer(10, 10, weightShape=(28, 28), activation='sigmoid'))
    testNet.addLayer(DenseLayer(1, 10, weightShape=(10, 10), activation='softmax'))
    result = testNet.forwardPropagate(inputs)
    ind = np.unravel_index(np.argmax(result, axis=None), result.shape)

    print('Predicted class: ', ind[1])
    print('maximum:', max(result[0]))
    
    print('Actual class', y_train[0])
    
    backPropArray = np.array([np.zeros(10)])
    backPropArray[0][y_train[0] - 1] = 1
    print('result:', result)


    loss = testNet.backpropagate(result, backPropArray)

    #for layer in testNet.layers:
        #layer.print()
   

if __name__ == '__main__':
    main()