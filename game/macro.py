# Define necessary game macros & model training parameters

# Chess game macros
UNICODE_PIECE_SYMBOLS = u'.●♟♞♝♜♛♚♔♕♖♗♘♙○'
ASCII_PIECE_CHARS = '.VPNBRQKkqrbnpv'
COLOR_WHITE = (220, 208, 194)
COLOR_BLACK = (53, 53, 53)
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
