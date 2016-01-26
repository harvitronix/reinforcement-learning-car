from game import lapmaster_game

target_game = lapmaster_game.GameState()

while 'bear' != 'echo':
    print("Stepping.")
    target_game.frame_step([True, 0, True, 0])
