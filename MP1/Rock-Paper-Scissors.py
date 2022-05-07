import matplotlib.pyplot as plt
import numpy as np
import enum

def enterPositiveInteger():
    try:
        number = int(input())
        if number < 1:
            print("Enter a non-negative integer: ")
            return enterPositiveInteger()       
    except:
        print("Enter a non-negative integer: ")
        return enterPositiveInteger()
    
    return number

def playerChoise(max):
 
    try:
        number = int(input())
        if number < 1 or number > max:
            print("Enter a non-negative less " + str(max) + " than  integer: ")
            return playerChoise(max)       
    except:
        print("Enter a non-negative less " + str(max) + " than  integer: ")
        return playerChoise(max)
    
    return number

def selectWinStrategy(enemyChoise, beats):
    for i in beats:
        if beats[i].value == enemyChoise:
            return i

@enum.unique
class Options (enum.Enum):
    rock = 1
    paper = 2
    scissors = 3

def main():
    beats = {
        Options.rock : Options.scissors,
        Options.paper : Options.rock,
        Options.scissors : Options.paper 
    }

    playerChoices = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    probability = [1, 1, 1]
    lastPlayerChoice = np.random.choice(Options, p = [1/3, 1/3, 1/3])
    points = 0

    print('\n')
    print("Enter count of Draws :")
    numberOfGames = enterPositiveInteger()
    print('\n')

    print("Options for player choise :")
    for option in Options:
        print(option.value, " " + option.name)
    print('\n')

    matches = np.zeros(numberOfGames) # Array of played matches

    for round in range(numberOfGames):

        choiceRow = int(lastPlayerChoice.value) - 1
        sumOfChoices = sum(playerChoices[choiceRow])

        for x in range(len(probability)):
            probability[x] = playerChoices[choiceRow][x] / sumOfChoices

        playerPredictedChoice = np.random.choice(Options, p = probability)

        computer = selectWinStrategy(playerPredictedChoice.value, beats)
        #computer = Options(np.random.choice(Options))
        player = Options(np.random.choice(Options, p = [0.1, 0.2, 0.7]))
        #player = Options(PlayerChoise(len(Options._member_map_)))

        playerChoices[choiceRow][choiceRow] += 1
        lastPlayerChoice = player

        print(computer.name + " — " + player.name)

        if beats[computer].value == player.value:
            print("computer wins\n")
            points -= 1
        elif computer.value == player.value:
            print("draw\n")
        else:
            print("player wins\n")
            points += 1

        matches[round] = points

    print("\nFinal score " + str(points) + '\n')

    plt.plot(matches, 'ro')
    plt.xlabel('Game rounds')
    plt.ylabel('Points')
    plt.show()

if __name__ == '__main__':
    main()