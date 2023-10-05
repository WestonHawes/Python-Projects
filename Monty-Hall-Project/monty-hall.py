# to run code in terminal run python3 monty-hall.py 
# here are the options: <--numDoors> <--iters> 
# <--choice> 0 for random switch 1 for never switch 2 for always switch
# <--banana> throws banana peel at host
# <--plot> shows the distribution of a variety of doors and Iterations
#running this script default with no options does not plot the probability distribution. Default options: 3 doors, 10000 iterations, no banana
import argparse
import random
import numpy as np 
import matplotlib.pyplot as plt

def montyHall(numDoors, choice, slip):
    # simulate picking doors by generating random indexes for winning and choice doors
    # use array to represent doors 1 == winning door 0 is losing -1 ==  closed
    doors = [0]* numDoors
    prizeIdx = random.randint(0, numDoors-1)
    doors[prizeIdx] = 1
    choiceIdx = random.randint(0, numDoors-1)
    #randomly choose a door to open to simulate slip if winning door is picked player loses 
    if slip:
        while True:
            slipIdx = random.randint(0, numDoors-1)
            if slipIdx != choiceIdx:
                doors[slipIdx] = -1
                break
            elif slipIdx == prizeIdx:
                return False
    #close all doors not winning 
    for i in range(numDoors):
        if doors[i] == 0 and i != choiceIdx:
            doors[i] = -1
    closed = doors.count(-1)
    # make sure winning and choice doors are not closed 
    if closed > numDoors-2:
        while(True):
            openIdx = random.randint(0, numDoors-1) 
            if openIdx != choiceIdx:
                doors[openIdx] = 0
                break
    if choice == 0: 
        ## randomly choose if switch; don't have to swap idx just determine if swap leads to win
        x = random.randint(0, 1) 
        if x == 0:
            return not(prizeIdx == choiceIdx) 
        else:
            return prizeIdx == choiceIdx
    elif choice == 2: 
        #always switch
        return not(prizeIdx == choiceIdx)
    # never switch
    return prizeIdx == choiceIdx

def main():
    #command line arguements
    parser = argparse.ArgumentParser(description="Monty Hall Simulation")
    parser.add_argument('--num-doors', dest='N', required=False)
    parser.add_argument('--iters', dest='iters', required=False)
    parser.add_argument('--choice', dest='C', required=False)
    parser.add_argument('--banana', action= 'store_true', required=False)
    parser.add_argument('--plot', action='store_true', required=False)
    parser.add_argument('--title', dest='title', required=False)
    args = parser.parse_args()
    global numDoors
    #default options
    if args.N: 
        numDoors = int(args.N)
    else: 
        numDoors = 3
    if args.iters: 
        iters = int(args.iters)
    else: 
        iters = 10000
    if args.C: 
        choice = int(args.C)
    else: 
        choice = 0
    if args.banana: 
        slip = True
    else: 
        slip = False
    if args.title: 
        title = args.title
    else: 
        title = "Monte Carlo Approximation for Monty Hall"
    
    if args.plot:
        #graph probabilty of picking winning door
        iterRanges = [10, 100, 1000, 10000]
        threeDoors = []
        sixDoors = []
        nineDoors = []
        twentyDoors = []
        hundredDoors = []

        for iterat in iterRanges: 
            threeDoors.append(sum([1 for i in range(iterat) if montyHall(3, choice, slip)])/iterat)
            sixDoors.append(sum([1 for i in range(iterat) if montyHall(6, choice, slip)])/iterat)
            nineDoors.append(sum([1 for i in range(iterat) if montyHall(9, choice, slip)])/iterat)
            twentyDoors.append(sum([1 for i in range(iterat) if montyHall(20, choice, slip)])/iterat)
            hundredDoors.append(sum([1 for i in range(iterat) if montyHall(100, choice, slip)])/iterat)
        barWidth = 0.15
        fig = plt.subplots(figsize =(30, 30))
        br1 = np.arange(len(threeDoors))
        br2 = [x + barWidth for x in br1]
        br3 = [x + barWidth for x in br2]
        br4 = [x + barWidth for x in br3]
        br5 = [x + barWidth for x in br4]
        plt.bar(br1, threeDoors, color ='r', width = barWidth,
        edgecolor ='grey', label ='Three Doors')
        plt.bar(br2, sixDoors, color ='g', width = barWidth,
        edgecolor ='grey', label ='Six Doors')
        plt.bar(br3, nineDoors, color ='b', width = barWidth,
        edgecolor ='grey', label = 'Nine Doors')
        plt.bar(br4, twentyDoors, color ='y', width = barWidth,
        edgecolor ='grey', label = 'Twenty Doors')
        plt.bar(br5, hundredDoors, color ='k', width = barWidth,
        edgecolor ='grey', label = 'Hundred Doors')

        plt.xlabel('Iterations', fontweight ='bold', fontsize = 15)
        plt.ylabel('Probability of Getting Right Door', fontweight ='bold', fontsize = 15)
        plt.xticks([r + barWidth for r in range(len(threeDoors))],
        ['10', '100', '1000', '10000'])
        plt.title(title)
        plt.legend()
        plt.show()
    else:
        win = 0
        for i in range(iters):
            if montyHall(numDoors, choice, slip):
                win = win + 1
        print(win / iters)
if __name__ == "__main__":
    main()
