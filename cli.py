# Script for interactive playing (playing vs another player, playing vs AI agents, etc.)
from game.board import Board
from scripts.ai import AI
from game.macro import *

def CLI():
    GameBoard = Board()
    print("Game start")
    GameBoard.printBoard()
    # print("Real Board: ")
    # GameBoard.printRealBoard()
    # print("Don't look at the real board during the competition. It's Cheating!")
    blackAI = AI(GameBoard, 1) # can be modified to customized later
    while not GameBoard.gameOver:
        print()
        player = GameBoard.currPlayer
        print("{}'s turn".format(player))
        if player == PLAYER_WHITE: # can be modified to customized later
            start = input("Enter starting position: ")
            end = input("Enter ending position: ")
            GameBoard.move(start, end)
        else: 
            start, end = blackAI.nextMove()[1]
            start, end = convertTupleToCoord(start), convertTupleToCoord(end)
            GameBoard.move(start, end)
        GameBoard.printBoard()

if __name__ == '__main__':
    CLI()


