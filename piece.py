from macro import * 

class Piece:
    def __init__(self, name, row, col, player):
        # use _{variable name} to denote protected/private instance attribute (in convention)
        self._name = name # name of true unveiled piece
        self._row = row
        self._col = col
        self._player = player # white or black
        self.unmoved = True # veiled (unmoved) for each piece, also for castling check for Rooks and Kings
    
    def getName(self):
        return self._name

    def getPlayer(self):
        return self._player

    def getRow(self):
        return self._row

    def setRow(self, newRow):
        self._row = newRow

    def getCol(self):
        return self._col

    def setCol(self, newCol):
        self._col = newCol
    
    def normalMove(self, GameBoard):
        '''
        Moves that does not take enemy's piece

        Input: 
            GameBoard (Board): current game state
        
        Output:
            moves (List[Tuple[int, int]]): list of (row, col) tuple that represents the 
            board position where the piece can move to
        '''
        pass 

    def pieceTakingMove(self, GameBoard):
        '''
        Moves that takes enemy's piece

        Input: 
            GameBoard (Board): current game state
        
        Output:
            moves (List[Tuple[int, int]]): list of (row, col) tuple that represents the 
            board position where the piece can move to
        '''
        pass

    def getLegalMoves(self, GameBoard):
        '''
        All possible legal moves

        Input: 
            GameBoard (Board): current game state
        
        Output:
            moves (List[Tuple[int, int]]): list of (row, col) tuple that represents the 
            board position where the piece can move to
        '''
        pass

# Pawn
class Pawn(Piece):
    def __init__(self, name, row, col, player):
        super().__init__(name, row, col, player)
    
    def normalMove(self, GameBoard):
        moves = []
        if self.getPlayer() == PLAYER_WHITE:
            x, y = self.getRow(), self.getCol() # current position
            if x-1 >= 0 and GameBoard.getPiece(x-1, y) == EMPTY: 
                moves.append((x-1, y))
                if x == 6 and GameBoard.getPiece(x-2, y) == EMPTY: # first move can move 2 squares vertically if unblocked
                    moves.append((x-2, y))
        elif self.getPlayer() == PLAYER_BLACK:
            x, y = self.getRow(), self.getCol() # current position
            if x+1 < BOARD_SIZE and GameBoard.getPiece(x+1, y) == EMPTY: 
                moves.append((x+1, y))
                if x == 1 and GameBoard.getPiece(x+2, y) == EMPTY: # first move can move 2 squares vertically if unblocked
                    moves.append((x+2, y))
        return moves
    
    def pieceTakingMove(self, GameBoard):
        moves = []
        if self.getPlayer() == PLAYER_WHITE:
            x, y = self.getRow(), self.getCol() # current position
            if x-1 >= 0 and y-1 >= 0 and GameBoard.getPiece(x-1, y-1) != EMPTY and GameBoard.getPiece(x-1, y-1).getPlayer() != self.getPlayer(): 
                moves.append((x-1, y-1))
            if x-1 >= 0 and y+1 < BOARD_SIZE and GameBoard.getPiece(x-1, y+1) != EMPTY and GameBoard.getPiece(x-1, y+1).getPlayer() != self.getPlayer(): 
                moves.append((x-1, y+1))
        elif self.getPlayer() == PLAYER_BLACK:
            x, y = self.getRow(), self.getCol() # current position
            if x+1 < BOARD_SIZE and y-1 >= 0 and GameBoard.getPiece(x+1, y-1) != EMPTY and GameBoard.getPiece(x+1, y-1).getPlayer() != self.getPlayer(): 
                moves.append((x+1, y-1))
            if x+1 < BOARD_SIZE and y+1 < BOARD_SIZE and GameBoard.getPiece(x+1, y+1) != EMPTY and GameBoard.getPiece(x+1, y+1).getPlayer() != self.getPlayer(): 
                moves.append((x+1, y+1))
        return moves
    
    def getLegalMoves(self, GameBoard):
        return self.normalMove(GameBoard)+self.pieceTakingMove(GameBoard)

# Rook
class Rook(Piece):
    def __init__(self, name, row, col, player):
        super().__init__(name, row, col, player)

    def traverse(self, GameBoard):
        normalMoves, pieceTakingMoves = [], []
        x, y = self.getRow(), self.getCol() # current position
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)] # position change in direction left, right, top, down
        for dir in dirs:
            currX, currY = x, y
            while currX+dir[0] >= 0 and currX+dir[0] < BOARD_SIZE and currY+dir[1] >= 0 and currY+dir[1] < BOARD_SIZE:
                currX += dir[0]
                currY += dir[1]
                if GameBoard.getPiece(currX, currY) == EMPTY:
                    normalMoves.append((currX, currY))
                elif GameBoard.getPiece(currX, currY) != EMPTY and GameBoard.getPiece(currX, currY).getPlayer() != self.getPlayer(): 
                    pieceTakingMoves.append((currX, currY))
                    break
                else: break
        return normalMoves, pieceTakingMoves
    
    def normalMove(self, GameBoard):
        return self.traverse(GameBoard)[0]
    
    def pieceTakingMove(self, GameBoard):
        return self.traverse(GameBoard)[1]
    
    def getLegalMoves(self, GameBoard):
        return self.normalMove(GameBoard)+self.pieceTakingMove(GameBoard)

