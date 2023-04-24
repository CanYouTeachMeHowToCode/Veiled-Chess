# Define necessary game macros & model training parameters

# Chess game macros
UNICODE_PIECE_SYMBOLS = u'.●♟♞♝♜♛♚♔♕♖♗♘♙○'
ASCII_PIECE_CHARS = '.VPNBRQKkqrbnpv'
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
