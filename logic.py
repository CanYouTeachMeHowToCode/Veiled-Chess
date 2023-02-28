class ChessGame:
    def __init__(self):
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        self.current_player = "white"
        self.game_over = False
        self.winner = None

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
        if self.current_player == "white" and self.board[x1][y1].islower():
            print("It is not your turn.")
            return
        if self.current_player == "black" and self.board[x1][y1].isupper():
            print("It is not your turn.")
            return
        if not self.isLegalMove(x1, y1, x2, y2):
            print("Invalid move.")
            return
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = " "
        self.current_player = "white" if self.current_player == "black" else "black"

    def convertPosition(self, position):
        letter = position[0].upper()
        number = int(position[1])-1
        if letter not in "ABCDEFGH" or number not in range(8): return -1, -1
        return number, ord(letter)-ord('A')

    def isLegalMove(self, x1, y1, x2, y2):
        piece = self.board[x1][y1]
        if piece == " ": return False
        if self.current_player == "white" and piece.islower(): return False
        if self.current_player == "black" and piece.isupper(): return False
        if x1 == x2 and y1 == y2: return False

        if piece.upper() == "P":
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

        if piece.upper() == "R":
            if x1 != x2 and y1 != y2: return False # must remain in the same row or column
            if x1 == x2:
                for y in range(min(y1, y2)+1, max(y1, y2)):
                    if self.board[x1][y] != " ": return False
            elif y1 == y2:
                for x in range(min(x1, x2)+1, max(x1, x2)):
                    if self.board[x][y1] != " ": return False
            return True

        if piece.upper() == "N":
            dx = abs(x1 - x2)
            dy = abs(y1 - y2)
            if (dx == 2 and dy == 1) or (dx == 1 and dy == 2): return True
            return False

        if piece.upper() == "B":
            if abs(x1-x2) != abs(y1-y2): return False # must remain in the square with same color
            dx = 1 if x2 > x1 else -1
            dy = 1 if y2 > y1 else -1
            x, y = x1 + dx, y1 + dy
            while x != x2 and y != y2:
                if self.board[x][y] != " ": return False
                x += dx
                y += dy
            return True

        if piece.upper() == "Q":
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
                    x, y = x1 + dx, y1 + dy
                    while x != x2 and y != y2:
                        if self.board[x][y] != " ": return False
                        x += dx
                        y += dy
                return True

        # TODO: king's move, check/checkmate check