# Knight
class Knight(Piece):
    def __init__(self, name, row, col, player):
        super().__init__(name, row, col, player)
    
    def traverse(self, GameBoard):
        normalMoves, pieceTakingMoves = [], []
        x, y = self.getRow(), self.getCol() # current position
        dirs = [(-1, -2), (-1, 2), (-2, -1), (-2, 1), (1, -2), (1, 2), (2, -1), (2, 1)] # position change in eight directions
        for dir in dirs:
            if x+dir[0] >= 0 and x+dir[0] < BOARD_SIZE and y+dir[1] >= 0 and y+dir[1] < BOARD_SIZE:
                if GameBoard.getPiece(x+dir[0], y+dir[1]) == EMPTY:
                    normalMoves.append((x+dir[0], y+dir[1]))
                elif GameBoard.getPiece(x+dir[0], y+dir[1]) != EMPTY and GameBoard.getPiece(x+dir[0], y+dir[1]).getPlayer() != self.getPlayer(): 
                    pieceTakingMoves.append((x+dir[0], y+dir[1]))
        return normalMoves, pieceTakingMoves
    
    def normalMove(self, GameBoard):
        return self.traverse(GameBoard)[0]
    
    def pieceTakingMove(self, GameBoard):
        return self.traverse(GameBoard)[1]
    
    def getLegalMoves(self, GameBoard):
        return self.normalMove(GameBoard)+self.pieceTakingMove(GameBoard)

# Bishop
class Bishop(Piece):
    def __init__(self, name, row, col, player):
        super().__init__(name, row, col, player)
    
    def traverse(self, GameBoard):
        normalMoves, pieceTakingMoves = [], []
        x, y = self.getRow(), self.getCol() # current position
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # position change in direction top-left, top-right, down-left, down-right
        for dir in dirs:
            currX, currY = x, y
            while currX+dir[0] >= 0 and currX+dir[0] < BOARD_SIZE and currY+dir[1] >= 0 and currY+dir[1] < BOARD_SIZE:
                currX += dir[0]
                currY += dir[1]
                if GameBoard.getPiece(currX, currY) == EMPTY:
                    normalMoves.append((currX, currY))
                elif GameBoard.getPiece(currX, currY) != EMPTY and GameBoard.getPiece(currX, currY).getPlayer() != self.getPlayer(): 
                    pieceTakingMoves.append((currX, currY))
                    break
                else: break
        return normalMoves, pieceTakingMoves
    
    def normalMove(self, GameBoard):
        return self.traverse(GameBoard)[0]
    
    def pieceTakingMove(self, GameBoard):
        return self.traverse(GameBoard)[1]
    
    def getLegalMoves(self, GameBoard):
        return self.normalMove(GameBoard)+self.pieceTakingMove(GameBoard)

class Queen(Piece):
    def __init__(self, name, row, col, player):
        super().__init__(name, row, col, player)
    
    # combination of checkings of Rooks and Bishops 
    def normalMove(self, GameBoard):
        return Rook.normalMove(Rook(self.getName(), self.getRow(), self.getCol(), self.getPlayer()), GameBoard) + \
               Bishop.normalMove(Bishop(self.getName(), self.getRow(), self.getCol(), self.getPlayer()), GameBoard)
    
    def pieceTakingMove(self, GameBoard):
        return Rook.pieceTakingMove(Rook(self.getName(), self.getRow(), self.getCol(), self.getPlayer()), GameBoard) + \
               Bishop.pieceTakingMove(Bishop(self.getName(), self.getRow(), self.getCol(), self.getPlayer()), GameBoard)
    
    def getLegalMoves(self, GameBoard):
        return self.normalMove(GameBoard)+self.pieceTakingMove(GameBoard)

class King(Piece):
    def __init__(self, name, row, col, player):
        super().__init__(name, row, col, player)
        
    def traverse(self, GameBoard):
        normalMoves, pieceTakingMoves = [], []
        x, y = self.getRow(), self.getCol() # current position
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)] # position change in eight directions
        for dir in dirs:
            if x+dir[0] >= 0 and x+dir[0] < BOARD_SIZE and y+dir[1] >= 0 and y+dir[1] < BOARD_SIZE:
                if GameBoard.getPiece(x+dir[0], y+dir[1]) == EMPTY:
                    normalMoves.append((x+dir[0], y+dir[1]))
                elif GameBoard.getPiece(x+dir[0], y+dir[1]) != EMPTY and GameBoard.getPiece(x+dir[0], y+dir[1]).getPlayer() != self.getPlayer(): 
                    pieceTakingMoves.append((x+dir[0], y+dir[1]))
        return normalMoves, pieceTakingMoves
    
    def normalMove(self, GameBoard):
        return self.traverse(GameBoard)[0]
    
    def pieceTakingMove(self, GameBoard):
        return self.traverse(GameBoard)[1]
    
    def getLegalMoves(self, GameBoard):
        return self.normalMove(GameBoard)+self.pieceTakingMove(GameBoard)