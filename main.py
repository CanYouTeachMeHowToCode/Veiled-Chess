# Main function
from cli import CLI
from ui import app
from gui import pygameApp
from game.board import Board


if __name__ == '__main__':
    # # Run the Streamlit app
    # app()

    # Run the CLI app
    CLI()

    # # Run the PyGame app
    # pygameApp()