# Using reinforcement learning to train an autonomous vehicle to avoid obstacles

This is a hobby project I created to learn the basics of reinforcement learning. It uses Python3, Pygame, Pymunk, Keras and Theanos. It employes a Q-learning (unsupervised) algorithm to learn how to move an object around a screen (drive itself) without running into obstacles.

The purpose of this project is to eventually use the learnings from the game to operate a real-life remote-control car, using distance sensors.

This version of the code attempts to simulate the use of sensors to get us a step closer to being able to use this in the real world.

**If you're coming here from parts 1 or 2 of the Medium posts, you want to visit the releases section and check out version 1.0.0, as the code has evolved passed that.**

Full writeups that pertain to version 1.0.0 can be found here:

*Part 1:* https://medium.com/@harvitronix/using-reinforcement-learning-in-python-to-teach-a-virtual-car-to-avoid-obstacles-6e782cc7d4c6

*Part 2:* https://medium.com/@harvitronix/reinforcement-learning-in-python-to-teach-a-virtual-car-to-avoid-obstacles-part-2-93e614fcd238#.vbakopk4o

## To run for your first time

### Installing

1. Clone this repo
1. Install numpy ```pip3 install numpy```
2. Install Pygame. I used these instructions: http://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3 but with ```pip3 install hg+http://bitbucket.org/pygame/pygame``` after I installed the dependencies
3. Install pymunk ```pip3 install pymunk```
4. Update pymunk to python3 by CDing into its directory and running ```2to3 -w *.py```
5. Install Keras ```pip3 install keras```
6. Upgrade Theanos ```pip3 install git+git://github.com/Theano/Theano.git --upgrade --no-deps```
7. Install h5py for saving models ```pip3 install h5py```

### Training

First, you need to train a model. This will save weights to the `saved-models` folder. You can do this by running:

`python3 learning.py`

It can take anywhere from an hour to 36 hours to train a model, depending on the complexity of the network and the size of your sample. However, it will spit out weights every 25,000 frames, so you can move on to the next step in much less time.

### Playing

Edit the `nn.py` file to change the path name for the model you want to load. Sorry about this, I know it should be a command line argument.

Then, watch the car drive itself around the obstacles!

`python3 playing.py`

That's all there is to it.

### plotting

Once you have a bunch of CSV files created via the learning, you can convert those into graphs by running:

`python3 plotting.py`

This will also spit out a bunch of loss and distance averages at the different parameters.

## Credits

I'm grateful to the following people and the work they did that helped me learn how to do this:

- Deep learning to play Atari games: https://github.com/spragunr/deep_q_rl
- Another deep learning project for video games: https://github.com/asrivat1/DeepLearningVideoGames
- A great tutorial on reinforcement learning that a lot of my project is based on: http://outlace.com/Reinforcement-Learning-Part-3/
