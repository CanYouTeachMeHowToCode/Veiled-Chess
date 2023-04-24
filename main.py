# Main function
from scripts.compete import simulateAICompetition

if __name__ == '__main__':
    # simulateAICompetition(numGame=1, whiteLevel=0, blackLevel=3) # random move vs deep learning recommendation model move
    simulateAICompetition(numGame=1, whiteLevel=2, blackLevel=3) # deep learning recommendation model move vs expectiminimax move
    # simulateAICompetition(numGame=1, whiteLevel=2, blackLevel=2) # deep learning recommendation model move vs deep learning recommendation model move