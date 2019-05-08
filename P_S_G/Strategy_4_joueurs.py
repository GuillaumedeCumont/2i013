# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 16:24:22 2019

@author: root
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH
from .Tools import *
from .Actions import Shoot, Move

#################################################################################################################

class Strategy_4_joueurs_goal(Strategy):
    def __init__(self):
        Strategy.__init__(self, "strategy a 4")
        
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
                
        if s.suis_je_le_plus_proche_du_ballon: #modifié
            return SoccerAction(move.aller_vers_anticiper_ballon, shoot.shootsurpasse_intelligente_goal)         
            
    
        elif s.je_suis_zone_goal_4_players:
            if not s.g_le_ballon and s.zone_ennemi:
                return SoccerAction(move.allerdef, None)
            else:
                return SoccerAction(move.aller_vers_anticiper_ballon, None)
            
        else: # je suis dans le cas ou je sors de ma zone
            return SoccerAction(move.allergoalzonegoaldepart, None)

#################################################################################################################

class Strategy_4_joueurs_defenseurA(Strategy):
    def __init__(self):
        Strategy.__init__(self, "strategy a 4")
        
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
                
        if s.suis_je_le_plus_proche_du_ballon:
            return SoccerAction(move.aller_vers_anticiper_ballon, shoot.shootsurpasse_intelligente_MilieuA)              
            
        ################################################
        elif s.si_un_joueur_ennemi_a_ballon:
            return SoccerAction(move.aller_vers_joueurennemiplusproche, None)
        ################################################
            
        elif s.ball_targetzoneA or s.ball_targetzoneD:
            return SoccerAction(move.aller_vers_anticiper_ballon, None)
        
        elif not s.ball_targetzoneA:
            return SoccerAction(move.allermillieuzoneAretranche, None)

#################################################################################################################

class Strategy_4_joueurs_milieuB(Strategy):
    def __init__(self):
        Strategy.__init__(self, "strategy a 4")
        
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
        
        if s.suis_je_le_plus_proche_du_ballon:
            return SoccerAction(move.aller_vers_anticiper_ballon, shoot.shootsurpasse_intelligente_MilieuB)              
          
        ################################################
        if s.si_un_joueur_ennemi_a_ballon:
            return SoccerAction(move.aller_vers_joueurennemiplusproche, None)
        ################################################
        
        if s.ball_targetzoneB or s.ball_targetzoneD:
            return SoccerAction(move.aller_vers_anticiper_ballon, None)
        if not s.ball_targetzoneB:
            return SoccerAction(move.allermillieuzoneBretranche, None)

#################################################################################################################

class Strategy_4_joueurs_attaquant(Strategy):
    def __init__(self):
        Strategy.__init__(self, "strategy a 4")
        
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
        
        if s.suis_je_le_plus_proche_du_ballon and not s.g_le_ballon:
            return SoccerAction(move.aller_vers_anticiper_ballon, None)         
        ################################################
        #if s.si_un_joueur_ennemi_a_ballon and s.zone_ennemi:
        #    return SoccerAction(move.aller_vers_joueurennemiplusproche, shoot.tire_au_but_si_peut_tirer_violent)
        ################################################  
        if(s.g_le_ballon):
            if (s.but_ennemi-s.player).norm<20:
                return SoccerAction(move.aller_vers_ballon,shoot.tire_au_but_si_peut_tirer_doucement)
            if(s.distance_entre_joueur_ennemi_proche<5):
                return SoccerAction(move.aller_vers_ballon,shoot.tire_au_but_si_peut_tirer_violent)
            if s.champ_libre:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer_doucement)
            if s.tout_le_monde_est_sur_le_ballon:
                return SoccerAction(move.aller_vers_ballon,shoot.tire_au_but_si_peut_tirer_violent)
            else:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer_violent)
        
        if not s.g_le_ballon:
            if s.ball_targetzoneC:
                return SoccerAction(move.aller_vers_anticiper_ballon, shoot.tire_au_but_si_peut_tirer)
            else:
                return SoccerAction(move.allerattaquantzoneCdepart, None)        

#################################################################################################################
#################################################################################################################
#################################################################################################################
    
        
        
        
        
        
        
        
        
        
        
        
        