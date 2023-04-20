# AI agent using deep learning & non-deep learning approaches
import random
import chess.engine
from board import Board
from macro import *

class AI():
    def __init__(self, GameBoard, level):
        self.GameBoard = GameBoard
        self.level = ['novice', 'competent', 'expert'][level]
    
    def getLegalMoves(self):
        return self.GameBoard.getAllLegalMoves()

    def nextMove(self):
        if self.level == 'novice': return self.noviceAIMove()
        elif self.level == 'competent': return self.competentAIMove()
    
    def noviceAIMove(self):
        '''
        Novice level AI move--just random choice of all legal moves

        Input:
            None

        Output:
            move (Tuple[Tuple[int, int], Tuple[int, int]]): best move from AI agent
        '''
        return random.choice(self.getLegalMoves())

    def evaluate(self, t=0.1):
        fen = self.GameBoard.boardToFEN()
        engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        board = chess.Board(fen)
        info = engine.analyse(board, chess.engine.Limit(time=t))
        score = info["score"].white().score()
        print(f"score: {score}")
        engine.quit()
        return score
    
    def competentAIMove(self):
        '''
        Competent level AI move--evaluated best moves with expectiMax algorithm and stockfish board evaluation

        Input:
            None

        Output:
            move (Tuple[Tuple[int, int], Tuple[int, int]]): best move from AI agent
        '''
        pass

if __name__ == '__main__':
    board = Board()
    ai = AI(board, 0)
    fen = board.boardToFEN()
    assert(fen) == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    ai.evaluate()
    move1 = ('E2', 'E4')
    board.move(move1[0], move1[1]) # can be different pieces after unveiling
    fen = board.boardToFEN()
    print(fen)
    ai.evaluate()
    move2 = ('E7', 'E5')
    board.move(move2[0], move2[1]) # can be different pieces after unveiling
    fen = board.boardToFEN()
    print(fen)
    ai.evaluate()