import time
import sys
import io
from board import Board
from ai import AI
from macro import *

def simulate(numGame, whiteLevel, blackLevel):
    for i in range(numGame):
        print(f"================== Game {i} ==================".format(i+1))
        GameBoard = Board()
        print("Game start")
        GameBoard.printBoard()
        print("Real Board: ")
        GameBoard.printRealBoard()
        whiteAI = AI(GameBoard, whiteLevel) # novice AI
        blackAI = AI(GameBoard, blackLevel) # competent AI
        sys.stdin = io.StringIO('q') # default pawn promotion to queen for AI (may be modified later)
        while not GameBoard.gameOver:
            print()
            print(f"{GameBoard.currPlayer}'s turn")
            startTime = time.time()
            start, end = whiteAI.nextMove() if GameBoard.currPlayer == PLAYER_WHITE else blackAI.nextMove()
            start, end = GameBoard.convertTupleToCoord(start), GameBoard.convertTupleToCoord(end)
            GameBoard.move(start, end, verbose=True)
            endTime = time.time()
            print(f"time taken: {round(endTime-startTime, 3)}s")
            GameBoard.printBoard()
        print("Game Log:")
        print(GameBoard.gameLog)

if __name__ == '__main__':
    simulate(numGame=2, whiteLevel=0, blackLevel=1)