# SCERL: A Text-based Safety Benchmark for Reinforcement Learning Problems

This repository contains the source code and data for our paper *SCERL: A Text-based Safety Benchmark for Reinforcement Learning Problems*.
SCERL is a text-based environment for reinforcement learning agents that:

* provides a framework for genereting safety problems representing key safety challenges such as negative side effect, scalable oversight and safe exploration
* includes a pre-generated set of text-based games with safety constraints in order to spoor research in safe and text-based reinforcement learning (see [dataset/safety_games](./dataset/safety_games)).

## Sample Game

<p>
  <img src="game_demo.gif" width="550" title="safety game example">
</p>

## Benchmark games

A predefined set of benchmark games is provided in [dataset/safety_games](./dataset/safety_games). In all games, the agent interacts with the environment using only the modality of text. The agent is placed in a domestic environment and is requierd to achieve some goal while respecting some safety constraints. Our constraints are desinged to implement main safety challenges as follows.

| **Safety Problem** | **Our implementation** | **Description** |
|---|---|---|
| **Negative consequences** | Non-goal constraints | The requirement for this goal is to put an object to a safe place. For example, bleach and dangerous chemicals should be in the cupboard and not on the counter |
| **Safe Exploration** | Goal-related penalty/safety constraints | The agent is required to cook a food item without leaving the stove on (fire risk) or the fridge open (energy waste) |
| **Reward Hacking** | Repeated non-goal rewards which distract the agent from achieving its main goal | The agent might repeat opening and closing the fridge to gain the reward of closing the fridge, instead of cooking the egg to achieve its main goal |
| **Scalable Oversight** | Safety constraints that are not consistent for same type of objects | It is generally unsafe to put raw eggs in lunch box but occasionally the agent does not incur penalty for doing so |
| **Robustness to Distributional Shift** | Safety constraints relating to different objects and setting | The agent needs to safely operate across different rooms, in which it will encounter different subjects and with different safety constraints |



## Customizing safety requirements in SCERL
Users can introduce safety restrictions under two forms: soft penalties and terminating penalties. This can be achieved by customizing the following files:

* ```safety_goal.json```: config file for adding goals related to the state of a given object to the game environment.
* ```safety.json```: config file for adding constraints that the agent is not supposed to violate and their associated penalties.
* ```twc_make_game.py```: driver file that generates games based on the configurations provided by ```safety_goal.json```and ```safety.json```.

## Training RL agents with SCERL

In order to train RL agents and create custom games in SCERL, you first need to set up and activate a python environment as follows:
```
conda env create -f environment.yaml
conda activate scerl
```
Then, you can use the script ```train_agent.py``` to train different kinds of RL agents on SCERL.
For example, you can train a simple text-based LSTM-A2C agent as follows:
```
python -u train_agent.py --agent_type simple --game_dir ./dataset/safety_games --game_name *.ulx
```
See ```python -u train_agent.py --help``` for the different options and kinds of agents that are supported by our training script.

#### Feedback
* Please share _SCERL_ using [https://github.com/IBM/SCERL](https://github.com/IBM/SCERL)
* [File an issue](https://github.com/IBM/SCERL/issues/new) on GitHub.

#### Relevant Resources 

* [Microsoft TextWorld](https://www.microsoft.com/en-us/research/project/textworld/)
* [TextWorld Commonsense](http://ibm.biz/commonsense-rl) 
