#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 19:09:24 2019

@author: noe
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS
from .tools      import SuperState
from .actions    import Actions
from .strategies import Strategies

class AttaquedroiteQ(Strategy):
    def __init__(self):
        Strategy.__init__(self, "AttaquedroiteQ")
        
    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState(state, id_team, id_player)
        a = Actions(state, id_team, id_player)
        
        if s.poscoequippier.distance(a.directionball) < PLAYER_RADIUS + BALL_RADIUS : #SI le coequippier a la balle
            
            return a.deplacement(s.pointcampeurdroit)
        
        elif s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS:
            if s.opposantsplusproche[1].distance(s.player)< PLAYER_RADIUS *10:
                
            #if s.player.distance(s.poscoequippier) < PLAYER_RADIUS*25 :
                if s.coepdevant == 1 :
                    print("DDDDD")
                    return a.tircoequippier + a.deplacement(s.pointattaquantdroit)
            elif  s.player.distance(s.goaladverse) < (PLAYER_RADIUS * 20) :#Si il est dans la surface de tir : shoot
                return a.shootbut
            elif s.playeradverse.distance(s.player) < (PLAYER_RADIUS*8):
                return a.dr2
            else :
                
                return a.avanceravecballe
        else:
            
            return a.deplacement(a.directionball)