![made-with-rust](img/built-with-science.svg?style=centerme)
![built-with-love](img/made-with-python.svg?style=centerme)
![works-on-linux](img/makes-people-smile.svg?style=centerme)
![works-on-my-machine](img/uses-git.svg?style=centerme)
![compatibility-club-penguin.svg](img/compatibility-club-penguin.svg?style=centerme)
![powered-by-rascar.svg](img/powered-by-rascar.svg?style=centerme)

# SoccerSimulator (Sorbonne Université) - 2019

## 🚩 Summary
This repository contains a computer project of the Sorbonne University. It is the programming of the team strategy of 1,2,4 players in a soccer simulator. The whole was developed in Python. 

This project develops first of all the strategies of the teams with 1,2 and 4 players.  It also uses machine learning to evolve team strategies via reinforcement learning.

The soccer simulator, takes as input from the player only a vector. Two classes can return a vector. The Move class returns the player's movement in vector, and the Shoot class returns the player's shot. (*The player can only shoot if the ball is in his reach*)

**In terms of power, the stronger of the shot, the less accurate the shot.**

## 📕 Reinforcement
These strategies have been improved via **reinforcement algorithms** (genetic algorithms and Q-learning)

## 📦 Dependencies
```bash
python -m pip install pyglet
python -m pip install sklearn
```

## ✅ Usage
>```bash
>python .\tournament.py
>```

## 🚀 Exemple
>• A game of two players started.
![screenshot_2v2](img/screenshot_2v2.png?style=centerme)

>• A game of four players started.
![screenshot](img/screenshot.png?style=centerme)

## 🏁 The End
![Rascar](img/rascar.png?style=centerme)