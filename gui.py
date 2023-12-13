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
	GameBoard = Board() # TODO

	def drawBoard(screen):
		for r in range(BOARD_SIZE):
			for c in range(BOARD_SIZE):
				color = COLOR_WHITE if (r+c) % 2 == 0 else COLOR_BLACK
				pygame.draw.rect(screen, color, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
				piece = GameBoard.getPiece(r, c)
				if piece != EMPTY:
					# Example: You can load images for each piece and blit them onto the squares
					# For simplicity, this example just draws the piece's initial as text
					font = pygame.font.Font(None, 36)
					pieceName = piece.getName()
					text_surface = font.render(pieceName, True, (255, 255, 255))
					text_rect = text_surface.get_rect(center=(c*SQUARE_SIZE+SQUARE_SIZE//2, r*SQUARE_SIZE+SQUARE_SIZE//2))
					screen.blit(text_surface, text_rect)
                
	# def draw(display):
	# 	display.fill('white')
	# 	GameBoard.draw(display)
	# 	pygame.display.update()

	while not GameBoard.gameOver:
		screen.fill((255, 255, 255))
		drawBoard(screen)
		pygame.display.flip()

if __name__ == '__main__':
	pygameApp()
