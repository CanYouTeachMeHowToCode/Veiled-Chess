from piece import *
UNICODE_PIECE_SYMBOLS = u'.♟♞♝♜♛♚♔♕♖♗♘♙'
ASCII_PIECE_CHARS = '.PNBRQKkqrbnp'
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

        # board initialization
        # whiteRook1 = Rook()

    def printBoard(self):
        print("  A B C D E F G H")
        for i in range(8):
            print(8-i, end=" ")
            for j in range(8):
                print(self.board[i][j], end=" ")
            print(8-i)
        print("  A B C D E F G H")

    def move(self, start, end):
        x1, y1 = self.convertPosition(start)
        x2, y2 = self.convertPosition(end)
        if (x1 == -1 and y1 == -1) or (x2 == -1 and y2 == -1): 
            print("Invalid input position.")
            return 
        x1, x2 = 7-x1, 7-x2
        if self.board[x1][y1] == " ":
            print("There is no piece at that position.")
            return
        if self.currPlayer == "white" and self.board[x1][y1].islower():
            print("It is not your turn.")
            return
        if self.currPlayer == "black" and self.board[x1][y1].isupper():
            print("It is not your turn.")
            return
        if not self.isLegalMove(x1, y1, x2, y2):
            print("Invalid move.")
            return
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = " "
        self.currPlayer = "white" if self.currPlayer == "black" else "black"

    def convertPosition(self, position):
        letter = position[0].upper()
        number = int(position[1])-1
        if letter not in "ABCDEFGH" or number not in range(8): return -1, -1
        return number, ord(letter)-ord('A')

    def isLegalMove(self, x1, y1, x2, y2):
        piece = self.board[x1][y1]
        if piece == " ": return False
        if self.currPlayer == "white" and piece.islower(): return False
        if self.currPlayer == "black" and piece.isupper(): return False
        if x1 == x2 and y1 == y2: return False

        if piece.upper() == "P": # Pawn
            # the first move of Pawns can be two blocks vertically if the path isn't blocked by other pieces
            if x1 == 6:
                if x2 == x1-2 and y1 == y2 and self.board[x2][y2] == " " and self.board[x2+1][y2] == " ": return True
            if x1 == 1:
                if x2 == x1+2 and y1 == y2 and self.board[x2][y2] == " " and self.board[x2-1][y2] == " ": return True

            # normal move
            if (x2 == x1-1 or x2 == x1+1) and y1 == y2 and self.board[x2][y2] == " ": return True

            # take opponent's piece
            if (x2 == x1-1 or x2 == x1+1) and abs(y2-y1) == 1 and self.board[x2][y2].isupper() != self.board[x1][y1].isupper(): return True
            return False

        elif piece.upper() == "R": # Rook
            if x1 != x2 and y1 != y2: return False # must remain in the same row or column
            if x1 == x2:
                for y in range(min(y1, y2)+1, max(y1, y2)):
                    if self.board[x1][y] != " ": return False
            elif y1 == y2:
                for x in range(min(x1, x2)+1, max(x1, x2)):
                    if self.board[x][y1] != " ": return False
            return True

        elif piece.upper() == "N": # Knight
            dx, dy = abs(x1-x2), abs(y1-y2)
            if (dx == 2 and dy == 1) or (dx == 1 and dy == 2): return True
            return False

        elif piece.upper() == "B": # Bishop
            if abs(x1-x2) != abs(y1-y2): return False # must remain in the square with same color
            dx, dy = 1 if x2 > x1 else -1, 1 if y2 > y1 else -1
            x, y = x1+dx, y1+dy
            while x != x2 and y != y2:
                if self.board[x][y] != " ": return False
                x += dx
                y += dy
            return True

        elif piece.upper() == "Q": # Queen
            # combination of checkings of Rooks and Bishops 
            if x1 == x2 or y1 == y2 or abs(x1-x2) == abs(y1-y2): 
                if x1 == x2:
                    for y in range(min(y1, y2)+1, max(y1, y2)):
                        if self.board[x1][y] != " ": return False
                elif y1 == y2:
                    for x in range(min(x1, x2)+1, max(x1, x2)):
                        if self.board[x][y1] != " ": return False
                else:
                    dx = 1 if x2 > x1 else -1
                    dy = 1 if y2 > y1 else -1
                    x, y = x1+dx, y1+dy
                    while x != x2 and y != y2:
                        if self.board[x][y] != " ": return False
                        x += dx
                        y += dy
                return True

        elif piece.upper() == "K": # King
            dx, dy = abs(x1-x2), abs(y1-y2)
            if dx <= 1 and dy <= 1: return True
            return False

    def check(self, player):
        opponentPlayer = ["white", "black"][int(self.currPlayer == "white")]
        

    # TODO: castling, check/checkmate check