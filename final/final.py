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
    if role.avgHappy * role.priorProb > best.avgHappy * best.priorProb:
      best = role
  return roles.indexOf(best)

def monteCarlo(roles):
  epsilon = .1
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
    posteriorProb = numerator / denominator

    return posteriorProb

def loop(data):
  done = False
  while not done:
    # get role to play
    action = monteCarlo(data.roles)
    role = data.roles[action]
    print(f"For your next game queue {role.name}")

    # wait for reported happyness
    #TODO: validate input
    happiness = input("Enter happiness from last match")

    # use bayseian to update model
    posteriorProb = bayseianUpdating(happiness, role.priorProb)
    # update file
    role.priorProb = posteriorProb
    updateFile(data)

    # call again
    #TODO: validate input
    end = input("Do you want to play another match? (y/n)")
    if (end == "y"):
      done = True

# def earlyStopping():

def updateFile(data, file='data.json'):
    json = json.dumps(data, indent=1)

    with open(file, "w") as outfile:
      outfile.write(json)

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
  for role in data.roles:
    ct += role.n
  # ask if we want to continue or reset
  #TODO: validate input
  reset = input(f"You have built this data set with {ct} games. Would you like to reset?(y/n)")
  if reset == "y":
  #   if continue go to loop()
    resetModel()
  #   if reset reset data and go to loop()
    loop()

