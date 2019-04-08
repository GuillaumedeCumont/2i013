#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:27:24 2019

@author: noe
"""

from soccersimulator import Ball, settings, Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator.settings  import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS,BALL_RADIUS
import math


class SuperState (object):
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              |FONCTIONS BASIQUES|                                                                                      |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|  
    def __init__ (self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        
    def __getattr__ (self , attr):
        return getattr (self.state , attr)
        
    @property
    #retourne la position de la balle
    def ball(self):
        return self.state.ball.position
    
    @property
    #retourne la position du joueur actuelle
    def player(self):
        return self.state.player_state (self.id_team, self.id_player).position
    
    @property
    #retourne la position des goals
    def goal(self):
        if(self.id_team == 2):
            return Vector2D(0,GAME_HEIGHT/2)
        else :
            return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        
    @property
    def angle(self):
        return math.atan2(self.y, self.x)
    
    @property
    #retourne la liste des opposants
    def listeop(self):
        return [self.state.player_state(id_team, id_player).position for (id_team , id_player) in self.state.players if id_team != self.id_team]
    
    @property
    #retourne l'opposant le plus proche
    def near(self):
        opponent = self.listeop
        return min([(self.player.distance (player), player) for player in opponent])[1]
        
    @property 
    #permet d'anticiper la balle
    def ballameliorer(self):
        return self.state.ball.position + 5 * self.state.ball.vitesse
    
    
    @property
    def teamatt(self):
        if self.id_team == 1 :
            (posattx,nextpos,defe) = (self.player.x < GAME_WIDTH*(1/2), GAME_WIDTH*(3/5),self.ballameliorer.x < GAME_WIDTH*(1/4))
        else : 
            (posattx,nextpos,defe) = (self.player.x > GAME_WIDTH*(1/2), GAME_WIDTH*(2/5),self.ballameliorer.x > GAME_WIDTH*(3/4))
        return (posattx,nextpos,defe)
    
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              |FIN FONCTIONS BASIQUES|                                                                                  |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------| 
        

#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              |FONCTIONS 1 VS 1|                                                                                        |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|           
    @property 
    def bouge(self) : 
        if self.goal.distance(self.near)<20:
            return False 
        else : 
            return True
    @property 
    def devant(self):
        if(self.goal.distance(self.player) < self.goal.distance(self.near)):
            return True 
        else : 
            return False
        
    
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              | FIN FONCTIONS 1 VS 1|                                                                                   |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------| 
        

#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              |FONCTIONS 4 VS 4|                                                                                        |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|   
    @property
    #Fonction utilisé pour que le defenseur fonctionne des 2 côtés 
    def teamdef(self):
        if self.id_team == 1 :
            (posdef,condition) = (1/4, self.ballameliorer.x > GAME_WIDTH*(1/3))
        else : 
            (posdef, condition) = (3/4, self.ballameliorer.x < GAME_WIDTH*(2/3))
        return (posdef,condition)    
    
    @property
     #Fonction utilisé pour que l'attaquant fonctionne des 2 côtés 
    def teamatt2(self):
        if self.id_team == 1 :
            (un,deux)=(self.ball.x >= GAME_WIDTH*(2/3), GAME_WIDTH*(2/3))
        else : 
            (un,deux)=(self.ball.x <= GAME_WIDTH*(1/3),GAME_WIDTH*(1/3))
        return  (un,deux)      
    
    @property
    #retourne la position du milieu le plus proche de nous
    def milieuproche(self):
        if self.player.distance(self.coequipier1) < self.player.distance(self.coequipier22):
            return self.coequipier1
        else:
            return self.coequipier22

    @property   
    #retourne la position du milieu le plus loin de nous
    def milieuloin(self):
        if self.player.distance(self.coequipier1) < self.player.distance(self.coequipier22):
            return self.coequipier22
        else:
            return self.coequipier1 

    @property
     #retourne la position du coéquipier avec l'id 1 ou 2 (milieu 1 ou milieu 2)
    def coequipier2(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and ((id_player == 1) or (id_player == 2)): 
                return self.state.player_state(id_team, id_player).position
            

    
    @property
    #retourne la position du coéquipier avec l'id 3 (attaquant)
    def coequipier3(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and (id_player == 3): 
                return self.state.player_state(id_team, id_player).position 
    
    @property
    #Savoir si le milieu est plus proche des goals que nous ou non
    def devantmil(self):
        if self.goal.distance(self.player) > self.goal.distance(self.coequipier2) :
            return True
        else:
            return False 
        
    @property
    #retourne la position du coéquipier avec l'id 2 (milieu2)
    def coequipier22(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and (id_player == 2): 
                return self.state.player_state(id_team, id_player).position        
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              | FIN FONCTIONS 4 VS 4|                                                                                   |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|   

#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              |FONCTIONS 4 VS 4 NON UTILISES|                                                                           |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|   

    @property
    def coequipieratt(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and ((id_player == 2) or (id_player == 3)):
                return self.state.player_state(id_team, id_player).position
            
    @property 
    #retourne le milieu le plus proche de la balle
    def distancemil(self):
        if self.ball.distance(self.player) > self.ball.distance(self.coequipier2) :
            return True 
        else :
            return False 
            

    
    @property
    #Savoir si l'attaquant est plus proche des goals que nous ou non
    def devantatt(self):
        if self.goal.distance(self.player) < self.goal.distance(self.coequipieratt) :
            return True
        else:
            return False
     

    @property
    #retourne la position du coéquipier avec l'id 0 (défenseur)
    def coequipier0(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and (id_player == 0): 
                return self.state.player_state(id_team, id_player).position
            
    @property
    #retourne la position du coéquipier avec l'id 1 (milieu 1)
    def coequipier1(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and (id_player == 1): 
                return self.state.player_state(id_team, id_player).position
  
    @property
    def teammil(self):
        if self.id_team == 1 :
            return self.ball.x <= GAME_WIDTH*(1/2) 
        else : 
            return self.ball.x >= GAME_WIDTH*(1/2)    
    @property
    def v4v4(self):
        if self.id_team == 1 :
            (def3, def4, att3, att4) = (self.ball.y <= GAME_HEIGHT*(1/2), self.ball.y >= GAME_HEIGHT*(1/2), self.ball.y <= GAME_HEIGHT*(1/2), self.ball.y >= GAME_HEIGHT*(1/2))
        else : 
            (def3, def4, att3, att4) = (self.ball.y <= GAME_HEIGHT*(1/2), self.ball.y >= GAME_HEIGHT*(1/2), self.ball.y <= GAME_HEIGHT*(1/2), self.ball.y >= GAME_HEIGHT*(1/2))
        return (def3, def4, att3, att4)
                
        

#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              | FIN FONCTIONS 4 VS 4 NON UTILISES|                                                                      |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|  


#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              |FONCTIONS NON UTILISES|                                                                                  |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|  
    @property 
    def oneatt(self): 
        if self.id_team == 1 :
            return (self.near.x < self.player.x)
        else : 
            return (self.near.x > self.player.x)


    @property
    def coequipier(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player): 
                return self.state.player_state(id_team, id_player).position
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|        
#|                                              | FIN FONCTIONS NON UTILISES|                                                                             |   
#|--------------------------------------------------------------------------------------------------------------------------------------------------------|  






                 

class SimpleStrategy (Strategy):
    def __init__ (self, action, name):
        super().__init__(name)
        self.action = action

    def compute_strategy (self, state ,id_team ,id_player):
        s = SuperState (state, id_team, id_player)
        return self.action(s)

    
class Move (object):
    def __init__ (self, superstate):
        self.superstate = superstate

    def move (self, acceleration = None):
        return SoccerAction(acceleration = acceleration)
    
    

    
    
    def to_ball (self):
        return self.move(self.superstate.ball-self.superstate.player)

class Shoot(object):
    def __init__ (self, superstate):
        self.superstate = superstate
    
    def shoot (self, direction = None):
        dist = self.superstate.player.distance(self.superstate.ball)
        if dist < PLAYER_RADIUS + BALL_RADIUS :
            return SoccerAction(shoot = direction)
        else :
            return SoccerAction()

    def to_goal (self, strength = None):
        return self.shoot((self.superstate.goal-self.superstate.player)*strength)

    
class GoTestStrategy (Strategy):
    def __init__ (self, strength=None ):
        Strategy.__init__(self, "Nasser")
        self.strength = strength

    def compute_strategy (self, state, id_team ,id_player):
        s = SuperState (state, id_team, id_player)
        move = Move(s)
        shoot = Shoot(s)
        return move.to_ball() + shoot.to_goal (self.strength)