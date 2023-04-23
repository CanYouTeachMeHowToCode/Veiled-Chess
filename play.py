from scripts.board import Board

if __name__ == '__main__':
    game = Board()
    print("Game start")
    game.printBoard()
    print("Real Board: ")
    game.printRealBoard()
    while not game.gameOver:
        print()
        print("{}'s turn".format(game.currPlayer))
        start = input("Enter starting position: ")
        end = input("Enter ending position: ")
        game.move(start, end)
        game.printBoard()