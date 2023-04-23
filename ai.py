# AI agent using deep learning & non-deep learning approaches
import random
import copy
import chess.engine
from board import Board
from macro import *

class AI():
    def __init__(self, GameBoard, level):
        self.GameBoard = GameBoard
        self.level = ['novice', 'competent', 'proficient', 'expert'][level]
    
    def getLegalMoves(self):
        return self.GameBoard.getAllLegalMoves()

    def nextMove(self):
        if self.level == 'novice': return self.noviceAIMove(verbose=False)
        elif self.level == 'competent': return self.competentAIMove(verbose=False)
        elif self.level == 'proficient': return self.proficientAIMove(verbose=False)
    
    def evaluate(self, currBoard, verbose, t=0.001):
        if currBoard.gameOver:
            if currBoard.winner == 1: return float('inf') # player white wins
            elif currBoard.winner == -1: return float('-inf') # player black wins
            else: return 0 # draw
        fen = currBoard.boardToFEN()
        engine = chess.engine.SimpleEngine.popen_uci("/usr/local/bin/stockfish")
        board = chess.Board(fen)
        info = engine.analyse(board, chess.engine.Limit(time=t))
        score = info["score"].white().score()
        if verbose: print(f"score: {score}")
        engine.quit()
        if not score: return 0
        else: return score

    def noviceAIMove(self, verbose):
        '''
        Novice level AI move--just random choice of all legal moves

        Input:
            None

        Output:
            score (float): best moving score from AI agent
            move (Tuple[Tuple[int, int], Tuple[int, int]]): best move from AI agent
        '''
        move = random.choice(self.getLegalMoves())
        simBoard = copy.deepcopy(self.GameBoard)
        simBoard.move(simBoard.convertTupleToCoord(move[0]), simBoard.convertTupleToCoord(move[1]), verbose)
        score = self.evaluate(simBoard, verbose)
        return score, move
    
    def competentAIMove(self, verbose):
        '''
        Competent level AI move--evaluated best moves with stockfish board evaluation

        Output:
            score (float): best moving score from AI agent
            move (Tuple[Tuple[int, int], Tuple[int, int]]): best move from AI agent
        '''
        moves = self.getLegalMoves()
        player = self.GameBoard.currPlayer
        if player == PLAYER_WHITE:
            bestScore, bestMove = float('-inf'), None
            for move in moves:
                simBoard = copy.deepcopy(self.GameBoard)
                simBoard.move(simBoard.convertTupleToCoord(move[0]), simBoard.convertTupleToCoord(move[1]), verbose)
                score = self.evaluate(simBoard, verbose)
                if score >= bestScore:
                    bestScore = score
                    bestMove = move
            return bestScore, bestMove
        else:
            bestScore, bestMove = float('inf'), None
            for move in moves:
                simBoard = copy.deepcopy(self.GameBoard)
                simBoard.move(simBoard.convertTupleToCoord(move[0]), simBoard.convertTupleToCoord(move[1]), verbose)
                score = self.evaluate(simBoard, verbose)
                if score <= bestScore:
                    bestScore = score
                    bestMove = move
            return bestScore, bestMove
    
    def expectiminimax(self, currBoard, player, depth, verbose):
        if currBoard.gameOver:
            if currBoard.winner == 1: return float('inf'), None # player white wins
            elif currBoard.winner == -1: return float('-inf'), None # player black wins
            else: return 0, None # draw
        
        if not depth: return self.evaluate(currBoard, verbose), None

        assert(currBoard.currPlayer == player)
        if player == PLAYER_WHITE: # max agent
            bestScore, bestMove = float('-inf'), None
            moves = currBoard.getAllLegalMoves()
            print(f"moves: {moves}")
            for move in moves:
                score = 0
                start, end = move[0], move[1]
                piece = currBoard.getPiece(start[0], start[1])
                assert(piece.getPlayer() == player)
                
                if piece.unmoved and piece.getName().upper() != 'K': # veiled piece
                    probs = currBoard.getProbabilityOfVeiledPiece(piece)
                    pieceTypes = ['P', 'R', 'N', 'B', 'Q']
                    for i in range(len(probs)):
                        simBoard = copy.deepcopy(currBoard) # board for expectiminimax child state simulation
                        prob, pieceType = probs[i], pieceTypes[i]
                        # perform move and let the piece unveil to the selected piece type
                        simBoard.move(simBoard.convertTupleToCoord(start), simBoard.convertTupleToCoord(end), verbose)
                        originalPiece = simBoard.getPiece(end[0], end[1])
                        expectedPiece = simBoard.makePiece(pieceType, end[0], end[1], player)
                        simBoard.whitePieces.remove(originalPiece)
                        simBoard.setPiece(end[0], end[1], expectedPiece)
                        simBoard.whitePieces.append(expectedPiece)
                        pieceScore, _ = self.expectiminimax(simBoard, PLAYER_BLACK, depth-1, verbose)
                        score += pieceScore*prob
                else: # unveiled piece
                    simBoard = copy.deepcopy(currBoard)
                    simBoard.move(simBoard.convertTupleToCoord(start), simBoard.convertTupleToCoord(end), verbose)
                    pieceScore, _ = self.expectiminimax(simBoard, PLAYER_BLACK, depth-1, verbose)
                    score += pieceScore
                    
                if score >= bestScore:
                    bestScore = score
                    bestMove = move
            
            return bestScore, bestMove
        
        elif player == PLAYER_BLACK: # min agent
            bestScore, bestMove = float('inf'), None
            moves = currBoard.getAllLegalMoves()
            print(f"moves: {moves}")
            for move in moves:
                score = 0
                start, end = move[0], move[1]
                piece = currBoard.getPiece(start[0], start[1])
                assert(piece.getPlayer() == player)
                if piece.unmoved and piece.getName().upper() != 'K': # veiled piece
                    probs = currBoard.getProbabilityOfVeiledPiece(piece)
                    pieceTypes = ['P', 'R', 'N', 'B', 'Q']
                    for i in range(len(probs)):
                        simBoard = copy.deepcopy(currBoard) # board for expectiminimax child state simulation
                        prob, pieceType = probs[i], pieceTypes[i]
                        # perform move and let the piece unveil to the selected piece type
                        simBoard.move(simBoard.convertTupleToCoord(start), simBoard.convertTupleToCoord(end), verbose)
                        originalPiece = simBoard.getPiece(end[0], end[1])
                        expectedPiece = simBoard.makePiece(pieceType, end[0], end[1], player)
                        simBoard.blackPieces.remove(originalPiece)
                        simBoard.setPiece(end[0], end[1], expectedPiece)
                        simBoard.blackPieces.append(expectedPiece)
                        pieceScore, _ = self.expectiminimax(simBoard, PLAYER_WHITE, depth-1, verbose)
                        score += pieceScore*prob
                else: # unveiled piece
                    simBoard = copy.deepcopy(currBoard)
                    simBoard.move(simBoard.convertTupleToCoord(start), simBoard.convertTupleToCoord(end), verbose)
                    pieceScore, _ = self.expectiminimax(simBoard, PLAYER_WHITE, depth-1, verbose)
                    score += pieceScore

                if score <= bestScore:
                    bestScore = score
                    bestMove = move
            
            return bestScore, bestMove
    
    def proficientAIMove(self, verbose):
        '''
        Proficient level AI move--evaluated best moves with Expectiminimax algorithm and stockfish board evaluation

        Output:
            score (float): best moving score from AI agent
            move (Tuple[Tuple[int, int], Tuple[int, int]]): best move from AI agent
        '''
        return self.expectiminimax(self.GameBoard, self.GameBoard.currPlayer, 1, verbose)

