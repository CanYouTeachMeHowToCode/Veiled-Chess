# Veiled Chess

> #### A Veiled Chess Game created by Yilun Wu (AIPI540 Spring 2023 Individual Project)

## Project Description
Chess is a famous board game of strategy and skill that has captivated players worldwide over centuries. As a perfect information game, Artificial Intelligence (AI) agents and engines with strong computing power emerge and prosper in recent decades, and the current cutting-edge Chess AI named *StockFish* is proved to be almost undefeatable by any human among the world. However, it might be another story if AI plays a variant of Chess that is an imperfect information game, in which some of the information is hidden for each player. Here comes the new variant of Chess: *Veiled Chess*. 

The rules of this variant are almost the same as Chess, except for the following rules:
- For each player, every piece except for the King is “veiled” in the beginning, and is randomly distributed among the remaining 15 start squares for each side. None of the players knows which piece is which.
- When a piece is “veiled”, it follows the moving rules of the piece at the same position on the original Chess board. For instance, a white piece at square F2 (a white Pawn located here in Chess) can move to either square F3 or square F4, by following Pawn's moving rules.
- After each move of a “veiled” piece, it “unveils”. That is, it becomes the chess it truly is and obeys the moving rules of itself.
- If one of the player's “unveiled” pieces is taken by an opponent, the opponent knows what the piece actually is, yet the player does not know.

An example of comparison between normal chess board and *Veiled* chess board is shown below:
<table>
  <tr>
    <td><img src=".images/Normal%20Chess%20Board%20Example.png" alt="Normal Chess Board"></td>
    <td><img src=".images/Veiled%20Chess%20Board%20Example.png" alt="Veiled Chess Board"></td>
  </tr>
</table>


## Data Source
For this project, we are using recipes and reviews data from popular cooking website food network.

The recipes dataset contains 522,517 recipes from 312 different categories. This dataset provides information about each recipe like cooking times, servings, ingredients, nutrition, instructions, and more.
The reviews dataset contains 1,401,982 reviews from 271,907 different users. This dataset provides information about the author, rating, review text, and more.

https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews

## Project Structure
```
.
|-- dist (Optional)           ----store temporary files when running api
|-- data (Optional)           ----store automatically fetched data
|-- notebooks      
|   |-- recommendation-2-3.ipynb
|   |-- recommendation.ipynb
|   `-- test.ipynb
|-- saved_models              ----best model will be saved here
|   `-- best_model.pt
|-- scripts
|   |-- FetchData.py          ----fetch data from s3 and unzip it
|   |-- RecipesData.py        ----data processing and loading
|   |-- RecipesModel.py       ----recommendation models
|   |-- RecipesRecommendor.py ----recommendation models training & evaluation to get final recommendations
|   `-- clustering.py         ----k-means clustering to group recipes by their cooking time and ingredients for recommendation dataset construction
|-- README.md
|-- api.py                    ----web demo script
|-- main.py                   ----main function
`-- requirements.txt
```

## Requirements
See `requirements.txt`
>pip3 install -r requirements.txt

### Run the code
>python3 main.py

### Run the web demo
>python3 api.py

open http://127.0.0.1:8000

## Architecture Diagram
![model architecture diagram](https://user-images.githubusercontent.com/50161537/231304318-7c07c38b-74b0-4ffb-8131-d6dd7bacdc49.png)

## Content-based Recipe Recommendation Model 
### Model Overview 
This is a content-based recipe recommender system. It generates recommendations based on the features of recipes (i.e., recipe ID, author ID, number of calories, and number of reviews).

The model is trained using the mean squared error loss function and the Adam optimizer. The training data is split into training and validation datasets, and the model is trained for 10 epochs. The best performing model is saved and later used for generating recommendations.

To generate recommendations, the model is loaded, and the predicted ratings are generated for a set of recipes that the user has not yet rated. The top 10 recipes with the highest predicted ratings are then recommended to the user.

One thing to note is that the model is a neural network model with embeddings and a multi-head attention layer, which are commonly used in natural language processing tasks. The model takes in non-sequential input features, and the attention mechanism is used to focus on relevant features and capture interactions between them.

### MultiHead Attention Model Architecture Details
- Inputs: recipe ID, author ID, number of calories, and # of reviews
- Embedding layers 
  - Convert inputs to embedding vectors and combine them into single vector
- Multi-head attention layer 
  - Helps model focus on different parts of input

- 2 fully connected layers

- Sigmoid activation function 


### Training and Evaluation
- Use mean squared error (MSE) loss function and Adam optimizer.
- Train dataset : Validation dataset = 8:2
- Number of Epochs = 100
- Model with best performance saved for final recommendation generation 

## Results
![image](https://user-images.githubusercontent.com/50161537/231260130-1bb17a5c-e53c-4e48-901c-7a15dd9de562.jpeg)
This document provides a recommendation on the performance of a model based on its MAP@k (Mean Average Precision at k) scores. The MAP@k scores were computed for k = 1, 3, 5, and 10, and the results are presented below:

* MAP@1: 0.1321
* MAP@3: 0.0865
* MAP@5: 0.0682
* MAP@10: 0.0485

The MAP@k is a popular evaluation metric for ranking models, and it measures the average precision at each cutoff k. In this case, the model's performance decreases as the cutoff k increases, indicating that it is better at identifying the top-ranked items than the lower-ranked ones.

The MAP@1 score of 0.1321 suggests that the model performs reasonably well in identifying the top-ranked item, but there is still room for improvement. The MAP@3 score of 0.0865 indicates that the model's performance drops significantly beyond the first item, suggesting that it may not be as effective in identifying the top three items. The MAP@5 score of 0.0682 and the MAP@10 score of 0.0485 indicate that the model's performance further decreases as more items are considered.

## Application

This is a Vue.js application that displays recipe recommendations based on user selections. The application uses the vue-router library to manage navigation and has a main app bar at the top of the page. The app bar contains a Log In button that opens a modal where the user can select their username from a dropdown menu. The app retrieves recipe data from an API using the @tanstack/vue-query library and displays it in a grid of recipe cards. The user can filter the recipe results by category by clicking on a category in the left-hand sidebar. The footer of the page provides information about the project and its developers.
