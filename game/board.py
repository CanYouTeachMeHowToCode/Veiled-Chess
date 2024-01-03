# Veiled Chess game logic
from game.macro import *
from game.piece import *
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
        # Game state initialization
        self.currPlayer = PLAYER_WHITE # white start
        self.checkmate = False
        self.stalemate = False
        self.gameOver = False
        self.winner = 0 # 1 represents player white wins, -1 represents player black wins, 0 represents draw or game haven't finished
        self.whiteCaptives = []
        self.blackCaptives = []
        self.gameLog = [] # game log (TODO: add info of piece being unveiled to which type in game log)
        self.numFullMoves = 1 # number of full moves, starts at 1 and is incremented after Black's move

        # Game board initialization
        whitePiecesExceptKing = 'p'*8+'r'*2+'n'*2+'b'*2+'q'
        blackPiecesExceptKing = 'P'*8+'R'*2+'N'*2+'B'*2+'Q'
        whiteShuffled = ''.join(random.sample(whitePiecesExceptKing, len(whitePiecesExceptKing)))
        blackShuffled = ''.join(random.sample(blackPiecesExceptKing, len(blackPiecesExceptKing)))
        self.whitePieces = [Pawn(whiteShuffled[c], 6, c, PLAYER_WHITE) for c in range(BOARD_SIZE)] + \
                           [Rook(whiteShuffled[8], 7, 0, PLAYER_WHITE), Rook(whiteShuffled[9], 7, 7, PLAYER_WHITE)] + \
                           [Knight(whiteShuffled[10], 7, 1, PLAYER_WHITE), Knight(whiteShuffled[11], 7, 6, PLAYER_WHITE)] + \
                           [Bishop(whiteShuffled[12], 7, 2, PLAYER_WHITE), Bishop(whiteShuffled[13], 7, 5, PLAYER_WHITE)] + \
                           [Queen(whiteShuffled[14], 7, 3, PLAYER_WHITE), King('k', 7, 4, PLAYER_WHITE)]
        self.blackPieces = [Pawn(blackShuffled[c], 1, c, PLAYER_BLACK) for c in range(BOARD_SIZE)] + \
                           [Rook(blackShuffled[8], 0, 0, PLAYER_BLACK), Rook(blackShuffled[9], 0, 7, PLAYER_BLACK)] + \
                           [Knight(blackShuffled[10], 0, 1, PLAYER_BLACK), Knight(blackShuffled[11], 0, 6, PLAYER_BLACK)] + \
                           [Bishop(blackShuffled[12], 0, 2, PLAYER_BLACK), Bishop(blackShuffled[13], 0, 5, PLAYER_BLACK)] + \
                           [Queen(blackShuffled[14], 0, 3, PLAYER_BLACK), King('K', 0, 4, PLAYER_BLACK)]
        
        self._board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for whitePiece in self.whitePieces: self.setPiece(whitePiece.getRow(), whitePiece.getCol(), whitePiece)
        for blackPiece in self.blackPieces: self.setPiece(blackPiece.getRow(), blackPiece.getCol(), blackPiece)

    def getPiece(self, r, c):
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE: return self._board[r][c]
        raise Exception("Out of bounds")

    def setPiece(self, r, c, piece):
        self._board[r][c] = piece

    def getPieceAsciiName(self, piece): # provisional piece type (either veiled or unveiled)
        player = piece.getPlayer()
        pieceType = piece.__class__.__name__
        if pieceType == "Pawn": return 'p' if player == PLAYER_WHITE else 'P'
        elif pieceType == "Rook": return 'r' if player == PLAYER_WHITE else 'R'
        elif pieceType == "Knight": return 'n' if player == PLAYER_WHITE else 'N'
        elif pieceType == "Bishop": return 'b' if player == PLAYER_WHITE else 'B'
        elif pieceType == "Queen": return 'q' if player == PLAYER_WHITE else 'Q'
        elif pieceType == "King": return 'k' if player == PLAYER_WHITE else 'K'

    def makePiece(self, pieceType, r, c, player):
        pieceType = pieceType.upper()
        if pieceType == 'P': newPiece = Pawn(pieceType, r, c, player)
        elif pieceType == 'N': newPiece = Knight(pieceType, r, c, player)
        elif pieceType == 'B': newPiece = Bishop(pieceType, r, c, player)
        elif pieceType == 'R': newPiece = Rook(pieceType, r, c, player)
        elif pieceType == 'Q': newPiece = Queen(pieceType, r, c, player)
        else: newPiece = King(pieceType, r, c, player)
        return newPiece

    def getBoard(self):
        '''
        Get the current board--the board that treats veiled pieces independently
        as well as the current state information;
        this function is mainly used for deep learning approach--for converting 
        current game state to the format matches with the deep nn-based content 
        filtering model for training

        Input: 
            None

        Output:
            board (List[List[str]]): board of the current game state
            gameStateInfo (List[bool]): current castling availibilities for white King, white Queen, black King and black queen
        '''
        board = []
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                piece = self.getPiece(r, c)
                if piece == EMPTY: asciiName = EMPTY
                else:
                    pieceName = self.getPieceAsciiName(piece)
                    if pieceName.upper() == 'K': asciiName = pieceName # Kings are always unveiled
                    elif piece.unmoved: asciiName = 'v' if piece.getPlayer() == PLAYER_WHITE else 'V'
                    else: asciiName = pieceName
                row.append(asciiName)
            board.append(row)
        gameStateInfo = [self.canCastlingKingsideFEN(PLAYER_WHITE),
                         self.canCastlingQueensideFEN(PLAYER_WHITE),
                         self.canCastlingKingsideFEN(PLAYER_BLACK),
                         self.canCastlingQueensideFEN(PLAYER_BLACK)]
        return board, gameStateInfo

    def getProvisionalBoard(self):
        '''
        Get the current "provisional" board--the board that treats veiled pieces 
        as the pieces they currently is; e.g. an unveiled white Queen piece at the second rank will be treated as a pawn; 
        also note that the cases of the characters that represent pieces are reversed 
        to match with FEN standard (white pieces are uppercases and black pieces are lowercases);
        this function is mainly used for non-deep learning approach--expectiminimax algorithm

        Input: 
            None

        Output:
            board (List[List[str]]): provisional board of the current game state
        '''
        board = []
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                piece = self.getPiece(r, c)
                asciiName = EMPTY if piece == EMPTY else self.getPieceAsciiName(piece)
                asciiName = asciiName.upper() if asciiName.islower() else asciiName.lower()
                row.append(asciiName)
            board.append(row)
        return board
    
    def getProbabilityOfVeiledPiece(self, piece):
        '''
        Compute the probability of the current veiled piece to become every type
        of pieces except King after unveiling; the probability of a certain veiled 
        piece that unveiled to a piece with type t is computed as follows:
        P(veiledPieceType=t) = ([# of veiled pieces with type t of the player]/[# of all veiled pieces of the player]) 
                             = ([# of pieces with type t in standard start state] -
                                [# of unveiled pieces with type t currently on board] -
                                [# of unveiled pieces with type t captured by opponent]/
                               ([# of veiled pieces currently on board] +
                                [# of veiled pieces captured by opponent]) (every piece here refers to the pieces of the same player)

        Input:
            piece (Piece): the veiled piece that is going to be unveiled in the next move

        Output:
            outputProbs (List[float]): the list of probabilities that has length equals to 5 and 
            the probability of unveil to Pawn, Rook, Knight, Bishop, and Queen from
            start to end respectively
        '''
        assert(piece.unmoved)
        pieceTypes = ['P', 'R', 'N', 'B', 'Q']
        pieceNums = [8, 2, 2, 2, 1] # number of veiled pieces (either captured or not captured) for each type of piece
        numVeiledPieces = 0 # number of veiled pieces of the player in total
        player = piece.getPlayer()
        pieces = self.whitePieces+self.blackCaptives if player == PLAYER_WHITE else self.blackPieces+self.whiteCaptives
        for piece in pieces:
            pieceType = piece.getName().upper()
            if pieceType == 'K': continue # do not consider King here
            if not piece.unmoved: pieceNums[pieceTypes.index(pieceType)] -= 1 # unveiled 
            else: numVeiledPieces += 1 # veiled     
        assert(sum(pieceNums) == numVeiledPieces)
        return list(map(lambda x:x/numVeiledPieces, pieceNums))
    
    def boardToFEN(self): 
        '''
        Get the FEN (Forsyth-Edwards Notation) of the current game state

        Input: 
            None

        Output:
            fen (str): FEN string of current board
        '''
        board = self.getProvisionalBoard()
        fen = ''
        emptyCount = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == EMPTY: emptyCount += 1
                else:
                    if emptyCount > 0:
                        fen += str(emptyCount)
                        emptyCount = 0
                    fen += board[r][c]
            if emptyCount > 0:
                fen += str(emptyCount)
                emptyCount = 0
            fen += '/'
        fen = fen[:-1]  # remove last '/'
        fen += ' '
        fen += 'w' if self.currPlayer == PLAYER_WHITE else 'b'
        fen += ' '
        castlingRights = ''
        if self.canCastlingKingsideFEN(PLAYER_WHITE): castlingRights += 'K'
        if self.canCastlingQueensideFEN(PLAYER_WHITE): castlingRights += 'Q'
        if self.canCastlingKingsideFEN(PLAYER_BLACK): castlingRights += 'k'
        if self.canCastlingQueensideFEN(PLAYER_BLACK): castlingRights += 'q'
        fen += castlingRights if castlingRights != '' else '-'
        fen += ' '
        fen += '-' # no en passant rule in veiled chess 
        fen += ' '
        fen += '0' # no half move clock rule in veiled chess
        fen += ' '
        fen += str(self.numFullMoves)
        return fen
    
    def printBoard(self):
        print("  A B C D E F G H")
        for r in range(BOARD_SIZE):
            print(BOARD_SIZE-r, end=" ")
            for c in range(BOARD_SIZE):
                piece = self.getPiece(r, c)
                if piece == EMPTY: asciiName = EMPTY
                else:
                    pieceName = self.getPieceAsciiName(piece)
                    if pieceName.upper() == 'K': asciiName = pieceName # Kings are always unveiled
                    elif piece.unmoved: asciiName = 'v' if piece.getPlayer() == PLAYER_WHITE else 'V'
                    else: asciiName = pieceName
                unicodeSymbol = UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(asciiName)]
                print(unicodeSymbol, end=" ")
            print(BOARD_SIZE-r)
        print("  A B C D E F G H")
        print("")

    def printRealBoard(self):
        print("  A B C D E F G H")
        for r in range(BOARD_SIZE):
            print(BOARD_SIZE-r, end=" ")
            for c in range(BOARD_SIZE):
                asciiName = ""
                piece = self.getPiece(r, c)
                asciiName = piece.getName() if piece != EMPTY else EMPTY
                unicodeSymbol = UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(asciiName)]
                print(unicodeSymbol, end=" ")
            print(BOARD_SIZE-c)
        print("  A B C D E F G H")
        print("")

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
        for move in allLegalMovesOfThisPiece: # we only need to check whether performing this move will not put the king in check or not
            pieceTaken, firstMove = self.doMove((r, c), move)
            if not self.isOnCheck(self.currPlayer): legalMoves.append(move)
            self.undoMove((r, c), move, pieceTaken, firstMove)
        # legal castling moves
        if self.getPieceAsciiName(piece) == 'K': 
            assert(self.currPlayer == PLAYER_BLACK)
            if self.canCastlingKingside(self.currPlayer): legalMoves.append((0, 6))
            elif self.canCastlingQueenside(self.currPlayer): legalMoves.append((0, 2))
        elif self.getPieceAsciiName(piece) == 'k': 
            assert(self.currPlayer == PLAYER_WHITE)
            if self.canCastlingKingside(self.currPlayer): legalMoves.append((7, 6))
            elif self.canCastlingQueenside(self.currPlayer): legalMoves.append((7, 2))
        return legalMoves

    def getKingLocation(self, player):
        '''
        Get the current location of the King piece of the current player on the board.

        Input:
            player (str): current player
            board (List[List[Piece]]): 2d list of piece that represents the current board
        
        Output:
            position (Tuple[int, int]): the location of the King of the player
        '''
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.getPiece(r, c)
                if piece == EMPTY: continue
                if (player == PLAYER_WHITE and self.getPieceAsciiName(piece) == 'k') or \
                   (player == PLAYER_BLACK and self.getPieceAsciiName(piece) == 'K'):
                    return (r, c)
        raise Exception("King not found.")

    def isThreatened(self, player, position):
        '''
        Check if the piece at position of current player is directly threatened by any of the enemy pieces

        Input:
            player (str): current player
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
            player (str): current player
        
        Output:
            isOnCheck (bool): whether current player is on check or not on the board
        '''
        kingLocation = self.getKingLocation(player)
        return self.isThreatened(player, kingLocation)
    
    def doMove(self, start, end):
        '''
        Perform the move of pieces at start (r1, c1) position to end (r2, c2) position
        and return the piece taken by this move if possible and whether this move is the
        piece's first move or not

        Input:
            start (Tuple[int, int]): position of the piece before move
            end (Tuple[int, int]): position of the piece after move
        
        Output:
            pieceTaken (Piece or EMPTY): the piece taken if there is a piece at end or EMPTY
            firstMove (bool): whether the move of the piece is its first move or not
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
        if piece.unmoved: 
            piece.unmoved = False
            firstMove = True
        else: firstMove = False
        # castling move
        if self.getPieceAsciiName(piece).upper() == 'K' and abs(c2-c1) == 2:
            if c2 == 6: # Kingside castling
                rook = self.getPiece(r1, 7)
                assert(self.getPieceAsciiName(rook).upper() == 'R')
                assert(r1 == r2)
                rook.setRow(r2)
                rook.setCol(5)
                self.setPiece(r2, 5, rook)
                self.setPiece(r2, 7, EMPTY)
            elif c2 == 2: # Kingside castling
                rook = self.getPiece(r1, 0)
                assert(self.getPieceAsciiName(rook).upper() == 'R')
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
        return pieceTaken, firstMove

    def undoMove(self, start, end, pieceTaken, firstMove):
        '''
        Undo the last move by restoring the taken piece if possible and the original piece from end to start

        Input:
            start (Tuple[int, int]): position of the piece before move
            end (Tuple[int, int]): position of the piece after move
            pieceTaken (Piece or EMPTY): the piece taken if there is a piece at end or EMPTY
            firstMove (bool): whether the move of the piece is its first move or not
        
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
        if firstMove:
            piece.unmoved = True
    
    '''
    Castling Rules:
    1. Neither the king nor the rook has previously moved.
    2. There are no pieces between the king and the rook.
    3. The king is not currently in check.
    4. The king does not pass through or finish on a square that is attacked by an enemy piece.
    '''
    def canCastlingKingsideFEN(self, player):
        '''
        Check whether the current player can castling kingside using the FEN notation rule

        Input:
            player (str): current player
        
        Output:
            canCastle (bool): can castling kingside or not
        '''
        return self.getPiece(0, 7) != EMPTY and self.getPieceAsciiName(self.getPiece(0, 7)) == 'R' and self.getPiece(0, 7).unmoved and \
                self.getPiece(0, 4) != EMPTY and self.getPieceAsciiName(self.getPiece(0, 4)) == 'K' and self.getPiece(0, 4).unmoved \
                if player == PLAYER_BLACK else \
                self.getPiece(7, 7) != EMPTY and self.getPieceAsciiName(self.getPiece(7, 7)) == 'r' and self.getPiece(7, 7).unmoved and \
                self.getPiece(7, 4) != EMPTY and self.getPieceAsciiName(self.getPiece(7, 4)) == 'k' and self.getPiece(7, 4).unmoved
    
    def canCastlingQueensideFEN(self, player):
        '''
        Check whether the current player can castling queenside using the FEN notation rule

        Input:
            player (str): current player
        
        Output:
            canCastle (bool): can castling queenside or not
        '''
        return self.getPiece(0, 0) != EMPTY and self.getPieceAsciiName(self.getPiece(0, 0)) == 'R' and self.getPiece(0, 0).unmoved and \
                self.getPiece(0, 4) != EMPTY and self.getPieceAsciiName(self.getPiece(0, 4)) == 'K' and self.getPiece(0, 4).unmoved \
                if player == PLAYER_BLACK else \
                self.getPiece(7, 0) != EMPTY and self.getPieceAsciiName(self.getPiece(7, 0)) == 'r' and self.getPiece(7, 0).unmoved and \
                self.getPiece(7, 4) != EMPTY and self.getPieceAsciiName(self.getPiece(7, 4)) == 'k' and self.getPiece(7, 4).unmoved
    
    def canCastlingKingside(self, player):
        '''
        Check whether the current player can castling kingside

        Input:
            player (str): current player
        
        Output:
            canCastle (bool): can castling kingside or not
        '''
        return self.canCastlingKingsideFEN(player) and \
                self.getPiece(0, 5) == EMPTY and not self.isThreatened(player, (0, 5)) and \
                self.getPiece(0, 6) == EMPTY and not self.isThreatened(player, (0, 6)) \
                if player == PLAYER_BLACK else self.canCastlingKingsideFEN(player) and \
                self.getPiece(7, 5) == EMPTY and not self.isThreatened(player, (7, 5)) and \
                self.getPiece(7, 6) == EMPTY and not self.isThreatened(player, (7, 6))

    def canCastlingQueenside(self, player):
        '''
        Check whether the current player can castling queenside

        Input:
            player (str): current player
        
        Output:
            canCastle (bool): can castling queenside or not
        '''
        return self.canCastlingQueensideFEN(player) and \
                self.getPiece(0, 3) == EMPTY and not self.isThreatened(player, (0, 3)) and \
                self.getPiece(0, 2) == EMPTY and not self.isThreatened(player, (0, 2)) and \
                self.getPiece(0, 1) == EMPTY if player == PLAYER_BLACK else \
                self.canCastlingQueensideFEN(player) and \
                self.getPiece(7, 3) == EMPTY and not self.isThreatened(player, (7, 3)) and \
                self.getPiece(7, 2) == EMPTY and not self.isThreatened(player, (7, 2)) and \
                self.getPiece(7, 1) == EMPTY

    def getAllLegalMoves(self):
        '''
        Find all legal moves of all pieces of the current player such that the move is legal; 

        Input: 
            None
        
        Output:
            allLegalMoves (List[Tuple[Tuple[int, int], Tuple[int, int]]]): list of 
            ((startRow, startCol), (endRow, endCol)) tuple that represents the 
            legal moves from position (startRow, startCol) to position (endRow, endCol)
        '''
        allLegalMoves = []
        pieces = self.whitePieces if self.currPlayer == PLAYER_WHITE else self.blackPieces
        for piece in pieces:
            piecePos = piece.getRow(), piece.getCol()
            legalMoves = self.getLegalMove(piecePos[0], piecePos[1])
            for endPos in legalMoves: allLegalMoves.append((piecePos, endPos))
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
                self.winner = 1 if opponent == "White" else -1
                print("{opponent} is victorious.".format(opponent=opponent))
            else: 
                print("Stalemate!")
                print("Tie")
            self.gameOver = True
        else:
            if len(self.whitePieces) == 1 and len(self.blackPieces) == 1: # only King left for each player is tie
                print("Tie")
                self.gameOver = True

    def switchPlayer(self):
        self.currPlayer = PLAYER_BLACK if self.currPlayer == PLAYER_WHITE else PLAYER_WHITE

    def convertTupleToCoord(self, position): # for terminal version used only (for simulation)
        return chr(ord('A')+position[1])+str(BOARD_SIZE-position[0])
    
    def convertCoordToTuple(self, position): # for terminal version used only
        letter = position[0].upper()
        number = BOARD_SIZE-int(position[1])
        if letter not in "ABCDEFGH" or number not in range(BOARD_SIZE): return -1, -1
        return number, ord(letter)-ord('A')

    def moveCLI(self, start, end): # for terminal version used only
        self.move(self.convertCoordToTuple(start), self.convertCoordToTuple(end))
  
    def move(self, start, end, verbose=True): 
        r1, c1 = start
        r2, c2 = end
        piece = self.getPiece(r1, c1)
        if piece != EMPTY and self.currPlayer == piece.getPlayer():
            legalMoves = self.getLegalMove(r1, c1)
            if (r2, c2) in legalMoves:
                pieceTaken, firstMove = self.doMove((r1, c1), (r2, c2))
                if verbose: print("{piece} at {start} moves to {end}".format(piece=UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(self.getPieceAsciiName(piece))], start=start, end=end))
                if firstMove: self.unveil(piece, verbose)

                # pawn promotion check
                canPromote = False
                if self.getPieceAsciiName(piece).upper() == 'P': canPromote = self.promoteCheck(self.currPlayer, (r2, c2))
                if verbose:
                    if canPromote: print("{pawn} promotes to {piece}".format(pawn=UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(['P', 'p'][int(self.currPlayer == PLAYER_WHITE)])], \
                                                                            piece=UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(self.getPieceAsciiName(self.getPiece(r2, c2)))]))
                
                self.switchPlayer()
                if self.currPlayer == PLAYER_WHITE: self.numFullMoves += 1
                self.gameLog.append((start, end))
                self.isGameOver()
                if self.gameOver:
                    if verbose: print("Game Over!")
                    return 
                elif self.isOnCheck(self.currPlayer): 
                    if verbose: print("check!")
                return pieceTaken
            else: print("Invalid move. Please try another one.")

        elif piece == EMPTY: print("This square has no pieces. Please try another one.")
        else: print("You cannot move your opponent's piece. Please try another one.")

    def unveil(self, piece, verbose):
        '''
        Unveil the current piece to the real piece after the first move.

        Input: 
            piece (Piece): piece going to be unveiled
        
        Output:
            None
        '''
        assert(not piece.unmoved)
        origPieceType, pieceType, r, c, player = self.getPieceAsciiName(piece), piece.getName(), piece.getRow(), piece.getCol(), piece.getPlayer()
        self.whitePieces.remove(piece) if player == PLAYER_WHITE else self.blackPieces.remove(piece)
        newPiece = self.makePiece(pieceType, r, c, player)
        newPiece.unmoved = False # mark as unveiled
        self.whitePieces.append(newPiece) if player == PLAYER_WHITE else self.blackPieces.append(newPiece)
        self.setPiece(r, c, newPiece)
        if verbose and pieceType.upper() != 'K': print(f'{UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(origPieceType)]} at {(r, c)} is unveiled to {UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(pieceType)]}')

    '''
    Pawn Promotion Rules:
    1. Pawn of current player reaches the bottom line of the opponent player
    2. Pawn can choose to promote to Knight, Bishop, Rook, or Queen
    '''
    def promoteCheck(self, player, pos):
        '''
        Check whether the current player can promote one of the Pawns after movement

        Input:
            player (str): current player
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
                    newPiece = self.makePiece(pieceType, r, c, player)
                    newPiece.unmoved = False # unveiled
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
                    self.blackPieces.remove(piece)
                    newPiece = self.makePiece(pieceType, r, c, player)
                    newPiece.unmoved = False # unveiled
                    self.blackPieces.append(newPiece)
                    self.setPiece(r, c, newPiece)
                    return True
            return False