import pygame
from game.macro import *
from game.board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = PLAYER_WHITE

    def run(self):
        pass
