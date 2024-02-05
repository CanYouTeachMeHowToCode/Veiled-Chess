# Define necessary game macros & model training parameters

# Chess game macros
UNICODE_PIECE_SYMBOLS = u'.●♟♞♝♜♛♚♔♕♖♗♘♙○'
ASCII_PIECE_CHARS = '.VPNBRQKkqrbnpv'
COLOR_WHITE = (234, 235, 200) 
COLOR_BLACK = (119, 154, 88)
COLOR_GREEN = (0, 255, 100)
COLOR_RED = (229, 57, 53)
COLOR_YELLOW = (255, 241, 118)
PLAYER_WHITE = 'white'
PLAYER_BLACK = 'black'
BOARD_SIZE = 8
EMPTY = '.'
STANDARD_BOARD = ['RNBQKBNR',
                  'PPPPPPPP',
                  '........',
                  '........',
                  '........',
                  '........',
                  'pppppppp',
                  'rnbqkbnr']

# CLI utility functions
def convertTupleToCoord(position):
    return chr(ord('A')+position[1])+str(BOARD_SIZE-position[0])

def convertCoordToTuple(position): 
    letter = position[0].upper()
    number = BOARD_SIZE-int(position[1])
    if letter not in "ABCDEFGH" or number not in range(BOARD_SIZE): return -1, -1
    return number, ord(letter)-ord('A')

# Model training parameters
BATCH_SIZE = 64
LR = 5e-5
NUM_EPOCHS = 100
