# Veiled Chess

> #### A Veiled Chess Game created by Yilun Wu (AIPI540 Spring 2023 Individual Project)

## Introduction & Project Description
Chess is a famous board game of strategy and skill that has captivated players worldwide over centuries. As a perfect information game, Artificial Intelligence (AI) agents and engines with strong computing power emerge and prosper in recent decades, and the current cutting-edge Chess AI named [*StockFish*](https://stockfishchess.org/) is proved to be almost undefeatable by any human among the world. However, it might be another story if AI plays a variant of Chess that is an imperfect information game, in which some of the information is hidden for each player. Here comes the new variant of Chess: *Veiled Chess*. 

The rules of this variant are almost the same as Chess, except for the following rules:
- For each player, every piece except for the King is “veiled” in the beginning, and is randomly distributed among the remaining 15 start squares for each side. None of the players knows which piece is which.
- When a piece is “veiled”, it follows the moving rules of the piece at the same position on the original Chess board. For instance, a white piece at square F2 (a white Pawn located here in Chess) can move to either square F3 or square F4, by following Pawn's moving rules.
- After each move of a “veiled” piece, it “unveils”. That is, it becomes the chess it truly is and obeys the moving rules of itself.
- If one of the player's “unveiled” pieces is taken by an opponent, the opponent knows what the piece actually is, yet the player does not know.

An example of comparison between normal chess board (left) and *Veiled* chess board (right) after the move series `1.e4 e5 2♗c4 ♝c5 3.♘f3 ♞f6 4.♘c3 d6 5.O-O ♛e7` is shown below:
<table>
  <tr>
    <td><img src=".images/Normal%20Chess%20Board%20Example.png" alt="Normal Chess Board"></td>
    <td><img src=".images/Veiled%20Chess%20Board%20Example.png" alt="Veiled Chess Board"></td>
  </tr>
</table>

In this project, I’ll focus on developing the *Veiled Chess* game as well as the recommendation engine for the best moves of *Veiled Chess* to explore if the agent can still outperform most human players in this kind of Chess with far more uncertainties like those AI agents who always beat human beings in Chess.


## Data Sources
- [*StockFish*](https://stockfishchess.org/) (Open Source Chess Engine)
  - For computing "expected" evaluation score for veiled chess boards 
- Veiled Chess Game simulation (details see [simulateData.py](scripts/simulateData.py))
  - Board 
    - Current board appears to each player
  - Game info 
    - Current player
    - Castling checks (Can castling kingside/queenside for each player)

## Project Repository Structure
```
.
|-- .images                   ---- Directory for storing images used in README
|-- data                      ---- Directory for storing simulated data
|-- models                    ---- Directory for storing (current) best Deep Learning Recommendation models
|   -- best_model.pth
|-- scripts
|   |-- macro.py              ---- Define necessary game macros & model training parameters
|   |-- piece.py              ---- Piece class for implementation of Veiled Chess game logic
|   |-- board.py              ---- Veiled Chess game logic
|   |-- ai.py                 ---- AI agent using deep learning & non-deep learning approaches
|   |-- processData.py        ---- Script for dataset processing
|   |-- simulateData.py       ---- Script for dataset simulation
|   |-- model.py              ---- Define NN-based content-based filtering recommendation model
|-- README.md
|-- docker-compose.yml        ---- Docker composing file
|-- Dockerfile
|-- setup.py                  ---- Script for setting up the project, including dataset simulation, model training & evaluation 
|-- play.py                   ---- Script for interactive playing (playing vs another player, playing vs AI agents, etc.)
|-- main.py                   ---- Main function
|-- requirements.txt
```

## Requirements
- See `requirements.txt`, or run the following command
  > pip3 install -r requirements.txt

- Install [*StockFish*](https://stockfishchess.org/) to local by following the instructions [here](https://stockfishchess.org/download/)

## Usage

### Run the streamlit web app 
- Locally by running command
  > streamlit run main.py --server.port=8080
- Open http://veiled-chess-streamlit.azurewebsites.net
  - NOTE: Recommendation from Expert AI currently unavailable on the web app if not running locally due to several incompatibility issue of [*StockFish*](https://stockfishchess.org/) during deployment, will fix this issue later.

### Start interactive playing
- Locally by running command
  > python3 play.py
- NOTE: the interactive playing mode is only the rudimentary version (will directly start Player vs Proficient AI mode), will upgrade it and integrate it into web app later.



## Data Processing Pipeline & Deep Learning Recommendation Model
![Data Processing Pipeline](.images/Data%20Processing%20Pipeline.png)

### Deep Learning Recommendation Model (Veiled Chess Net) Architecture

```
VeiledChessNet(
  (conv1): Conv2d(1, 32, kernel_size=(3, 3), stride=(1, 1), padding=(2, 2))
  (conv2): Conv2d(32, 64, kernel_size=(3, 3), stride=(1, 1), padding=(2, 2))
  (conv3): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(2, 2))
  (conv4): Conv2d(128, 32, kernel_size=(3, 3), stride=(1, 1), padding=(2, 2))
  (bn1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (pool): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (dropout): Dropout(p=0.3, inplace=False)
  (fc1): Linear(in_features=5, out_features=16, bias=True)
  (fc2): Linear(in_features=16, out_features=64, bias=True)
  (out): Linear(in_features=576, out_features=1, bias=True)
)
```
For more details see [model.py](scripts/model.py)

### Training and Evaluation
- Loss: MSE (mean squared error) loss
- Optimizer: RMSprop
- Train dataset size: Validation dataset size = 8:2
- Number of Epochs: 100
- Model with best performance (validation loss) saved for final recommendation

## Non-deep Learning Model
- Expectiminimax
  - Evaluate each game state using [*StockFish*](https://stockfishchess.org/)
  - Compute the probability of unveiling to each piece type of each move of veiled piece
    - High branching factor early stage and so high computational costs 
  - Compute the expected score by summing up scores from all child states 

## Results

- Denote AI Agents
  - Random move -> Novice AI
  - Deep Learning Recommendation Model move -> Proficient AI
  - Expectiminimax move -> Expert AI

- Results of 100 games (Win/Tie/Lose)
  - Novice AI vs  Proficient AI: 0/3/97
  - Novice AI vs Expert AI: 0/0/100
  - Proficient AI vs Expert AI: 2/9/89

- Observations
  - Proficient AI plays well in the early stage but bad at endgames
  - Expert AI always plays cautiously 

## Future Expectations
- Balance between computational costs and performance for expectiminimax algorithm is vital
  - StockFish is accurate but costs too much 
 
- More training samples (game logs) for deep learning recommendation model should leads to better performance 

- Can try various deep models (even pre-trained models) besides the current *VeiledChessNet*

- Still lots of open spaces for game strategies, especially during the early game 
