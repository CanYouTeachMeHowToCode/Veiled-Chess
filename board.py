from macro import *
from piece import *

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
        self.currPlayer = PLAYER_WHITE # white start
        self.canCastlingWhite = [True, True, True] # (king unmoved, rook1 (at col A) unmoved, rook2 (at col H) unmoved)
        self.canCastlingBlack = [True, True, True] 
        self.checkmate = False
        self.stalemate = False
        self.gameOver = False
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
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE: return self.board[r][c]
        raise Exception("Out of bounds")

    def getLegalMove(self, r, c):
        '''
        Find all legal moves of current piece located at board[r][c] such that
        the move is legal and cannot lead to the check of the king of
        the player; also, if the king is currently in check, the move must remove
        the check if possible.

        Input: 
            r (int): row of the current piece
            c (int): column of the current piece
        
        Output:
            legalMoves (List[Tuple[int, int]]): list of (row, col) tuple that represents the 
            board position where the piece can move to
        '''
        piece = self.getPiece(r, c)
        if piece == EMPTY: return []
        legalMoves = []
        allLegalMovesOfThisPiece = piece.getLegalMoves(self)
        # print("allLegalMovesOfThisPiece: ", allLegalMovesOfThisPiece)
        for move in allLegalMovesOfThisPiece: # we only need to check whether performing this move will not put the king in check or not
            # print("move: ", move)
            pieceTaken = self.doMove((r, c), move)
            if not self.isOnCheck(self.currPlayer): legalMoves.append(move)
            self.undoMove((r, c), move, pieceTaken)
        # print("legalMoves: ", legalMoves)
        return legalMoves

    def getKingLocation(self, player):
        '''
        Get the current location of the King piece of the current player on the board.

        Input:
            player (String): current player
            board (List[List[Piece]]): 2d list of piece that represents the current board
        
        Output:
            position (Tuple[int, int]): the location of the King of the player
        '''
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.getPiece(r, c)
                if piece == EMPTY: continue
                if (player == PLAYER_WHITE and piece.getName() == 'k') or \
                   (player == PLAYER_BLACK and piece.getName() == 'K'):
                    return (r, c)
        raise Exception("King not found.")

    def isOnCheck(self, player):
        '''
        Check if current player is immmediately on check (the King of the player)
        is directly threatened by any of the enemy pieces

        Input:
            player (String): current player
            board (List[List[Piece]]): 2d list of piece that represents the current board
        
        Output:
            isOnCheck (bool): whether current player is on check or not on the board
        '''
        kingLocation = self.getKingLocation(player)
        opponentPieces = self.blackPieces if player == PLAYER_WHITE else self.whitePieces
        for piece in opponentPieces:
            if kingLocation in piece.getLegalMoves(self): return True
        return False
    
    def doMove(self, start, end):
        '''
        Perform the move of pieces at start (r1, c1) position to end (r2, c2) position
        and return the piece taken by this move if possible

        Input:
            start (Tuple[int, int]): position of the piece before move
            end (Tuple[int, int]): position of the piece after move
        
        Output:
            pieceTaken (Piece or EMPTY): the piece taken if there is a piece at end or EMPTY
        '''
        r1, c1 = start
        r2, c2 = end
        piece = self.getPiece(r1, c1)
        player = piece.getPlayer()
        piece.setRow(r2)
        piece.setCol(c2)
        pieceTaken = self.board[r2][c2]
        self.board[r2][c2] = piece
        self.board[r1][c1] = EMPTY
        if pieceTaken != EMPTY:
            if player == PLAYER_WHITE: 
                self.blackPieces.remove(pieceTaken)
                self.whiteCaptives.append(pieceTaken)
            else:
                self.whitePieces.remove(pieceTaken)
                self.blackCaptives.append(pieceTaken)
        return pieceTaken

    def undoMove(self, start, end, pieceTaken):
        '''
        Undo the last move by restoring the taken piece if possible and the original piece from end to start

        Input:
            start (Tuple[int, int]): position of the piece before move
            end (Tuple[int, int]): position of the piece after move
            pieceTaken (Piece or EMPTY): the piece taken if there is a piece at end or EMPTY
        
        Output:
            None
        '''
        r1, c1 = start
        r2, c2 = end
        piece = self.getPiece(r2, c2)
        player = piece.getPlayer()
        piece.setRow(r1)
        piece.setCol(c1)
        self.board[r1][c1] = piece
        self.board[r2][c2] = pieceTaken
        if pieceTaken != EMPTY:
            if player == PLAYER_WHITE: 
                self.blackPieces.append(pieceTaken)
                self.whiteCaptives.pop()
            else:
                self.whitePieces.append(pieceTaken)
                self.blackCaptives.pop()

    def getAllLegalMoves(self):
        '''
        Find all legal moves of all pieces of the current player such that the move is legal; 

        Input: 
            None
        
        Output:
            allLegalMoves (List[Tuple[int, int]]): list of (row, col) tuple that represents the 
            board position where the piece can move to
        '''
        allLegalMoves = []
        if self.currPlayer == PLAYER_WHITE:
            for piece in self.whitePieces:
                allLegalMoves += self.getLegalMove(piece.getRow(), piece.getCol())
        else:
            for piece in self.blackPieces:
                allLegalMoves += self.getLegalMove(piece.getRow(), piece.getCol())
        return allLegalMoves

    def isGameOver(self):
        '''
        Check if the current game over or not.
        If there is no legal moves and the King piece of the current player is on check, 
        checkmate and opponent wins;
        else if there is no legal moves yet the King piece of the current player is not on check, 
        stalemate and tie

        Input:
            None

        Output:
            isGameOver (bool): is game over or not
        '''
        allLegalMoves = self.getAllLegalMoves()
        isOnCheck = self.isOnCheck(self.currPlayer)
        if not allLegalMoves:
            if isOnCheck: print("checkmate!")
            else: print("stalemate!")
            return True
        else: return False
                

    def switchPlayer(self):
        self.currPlayer = PLAYER_BLACK if self.currPlayer == PLAYER_WHITE else PLAYER_WHITE

    def convertPosition(self, position): # for terminal version used only
        letter = position[0].upper()
        number = BOARD_SIZE-int(position[1])
        if letter not in "ABCDEFGH" or number not in range(BOARD_SIZE): return -1, -1
        return number, ord(letter)-ord('A')
    
    def move(self, start, end): # for terminal version used only
        r1, c1 = self.convertPosition(start)
        r2, c2 = self.convertPosition(end)
        piece = self.getPiece(r1, c1)
        if piece != EMPTY and self.currPlayer == piece.getPlayer():
            legalMoves = self.getLegalMove(r1, c1)
            if (r2, c2) in legalMoves:
                self.doMove((r1, c1), (r2, c2))
                print("{piece} at {start} moves to {end}".format(piece=UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(piece.getName())], start=start, end=end))
                self.switchPlayer()
                if self.isGameOver(): 
                    print("Game Over!")
                    return 
                elif self.isOnCheck(self.currPlayer): print("check!")
            else: print("Invalid move. Please try another one.")

        elif piece == EMPTY: print("This square has no pieces. Please try another one.")
        else: print("You cannot move your opponent's piece. Please try another one.")

