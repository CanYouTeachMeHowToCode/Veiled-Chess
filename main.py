# Main function
from scripts.macro import *
from scripts.board import Board
from scripts.ai import AI
from scripts.compete import simulateAICompetition

if __name__ == '__main__':
    # simulateAICompetition(numGame=1, whiteLevel=0, blackLevel=3) # random move vs deep learning recommendation model move
    simulateAICompetition(numGame=1, whiteLevel=2, blackLevel=3) # proficient move vs deep learning recommendation model move