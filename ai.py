# AI agent using deep learning & non-deep learning approaches
import random
from board import Board

class AI():
    def __init__(self, GameBoard, level):
        self.GameBoard = GameBoard
        self.level = ['novice', 'competent', 'expert'][level]
    
    def getLegalMoves(self):
        return self.GameBoard.getAllLegalMoves()

    def move(self):
        legalMoves = self.getLegalMoves()
        if self.level == 'novice': return random.choice(legalMoves)