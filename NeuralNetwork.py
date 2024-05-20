import numpy as np
from os.path  import join
from math import sqrt

def sigmoid(x):
    x = np.clip(x, -500, 500) # limit range of x to avoid overflow
    return 1.0 / (1.0 + np.exp(-x))

def relu(x):
    return max(x, 0)


def softmax(inputs):
    #print('softmax inputs', inputs)
    exp_scores = np.exp(inputs)
    #print('softmax exp:', exp_scores)
    probs = exp_scores / np.sum(exp_scores)
    #print('numpy sum', sum(np.sum(exp_scores, axis=1, keepdims=True)))
    #print('probs:', probs)
    return probs



class Perceptron:
    def __init__(self, n):
    
        # number of nodes in the previous laye
        # calculate the range for the weights
        std = sqrt(2.0 / n)
        # generate random numbers
        numbers = np.random.randn(n)
        # scale to the desired range
        self.weights = numbers * std
        self.bias = 0

        #print('rand weights test:', self.weights)

class DenseLayer:
    def __init__(self, n, weightShape, activation):
        self.activation  = activation
        self.neurons = []
        self.count = n
        for i in range(n):
            self.neurons.append(Perceptron(weightShape))
        
        #for row in self.neurons:
            #for neuron in row:
                #print(neuron.weights, neuron.bias)

    def calculateOutputs(self, inputs):
        output = np.zeros(self.count)

        if self.activation == 'sigmoid' or self.activation == 'relu':
            for i, neuron in enumerate(self.neurons):

                temp = np.sum(np.dot(inputs, neuron.weights)) + neuron.bias
                match self.activation:
                    case 'sigmoid':
                        output[i] = sigmoid(temp)

                    case 'relu':
                        output[i] = relu(temp)

        elif self.activation == 'softmax':
            for i, neuron in enumerate(self.neurons):
                temp = np.sum(np.dot(inputs, neuron.weights)) + neuron.bias
                output[i] = temp

            output = softmax(output)

        else:
            raise KeyError('Invalid Activation Function')

        return output

    def shape(self) -> tuple:
        return (len(self.neurons))
    
    def print(self) -> None:
        for neuron in self.neurons:
            print(f'Neuron Weight: {neuron.weights}')
            print(f'Neuron Bias: {neuron.bias}')

class NeuralNetwork:
    def __init__(self):
        self.layers = []

    def addLayer(self, layer):
        self.layers.append(layer)

    def forwardPropagate(self, input):
        for i, layer in enumerate(self.layers):
            print('i', i)
            if i == 0:
                print('network input:', input)
            input = layer.calculateOutputs(input)

        return input
    


