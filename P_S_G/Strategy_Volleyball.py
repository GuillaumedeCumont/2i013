#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 16:45:14 2019

@author: 3535014
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from P_S_G.Tools import *
from P_S_G.Actions import Shoot, Move

class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        return SoccerAction(acceleration=Vector2D.create_random(-1, 1),
                            shoot=Vector2D.create_random(-1, 1))


class Echauffement(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
        print(s.player)
        return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_la_balle_a_ennemi)


class Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
        
        #return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_la_balle_loin_ennemi) ne fonctionne pas en raison du GAME_WIDTH
        return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_la_balle_a_ennemi)

class Defense(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
        
        while s.ballonsurmonterrain:
            return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_la_balle_a_ennemi)
        
        if not s.ballonsurmonterrain:
            return SoccerAction(move.aller_vers_positionsolodepart, None)


class Strategy1v1(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
        
        while s.ballonsurmonterrain:
            return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_la_balle_a_ennemi)
        
        if not s.ballonsurmonterrain:
            return SoccerAction(move.aller_vers_positionsolodepart, None)
        
        
class Strategy2v2(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState(state, id_team, id_player)
        shoot = Shoot(s)
        move = Move(s)
        
        
        if id_player==0:
            if s.ballonsurmonterrain:
                if s.suis_je_le_plus_proche_du_ballon:
                    return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_la_balle_a_ennemi)
            if not s.ballonsurmonterrain:
                return SoccerAction(move.aller_vers_p1, None)
        
        if id_player==1:
            if s.ballonsurmonterrain:
                if s.suis_je_le_plus_proche_du_ballon:
                    return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_la_balle_a_ennemi)
                else:
                    return SoccerAction(move.aller_vers_anticiper_ballon, shoot.passe_la_balle_a_ennemi)
            if not s.ballonsurmonterrain:
                return SoccerAction(move.aller_vers_p2, None)

    
        
        
