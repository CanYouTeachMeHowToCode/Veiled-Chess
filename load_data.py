import lichess.api
from lichess.format import SINGLE_PGN
from lichess.format import PYCHESS
from macro import LICHESS_API_TOKEN

username = 'YilunWu'
user = lichess.api.user(username)
print(user.get('perfs', {}).get('blitz', {}).get('rating'))
# pgn = lichess.api.user_games('thibault', max=200, format=SINGLE_PGN)
# with open('last200.pgn', 'w') as f:
#     f.write(pgn)
games = lichess.api.user_games(username, max=100, perfType=None, analyzed=None)
for game in games:  
    print(game)
# game = lichess.api.game('Qa7FJNk2', format=PYCHESS)