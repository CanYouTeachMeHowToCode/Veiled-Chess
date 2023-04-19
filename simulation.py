from board import Board
from ai import AI

def simulate(numGame=10):
    for i in range(numGame):
        print(f"================== Game {i} ==================".format(i+1))
        GameBoard = Board()
        print("Game start")
        GameBoard.printBoard()
        print("Real Board: ")
        GameBoard.printRealBoard()
        while not GameBoard.gameOver:
            print()
            print("{}'s turn".format(GameBoard.currPlayer))
            noviceAI = AI(GameBoard, 0)
            start, end = noviceAI.move()
            start, end = GameBoard.convertTupleToCoord(start), GameBoard.convertTupleToCoord(end)
            GameBoard.move(start, end)
            GameBoard.printBoard()
        print("Game Log:")
        print(GameBoard.gameLog)

if __name__ == '__main__':
    simulate()