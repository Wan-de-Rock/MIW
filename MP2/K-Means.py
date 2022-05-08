import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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

    #return np.sqrt(sum)
    return sum

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

def k_means(data, numberOfClusters):
    centroids = generateCentroids(data.iloc[:, :3], numberOfClusters)   
    colors = [np.random.random(3) for k in range(numberOfClusters)]

    while(True):
        hasChanged = False
        
        for point in range(len(data)):
            for centroid in centroids:
                distance = euclideanDistance(data.iloc[point, :3].values, centroid.vector)

                if(data['Distance'].get(point) > distance):
                    data['Distance'].values[point] = distance
                    data['Centroid'].values[point] = centroid
                    data['Color'].values[point] = colors[centroid.name]

                    hasChanged = True
            
            data['Centroid'].values[point].numberOfRelations += 1
            data['Centroid'].values[point].sumOfPoints += data.iloc[point, :3].values
                           
        if(hasChanged == False):
            break

        for centroid in centroids:
            if (centroid.numberOfRelations == 0):
                continue

            centroid.vector = centroid.sumOfPoints / centroid.numberOfRelations
            centroid.sumOfPoints  = (0.0, 0.0, 0.0)
            centroid.numberOfRelations = 0

class Centroid:
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector
        self.numberOfRelations = 0
        self.sumOfPoints = (0.0, 0.0, 0.0)
    
    def __str__(self):
        return str(self.name) + '  ' + str(self.vector)


def main():

    # Distance A  Distance B  Distance C  Position X  Position Y
    data = pd.read_csv("MIW/MP2/data/beacon_readings.csv", usecols=range(5))
    data['Centroid'] = Centroid
    data['Distance'] = np.double('inf')
    data['Color'] = [np.zeros(3) for i in range(len(data))]

    numberOfClusters = 5

    k_means(data, numberOfClusters)
    print(data.iloc[:, [0,1,2,5,6]].to_string())  
    #plt.scatter(data['Distance A'], data['Distance B'], data['Distance C'], data['Color'])
    #plt.scatter(data['Position X'], data['Position Y'], c=data['Color'])
    #plt.show()


if __name__ == '__main__':
    main()
