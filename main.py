from logic import *

if __name__ == '__main__':
    game = ChessGame()
    print("Game start")
    game.print_board()
    while not game.game_over:
        print()
        print("{}'s turn".format(game.current_player))
        start = input("Enter starting position: ")
        end = input("Enter ending position: ")
        game.move(start, end)
        game.print_board()