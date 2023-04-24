# User interface
import streamlit as st
from scripts.board import Board
from scripts.ai import AI
from scripts.macro import *

# Define the Streamlit app
def app():
    st.title("Veiled Chess Move Recommender")
    st.markdown('**A Veiled Chess game move strategy recommender using NN-based recommendation model**')
    st.markdown('*AIPI 540 Individual Project by Yilun Wu*')
    st.write("Enter the current state of the chessboard below:")

    def getBoard():
        board = []
        for r in range(BOARD_SIZE):
            row = st.text_input(f"Row {r+1}", value="", max_chars=BOARD_SIZE, key=f"row_{r}")
            if len(row) != BOARD_SIZE: 
                st.error("Each row must have exactly 8 squares!")
                return None
            else: board.append(row)
        return board

    def convertBoard(board):
        convertedBoard = []
        for r in range(BOARD_SIZE):
            row = ''
            for c in range(BOARD_SIZE):
                pieceType = board[r][c]
                row += UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.find(pieceType)]
            convertedBoard.append(row)
        return convertedBoard
    
    board = getBoard()
    if board is not None: # input further info only when board is ready
        convertedBoard = convertBoard(board)
        st.write("Input board:")
        st.write(convertedBoard)

        allSet = True
        # Input player info
        currPlayer = st.text_input("Enter Current Player (white or black):", value="", max_chars=5, key="player")
        if currPlayer != PLAYER_WHITE and currPlayer != PLAYER_BLACK: 
            st.error("Player must be either white or black!")
            allSet = False

        # Input castling info
        if allSet:
            wk = st.text_input("Enter If Player White Can Castle King Side (y or n):", value="", max_chars=1, key="wk")
            wq = st.text_input("Enter If Player White Can Castle Queen Side (y or n):", value="", max_chars=1, key="wq")
            bk = st.text_input("Enter If Player Black Can Castle King Side (y or n):", value="", max_chars=1, key="bk")
            bq = st.text_input("Enter If Player Black Can Castle Queen Side (y or n):", value="", max_chars=1, key="bq")
            for i in [wk, wq, bk, bq]:
                if i != 'y' and i != 'n': 
                    st.error("Must enter either y or n for every castling info!")
                    allSet = False
        
        # Input captives info (each player can at most capture 15 pieces in a game)
        if allSet:
            whiteCaptives = st.text_input("Enter Veiled/Unveiled Black Pieces Captured by Player White:", value="", max_chars=15, key="wc")
            blackCaptives = st.text_input("Enter Veiled/Unveiled White Pieces Captured by Player Black:", value="", max_chars=15, key="bc")
            if whiteCaptives:
                for wc in whiteCaptives:
                    if wc not in ASCII_PIECE_CHARS.upper()[1:]: 
                        st.error("Entered invalid piece types captured by white!")
                        allSet = False
            if blackCaptives:
                for bc in whiteCaptives:
                    if bc not in ASCII_PIECE_CHARS.lower()[1:]: 
                        st.error("Entered invalid piece types captured by black!")
                        allSet = False
        
        # Input number of full moves 
        if allSet:
            numFullMoves = st.text_input("Enter Number of Full Moves:", value="", max_chars=3, key="fullMove")
            if not numFullMoves:
                st.error("Please enter the number of full moves to proceed.")
                allSet = False
            else:
                numFullMoves = int(numFullMoves) # convert to int
                if numFullMoves < 1:
                    st.error("Entered invalid number of full moves!")
                    allSet = False
        
        # Construct the game board with the available valid info provided by user
        '''
        NOTE: For each veiled piece, since we don't know the piece type, 
        we assume they have the same real piece type when forming the game board;
        this will not affect the recommendation since AI agent do not need 
        to know the real piece type
        '''
        if allSet:
            # convert castling info to boolean values
            wk, wq, bk, bq = wk == 'y', wq == 'y', bk == 'y', bq == 'y'

            # reset game board first for initialization
            GameBoard = Board()
            GameBoard.whitePieces = []
            GameBoard.blackPieces = []
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if board[r][c] == '.': GameBoard.setPiece(r, c, EMPTY)
                    else:
                        pieceType = board[r][c]
                        player = PLAYER_WHITE if pieceType.islower() else PLAYER_BLACK
                        if pieceType == 'k': # white King
                            piece = GameBoard.makePiece(pieceType, r, c, player)
                            if not wk or not wq: piece.unmoved = False
                            GameBoard.whitePieces.append(piece)
                        elif pieceType == 'K': # black King
                            piece = GameBoard.makePiece(pieceType, r, c, player)
                            if not bk or not bq: piece.unmoved = False
                            GameBoard.blackPieces.append(piece)
                        elif pieceType == 'v':
                            piece = GameBoard.makePiece(STANDARD_BOARD[r][c], r, c, player) 
                            piece.unmoved = True # veiled
                            GameBoard.whitePieces.append(piece)
                        elif pieceType == 'V':
                            piece = GameBoard.makePiece(STANDARD_BOARD[r][c], r, c, player) 
                            piece.unmoved = True # veiled
                            GameBoard.blackPieces.append(piece)
                        else:
                            piece = GameBoard.makePiece(pieceType, r, c, player)
                            piece.unmoved = False # unveiled
                            GameBoard.setPiece(r, c, piece)
                            if player == PLAYER_WHITE: GameBoard.whitePieces.append(piece)
                            else: GameBoard.blackPieces.append(piece)
                        GameBoard.setPiece(r, c, piece)
            
            # convert white/black captives from string to list
            # NOTE: For captured pieces, we use random piece and position to make it since this info is not important for it
            whiteCaptivesList = []
            if whiteCaptives:
                for wc in whiteCaptives:
                    if wc == 'V': # veiled
                        capturedPiece = GameBoard.makePiece('R', 0, 0, player) 
                        whiteCaptivesList.append(capturedPiece)
                    else:
                        capturedPiece = GameBoard.makePiece(wc, 0, 0, player)
                        whiteCaptivesList.append(capturedPiece)
            whiteCaptives = whiteCaptivesList
            GameBoard.whiteCaptives = whiteCaptives

            blackCaptivesList = []
            if blackCaptives:
                for bc in blackCaptives:
                    if bc == 'V': # veiled
                        capturedPiece = GameBoard.makePiece('r', 0, 0, player)
                        blackCaptivesList.append(capturedPiece)
                    else:
                        capturedPiece = GameBoard.makePiece(bc, 0, 0, player)
                        blackCaptivesList.append(capturedPiece)
            blackCaptives = blackCaptivesList
            GameBoard.blackCaptives = blackCaptives

            GameBoard.numFullMoves = numFullMoves
            # Initialize AI Agents
            proficientAI = AI(GameBoard, 2)
            expertAI = AI(GameBoard, 3)

            # Add a button to recommend the next move from proficient AI (Deep Learning AI Agent move)
            if st.button("Recommend Move from Proficient AI"):
                move = proficientAI.nextMove()[1]
                start, end = GameBoard.convertTupleToCoord(move[0]), GameBoard.convertTupleToCoord(move[1])
                piece = GameBoard.getPiece(move[0][0], move[0][1])
                if piece.unmoved and piece.getName().upper() != 'K': pieceSymbol = '○' if piece.getPlayer() == PLAYER_WHITE else '●'
                else: pieceSymbol = UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(GameBoard.getPieceAsciiName(piece))]
                st.write(f"The recommended move is {pieceSymbol} from {start} to {end}.")

            # Add a button to recommend the next move from expert AI (Expectiminimax AI Agent move)
            if st.button("Recommend Move from Expert AI"):
                move = expertAI.nextMove()[1]
                start, end = GameBoard.convertTupleToCoord(move[0]), GameBoard.convertTupleToCoord(move[1])
                piece = GameBoard.getPiece(move[0][0], move[0][1])
                if piece.unmoved and piece.getName().upper() != 'K': pieceSymbol = '○' if piece.getPlayer() == PLAYER_WHITE else '●'
                else: pieceSymbol = UNICODE_PIECE_SYMBOLS[ASCII_PIECE_CHARS.index(GameBoard.getPieceAsciiName(piece))]
                st.write(f"The recommended move is {pieceSymbol} from {start} to {end}.")

# Run the Streamlit app
if __name__ == '__main__':
    app()