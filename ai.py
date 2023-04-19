# AI agent using deep learning & non-deep learning approaches
import random
from board import Board
from macro import *

class AI():
    def __init__(self, GameBoard, level):
        self.GameBoard = GameBoard
        self.level = ['novice', 'competent', 'expert'][level]
    
    def getLegalMoves(self):
        return self.GameBoard.getAllLegalMoves()

    def move(self):
        legalMoves = self.getLegalMoves()
        if self.level == 'novice': return random.choice(legalMoves)
    
    def boardToFEN(self): 
        board = self.GameBoard.getSuperficialBoard()
        print(board)
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
        fen += 'w' if self.GameBoard.currPlayer == PLAYER_WHITE else 'b'
        fen += ' '
        castlingRights = ''
        if self.GameBoard.canCastlingKingsideFEN(PLAYER_WHITE): castlingRights += 'K'
        if self.GameBoard.canCastlingQueensideFEN(PLAYER_WHITE): castlingRights += 'Q'
        if self.GameBoard.canCastlingKingsideFEN(PLAYER_BLACK): castlingRights += 'k'
        if self.GameBoard.canCastlingQueensideFEN(PLAYER_BLACK): castlingRights += 'q'
        fen += castlingRights if castlingRights != '' else '-'
        fen += ' '
        fen += '-' # no en passant rule in veiled chess 
        fen += ' '
        fen += '0' # no half move clock rule in veiled chess
        fen += ' '
        fen += str(self.GameBoard.numFullMoves)
        return fen

    def evaluate(self):
        pass

if __name__ == '__main__':
    board = Board()
    ai = AI(board, 0)
    fen = ai.boardToFEN()
    assert(fen) == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
