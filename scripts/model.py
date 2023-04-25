# Define NN-based content-based filtering recommendation model
import torch
import torch.nn as nn
import torch.nn.functional as F

class VeiledChessNet(nn.Module):
    def __init__(self):
        super(VeiledChessNet, self).__init__()
        
        # CNN layers for processing the 2D chess board
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=2)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=2)
        self.conv4 = nn.Conv2d(128, 32, kernel_size=3, stride=1, padding=2)
        self.bn1 = nn.BatchNorm2d(128)
        
        # Max pooling layer
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Dropout layer
        self.dropout = nn.Dropout(p=0.3)

        # FCN layers for processing the game state info
        self.fc1 = nn.Linear(5, 16) # 4 castling check boolean values + 1 player string value
        self.fc2 = nn.Linear(16, 64) 
        
        # Final output layer
        self.out = nn.Linear(576, 1) # containing both processed board features and game info features
        
    def forward(self, board, gameInfo):
        # CNN for processing the chess board
        x = self.pool(F.relu(self.conv1(board)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.bn1(x)
        x = F.relu(self.conv4(x))
        x = self.dropout(x)
        x = x.view(x.size(0), -1) # flatten the output
        
        # FCN for processing the game state info
        y = F.relu(self.fc1(gameInfo))
        y = F.relu(self.fc2(y))
        y = y.view(y.size(0), -1) # flatten the output
        
        # Concatenate the outputs of the CNN and FCN
        z = torch.cat((x, y), dim=1)
        
        # Final output layer
        z = self.out(z)
        z = torch.tanh(z) # maps output to range (-1, 1)
        return z