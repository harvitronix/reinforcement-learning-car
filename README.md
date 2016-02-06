# Using reinforcement learning to train an autonomous vehicle to avoid obstacles

This is a hobby project I created to learn the basics of reinforcement learning. It uses Python3, Pygame, Pymunk, Keras and Theanos. It employes a Q-learning (unsupervised) algorithm to learn how to move an object around a screen (drive itself) without running into obstacles.

Full writeup can be found here:

https://medium.com/@harvitronix/using-reinforcement-learning-in-python-to-teach-a-virtual-car-to-avoid-obstacles-6e782cc7d4c6

## To run for your first time

### Training

First, you need to train a model. This will save weights to the `saved-models` folder. You can do this by running:

`python3 learning.py`

On my MBP with four cores, it takes 2-3 hours to train a model. However, it will spit out weights whenever it has a "best" run, so you can move on to the next step in just 5-10 minutes while it continues to train.

### Playing

Edit the `nn.py` file to change the path name for the model you want to load. Sorry about this, I know it should be a command line argument.

Then, watch the car drive itself around the obstacles!

`python3 playing.py`

That's all there is to it.

## Credits

I'm grateful to the following people and the work they did that helped me learn how to do this:

- Deep learning to play Atari games: https://github.com/spragunr/deep_q_rl
- Another deep learning project for video games: https://github.com/asrivat1/DeepLearningVideoGames
- A great tutorial on reinforcement learning that a lot of my project is based on: http://outlace.com/Reinforcement-Learning-Part-3/
