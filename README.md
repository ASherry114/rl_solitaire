# Reinforcement Learning Agents for flavours of Solitaire

A collection of reinforcement learning agents for different flavours of solitaire.
The agents are implemented in Python using the [PyTorch](https://pytorch.org/) library.

## Installation

## Usage

### Training

### Playing

1. Run main.py with the `--play` flag to play a game with the trained agent.
1. Interactively set the starting state of the game.
1. Each turn, the agent will choose an action and present it to the user.
1. Before the next iteration, the user must update the state of the game (if applicable).

## Agents / Games

- [ ] Escalator
- [ ] FreeCell
- [ ] Eliminator
- [ ] Elevator
- [ ] Klondike

Have the agent spit out the probability distribution of the source and destination.
Then, can mask it with the list of possible actions.
Will need to normalize the probability distribution of the remaining actions to sum to 1.
Then can pass into numpy random choice without having to iterate until a valid selection is made.

## State encoding

### Truncation

Could just truncate the game state in some intelligent way as some aspects of the state might not be relevant.
Truncating would be a way of simplifying the assessment of what is relavent and just hoping it works out.

### RNN-CNN

Use RNN to encode the variable length game state into a fixed length vector.
Then use CNN on this fixed length vector to extract features.
Then use a fully connected layer to map these features to the action space.

### Attention Mechanism

Attention mechanism could be used to focus on the relevant parts of the game state.
This would be useful for games where the state is variable length.
Focus on just a part of the state at any given time, and have this part be of fixed size.
(Side note, this is used in some natural language processing tasks as not all words are relevent in a sentence.)

### Transformer

Transformer is a neural network architecture that uses attention mechanism.
Specifically uses self-attention, which is attention mechanism applied to the same input.
