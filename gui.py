# Graphic User Interface using PyGame
import pygame
import sys
from game.board import Board
from game.macro import *

def pygameApp():
	# initialization
	pygame.init()
	WINDOW_SIZE = (1000, 1000)
	screen = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Veiled Chess")
	SQUARE_SIZE = WINDOW_SIZE[0] // BOARD_SIZE
	font = pygame.font.Font(None, 36)
	GameBoard = Board()
	dragging = False
	draggingPiece = None
	draggingFrom = None
	offset_x, offset_y = 0, 0
	lastMove = None

	# load sound effects
	capturedSound = pygame.mixer.Sound('sounds/capture.wav')
	moveSound = pygame.mixer.Sound('sounds/move.wav')

	def getPieceImage(piece):
		pieceType = piece.__class__.__name__
		piecePlayer = piece.getPlayer()
		pieceImgPath = f'images/{piecePlayer}_{pieceType.lower()}.png' if not piece.unmoved or pieceType == 'King' else f'images/veiled_{piecePlayer}_{pieceType.lower()}.png'
		pieceImage = pygame.image.load(pieceImgPath)
		return pieceImage
	
	def drawBoard(screen):
		# draw the game board 
		for r in range(BOARD_SIZE):
			for c in range(BOARD_SIZE):
				color = COLOR_WHITE if (r+c) % 2 == 0 else COLOR_BLACK
				coordColor = COLOR_BLACK if color == COLOR_WHITE else COLOR_WHITE
				pygame.draw.rect(screen, color, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
				# row coordinates
				if c == 0: screen.blit(font.render(str(BOARD_SIZE-r), 1, coordColor), (5, 5+r*SQUARE_SIZE))
				# col coordinates
				if r == 7: screen.blit(font.render(chr(ord('A')+c), 1, coordColor), (c*SQUARE_SIZE+SQUARE_SIZE-20, WINDOW_SIZE[1]-20))
		# draw the last move tiles
		if lastMove is not None:
			start, end = lastMove
			pygame.draw.rect(screen, COLOR_YELLOW, (start[1]*SQUARE_SIZE, start[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.rect(screen, COLOR_YELLOW, (end[1]*SQUARE_SIZE, end[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
		# draw pieces
		for r in range(BOARD_SIZE):
			for c in range(BOARD_SIZE):
				piece = GameBoard.getPiece(r, c)
				if piece != EMPTY:
					pieceImage = getPieceImage(piece)
					# draw red circle with gradient color to mark that the king piece is on check
					if piece.getName().upper() == 'K' and GameBoard.isOnCheck(GameBoard.currPlayer) and piece.getPlayer() == GameBoard.currPlayer: 
						pygame.draw.circle(screen, COLOR_RED, (c*SQUARE_SIZE+SQUARE_SIZE//2, r*SQUARE_SIZE+SQUARE_SIZE//2), SQUARE_SIZE//2)
					screen.blit(pieceImage, (c*SQUARE_SIZE+(SQUARE_SIZE-pieceImage.get_width())//2, r*SQUARE_SIZE+(SQUARE_SIZE-pieceImage.get_height())//2))
	
	screen.fill((255, 255, 255))
	drawBoard(screen)
	pygame.display.flip()

	while not GameBoard.gameOver:
		drawBoard(screen)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if not dragging:
					r, c = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
					piece = GameBoard.getPiece(r, c)
					if piece != EMPTY and piece.getPlayer() == GameBoard.currPlayer:
						dragging = True
						draggingPiece = piece
						draggingFrom = (r, c)
						offset_x = event.pos[0]-c*SQUARE_SIZE
						offset_y = event.pos[1]-r*SQUARE_SIZE
			elif event.type == pygame.MOUSEBUTTONUP:
				if dragging:
					r, c = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
					# Check if the move is legal
					piece = GameBoard.getPiece(draggingFrom[0], draggingFrom[1])
					legalMoves = GameBoard.getLegalMove(draggingFrom[0], draggingFrom[1])
					if (r, c) in legalMoves:
						pieceTaken = GameBoard.move((draggingFrom[0], draggingFrom[1]), (r, c))
						lastMove = ((draggingFrom[0], draggingFrom[1]), (r, c))
						if pieceTaken == EMPTY: moveSound.play()
						else: capturedSound.play()
					dragging = False
					draggingPiece = None
			elif event.type == pygame.MOUSEMOTION:
				if dragging:
					x, y = event.pos
					x -= offset_x
					y -= offset_y
					legalMoves = GameBoard.getLegalMove(draggingFrom[0], draggingFrom[1])
					for move in legalMoves:
						pygame.draw.rect(screen, COLOR_GREEN, (move[1]*SQUARE_SIZE, move[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
					screen.blit(getPieceImage(draggingPiece), (x, y))
					pygame.display.flip()
					
		if not dragging: 
			pygame.display.flip()

if __name__ == '__main__':
	pygameApp()
