#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 18:29:32 2019

@author: 3535014
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH
from .Tools import *
   
    
class Strategy_Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        
        if(id_player == 0):
            allier_plus_proche_du_ballon_y_va
            
            
        if(id_player == 1):
            SoccerAction(s.aller_vers_anticiper_ballon, s.tire_au_but_si_peut_tirer_violent)
            SoccerAction(s.aller_vers_but_allie,None)
