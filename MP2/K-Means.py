import os
from turtle import clone
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import davies_bouldin_score


def enterPositiveInteger():
    print("Enter a non-negative integer: ")
    try:
        number = int(input())
        if number < 1:
            return enterPositiveInteger()       
    except:
        return enterPositiveInteger()
    
    return number

def euclideanDistance(vector1, vector2):
    sum = 0
    for i in range(len(vector1)):
        sum += ((vector1[i] - vector2[i]) * (vector1[i] - vector2[i]))

    return np.sqrt(sum)

def generateCentroids(data, number):
    list = []
    centroids = []

    for k in data.keys():
        m = max(data[k])
        random_list  = np.random.uniform(0, m, number)
        list.append(random_list)

    list = np.transpose(list)

    for i in range(len(list)):
        centroids.append(Centroid(i, list[i]))

    return centroids

def k_means(data, centroids):
    numberOfClusters = len(centroids)
    colors = [np.random.random(3) for k in range(numberOfClusters)]

    while(True):
        hasChanged = False
        
        for point in range(len(data)):
            for centroid in centroids:
                distance = euclideanDistance(data.iloc[point, :3].values, centroid.vector)

                if(data['Distance'].get(point) > distance):
                    data['Distance'].values[point] = distance
                    data['Centroid'].values[point] = centroid.name
                    data['Color'].values[point] = colors[centroid.name]

                    hasChanged = True
            
            centroids[data['Centroid'].values[point]].numberOfRelations += 1
            centroids[data['Centroid'].values[point]].sumOfPoints += data.iloc[point, :3].values
                           
        if(hasChanged == False):
            break

        for centroid in centroids:
            if (centroid.numberOfRelations == 0):
                continue

            centroid.vector = centroid.sumOfPoints / centroid.numberOfRelations
            centroid.sumOfPoints = np.zeros(len(centroid.vector), 'O')
            centroid.numberOfRelations = 0

class Centroid:
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector
        self.numberOfRelations = 0
        self.sumOfPoints = np.zeros(len(vector), 'O')
    
    def __str__(self):
        return str(self.name) + '  ' + str(self.vector)


def main():

    dirname, filename = os.path.split(os.path.abspath(__file__))
    dataPath = os.path.join(dirname, 'data')
    resultPath = os.path.join(dirname, 'result')

    # Distance A  Distance B  Distance C  Position X  Position Y
    data = pd.read_csv(os.path.join(dataPath, 'beacon_readings.csv'), usecols=range(5))
    data['Position X'] = data.apply(lambda row : row['Position X'] + np.random.randint(-9, 9), axis = 1)
    data['Position Y'] = data.apply(lambda row : row['Position Y'] + np.random.randint(-9, 9), axis = 1)
    data['Centroid'] = int
    data['Distance'] = np.double('inf')
    data['Color'] = [np.zeros(3) for i in range(len(data))]

    if not os.path.exists(resultPath):
        os.mkdir(resultPath)

    results = {}
    bestByIndex = 2
    fileWriter = open(os.path.join(resultPath, 'score.txt'), 'w')
    for numberOfClusters in range(2,11):
        centroids = generateCentroids(data.iloc[:, :3], numberOfClusters)
        k_means(data, centroids)
        index = davies_bouldin_score(data.iloc[:, [0,1,2]], data['Centroid'])

        fileWriter.write(f'{numberOfClusters} clusters -> {index}\n')
        results.update({numberOfClusters: index})

        if results[bestByIndex] > index:
            bestByIndex = numberOfClusters

        data['Centroid'] = int
        data['Distance'] = np.double('inf')
        data['Color'] = [np.zeros(3) for i in range(len(data))]

    fileWriter.close()
    centroids = generateCentroids(data.iloc[:, :3], bestByIndex)
    k_means(data, centroids)

    print(data.iloc[:, [0,1,2,5,6]].to_string())  
    print(bestByIndex)
    plt.scatter(data['Position X'], data['Position Y'], c=data['Color'])
    plt.xlabel('Position X')
    plt.ylabel('Position Y')
    plt.savefig(os.path.join(resultPath, 'clusters_visualisation.png'))

    # plt.plot(list(results.keys()), list(results.values()))
    # plt.xlabel("Number of clusters")
    # plt.ylabel("Davies-Boulding Index")
    # plt.show()


if __name__ == '__main__':
    main()
