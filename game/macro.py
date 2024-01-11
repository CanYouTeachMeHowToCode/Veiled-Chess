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

# Model training parameters
BATCH_SIZE = 64
LR = 5e-5
NUM_EPOCHS = 100