if __name__ == '__main__':
    board = Board()
    ai = AI(board, 0)
    fen = board.boardToFEN()
    assert(fen) == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    ai.evaluate(board, True)
    board.printBoard()
    board.printRealBoard()

    move1 = ('E2', 'E4')
    board.move(move1[0], move1[1]) # can be different pieces after unveiling
    fen = board.boardToFEN()
    print(fen)
    ai.evaluate(board, True)
    board.printBoard()

    move2 = ('E7', 'E5')
    board.move(move2[0], move2[1]) # can be different pieces after unveiling
    fen = board.boardToFEN()
    print(fen)
    ai.evaluate(board, True)
    board.printBoard()

    print("============================")
    score, move = ai.competentAIMove(verbose=True)
    print(f"score: {score}")
    print(f"move: {move}")
    move3 = board.convertTupleToCoord(move[0]), board.convertTupleToCoord(move[1])
    board.move(move3[0], move3[1]) # competent AI move
    fen = board.boardToFEN()
    print(fen)
    board.printBoard()

    print("============================")
    score, move = ai.competentAIMove(verbose=True)
    print(f"score: {score}")
    print(f"move: {move}")
    move4 = board.convertTupleToCoord(move[0]), board.convertTupleToCoord(move[1])
    board.move(move4[0], move4[1]) # competent AI move
    fen = board.boardToFEN()
    print(fen)
    board.printBoard()