## Machine Learning Snake
A recreation of Snake, written in Python using PyGame, with an added implementation of a neural network for deep learning.

This project is very much in a work in progress state, with a fully functioning NumPy neural network, however I have approached this problem from a genetic learning approach, which has proved difficult.

I may end up switching this project to a deep Q-learning algorithm if it proves more successful. If I do this, I will likely also transition from NumPy exclusively to PyTorch

#### End Goal
  - Train a neural network to successfully play Snake.

#### Agent Observations:
  - Distance to food in each cardinal direction (+ diagonals)
  - Safe distance in each cardinal direction (+ diagonals)

#### Network Layers
  - Input Layer
      - (16 x 1)
  - Layer 1
      - (16 x 1) Perceptrons
      - Activation: Sigmoid
    
  - Layer 2
      - (8 x 1) Perceptrons
      - Activation: Sigmoid
    
  - Layer 3
     - (4 x 1)
     - Activation: Softmax
