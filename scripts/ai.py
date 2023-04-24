# AI agent using deep learning & non-deep learning approaches
import random
import copy
import chess.engine
import torch
import numpy as np
from scripts.macro import *
from scripts.model import VeiledChessNet

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
        else: return self.expertAIMove(verbose=False)
    
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
        NOTE: this function is indeed a "cheating" function for dataset simulation, since it 
        tries out the possible moves and unveiled the chess piece directly and perform evaluation, 
        which violates the rule of real-time player veiled chess; therefore, we cannot
        directly use this function for predicting the next move 

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
    
    def convertToModelInput(self, currBoard):
        # Encode player
        playerEncoded = 1 if currBoard.currPlayer == PLAYER_WHITE else -1
        board, gameStateInfo = currBoard.getBoard()
        # Encode board
        scores = [0, -7, -1, -3, -3, -5, -9, -100, 100, 9, 5, 3, 3, 1, 7]
        boards = np.array([board])
        ordinalBoards = np.zeros((boards.shape[0], boards.shape[1], boards.shape[2]), dtype=int)
        for i in range(boards.shape[0]):
            for j in range(boards.shape[1]):
                for k in range(boards.shape[2]):
                    char = str(boards[i, j, k]).replace("'", "")
                    ordinalBoards[i, j, k] = scores[ASCII_PIECE_CHARS.find(char)]
        ordinalBoards = np.reshape(ordinalBoards, (ordinalBoards.shape[0], 1, ordinalBoards.shape[1], ordinalBoards.shape[2]))
        gameInfo = np.array([playerEncoded]+gameStateInfo).reshape(1, -1)
        return torch.Tensor(ordinalBoards), torch.Tensor(gameInfo)

    def moveFromModel(self, model, currBoard, player, verbose):
        '''
        Find the move with highest recommedation score from the input model; for 
        each move, the scores are computed based on all the scenarios of the move 
        and added together with the multiplication of the corresponding probability

        Input: 
            model (torch.nn): the trained model for move recommendation
            currBoard (Board): the current chess board including all the game states
            player (str): current player
            verbose (bool): verbose mode
        
        Output:
            score (float): best moving score from AI agent
            move (Tuple[Tuple[int, int], Tuple[int, int]]): best move from AI agent
        '''
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
                        board, gameInfo = self.convertToModelInput(simBoard)
                        if currBoard.gameOver:
                            if currBoard.winner == 1: pieceScore = float('inf') # player white wins
                            elif currBoard.winner == -1: pieceScore = float('-inf')# player black wins
                            else: pieceScore = 0 # draw
                        else: pieceScore = model(board.float(), gameInfo.float())
                        score += pieceScore*prob
                else: # unveiled piece
                    simBoard = copy.deepcopy(currBoard)
                    simBoard.move(simBoard.convertTupleToCoord(start), simBoard.convertTupleToCoord(end), verbose)
                    board, gameInfo = self.convertToModelInput(simBoard)
                    if currBoard.gameOver:
                        if currBoard.winner == 1: pieceScore = float('inf') # player white wins
                        elif currBoard.winner == -1: pieceScore = float('-inf')# player black wins
                        else: pieceScore = 0 # draw
                    else: pieceScore = model(board.float(), gameInfo.float())
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
                        board, gameInfo = self.convertToModelInput(simBoard)
                        pieceScore = model(board.float(), gameInfo.float())
                        score += pieceScore*prob
                else: # unveiled piece
                    simBoard = copy.deepcopy(currBoard)
                    simBoard.move(simBoard.convertTupleToCoord(start), simBoard.convertTupleToCoord(end), verbose)
                    board, gameInfo = self.convertToModelInput(simBoard)
                    pieceScore = model(board.float(), gameInfo.float())
                    score += pieceScore

                if score <= bestScore:
                    bestScore = score
                    bestMove = move
            
            return bestScore, bestMove

    def proficientAIMove(self, verbose):
        '''
        Proficient level AI move--evaluated expected best moves recommended by nn-based content filtering recommendation model

        Output:
            score (float): best moving score from AI agent
            move (Tuple[Tuple[int, int], Tuple[int, int]]): best move from AI agent
        '''
        model = VeiledChessNet()
        model.load_state_dict(torch.load("./models/best_model.pth"))
        return self.moveFromModel(model, self.GameBoard, self.GameBoard.currPlayer, verbose)
    
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

    def expertAIMove(self, verbose):
        '''
        Expert level AI move--evaluated best moves with Expectiminimax algorithm and stockfish board evaluation

        Output:
            score (float): best moving score from AI agent
            move (Tuple[Tuple[int, int], Tuple[int, int]]): best move from AI agent
        '''
        return self.expectiminimax(self.GameBoard, self.GameBoard.currPlayer, 1, verbose)