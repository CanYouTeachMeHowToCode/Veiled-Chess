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
	GameBoard = Board()
	dragging = False
	draggingPiece = None
	draggingFrom = None
	offset_x, offset_y = 0, 0

	def getPieceImage(piece):
		pieceType = piece.__class__.__name__
		piecePlayer = piece.getPlayer()
		pieceImgPath = f'images/{piecePlayer}_{pieceType.lower()}.png' if not piece.unmoved or pieceType == 'King' else f'images/veiled_{piecePlayer}_{pieceType.lower()}.png'
		pieceImage = pygame.image.load(pieceImgPath)
		return pieceImage
	
	def drawBoard(screen):
		for r in range(BOARD_SIZE):
			for c in range(BOARD_SIZE):
				color = COLOR_WHITE if (r+c) % 2 == 0 else COLOR_BLACK
				pygame.draw.rect(screen, color, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
				piece = GameBoard.getPiece(r, c)
				if piece != EMPTY:
					screen.blit(getPieceImage(piece), (c*SQUARE_SIZE, r*SQUARE_SIZE))

	screen.fill((255, 255, 255))
	drawBoard(screen)

	while not GameBoard.gameOver:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if not dragging:
					r, c = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
					piece = GameBoard.getPiece(r, c)
					if piece != EMPTY and piece.getPlayer() == GameBoard.currPlayer:
						legalMoves = piece.getLegalMoves(GameBoard)
						print(legalMoves)
						for move in legalMoves:
							pygame.draw.rect(screen, COLOR_GREEN, (move[1]*SQUARE_SIZE, move[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
							print("vedfolnir")
						dragging = True
						draggingPiece = piece
						draggingFrom = (r, c)
						offset_x = event.pos[0]-c*SQUARE_SIZE
						offset_y = event.pos[1]-r*SQUARE_SIZE
			# if event.type == pygame.MOUSEBUTTONUP:
			# 	if dragging:
			# 		r, c = event.pos[1] // SQUARE_SIZE, event.pos[0] // SQUARE_SIZE
			# 		# Check if the move is legal
			# 		piece = GameBoard.getPiece(draggingFrom[0], draggingFrom[1])
			# 		legalMoves = piece.getLegalMoves(GameBoard)
			# 		if (r, c) in legalMoves:
			# 			board[row][col] = dragging_piece
			# 			board[dragging_from[0]][dragging_from[1]] = ' '
			# 		dragging = False
			# 		draggingPiece = None
			if event.type == pygame.MOUSEMOTION:
				if dragging:
					x, y = event.pos
					x -= offset_x
					y -= offset_y
					screen.fill((255, 255, 255))
					drawBoard(screen)
					screen.blit(getPieceImage(draggingPiece), (x, y))
					pygame.display.update()
		pygame.display.flip()

if __name__ == '__main__':
	pygameApp()
