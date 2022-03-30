import matplotlib.pyplot as plt
import numpy as np
import enum

def EnterPositiveInteger():
    try:
        count = int(input())
        if count < 1:
            print("Enter a non-negative integer: ")
            return EnterPositiveInteger()       
    except:
        print("Enter a non-negative integer: ")
        return EnterPositiveInteger()
    
    return count

def PlayerChoise(max):
 
    try:
        count = int(input())
        if count < 1 or count > max:
            print("Enter a non-negative less " + str(max) + " than  integer: ")
            return PlayerChoise(max)       
    except:
        print("Enter a non-negative less " + str(max) + " than  integer: ")
        return PlayerChoise(max)
    
    return count

def SelectWinStrategy(enemyChoise):
    for i in beats:
        if beats[i].value == enemyChoise:
            return i

@enum.unique
class Options (enum.Enum):
    rock = 1
    paper = 2
    scissors = 3

#optionsCount = len(Options._member_map_)

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
numberOfGames = EnterPositiveInteger()
print('\n')

print("Options for player choise :")
for option in Options:
    print(option.value, " " + option.name)
print('\n')

for round in range(numberOfGames):

    choiceRow = int(lastPlayerChoice.value) - 1
    sumOfChoices = sum(playerChoices[choiceRow])

    for x in range(len(probability)):
        probability[x] = playerChoices[choiceRow][x] / sumOfChoices

    playerPredictedChoice = np.random.choice(Options, p = probability)

    computer = SelectWinStrategy(playerPredictedChoice.value)
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

print("\nFinal score " + str(points) + '\n')
    