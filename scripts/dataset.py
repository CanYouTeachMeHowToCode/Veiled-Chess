# Define veiled chess dataset used for training
from torch.utils.data import Dataset, DataLoader
from torch.utils.data import random_split
from scripts.macro import *

class VeiledChessDataset(Dataset):
    def __init__(self, board, gameInfo, labels):
        self.board = board
        self.gameInfo = gameInfo
        self.labels = labels
        
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, index):
        return self.board[index], self.gameInfo[index], self.labels[index]

    def trainTestSplit(self, ratio):
        # Split the dataset into training and validation sets
        trainSize = int(ratio*len(self))
        testSize = len(self)-trainSize
        trainDataset, testDataset = random_split(self, [trainSize, testSize])

        # Create DataLoader instances for training and validation datasets
        trainLoader = DataLoader(trainDataset, batch_size=BATCH_SIZE, shuffle=True)
        testLoader = DataLoader(testDataset, batch_size=BATCH_SIZE, shuffle=False)

        # Return the DataLoader instances, datasets, saved models directory, device
        return trainLoader, testLoader, trainDataset, testDataset