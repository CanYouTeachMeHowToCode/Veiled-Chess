from origin import *

if __name__ == '__main__':
    game = ChessGame()
    print("Game start")
    game.printBoard()
    while not game.game_over:
        print()
        print("{}'s turn".format(game.currPlayer))
        start = input("Enter starting position: ")
        end = input("Enter ending position: ")
        game.move(start, end)
        game.printBoard()