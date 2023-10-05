#to run code, just type python3 blackjack.py
#there are no flags
#the way to see the infinite deck is to edit it in the hard code
#look for ######## in code to see where to edit the deck type to see infinite deck
import os
import random
import string
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import statistics as st

Ace = 1
J = Q = K = 10
deck = []
hard = True
######## Modify deck type by changing this standard boolean to False
standard = True
sumTotal = 0
policy = 1
totalWin = 0
p1Value = 0

# Intro
print("Welcome to Blackjack simulation, where we will test how often we bust based on predetermined policies!\n")


def infDeckGame():
    print("You have chosen an infinite deck!\n")
    global standard
    standard = False


def stanDeckGame():
    print("You have chosen a standard deck!\n")
    global standard
    standard = True


def startGame():
    decktype = 0
    _ace = 0
    global Ace  # needs to be defined here as global to change value of variable

    # Player chooses whether Ace's value is 1 or 11
    _ace = input(
        "Select value of Ace, Choose [0] for a value of 1 or [1] for a value of 10 \n")
    if _ace == "0":
        Ace = 1
        print("A is now ", Ace)
    elif _ace == "1":
        Ace = 11
        print("A is now ", Ace)
    else:
        print("Incorrect input, Ace value will be defaulted to 1")

    decktype = input("Choose a deck type [I]nfinite or [S]tandard: \n")
    if decktype == "I" or decktype == "i":
        infDeckGame()
        # exit()
    elif decktype == "S" or decktype == "s":
        stanDeckGame()
        # exit()
    else:
        print("Incorrect input! Ending simulation!")
        exit()


# POLICY
def _PolicySelected(x):
    # POLICY 1
    global sumTotal
    if x == 1:
        if sumTotal < 17:
            # print("hit, Policy 1")
            hit()
            check()
    # POLICY 2
    elif x == 2:
        if sumTotal < 17 and hard:
            printLog("No Ace, draw")
            hit()
            check()
    # POLICY 3
    elif x == 3:
        return
    # POLICY 4
    elif x == 4:
        # print("hit, Policy 4")
        hit()
        hit()
        check()
    # POLICY 5
    elif x == 5:
        if sumTotal <= 10:
            hit()
            check()


# Change settings prompt
# settings = input(
#     "Do you want to change settings[Y]? Default: Ace=1, No card replacement \n")
# if settings == "Y" or settings == "y":
#     startGame()


# CHECK IF 21 OR OVER
def check():
    global totalWin
    # print(len(deck))
    if sumTotal == 21:
        # print("21! You win")
        totalWin += 1
        return
    elif sumTotal > 21:
        # print("Bust! You went over 21")
        return

# HIT


def hit():
    if (len(deck)) <= 0:
        return

    global sumTotal
    pick = random.randint(0, len(deck)-1)
    card = deck[pick]
    printLog("card drawn: " + str(card))
    # HARD IF ACE IS NOT IN HAND, SOFT IF ACE IS IN HAND
    if card == Ace:
        hard = False
        if policy == 5 and sumTotal <= 10:
            printLog("Drew an ace, will now switch from 1 to 11")
    else:
        hard = True
        # print("hard \n")

    if standard:
        del deck[pick]
        # print("hit:", len(deck))
    sumTotal += card
    # print("After Hit:", sumTotal, " Deck:", len(deck))
    printLog("New sum after draw: " + str(sumTotal))
    # check()
    # _PolicySelected(policy)

# DEAL CARDS


