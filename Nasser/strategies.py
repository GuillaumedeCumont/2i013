#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 17:18:55 2019

@author: 3700052
"""
from soccersimulator import Ball,settings, Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from .tools  import SimpleStrategy,SuperState
from soccersimulator.settings  import GAME_WIDTH, GAME_HEIGHT,PLAYER_RADIUS,BALL_RADIUS,maxPlayerShoot

class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        return SoccerAction(Vector2D.create_random(-0.5 ,0.5),
                            Vector2D.create_random(-0.5 ,0.5))
                    
def gobetter(state) : 
     if state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
        return SoccerAction(shoot=state.goal-state.player)
     else :
        return SoccerAction(acceleration=state.ballameliorer-state.player)
    

                    
def gobetteratt(state) : 
     if state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
        return SoccerAction(shoot=(state.coequipier2-state.player).normalize()*4)
     else :
        return SoccerAction(acceleration=state.ballameliorer-state.player)
                    
def gobetterdef (state):
    if state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
        return SoccerAction(shoot=state.milieuproche-state.player)
    else :
        return SoccerAction(acceleration=state.ballameliorer-state.player)
    
def gobetterdef1 (state):
    if state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
        return SoccerAction(shoot=(state.coequipier2-state.player).normalize()*4)
    else :
        return SoccerAction(acceleration=state.ballameliorer-state.player)    

def gobetterdef2 (state):
    if state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
        return SoccerAction(shoot=(state.coequipier3-state.player).normalize()*4)
    else :
        return SoccerAction(acceleration=state.ballameliorer-state.player)  

    
def defenseur2 (state):
    if state.teamdef[1] : 
        return SoccerAction(Vector2D(GAME_WIDTH*(state.teamdef[0]), (state.ballameliorer.y+state.goal.y)/2 )-state.player, state.goal-state.player)
    else :
        return gobetter(state)

def gobetteratt1 (state):
    if state.teamatt[0] :
        if state.player.y < GAME_HEIGHT/2 :
            if state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
                return SoccerAction(shoot=Vector2D(state.teamatt[1], 0)-state.player)
            else :
                return SoccerAction (acceleration=state.ballameliorer-state.player)
        else : 
            if state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
                return SoccerAction(shoot=Vector2D(state.teamatt[1], GAME_HEIGHT)-state.player)
            else :
                return SoccerAction (acceleration=state.ballameliorer-state.player)
    else : 
        if state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
            return SoccerAction(shoot=state.goal-state.player)
        else :
            return SoccerAction (acceleration=state.ballameliorer-state.player)
        
        
        
def attaquant2(state):
    if state.teamatt[2] : 
        return SoccerAction(Vector2D(GAME_WIDTH*(state.teamdef[0]), (state.ballameliorer.y+state.goal.y)/2 )-state.player, state.goal-state.player)
    else :
        return gobetteratt(state) 
    
def attaquant3(state):
    if state.v4v4[2]:
        if state.devantatt == False : 
            return SoccerAction(state.ballameliorer-state.player, (state.coequipier3-state.player).normalize()*4)
        else :
            return attaquant2(state)
    else : 
        return SoccerAction(Vector2D(state.coequipier3.x, state.player.y)-state.player, state.goal-state.player)
 
def defenseur3(state):
    if state.v4v4[0]:
        return defenseur2(state)
    else :
        return SoccerAction(Vector2D(state.coequipier1.x, state.coequipier22.y)-state.player, state.coequipier22-state.player)
    
def attaquant4(state):
    if state.v4v4[3]:
        if state.devantatt == False : 
            return SoccerAction(state.ballameliorer-state.player, (state.coequipier22-state.player).normalize()*4)
        else :
            return attaquant2(state)
    else :
        return SoccerAction(Vector2D(state.coequipier22.x, state.player.y)-state.player, state.goal-state.player)
        
def defenseur4(state):
    if state.v4v4[1]:
        return defenseur2(state)
    else : 
        return SoccerAction(Vector2D(state.coequipier0.x,  state.coequipier3.y)-state.player, state.coequipier3-state.player)
    
    
    
    
    
    
    
def one(state):
    if state.bouge == True : 
        if (state.ball.x == GAME_WIDTH/2) and (state.ball.y == GAME_HEIGHT/2) and state.player.distance(state.ball)<1+PLAYER_RADIUS + BALL_RADIUS :
            return SoccerAction(state.ballameliorer-state.player, state.goal-state.player)
        if (state.devant == True) and state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS: 
            return SoccerAction(state.ballameliorer-state.player,(state.goal-state.player).normalize()*3)
        else :
            return gobetter(state)
    else : 
        if (state.ball.x == GAME_WIDTH/2) and (state.ball.y == GAME_HEIGHT/2) and state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
            return SoccerAction(state.ballameliorer-state.player, (state.goal-state.player).normalize()*2)
        else : 
            return gobetter(state)
            
        
def gardien(state) : 
     return SoccerAction(0, state.goal-state.player)

def milieu1(state) :
    if state.ball.x >= GAME_WIDTH*1/3  and state.ball.x <= GAME_WIDTH * 2/3 and state.ball.y >= GAME_HEIGHT * 1/2 :
        if state.devantmil == True :
            return gobetterdef1(state)
        else:
            return gobetterdef2(state)
    else:
        return SoccerAction(Vector2D(GAME_WIDTH*1/2,GAME_HEIGHT *3/4)-state.player,state.coequipier3-state.player)                          
                    
def milieu2(state) :
     if state.ball.x >= GAME_WIDTH*1/3  and state.ball.x <= GAME_WIDTH * 2/3 and state.ball.y <= GAME_HEIGHT * 1/2 :
        if state.devantmil == True :
            return gobetterdef1(state)
        else:
            return gobetterdef2(state)
     else:
        return SoccerAction(Vector2D(GAME_WIDTH*1/2,GAME_HEIGHT *1/4)-state.player,state.coequipier3-state.player)    
                

def defenseur5(state):
    if state.teamdef[1] : 
        return SoccerAction(Vector2D(GAME_WIDTH*(state.teamdef[0]), (state.ballameliorer.y+state.goal.y)/2 )-state.player, state.goal-state.player)
    else :
        return gobetterdef(state)
    
    
    
    
def attaquant5(state):
    if state.teamatt2[0]:
        return gobetteratt1(state)
    else:
        return SoccerAction(acceleration = Vector2D(state.teamatt2[1],(state.milieuloin).y)-state.player)
    
    
"""    
def milieu546546(state) :
   if state.teammil:
        if state.distancemil == True :
            return SoccerAction(Vector2D(GAME_WIDTH*(1/3), state.coequipier2.y)-state.player, state.goal-state.player)
        else :
           return gobetter(state) 
    else :
        if state.devantmil == True :
                if state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
                    return SoccerAction(state.ballameliorer-state.player,(state.coequipier2-state.player))
                else :
                    if state.player.distance(state.goal) < 30 and state.player.distance(state.ball)<PLAYER_RADIUS + BALL_RADIUS :
                        return SoccerAction(state.ballameliorer-state.player, state.goal-state.player)
                    else : 
                        return SoccerAction(state.ballameliorer-state.player,state.coequipier3-state.player)
"""                      
    
    
    
    
    
