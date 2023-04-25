# Script for setting up the project, including dataset simulation, model training & evaluation 
import numpy as np
import os
import ast
import torch
import torch.nn as nn
import torch.optim as optim
from scripts.macro import *
from scripts.model import VeiledChessNet
from scripts.dataset import VeiledChessDataset
from scripts.simulateData import generateData
from scripts.processData import loadAndProcessData

# Directory for storing training dataset
dataDir = './data'

# generate the training dataset if it currently does not exist
if not os.path.exists(dataDir): 
    # generate data of competent white AI vs novice black AI (can be customized)
    generateData(10, os.path.join(dataDir, 'data_white.csv'), 1, 0) 

# Load and process data
df = loadAndProcessData(dataDir)

def strToList(s): # convert the string representation of 2D list to actual 2D list
    strList = [s.strip('][').split(', ') for s in s.strip('][').split('], [')]
    return [[c for c in row] for row in strList]

def encodeBoard(boards): # encode all the boards using ordinal encoding
    scores = [0, -7, -1, -3, -3, -5, -9, -100, 100, 9, 5, 3, 3, 1, 7]
    ordinalBoards = np.zeros((boards.shape[0], boards.shape[1], boards.shape[2]), dtype=int)
    for i in range(boards.shape[0]):
        for j in range(boards.shape[1]):
            for k in range(boards.shape[2]):
                char = str(boards[i, j, k]).replace("'", "")
                ordinalBoards[i, j, k] = scores[ASCII_PIECE_CHARS.find(char)]
    return ordinalBoards

def encodePlayer(player):
    return 1 if player == PLAYER_WHITE else -1

def normalizeScores(scores):
    scores[scores == np.inf] = 1e5 # replace infinity values with large finite numbers
    scores[scores == -np.inf] = -1e5
    scoresCentered = scores-np.mean(scores)
    return scoresCentered / np.max(np.abs(scoresCentered))

# Convert chess boards from string of 2D list to actual 2D list
boards = np.array(df['board'].apply(strToList).tolist())

# Encode board using ordinal encoding
boardData = encodeBoard(boards) 

# Reshape the data to "minic an grayscale image" to fit with the model input 
boardData = np.reshape(boardData, (boardData.shape[0], 1, boardData.shape[1], boardData.shape[2]))

# Encode player data by converting white player to 1 and black player to -1
playerData = np.array(df['player'].apply(encodePlayer).tolist()) 

# Convert castling info from string of list to actual list
gameInfoData = np.array(df['gameInfo'].apply(ast.literal_eval).tolist()) 

# Convert and normalize the scores
scores = np.array(df['score'].tolist()) 
scoreData = normalizeScores(scores) 

# Combine the castling info and player info together
combinedGameInfoData = np.hstack((playerData.reshape(-1, 1), gameInfoData))

# Create datasets and dataloaders with train-test split
dataset = VeiledChessDataset(boardData, combinedGameInfoData, scoreData)
ratio = 0.8
trainLoader, testLoader, trainDataset, testDataset = dataset.trainTestSplit(ratio) 

# Determine the device to use for training (GPU or CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize model, optimizer, and criterion
model = VeiledChessNet().to(device)
optimizer = optim.RMSprop(model.parameters(), lr=LR)
criterion = nn.MSELoss()

# Directory for storing best model so far
modelDir = './models'

# Training
def train(model, trainLoader, optimizer, criterion, device):
    model.train()
    trainLoss = 0
    for _, (board, gameInfo, score) in enumerate(trainLoader):
        board, gameInfo, score = board.to(device), gameInfo.to(device), score.to(device)
        optimizer.zero_grad()
        output = model(board.float(), gameInfo.float())
        output = output.view(-1)
        loss = criterion(output, score.float())
        loss.backward()
        optimizer.step()
        trainLoss += loss.item()
    return trainLoss / len(trainLoader)

def evaluate(model, testLoader, criterion, device):
    model.eval()
    testLoss = 0
    with torch.no_grad():
        for _, (board, gameInfo, score) in enumerate(testLoader):
            board, gameInfo, score = board.to(device), gameInfo.to(device), score.to(device)
            output = model(board.float(), gameInfo.float())
            testLoss += criterion(output, score.float()).item()
    return testLoss / len(testLoader)

bestTestLoss = float('inf')
for epoch in range(1, NUM_EPOCHS+1):
    trainLoss = train(model, trainLoader, optimizer, criterion, device)
    testLoss = evaluate(model, testLoader, criterion, device)
    print(f"Epoch {epoch}/{NUM_EPOCHS}, Train Loss: {trainLoss:.4f}, Test Loss: {testLoss:.4f}")

    # Check if the current validation loss is lower than the best validation loss
    if testLoss < bestTestLoss:
        bestTestLoss = testLoss
        print(f"Validation loss improved. Saving the model to {modelDir}/best_model.pth")
        torch.save(model.state_dict(), f"{modelDir}/best_model.pth")

