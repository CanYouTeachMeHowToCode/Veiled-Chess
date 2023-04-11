from board import Board
from ai import AI

def simulate(numGame=10):
    for i in range(numGame):
        print(f"================== Game {i} ==================".format(i+1))
        game = Board()
        print("Game start")
        game.printBoard()
        print("Real Board: ")
        game.printRealBoard()
        gameLog = []
        while not game.gameOver:
            print()
            print("{}'s turn".format(game.currPlayer))
            noviceAI = AI(game, 0)
            start, end = noviceAI.move()
            start, end = game.convertTupleToCoord(start), game.convertTupleToCoord(end)
            gameLog.append((start, end))
            game.move(start, end)
            game.printBoard()
        print("Game Log:")
        print(gameLog)

if __name__ == '__main__':
    simulate()