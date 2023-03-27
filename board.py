from macro import *
from piece import *
import sys
import io
import random

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

'''
Veiled chess board  
  A B C D E F G H
8 ● ● ● ● ♚ ● ● ● 8
7 ● ● ● ● ● ● ● ● 7
6                 6
5                 5
4                 4
3                 3
2 ○ ○ ○ ○ ○ ○ ○ ○ 2
1 ○ ○ ○ ○ ♔ ○ ○ ○ 1
  A B C D E F G H
'''

class Board:
    def __init__(self):
        self.currPlayer = PLAYER_WHITE # white start
        self.checkmate = False
        self.stalemate = False
        self.gameOver = False
        self.whiteCaptives = []
        self.blackCaptives = []

        # initialization
        whitePiecesExceptKing = 'p'*8+'r'*2+'n'*2+'b'*2+'q'
        blackPiecesExceptKing = 'P'*8+'R'*2+'N'*2+'B'*2+'Q'
        whiteShuffled = ''.join(random.sample(whitePiecesExceptKing, len(whitePiecesExceptKing)))
        blackShuffled = ''.join(random.sample(blackPiecesExceptKing, len(blackPiecesExceptKing)))
        # self.whitePieces = [Pawn('p', 6, c, PLAYER_WHITE, whiteShuffled[c]) for c in range(BOARD_SIZE)] + \
        #                    [Rook('r', 7, 0, PLAYER_WHITE, whiteShuffled[8]), Rook('r', 7, 7, PLAYER_WHITE, whiteShuffled[9])] + \
        #                    [Knight('n', 7, 1, PLAYER_WHITE, whiteShuffled[10]), Knight('n', 7, 6, PLAYER_WHITE, whiteShuffled[11])] + \
        #                    [Bishop('b', 7, 2, PLAYER_WHITE, whiteShuffled[12]), Bishop('b', 7, 5, PLAYER_WHITE, whiteShuffled[13])] + \
        #                    [Queen('q', 7, 3, PLAYER_WHITE, whiteShuffled[14]), King('k', 7, 4, PLAYER_WHITE, 'k')]
        # self.blackPieces = [Pawn('P', 1, c, PLAYER_BLACK, blackShuffled[c]) for c in range(BOARD_SIZE)] + \
        #                    [Rook('R', 0, 0, PLAYER_BLACK, blackShuffled[8]), Rook('R', 0, 7, PLAYER_BLACK, blackShuffled[9])] + \
        #                    [Knight('N', 0, 1, PLAYER_BLACK, blackShuffled[10]), Knight('N', 0, 6, PLAYER_BLACK, blackShuffled[11])] + \
        #                    [Bishop('B', 0, 2, PLAYER_BLACK, blackShuffled[12]), Bishop('B', 0, 5, PLAYER_BLACK, blackShuffled[13])] + \
        #                    [Queen('Q', 0, 3, PLAYER_BLACK, blackShuffled[14]), King('K', 0, 4, PLAYER_BLACK, 'K')]

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
        
        self._board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for whitePiece in self.whitePieces: self.setPiece(whitePiece.getRow(), whitePiece.getCol(), whitePiece)
        for blackPiece in self.blackPieces: self.setPiece(blackPiece.getRow(), blackPiece.getCol(), blackPiece)

    # def printBoard(self): 
    #     print("  A B C D E F G H")
    #     for i in range(BOARD_SIZE):
    #         print(BOARD_SIZE-i, end=" ")
    #         for j in range(BOARD_SIZE):
    #             asciiName = ""
    #             piece = self.getPiece(i, j)
    #             if piece == EMPTY: asciiName = EMPTY
    #             elif piece.getName().upper == 'K': asciiName = piece.getName() # Kings are always unveiled
    #             elif piece.unmoved: asciiName = 'v' if piece.getPlayer() == PLAYER_WHITE else 'V'
    #             else: asciiName = piece.getName()
    #             unicodeSymbol = UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(asciiName)]
    #             print(unicodeSymbol, end=" ")
    #         print(BOARD_SIZE-i)
    #     print("  A B C D E F G H")

    def printBoard(self):
        print("  A B C D E F G H")
        for i in range(BOARD_SIZE):
            print(BOARD_SIZE-i, end=" ")
            for j in range(BOARD_SIZE):
                piece = self.getPiece(i, j)
                asciiName = piece.getName() if piece != EMPTY else EMPTY
                unicodeSymbol = UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(asciiName)]
                print(unicodeSymbol, end=" ")
            print(BOARD_SIZE-i)
        print("  A B C D E F G H")
    
    def printRealBoard(self):
        print("  A B C D E F G H")
        for i in range(BOARD_SIZE):
            print(BOARD_SIZE-i, end=" ")
            for j in range(BOARD_SIZE):
                asciiName = ""
                piece = self.getPiece(i, j)
                asciiName = piece.getRealPieceName() if piece != EMPTY else EMPTY
                unicodeSymbol = UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(asciiName)]
                print(unicodeSymbol, end=" ")
            print(BOARD_SIZE-i)
        print("  A B C D E F G H")

    def getPiece(self, r, c):
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE: return self._board[r][c]
        raise Exception("Out of bounds")

    def setPiece(self, r, c, piece):
        self._board[r][c] = piece

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
        # legal castling moves
        if piece.getName() == 'K': 
            assert(self.currPlayer == PLAYER_BLACK)
            if self.canCastlingKingside(self.currPlayer): legalMoves.append((0, 6))
            elif self.canCastlingQueenside(self.currPlayer): legalMoves.append((0, 2))
        elif piece.getName() == 'k': 
            assert(self.currPlayer == PLAYER_WHITE)
            if self.canCastlingKingside(self.currPlayer): legalMoves.append((7, 6))
            elif self.canCastlingQueenside(self.currPlayer): legalMoves.append((7, 2))
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

    def isThreatened(self, player, position):
        '''
        Check if the piece at position of current player is directly threatened by any of the enemy pieces

        Input:
            player (String): current player
            position (Tuple[int, int]): tuple of piece position
        
        Output:
            isThreatened (bool): whether piece at this position of current player is threatened or not
        '''
        opponentPieces = self.blackPieces if player == PLAYER_WHITE else self.whitePieces
        for piece in opponentPieces:
            if position in piece.getLegalMoves(self): return True
        return False

    def isOnCheck(self, player):
        '''
        Check if current player is immmediately on check (the King of the player
        is directly threatened by any of the enemy pieces)

        Input:
            player (String): current player
        
        Output:
            isOnCheck (bool): whether current player is on check or not on the board
        '''
        kingLocation = self.getKingLocation(player)
        return self.isThreatened(player, kingLocation)
    
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
        pieceTaken = self.getPiece(r2, c2)
        self.setPiece(r2, c2, piece)
        self.setPiece(r1, c1, EMPTY)
        # castling move
        if piece.getName().upper() == 'K' and abs(c2-c1) == 2:
            if c2 == 6: # Kingside castling
                rook = self.getPiece(r1, 7)
                assert(rook.getName().upper() == 'R')
                assert(r1 == r2)
                rook.setRow(r2)
                rook.setCol(5)
                self.setPiece(r2, 5, rook)
                self.setPiece(r2, 7, EMPTY)
            elif c2 == 2: # Kingside castling
                rook = self.getPiece(r1, 0)
                assert(rook.getName().upper() == 'R')
                assert(r1 == r2)
                rook.setRow(r2)
                rook.setCol(3)
                self.setPiece(r2, 3, rook)
                self.setPiece(r2, 0, EMPTY)
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
        self.setPiece(r1, c1, piece)
        self.setPiece(r2, c2, pieceTaken)
        if pieceTaken != EMPTY:
            if player == PLAYER_WHITE: 
                self.blackPieces.append(pieceTaken)
                self.whiteCaptives.pop()
            else:
                self.whitePieces.append(pieceTaken)
                self.blackCaptives.pop()
    
    '''
    Castling Rules:
    1. Neither the king nor the rook has previously moved.
    2. There are no pieces between the king and the rook.
    3. The king is not currently in check.
    4. The king does not pass through or finish on a square that is attacked by an enemy piece.
    '''
    def canCastlingKingside(self, player):
        '''
        Check whether the current player can castling kingside

        Input:
            player (String): current player
        
        Output:
            canCastle (bool): can castling kingside or not
        '''
        return self.getPiece(0, 7) != EMPTY and self.getPiece(0, 7).getName() == 'R' and self.getPiece(0, 7).unmoved and \
                self.getPiece(0, 4) != EMPTY and self.getPiece(0, 4).getName() == 'K' and self.getPiece(0, 4).unmoved and \
                self.getPiece(0, 5) == EMPTY and not self.isThreatened(player, (0, 5)) and \
                self.getPiece(0, 6) == EMPTY and not self.isThreatened(player, (0, 6)) \
                if player == PLAYER_BLACK else \
                self.getPiece(7, 7) != EMPTY and self.getPiece(7, 7).getName() == 'r' and self.getPiece(7, 7).unmoved and \
                self.getPiece(7, 4) != EMPTY and self.getPiece(7, 4).getName() == 'k' and self.getPiece(7, 4).unmoved and \
                self.getPiece(7, 5) == EMPTY and not self.isThreatened(player, (7, 5)) and \
                self.getPiece(7, 6) == EMPTY and not self.isThreatened(player, (7, 6))

    def canCastlingQueenside(self, player):
        '''
        Check whether the current player can castling queenside

        Input:
            player (String): current player
        
        Output:
            canCastle (bool): can castling queenside or not
        '''
        return self.getPiece(0, 0) != EMPTY and self.getPiece(0, 0).getName() == 'R' and self.getPiece(0, 0).unmoved and \
                self.getPiece(0, 4) != EMPTY and self.getPiece(0, 4).getName() == 'K' and self.getPiece(0, 4).unmoved and \
                self.getPiece(0, 3) == EMPTY and not self.isThreatened(player, (0, 3)) and \
                self.getPiece(0, 2) == EMPTY and not self.isThreatened(player, (0, 2)) and \
                self.getPiece(0, 1) == EMPTY if player == PLAYER_BLACK else \
                self.getPiece(7, 0) != EMPTY and self.getPiece(7, 0).getName() == 'r' and self.getPiece(7, 0).unmoved and \
                self.getPiece(7, 4) != EMPTY and self.getPiece(7, 4).getName() == 'k' and self.getPiece(7, 4).unmoved and \
                self.getPiece(7, 3) == EMPTY and not self.isThreatened(player, (7, 3)) and \
                self.getPiece(7, 2) == EMPTY and not self.isThreatened(player, (7, 2)) and \
                self.getPiece(7, 1) == EMPTY

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
            None
        '''
        allLegalMoves = self.getAllLegalMoves()
        isOnCheck = self.isOnCheck(self.currPlayer)
        if not allLegalMoves:
            if isOnCheck: 
                print("Checkmate!")
                opponent = "Black" if self.currPlayer == PLAYER_WHITE else "White"
                print("{opponent} is victorious.".format(opponent=opponent))
            else: 
                print("Stalemate!")
                print("Tie")
            self.gameOver = True

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
                canPromote = False
                if piece.getName().upper() == 'K' or piece.getName().upper() == 'R': piece.unmoved = False
                if piece.getName().upper() == 'P': canPromote = self.promoteCheck(self.currPlayer, (r2, c2))
                if canPromote: print("{pawn} promotes to {piece}".format(pawn=UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(['P', 'p'][int(self.currPlayer == PLAYER_WHITE)])], \
                                                                         piece=UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(self.getPiece(r2, c2).getName())]))
                else: print("{piece} at {start} moves to {end}".format(piece=UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(piece.getName())], start=start, end=end))
                self.switchPlayer()
                self.isGameOver()
                if self.gameOver:
                    print("Game Over!")
                    return 
                elif self.isOnCheck(self.currPlayer): print("check!")
            else: print("Invalid move. Please try another one.")

        elif piece == EMPTY: print("This square has no pieces. Please try another one.")
        else: print("You cannot move your opponent's piece. Please try another one.")

    '''
    Pawn Promotion Rules:
    1. Pawn of current player reaches the bottom line of the opponent player
    2. Pawn can choose to promote to Knight, Bishop, Rook, or Queen
    '''
    def promoteCheck(self, player, pos):
        '''
        Check whether the current player can promote one of the Pawns after movement

        Input:
            player (String): current player
            pos (Tuple[int, int]): position of the Pawn intend to promote
        
        Output:
            canPromote (bool): can promote or not
        '''
        if player == PLAYER_WHITE:
            if pos[0] == 0: 
                pieceType = input("Enter the piece you want to promote to from ['n', 'b', 'r', 'q']: \n").lower()
                if pieceType not in ['n', 'b', 'r', 'q']: 
                    raise Exception("Invalid promotion piece type. Please try another one.")
                else: 
                    piece = self.getPiece(pos[0], pos[1])
                    r, c = piece.getRow(), piece.getCol()
                    self.whitePieces.remove(piece)
                    if pieceType == 'n': newPiece = Knight(pieceType, r, c, player)
                    elif pieceType == 'b': newPiece = Bishop(pieceType, r, c, player)
                    elif pieceType == 'r': newPiece = Rook(pieceType, r, c, player)
                    elif pieceType == 'q': newPiece = Queen(pieceType, r, c, player)
                    self.whitePieces.append(newPiece)
                    self.setPiece(r, c, newPiece)
                    return True
            return False
        else: 
            if pos[0] == 7: 
                pieceType = input("Enter the piece you want to promote to from ['N', 'B', 'R', 'Q']: ").upper()
                if pieceType not in ['N', 'B', 'R', 'Q']: 
                    raise Exception("Invalid promotion piece type. Please try another one.")
                else: 
                    piece = self.getPiece(pos[0], pos[1])
                    r, c = piece.getRow(), piece.getCol()
                    self.whitePieces.remove(piece)
                    if pieceType == 'N': newPiece = Knight(pieceType, r, c, player)
                    elif pieceType == 'B': newPiece = Bishop(pieceType, r, c, player)
                    elif pieceType == 'R': newPiece = Rook(pieceType, r, c, player)
                    elif pieceType == 'Q': newPiece = Queen(pieceType, r, c, player)
                    self.whitePieces.append(newPiece)
                    self.setPiece(r, c, newPiece)
                    return True
            return False

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
    # castling check 1 (white cannot castling since King has moved)
    board.move("G1", "F3")
    board.printBoard()
    board.move("F8", "D6")
    board.printBoard()
    board.move("E1", "G1") # cannot castling
    board.printBoard()
    board.move("B1", "C3") 
    board.printBoard()
    board.move("G8", "F6") 
    board.printBoard()
    board.move("D2", "D3") 
    board.printBoard()
    board.move("E8", "G8") # can castling
    board.printBoard()

    # Checkmate test (2-step fool's checkmate)
    print("========================================")
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

    # Pawn promotion test 
    print("========================================")
    board = Board()
    board.printBoard()
    board.move("E2", "E4")
    board.printBoard()
    board.move("D7", "D5")
    board.printBoard()
    board.move("E4", "D5")
    board.printBoard()
    board.move("C7", "C6")
    board.printBoard()
    board.move("D5", "C6")
    board.printBoard()
    board.move("C8", "D7")
    board.printBoard()
    board.move("C6", "B7")
    board.printBoard()
    board.move("B8", "C6")
    board.printBoard()
    inputStr = io.StringIO('n') # mock input for promoting pawn to knight
    sys.stdin = inputStr
    board.move("B7", "A8") # promote
    board.printBoard()
    board.move("D8", "A5")
    board.printBoard()
    board.move("A8", "C7") # promoted piece move
    board.printBoard()
    print("white captives:", board.whiteCaptives)
    print("black captives:", board.blackCaptives)

