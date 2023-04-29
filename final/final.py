#### concept
# build model
  # take inputs and spit out happiness score

  # monte carlo

  # bayseian updating - decided it was reduntint 

  # loop

# take model and use early stoping to figure out when to stop
#### end concept

import json
from math import exp
import numpy as np
import matplotlib.pyplot as plt

def getBest(roles):
  best = roles[0]
  for role in roles:
    if role['avgHappy']> best['avgHappy']:
      best = role
  return roles.index(best)

def monteCarlo(roles, epsilon):
  # get action
  if np.random.random() < epsilon:
    action = np.random.randint(len(roles))
  else:
    action = getBest(roles)

  # return role to play
  return action

def getEpsilon(epsilon, ct):
  newEps = .5 - (ct * .01)
  if newEps < .01:
    newEps = .01
  return newEps

def updatingLoop(data, ct):
  done = False
  while not done:
    epsilon = getEpsilon(data, ct)
    # get role to play
    action = monteCarlo(data['roles'], epsilon)
    role = data['roles'][action]
    history = data['history']
    print(f"\nFor your next game queue {role['role']}")

    # wait for reported happyness
    valid = False
    while not valid:
      happiness = input("Enter happiness from last match(1-10): ")
      if happiness.isnumeric():
        happiness = float(happiness)
        if happiness >= 0 and happiness <= 10:
          valid = True
        else:
          print("Please enter a number between 0 and 10")
      else:
        print("Please enter a number")
    
    # update file
    newAvg = (role['n'] * role['avgHappy'] + happiness) / (role['n'] + 1)
    role['avgHappy'] = newAvg
    role['n'] += 1
    data['roles'][action] = role

    if ct >= 100:
      gameData = {
        "rolePlayed": role['role'],
        "happiness" : happiness
      }
      
      history[-1].append(gameData)
    updateFile(data)
    ct += 1

    # call again
    end = input("Do you want to play another match? (y/n)")
    if (end == "n"):
      done = True

def earlyStopping(data):
  solutions = {}
  for i in range(20):
    solutions[str(i)] = 0

  for i in range(len(data['history'])):
    session = data['history'][i]
    if len(session) > 3:
      for j in range(len(session)):
        game = session[j]

        if game['happiness'] >= 5:
          solutions[str(j)] += 1

  maxKey = max(solutions, key=solutions.get)
  print(f'According to our data, you should stop playing after {int(maxKey) + 1} games\n')
  x, y = zip(*solutions.items())
  plt.plot(x,y)
  plt.show()

def updateFile(data, file='data.json'):
    toWrite = json.dumps(data, indent=1)

    with open(file, "w") as outfile:
      outfile.write(toWrite)

def loadFile(file='data.json'):
  with open(file, "r") as openFile:
    return json.load(openFile)
  
def resetModel():
  reset = input(f"Are you sure?(y/n) ")
  if reset == "y":
    initData = loadFile(file="initData.json")
    updateFile(initData)

def init():
  # read from data.txt
  data = loadFile()
  # get total games played
  ct = 0
  for role in data['roles']:
    ct += role['n']

  # ask if we want to continue or reset
  if ct > 100:
    choice = input(f"You have we have a good distrabution of how you play now. Would you like to move on to seeing how many games you should play in a session?(y/n) ")
    if choice == "y":
      earlyStopping(data)

    choice = input(f"Would you like to play some more games?(y/n) ")
    if choice == "y":
      data['history'].append([])
      updatingLoop(data, ct)
  else:
    reset = input(f"You have built this data set with {ct} games. Would you like to reset?(y/n) ")
    if reset == "y":
    #   if reset reset data and go to loop()
      resetModel()
      ct = 0

    data['history'].append([])
    updatingLoop(data, ct)


init()