if __name__ == '__main__': # some trivial tests (will implement test in formal format later)
    # start
    board = Board()
    board.printBoard()
    # Pawn normal move test (start 2 blocks)
    board.move("E2", "E4")
    board.printBoard()
    board.move("F7", "F5")
    board.printBoard()
    # Pawn taking piece test
    board.move("E4", "F5")
    board.printBoard()
    # Knight normal move test
    board.move("B8", "C6")
    board.printBoard()
    # Bishop normal move test
    board.move("F1", "B5")
    board.printBoard()
    # Rook normal move test
    board.move("A8", "B8")
    board.printBoard()
    # Queen normal move test (also a check test)
    board.move("D1", "H5")
    board.printBoard()
    # cannot move this Pawn since Black king is on check
    board.move("E7", "E6")
    board.printBoard()
    # also cannot move the Black King since all the place the King can move to are threatened
    board.move("E8", "F7")
    board.printBoard()
    # resolve check by blocking it using black Pawn
    board.move("G7", "G6")
    board.printBoard()
    # King move test
    board.move("E1", "E2")
    board.printBoard()

    # Check test
    board.move("C6", "D4")
    board.printBoard()
    # cannot perform this step since white King is on check
    board.move("B1", "C3")
    board.printBoard()
    # resolve check by moving the king
    board.move("E2", "E1")
    board.printBoard()
    # a random move 
    board.move("E7", "E5")
    board.printBoard()
    # check again
    board.move("H5", "G6")
    board.printBoard()
    # resolve check by taking the threatening piece
    board.move("H7", "G6")
    board.printBoard()

    # Checkmate test (2-step fool's checkmate)
    board = Board()
    board.printBoard()
    board.move("G2", "G4")
    board.printBoard()
    board.move("E7", "E5")
    board.printBoard()
    board.move("F2", "F4")
    board.printBoard()
    board.move("D8", "H4")
    board.printBoard()
