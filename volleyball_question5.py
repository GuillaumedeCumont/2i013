#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 18:32:42 2019

@author: 3535014
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu

from P_S_G.Tools import *
from P_S_G.Actions import Shoot, Move
from P_S_G.Strategy_Volleyball import Strategy2v2



# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add playe
team1.add("Player 1", Strategy2v2())  
team1.add("Player 1", Strategy2v2())
team2.add("Player 1", Strategy2v2())
team2.add("Player 2", Strategy2v2())

# Create a match
simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)