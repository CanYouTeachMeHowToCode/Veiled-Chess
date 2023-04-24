# Script for dataset simulation
import sys
import io
import pandas as pd
from scripts.board import Board
from scripts.ai import AI
from scripts.macro import *

def generateData(numGames, path, whiteLevel, blackLevel):
    '''
    Function for generating dataset for training nn-based content filtering model;
    Dataset columns:
    board (List[List[str]]): current veiled chess board (with veiled pieces represented by 'v' or 'V')
    player (str): current player to move
    gameStateInfo (List[bool]): current castling availibilities for white King, white Queen, black King and black queen
    score (float): the "true score" from stockfish, the label column 

    Input:
        numGames (int): number of games to player to generate the dataset
        path (str): path of output csv file
        whiteLevel (int): level of AI agent for player white
        blackLevel (int): level of AI agent for player black
    
    Output:
        data (pd.DataFrame): dataset for training in pandas dataframe format
    '''
    # initialization
    data = pd.DataFrame(columns=['board', 'player', 'gameInfo', 'score'])
    index = 0
    for i in range(numGames):
        print(f"================== Game {i+1} ==================")
        GameBoard = Board()
        print("Game start")
        GameBoard.printBoard()
        print("Real Board: ")
        GameBoard.printRealBoard()
        whiteAI = AI(GameBoard, whiteLevel) 
        blackAI = AI(GameBoard, blackLevel)
        sys.stdin = io.StringIO('q\n'*100000) # default pawn promotion to queen for AI (may be modified later)
        while not GameBoard.gameOver:
            print()
            player = GameBoard.currPlayer
            print(f"{player}'s turn")
            board, gameStateInfo = GameBoard.getBoard()
            score, move = whiteAI.nextMove() if player == PLAYER_WHITE else blackAI.nextMove() 
            start, end = GameBoard.convertTupleToCoord(move[0]), GameBoard.convertTupleToCoord(move[1])
            # create new row and insert new row to dataframe
            data.at[index, 'board'] = board
            data.at[index, 'player'] = player
            data.at[index, 'gameInfo'] = gameStateInfo
            data.at[index, 'score'] = score
            print(data)
            print(len(data))
            data.to_csv(path, index=False)
            
            GameBoard.move(start, end, verbose=True)
            GameBoard.printBoard()
            index += 1
    return data
    
if __name__ == '__main__':
    data = generateData(10)