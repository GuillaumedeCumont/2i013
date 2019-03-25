# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 16:24:22 2019

@author: root
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
            if s.suis_je_le_plus_proche_du_ballon:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_milieu_A_forte)              
            
            elif s.je_suis_zone_goal_4_players:
                if not s.g_le_ballon and s.zone_ennemi:
                    return SoccerAction(move.allerdef, None)
                else:
                    return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_milieu_A_forte)
            
            else: # je suis dans le cas ou je sors de ma zone
                return SoccerAction(move.allergoalzonegoaldepart, None)
            
        #programmation de l'allié Zone 
        if id_player == 1:
            
            if s.suis_je_le_plus_proche_du_ballon:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_milieu_B_forte)              
            
            if s.ball_targetzoneA or s.ball_targetzoneD:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_milieu_B_forte)
            if not s.ball_targetzoneA:
                return SoccerAction(move.allermillieuzoneAretranche, None)
        
        #programmation de l'allié Zone B
        if id_player == 2:

            if s.suis_je_le_plus_proche_du_ballon:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_attaquant_faiblouille)              
            
            if s.ball_targetzoneB or s.ball_targetzoneD:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_attaquant_faiblouille)
            if not s.ball_targetzoneB:
                return SoccerAction(move.allermillieuzoneBretranche, None)
        
        #programmation de l'attaquant
        if id_player == 3:
            
            if s.suis_je_le_plus_proche_du_ballon:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer_violent)
            
            if(s.g_le_ballon):
                if (s.but_ennemi-s.player).norm<30:
                    return SoccerAction(move.aller_vers_ballon,shoot.tire_au_but_si_peut_tirer_violent)
                if(s.distance_entre_joueur_ennemi_proche<5):
                    return SoccerAction(move.aller_vers_ballon,shoot.tire_au_but_si_peut_tirer_violent)
                if s.champ_libre:
                    return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer)
                if s.tout_le_monde_est_sur_le_ballon:
                    return SoccerAction(move.aller_vers_ballon,shoot.passe_milieu_A_forte)
                else:
                    return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer)
            
            if not s.g_le_ballon:
                if s.ball_targetzoneC:
                    return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer)
                else:
                    return SoccerAction(move.allerattaquantzoneCdepart, None)