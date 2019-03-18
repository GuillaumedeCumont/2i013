# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 16:24:22 2019

@author: gamer
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH
from .Tools import *
from .Actions import Shoot, Move

class Strategy_4_joueurs(Strategy):
    def __init__(self):
        Strategy.__init__(self, "strategy a 4")
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
            
        #programmation du goal
        if id_player == 0:
            if s.zone_allie and ((s.ball - s.position_joueur_allier_le_plus_proche).norm < PLAYER_RADIUS + BALL_RADIUS):
                return SoccerAction(move.allerdef, shoot.passe_milieu_A_forte)
            if s.zone_ennemi:
                return SoccerAction(move.allerdef, shoot.passe_milieu_A_forte)
            else:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer_violent) 

        #programmation de l'allié Zone A
        if id_player == 1:
            if s.ball_targetzoneA or s.ball_targetzoneD:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_milieu_B_forte)
            if not s.ball_targetzoneA:
                return SoccerAction(move.allermillieuzoneAretranche, None)
        
        #programmation de l'allié Zone B
        if id_player == 2:
            if s.ball_targetzoneB or s.ball_targetzoneD:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_attaquant_forte)
            if not s.ball_targetzoneB:
                return SoccerAction(move.allermillieuzoneBretranche, None)
        
        #programmation de l'attaquant
        if id_player == 3:
            if not s.g_le_ballon:
                if s.ball_targetzoneC:
                    return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer)
                else:
                    return SoccerAction(move.allerattaquantzoneCdepart, None)
            
            if(s.g_le_ballon):
                if s.tout_le_monde_est_sur_le_ballon:
                    return SoccerAction(move.aller_vers_ballon,shoot.passe_milieu_A_forte)
                if(s.distance_entre_joueur_ennemi_proche<30 and s.distance_entre_joueur_ennemi_proche>15):
                    return SoccerAction(move.aller_vers_ballon,shoot.tire_au_but_si_peut_tirer_violent)
                else:
                    return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer)
    