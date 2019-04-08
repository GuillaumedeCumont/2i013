#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:36:26 2019

@author: noe
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS

from .tools   import SuperState
from .actions import Actions



class Strategies(object) : 
    
    def __init__(self, state, id_team, id_player):
    
        self.state     = state 
        self.id_team   = id_team 
        self.id_player = id_player
    

    @property
    def attaquesolo(self):
            
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS:
            if  s.player.distance(s.goaladverse) < (PLAYER_RADIUS * 20) :#Si il est dans la surface de tir : shoot, sinon avance
                return a.shootbut
            elif s.playeradverse.distance(s.player) < (PLAYER_RADIUS*5):
               return a.dribble
            else :
               return a.avanceravecballe
        else:
            return a.deplacement(s.ball)
        

    @property
    def defensesolo(self):

        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
            
        if s.player.distance(s.ball) < PLAYER_RADIUS*12:
            return a.deplacement(s.ball) + a.shootbut
            return a.allerdefensesolo
            
        else:
            return a.allerdefensesolo
        
    
    @property
    def gardien(self):
            
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS :
            return a.shootbut
            
        
        elif s.player.distance(s.ball) < PLAYER_RADIUS*10 :
            return a.deplacement(s.ball)
        
        else:
            return a.allerpositiongardien


    
  
        




                                           
