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
	promotionMode = False
	promotePos = None

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
		if promotionMode: 
			# draw the promotion menu
			pygame.draw.rect(screen, COLOR_WHITE, (WINDOW_SIZE[0]//2-300, WINDOW_SIZE[1]//2-200, 600, 300))
			pygame.draw.rect(screen, COLOR_BLACK, (WINDOW_SIZE[0]//2-300, WINDOW_SIZE[1]//2-200, 600, 300), 5)
			promotionFont = pygame.font.Font(None, 60)
			screen.blit(promotionFont.render('Promote to:', 1, COLOR_BLACK), (WINDOW_SIZE[0]//2-110, WINDOW_SIZE[1]//2-175))
			# draw the promotion pieces options
			promotionPieces = [GameBoard.makePiece(pieceType, promotePos, promotePos, GameBoard.currPlayer) for pieceType in ['N', 'R', 'B', 'Q']]
			for idx, piece in enumerate(promotionPieces):
				pieceImage = getPieceImage(piece)
				screen.blit(pieceImage, (WINDOW_SIZE[0]//4+idx*(WINDOW_SIZE[0]//8), WINDOW_SIZE[1]*(3/8)))
			# draw the selection box
			x, y = event.pos
			if WINDOW_SIZE[0]//4 <= x < WINDOW_SIZE[0]*(3/4) and WINDOW_SIZE[1]*(3/8) <= y <= WINDOW_SIZE[1]//2:
				idx = (x-WINDOW_SIZE[0]//4)//(WINDOW_SIZE[0]//8)
				pygame.draw.rect(screen, COLOR_GREEN, (WINDOW_SIZE[0]//4+idx*(WINDOW_SIZE[0]//8), WINDOW_SIZE[0]*(3/8), WINDOW_SIZE[0]//8, WINDOW_SIZE[0]//8), 5)
			# event handling
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos
					if WINDOW_SIZE[0]//4 <= x < WINDOW_SIZE[0]*(3/4) and WINDOW_SIZE[1]*(3/8) <= y <= WINDOW_SIZE[1]//2:
						idx = (x-WINDOW_SIZE[0]//4)//(WINDOW_SIZE[0]//8)
					promotionMode = False
					GameBoard.promote(GameBoard.getPiece(promotePos[0], promotePos[1]), ['N', 'R', 'B', 'Q'][idx])
					# add some sound effect here for pawn promotion later # TODO
					# switch player and check if game is over after pawn promotion
					GameBoard.switchPlayer()
					if GameBoard.currPlayer == PLAYER_WHITE: GameBoard.numFullMoves += 1
					GameBoard.isGameOver()
					break 
		else: # normal moving mode
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
							pieceTaken, firstMove = GameBoard.doMove((draggingFrom[0], draggingFrom[1]), (r, c))
							if firstMove: GameBoard.unveil(piece) # unveil the piece after the first move
							lastMove = ((draggingFrom[0], draggingFrom[1]), (r, c))
							if pieceTaken == EMPTY: moveSound.play()
							else: capturedSound.play()
							# pawn promotion
							if GameBoard.getPieceAsciiName(piece).upper() == 'P': # first it should be a pawn
								canPromote = GameBoard.promoteCheck(GameBoard.currPlayer, (r, c))
								if canPromote: 
									promotePos = (r, c)
									promotionMode = True
							if not promotionMode: # do not switch player and check if game is over if in promotion mode
								GameBoard.switchPlayer()
								if GameBoard.currPlayer == PLAYER_WHITE: GameBoard.numFullMoves += 1
								GameBoard.isGameOver()
						dragging = False
						draggingPiece = None
				elif event.type == pygame.MOUSEMOTION:
					if dragging:
						x, y = event.pos
						x -= offset_x
						y -= offset_y
						legalMoves = GameBoard.getLegalMove(draggingFrom[0], draggingFrom[1])
						for (r, c) in legalMoves:
							pygame.draw.rect(screen, COLOR_GREEN, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
						screen.blit(getPieceImage(draggingPiece), (x, y))
						pygame.display.flip()
					
		if not dragging: 
			pygame.display.flip()

if __name__ == '__main__':
	pygameApp()
