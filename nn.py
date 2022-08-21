import math
import numpy as np


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        self.weights = []
        self.biasis = []

        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i + 1], layer_sizes[i])
            b = np.zeros((layer_sizes[i + 1], 1))
            
            self.weights.append(w)
            self.biasis.append(b)

    def sigmoid(self,z):
        try:
            res = 1 / (1 + math.exp(-z))
        except:
            res = 0
        return res

    def activation(self, x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        if x>0:
            return self.sigmoid(x)
        else:
            return 1 - self.sigmoid(x)

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """ 

        arr_a = []
        arr_z = []

        a = x.copy()
        activation_function = np.vectorize(self.activation)

        for i in range(len(self.weights)):
            x = x.reshape(len(x),1)
            z = (self.weights[i] @ a) + self.biasis[i]
            a = activation_function(z)

            arr_a.append(a)
            arr_z.append(z)
        
        return a