from game import lapmaster_game

target_game = lapmaster_game.GameState()

while 'bear' != 'echo':
    reward = target_game.frame_step([False, 0, True, 0])
    print(reward)
