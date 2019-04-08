#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 19:14:29 2019

@author: noe
"""
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS
from .tools      import SuperState
from .actions    import Actions
from .strategies import Strategies

class DefenseQ(Strategy):
    def __init__(self):
        Strategy.__init__(self, "DefenseQ")
        
    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState(state, id_team, id_player)
        a = Actions(state, id_team, id_player)
        
        if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS :
            return a.tircoequippier
        else :
            return a.deplacement(s.ball)