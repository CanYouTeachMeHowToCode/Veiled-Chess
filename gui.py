# Graphic User Interface using PyGame
import pygame
from game.board import Board
from game.macro import *

def pygameApp():
	pygame.init()
	WINDOW_SIZE = (1000, 1000)
	screen = pygame.display.set_mode(WINDOW_SIZE)
	pygame.display.set_caption("Veiled Chess")
	SQUARE_SIZE = WINDOW_SIZE[0] // BOARD_SIZE
	GameBoard = Board()

	def drawBoard(screen):
		for r in range(BOARD_SIZE):
			for c in range(BOARD_SIZE):
				color = COLOR_WHITE if (r+c) % 2 == 0 else COLOR_BLACK
				pygame.draw.rect(screen, color, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
				piece = GameBoard.getPiece(r, c)
				if piece != EMPTY:
					pieceType = piece.__class__.__name__
					piecePlayer = piece.getPlayer()
					pieceImgPath = f'images/{piecePlayer}_{pieceType.lower()}.png' if not piece.unmoved or pieceType == 'King' else f'images/veiled_{piecePlayer}_{pieceType.lower()}.png'
					pieceImage = pygame.image.load(pieceImgPath)
					pieceImage = pygame.transform.scale(pieceImage, (SQUARE_SIZE, SQUARE_SIZE))
					screen.blit(pieceImage, (c*SQUARE_SIZE, r*SQUARE_SIZE))

	while not GameBoard.gameOver:
		screen.fill((255, 255, 255))
		drawBoard(screen)
		pygame.display.flip()

if __name__ == '__main__':
	pygameApp()
