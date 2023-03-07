from piece import *
from macro import *

'''
Standard chess board  
  A B C D E F G H
8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 8
7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 7
6                 6
5                 5
4                 4
3                 3
2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ 2
1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 1
  A B C D E F G H
'''

class Board:
    def __init__(self):
        self.currPlayer = "white"
        self.checking = False
        self.canCastlingWhite = [True, True, True] # (king unmoved, rook1 (at col A) unmoved, rook2 (at col H) unmoved)
        self.canCastlingBlack = [True, True, True] 
        self.checkmate = False
        self.stalemate = False
        self.whiteCaptives = []
        self.blackCaptives = []

        # standard board initialization
        self.whitePieces = [Pawn('p', 6, c, PLAYER_WHITE) for c in range(BOARD_SIZE)] + \
                           [Rook('r', 7, 0, PLAYER_WHITE), Rook('r', 7, 7, PLAYER_WHITE)] + \
                           [Knight('n', 7, 1, PLAYER_WHITE), Knight('n', 7, 6, PLAYER_WHITE)] + \
                           [Bishop('b', 7, 2, PLAYER_WHITE), Bishop('b', 7, 5, PLAYER_WHITE)] + \
                           [Queen('q', 7, 3, PLAYER_WHITE), King('k', 7, 4, PLAYER_WHITE)]
        self.blackPieces = [Pawn('P', 1, c, PLAYER_BLACK) for c in range(BOARD_SIZE)] + \
                           [Rook('R', 0, 0, PLAYER_BLACK), Rook('R', 0, 7, PLAYER_BLACK)] + \
                           [Knight('N', 0, 1, PLAYER_BLACK), Knight('N', 0, 6, PLAYER_BLACK)] + \
                           [Bishop('B', 0, 2, PLAYER_BLACK), Bishop('B', 0, 5, PLAYER_BLACK)] + \
                           [Queen('Q', 0, 3, PLAYER_BLACK), King('K', 0, 4, PLAYER_BLACK)]
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for whitePiece in self.whitePieces: 
            x, y = whitePiece.getRow(), whitePiece.getCol()
            self.board[x][y] = whitePiece
        for blackPiece in self.blackPieces: 
            x, y = blackPiece.getRow(), blackPiece.getCol()
            self.board[x][y] = blackPiece
            
        # TODO: initialization of veiled chess board and a board that stores the real state (true chess under the veil)

    def printBoard(self):
        print("  A B C D E F G H")
        for i in range(BOARD_SIZE):
            print(BOARD_SIZE-i, end=" ")
            for j in range(BOARD_SIZE):
                asciiName = self.board[i][j].getName() if self.board[i][j] != EMPTY else EMPTY
                unicodeSymbol = UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(asciiName)]
                print(unicodeSymbol, end=" ")
            print(BOARD_SIZE-i)
        print("  A B C D E F G H")

    def getPiece(self, r, c):
        if 0 <= r < 8 and 0 <= c < 8: return self.board[r][c]
        else: raise Exception("Out of bounds")


if __name__ == '__main__':
    board = Board()
    board.printBoard()