def deal():

    global sumTotal
    global deck
    global totalWin
    # global index1,index2,index3,index4
    # print(len(deck))
    # Random  index for player
    pick1 = random.randint(0, len(deck)-1)
    pick2 = random.randint(0, len(deck)-1)

    # Checks if the same card index is chosen again. Avoids selecting the same card
    while pick2 == pick1:
        pick2 = random.randint(0, len(deck)-1)

    # Select card based on index for player

    card1 = deck[pick1]
    card2 = deck[pick2]
    # print(card1,card2)
    # print(card1, card2, len(deck))
    if standard:
        # print(pick1, pick2, card1, card2)
        deck[pick1] = 0
        deck[pick2] = 0
        deck = [i for i in deck if i != 0]
        # print(len(deck),x)
    # REMOVE CARD FROM DECK ONE BY ONE, OTHERWISE SAME CARD CAN BE PICKED

    pick3 = random.randint(0, len(deck)-1)
    pick4 = random.randint(0, len(deck)-1)
    while pick4 == pick3:
        pick4 = random.randint(0, len(deck)-1)
    card3 = deck[pick3]
    card4 = deck[pick4]

    printLog("card1-> "+str(card1) + " card2-> " + str(card2) +
             " card3-> "+str(card3)+" card4-> "+str(card4))
    # REMOVE CARDS FROM DECK
    if standard:
        # print(pick3, pick4, card3, card4)
        deck[pick3] = 0
        deck[pick4] = 0
        deck = [i for i in deck if i != 0]
        # print(len(deck))

    # HARD IF ACE IS NOT IN HAND, SOFT IF ACE IS IN HAND
    if card1 == Ace or card2 == Ace:
        printLog("P1 drew Ace")
        hard = False
        # print("Drew an ace: ", Ace)
    else:
        hard = True
        # print("hard \n")

    # print("Player 1")
    # print("Card 1:", card1)
    # print("Card 2:", card2)
    # print("your sum is: ", card1+card2)

    # print("Player 2")
    # print("Card 3:", card3)
    # print("Card 4:", card4)
    # print("your sum is: ", card3+card4)

    # print("P1 chooses \n")
    sumTotal = card1+card2
    check()  # CHECK WIN/BUST BEFORE HITTING
    _PolicySelected(policy)

    if (policy > 0):
        # print("entering dealer")
        global p1Value
        p1Value = sumTotal  # sum plus the hit of p1
        sumTotal = card3+card4
        if card3 == Ace or card4 == Ace:
            printLog("dealer has an ace")
            sumTotal += 10
        check()
        if sumTotal < 21:
            printLog("dealer hit")
            hit()
        if p1Value < 21 and sumTotal < 21:
            # print(x,p1Value, sumTotal, len(deck))
            printLog("p1 and dealer both have less than 21")
            if p1Value > sumTotal:
                printLog("p1 beats dealer " +
                         str(p1Value) + " > " + str(sumTotal))
                totalWin += 1
        if p1Value < 21 and sumTotal > 21:
            printLog(
                "dealer busted after drawing and player hasn't busted. So p1 wins")
            totalWin += 1


def printLog(mString):
    # display cards
    # print(mString)
    return


# rounds = int(input("Enter a number of rounds \n"))
# policy = int(input("Select a policy to play. 1,2,3,4,5"))
rounds = 10

policy = 1
# print(policy)

# rounds = 5
# policy = 3
# index1 = 6 #7,6
# index2 = 5 #19
# index3 = 0
# index4 = 1


plotArray = []
_policy1Ar = []
_policy2Ar = []
_policy3Ar = []
_policy4Ar = []
_policy5Ar = []

_policy1Bar = []
_policy2Bar = []
_policy3Bar = []
_policy4Bar = []
_policy5Bar = []

_policy1Sd = []
_policy2Sd = []
_policy3Sd = []
_policy4Sd = []
_policy5Sd = []


def simulate():
    global rounds
    global deck
    global totalWin
    x = 1
    for i in range(4):
        while x <= rounds:
            printLog("Standard Deck? " + str(standard))
            printLog("round start: " + str(x))
            printLog("policy played: " + str(policy))
            # Create deck and shuffle deck after settings
            deck = [Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K]*4
            random.shuffle(deck)
            # print("\n---------------------------------------")
            # print("Round: ", x)
            deal()
            # print("\n")
            printLog("total wins so far: " + str(totalWin))
            x += 1

            # time.sleep(.2)
        x = 1
        plotArray.append(totalWin)
        totalWin = 0


def sim():
    global rounds, plotArray, _policy1Ar, _policy2Ar, _policy3Ar, _policy4Ar, _policy5Ar, policy
    simulate()
    _policy1Ar = plotArray
    _policy1Sd.append(st.stdev(_policy1Ar)/rounds)
    policy = 2
    plotArray = []
    simulate()
    _policy2Ar = plotArray
    _policy2Sd.append(st.stdev(_policy2Ar)/rounds)
    policy = 3
    plotArray = []
    simulate()
    _policy3Ar = plotArray
    _policy3Sd.append(st.stdev(_policy3Ar)/rounds)
    policy = 4
    plotArray = []
    simulate()
    _policy4Ar = plotArray
    _policy4Sd.append(st.stdev(_policy4Ar)/rounds)
    policy = 5
    plotArray = []
    simulate()
    _policy5Ar = plotArray
    _policy5Sd.append(st.stdev(_policy5Ar)/rounds)
    plotArray = []
    rounds *= 10


