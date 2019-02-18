#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:30:38 2019

@author: 3535014
"""

"""***// A MODIFIER //***"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH
from .Tools import *

class TestStrategy(Strategy):
    def __init__(self, strength=None):
        Strategy.__init__(self,"Go-getter")
        self.strength = strength
        
    def compute_strategy(self,state,id_team,id_player):
        s = SuperState(state,id_team,id_player)
        move = Move(s)
        shoot = Shoot(s)
        return move.to_ball() + shoot.to_goal()
    
    