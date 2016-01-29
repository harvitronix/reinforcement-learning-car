from game import lapmaster_game
import numpy as np

# Play the game directly.
game_state = lapmaster_game.GameState()
while 'bear' != 'echo':
    reward, _ = game_state.frame_step(np.random.randint(0, 4))
    if reward < 0:
        game_state = lapmaster_game.GameState()