def populateBar():
    global policy1Avg, policy2Avg, policy3Avg, policy4Avg, policy5Avg, _policy1Bar, _policy2Bar, _policy3Bar, _policy4Bar, _policy5Bar
    policy1Avg = st.mean(_policy1Ar)/rounds*10
    _policy1Bar.append(policy1Avg)
    policy2Avg = st.mean(_policy2Ar)/rounds*10
    _policy2Bar.append(policy2Avg)
    policy3Avg = st.mean(_policy3Ar)/rounds*10
    _policy3Bar.append(policy3Avg)
    policy4Avg = st.mean(_policy4Ar)/rounds*10
    _policy4Bar.append(policy4Avg)
    policy5Avg = st.mean(_policy5Ar)/rounds*10
    _policy5Bar.append(policy5Avg)

# simulate()
# _policy4Ar = plotArray
# policy = 5
# plotArray = []
# simulate()
# _policy5Ar = plotArray


sim()
populateBar()
print(policy1Avg, policy2Avg, policy3Avg, policy4Avg, policy5Avg)
sim()
populateBar()
print(policy1Avg, policy2Avg, policy3Avg, policy4Avg, policy5Avg)
sim()
populateBar()
print(policy1Avg, policy2Avg, policy3Avg, policy4Avg, policy5Avg)
sim()
populateBar()
print(policy1Avg, policy2Avg, policy3Avg, policy4Avg, policy5Avg)

print("p1 array:", _policy1Ar, st.stdev(_policy1Ar))

# def runSimulation():
#     global policy, _policy3Ar, _policy4Ar, plotArray
#     simulate()
#     _policy3Ar = plotArray
#     policy = 4
#     plotArray = []
#     simulate()
#     _policy4Ar = plotArray
#     if policy == 4: policy=3

# for i in range(1):
#     runSimulation()
#     print("next rounds")
#     rounds *= 10
#     print("policy bar update:",_policy3Ar)
#     _policy3Bar.append(_policy3Ar)
#     _policy4Bar.append(_policy4Ar)


# print(_policy3Ar, policy3Avg, _policy4Ar, policy4Avg)
# print("policy bar:", _policy3Bar)
# #xpoints = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
# plt.ylim(0,rounds)
# ypoints = np.array(plotArray)

# plt.plot(ypoints)
# plt.show()


plt.ylim(0, 1)
barWidth = 0.15
fig = plt.subplots(figsize=(30, 30))
br1 = np.arange(len(_policy1Ar))
br2 = [x + barWidth for x in br1]  # x is height
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
br5 = [x + barWidth for x in br4]

plt.bar(br1, _policy1Bar, color='r', width=barWidth,
        edgecolor='grey', label='Policy 1')
plt.errorbar(br1, _policy1Bar, yerr=_policy1Sd, fmt='None')
plt.bar(br2, _policy2Bar, color='g', width=barWidth,
        edgecolor='grey', label='Policy 2')
plt.errorbar(br2, _policy2Bar, yerr=_policy2Sd, fmt='None')
plt.bar(br3, _policy3Bar, color='b', width=barWidth,
        edgecolor='grey', label='Policy 3')
plt.errorbar(br3, _policy3Bar, yerr=_policy3Sd, fmt='None')
plt.bar(br4, _policy4Bar, color='y', width=barWidth,
        edgecolor='grey', label='Policy 4')
plt.errorbar(br4, _policy4Bar, yerr=_policy4Sd, fmt='None')
plt.bar(br5, _policy5Bar, color='k', width=barWidth,
        edgecolor='grey', label='Policy 5')
plt.errorbar(br5, _policy5Bar, yerr=_policy5Sd, fmt='None')


print(_policy1Sd)
print(_policy2Sd)
print(_policy3Sd)
print(_policy4Sd)
print(_policy5Sd)

plt.xlabel('Iterations', fontweight='bold', fontsize=25)
plt.ylabel('Win Ratio', fontweight='bold', fontsize=25)
plt.xticks([r + barWidth for r in range(len(_policy1Ar))],
           ['10', '100', '1000', '10000'])

if standard:
    plt.title("Win Ratio vs. Iterations of all Policies wtih a Standard Deck ")
else:
    plt.title("Win Ratio vs. Iterations of all Policies wtih an Infinite Deck")

plt.legend()
plt.show()


# barList = plt.bar(["policy 4", "policy 5"], [policy4Avg, policy5Avg])
# barList[0].set_color('r')
# barList[1].set_color('b')
# plt.text(0, .25, policy4Avg, ha='center')
# plt.text(1, 1, policy5Avg, ha='center')
# plt.ylabel("Average win rate")
# plt.xlabel(str(rounds) + " rounds with 15 iteration")


# plt.show()
