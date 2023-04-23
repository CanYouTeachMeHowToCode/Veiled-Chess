import time
import sys
import io
from scripts.board import Board
from scripts.ai import AI
from scripts.macro import *

def simulateAICompetition(numGame, whiteLevel, blackLevel):
    for i in range(numGame):
        print(f"================== Game {i+1} ==================")
        GameBoard = Board()
        print("Game start")
        GameBoard.printBoard()
        print("Real Board: ")
        GameBoard.printRealBoard()
        whiteAI = AI(GameBoard, whiteLevel) # novice AI
        blackAI = AI(GameBoard, blackLevel) # competent AI
        sys.stdin = io.StringIO('q\n'*100000) # default pawn promotion to queen for AI (may be modified later)
        while not GameBoard.gameOver:
            print()
            print(f"{GameBoard.currPlayer}'s turn")
            startTime = time.time()
            start, end = whiteAI.nextMove()[1] if GameBoard.currPlayer == PLAYER_WHITE else blackAI.nextMove()[1]
            start, end = GameBoard.convertTupleToCoord(start), GameBoard.convertTupleToCoord(end)
            GameBoard.move(start, end, verbose=True)
            endTime = time.time()
            print(f"time taken: {round(endTime-startTime, 3)}s")
            GameBoard.printBoard()
        print("Game Log:")
        print(GameBoard.gameLog)

if __name__ == '__main__':
    # simulateAICompetition(numGame=2, whiteLevel=0, blackLevel=1) # novice vs competent
    simulateAICompetition(numGame=1, whiteLevel=1, blackLevel=1) # competent vs competent