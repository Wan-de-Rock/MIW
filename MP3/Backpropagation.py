import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_data(path):
    
    # Distance A  Distance B  Distance C  Position X  Position Y
    dataset = pd.read_csv(os.path.join(path, 'beacon.csv'))
    
    observation = dataset.iloc[:,:-2].to_numpy().T # A B C

    classification = dataset.iloc[:,[-2,-1]].to_numpy() # X Y
    categoryIndexes = np.unique(classification, return_index=True, axis=0)[1] 
    categories = np.array([classification[index] for index in sorted(categoryIndexes)]) # X Y unique

    classificationTyple = [tuple(x) for x in classification] # X Y
    categoriesTyple = [tuple(x) for x in categories] # X Y unique
     
    category_indexer = dict(enumerate(categoriesTyple)) # 0..N — (X Y)
    category_indexer_reversed = dict((v, k) for k, v in category_indexer.items()) # (X Y) — 0..N

    classification = np.array([category_indexer_reversed[x] for x in classificationTyple])

    one_hot_decoder = np.eye(categories.shape[0])
    classification = one_hot_decoder[classification].T

    return observation, classification, category_indexer

def print_classifications(classifications, decoder):
    classifications = classifications.argmax(axis=0)
    for observation_id, classification in enumerate(classifications):
        print(f"#{observation_id} —> {decoder[classification]}")

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    y = sigmoid(x)
    return y * (1.0 - y)

def mse(result, expected):
    return np.mean((result-expected)**2)
    #return np.sum((result-expected)**2)/len(result)

def initialize_network(n_inputs, n_hidden, n_outputs):
	network = []
	network.append(np.random.rand(n_hidden, n_inputs+1)*2-1)
	network.append(np.random.rand(n_outputs, n_hidden+1)*2-1)
	return network

def activate(network, observation):
    responses = []
    layer_input = observation
    for layer in network:
        layer_input = np.append(layer_input, np.ones([1,layer_input.shape[1]]), 0)
        response = sigmoid(layer@layer_input)
        responses.append(response)
        layer_input = response
        classification = responses[-1]
    return classification, responses

def calculate_error_gradients(network, responses, expected_classification):  
    gradients = []
    error = responses[-1] - expected_classification
    for layer, response in zip(reversed(network), reversed(responses)):
        gradient = error + sigmoid_derivative(response)
        gradients.append(gradient)
        error = layer.T@gradient
        error = error[1:,:]
    return reversed(gradients)

def calculate_weight_changes(network, observation, responses, gradients, learning_factor):
    layer_inputs = [observation] + responses[:-1]
    weight_changes = []
    for layer, layer_input, gradient in zip(network, layer_inputs, gradients):
        layer_input = np.append(layer_input, np.ones([1,layer_input.shape[1]]), 0)
        change = layer_input@gradient.T*learning_factor
        weight_changes.append(change.T)
    return weight_changes

def adjust_weights(network, weight_changes):
    new_network = []
    for layer, adjustment in zip(network, weight_changes):
        new_layer = layer - adjustment
        new_network.append(new_layer)
    return new_network

def fit(network, observation, expected_classification, learning_factor, epochs):
    for epoch in range(epochs):
        classification, responses = activate(network, observation)
        print(f"Epoch: {epoch} —> mse value: {mse(classification, expected_classification)}")
        gradients = calculate_error_gradients(network, responses, expected_classification)
        weight_changes = calculate_weight_changes(network, observation, responses, gradients, learning_factor)
        network = adjust_weights(network, weight_changes)
    print(f"Epoch: {epochs} —> mse value: {mse(classification, expected_classification)}")
    return classification

def main():

    dirname, filename = os.path.split(os.path.abspath(__file__))
    dataPath = os.path.join(dirname, 'data')
    resultPath = os.path.join(dirname, 'result')

    observation, classification, category_indexer = get_data(dataPath)

    n_hidden = 5
    learning_factor = 0.1
    epochs = 20

    network = initialize_network(observation.shape[0], n_hidden, classification.shape[0])
    # print(network.T)
    # print(observation.T)
    classification = fit(network, observation, classification, learning_factor, epochs)
    print_classifications(classification, category_indexer)
   # print(classification.T)


    
    


if __name__ == '__main__':
    main()
