#### concept
# build model
  # take inputs and spit out happiness score

  # monte carlo

  # bayseian updating

  # loop

# take model and use early stoping to figure out when to stop
#### end concept

import json
from math import exp
import numpy as np

def getBest(roles):
  best = roles[0]
  for role in roles:
    if role['avgHappy'] * role['priorProb'] > best['avgHappy'] * best['priorProb']:
      best = role
  return roles.index(best)

def monteCarlo(roles, epsilon):
  # do explore exploit step

  # get action
  if np.random.random() < epsilon:
    action = np.random.randint(len(roles))
  else:
    action = getBest(roles)

  # return role to play
  return action

def bayseianUpdating(actualVal, priorProb):
    # Convert predicted and actual values to probabilities
    # probPredicted = 1 / (1 + exp(-predictedVal))
    probActual = 1 / (1 + exp(-actualVal))

    # Compute likelihood of actual value given predicted value
    likelihood = probActual ** actualVal * (1 - probActual) ** (1 - actualVal)

    # Compute posterior probability
    numerator = likelihood * priorProb
    denominator = numerator + (1 - priorProb) * (1 - likelihood)
    print(numerator)
    print(1 - priorProb)
    print(1 - likelihood)
    print((1 - priorProb) * (1 - likelihood))
    print(numerator + (1 - priorProb) * (1 - likelihood))
    posteriorProb = numerator / denominator

    return posteriorProb

def updatingLoop(data, ct):
  epsilon = .01
  done = False
  while not done:
    # get role to play
    action = monteCarlo(data['roles'], epsilon)
    role = data['roles'][action]
    print(f"For your next game queue {role['role']}")

    # wait for reported happyness
    #TODO: validate input
    valid = False
    while not valid:
      happiness = input("Enter happiness from last match: ")
      if happiness.isnumeric():
        happiness = float(happiness)
        if happiness >= 0 and happiness <= 10:
          valid = True
        else:
          print("Please enter a number between 0 and 10")
      else:
        print("Please enter a number")

    # use bayseian to update model
    posteriorProb = bayseianUpdating(happiness, role['priorProb'])
    
    # update file
    newAvg = (role['n'] * role['avgHappy'] + happiness) / (role['n'] + 1)
    role['priorProb'] = posteriorProb
    role['avgHappy'] = newAvg
    role['n'] += 1
    data['roles'][action] = role

    if ct >= 100:
      gameData = {
        "rolePlayed": role,
        "happiness" : happiness
      }
      data['history'][-1].append(gameData)
    updateFile(data)
    ct += 1

    # call again
    #TODO: validate input
    end = input("Do you want to play another match? (y/n)")
    if (end == "n"):
      done = True

def earlyStopping(data):
  print("TODO:")



def updateFile(data, file='data.json'):
    toWrite = json.dumps(data, indent=1)

    with open(file, "w") as outfile:
      outfile.write(toWrite)

def loadFile(file='data.json'):
  with open(file, "r") as openFile:
    return json.load(openFile)
  
def resetModel():
  reset = input(f"Are you sure?(y/n)")
  if reset == "y":
    initData = loadFile(file="initData.json")
    updateFile(initData)
  else:
    loop()

# TODO: check if we want to collect data or do early stopping
def init():
  # read from data.txt
  data = loadFile()
  # get total games played
  ct = 0
  for role in data['roles']:
    ct += role['n']

  # ask if we want to continue or reset
  if ct > 100:
    choice = input(f"You have we have a good distrabution of how you play now. Would you like to move on to seeing how many games you should play in a session?")
    if choice == "y":
      earlyStopping(data)
  else:
    #TODO: validate input
    reset = input(f"You have built this data set with {ct} games. Would you like to reset?(y/n)")
    if reset == "y":
    #   if reset reset data and go to loop()
      resetModel()

    data['history'].append([])
    updatingLoop(data, ct)


init()