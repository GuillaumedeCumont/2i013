#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 16:14:40 2019

@author: root
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH
from .Tools import *
from .Actions import *


class Strategy_Defense(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        move = Move(s)
        shoot = Shoot(s)
        
        if(id_player == 0):
            if(s.distance_but_ennemi < GAME_HEIGHT/3.2):
                return SoccerAction(move.aller_vers_ballon,shoot.tire_au_but_si_peut_tirer_violent)
            else:
                if s.tout_le_monde_est_sur_le_ballon:
                    return SoccerAction(move.aller_vers_ballon,shoot.passe_joueur_allier_forte)
                else:
                    return SoccerAction(move.aller_vers_ballon,shoot.tire_au_but_si_peut_tirer)
            
        if(id_player == 1):
            if(s.zone_allie):
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer_violent)
            else:
                if(s.distance_entre_joueur_allier_proche<1):
                    return SoccerAction(None, None)
                else:
                    return SoccerAction(move.aller_vers_but_allie,None)
