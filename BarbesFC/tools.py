#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:22:24 2019

@author: noe
"""
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS

from soccersimulator import settings


# Encapsulation


class SuperState(object):
    
    def __init__(self, state, id_team, id_player):
    
        self.state     = state 
        self.id_team   = id_team 
        self.id_player = id_player


# Position de la balle
    @property
    def ball(self):
        return self.state.ball.position

# Position du Joueur
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position

    @property
    def playeradverse(self):
        if self.id_team == 1  :
            return self.state.player_state(2, 0).position

        else :
            return self.state.player_state(1, 0).position

# Position du Goal adverse
    @property
    def goaladverse(self):
        if self.id_team == 1 :
            return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        else : 
            return Vector2D(0, GAME_HEIGHT/2)

# Position du Goal de l'équipe
    @property
    def goalequipe(self):
        if self.id_team == 1 :
            return Vector2D(0, GAME_HEIGHT/2)
        else : 
            return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)

    
    @property
    def pointdefensesolo(self):
        if self.id_team == 1 :
            if (self.positionadverse == 1 or self.positionadverse == 7) :
                return self.goalequipe
            else :
                return Vector2D(GAME_WIDTH/6, GAME_HEIGHT/2)
        else :
            if (self.positionadverse == 6 or self.positionadverse == 12): 
                return self.goalequipe
                
            else :
                return Vector2D((GAME_WIDTH*5)/6, GAME_HEIGHT/2)
            
    @property
    def pointdefenseduo(self):
        if self.id_team == 1 :
            return Vector2D(GAME_WIDTH*5/8, GAME_HEIGHT/4)
        else :
            return Vector2D(GAME_WIDTH*3/8, GAME_HEIGHT/4)
        
    @property
    def pointmilieu(self):
        if self.id_team == 1 :
            return Vector2D(GAME_WIDTH/2 - 10, GAME_HEIGHT/2)
        else :
            return Vector2D(GAME_WIDTH/2 + 10, GAME_HEIGHT/2)
        
        
        

# Liste des opposants
    @property
    def opposants(self) :
        opponents = [self.state.player_state(id_team, id_player).position for (id_team , id_player) in self.state.players
                     if id_team != self.id_team]
        return opponents
    
    @property
    def opposantsplusproche(self) :
        return min([(self.player.distance(player), player) for player in self.opposants])
    
    @property
    def ballecampadverse(self) :
        if self.id_team == 1 :
            if self.ball.x < GAME_WIDTH/2:
                return 1
            else :
                return 0
        else:
            if self.ball.x > GAME_WIDTH/2:
                return 1
            else :
                return 0
    

     
    @property
    def estderriere(self):
        if self.id_team == 1 :
            if self.opposantsplusproche[1].x < self.player.x :
                return 1 
            else:
                return 0
            
        if self.id_team == 2 :
            if self.opposantsplusproche[1].x > self.player.x :
                return 1 
            else:
                return 0
            
    @property
    def estballderriere(self):
        if self.id_team == 1 :
            if self.ball.x < self.player.x :
                return 1 
            else:
                return 0
            
        if self.id_team == 2 :
            if self.ball.x > self.player.x :
                return 1 
            else:
                return 0
    

    def estballderrierelegoal(self): 
        
        if self.id_team == 1 :
            if self.ball.x < self.state.player_state(1, 0).position.x :
                return 1 
            else:
                return 0
            
        if self.id_team == 2 :
            if self.ball.x > self.state.player_state(2, 0).position.x :
                return 1 
            else:
                return 0
    
    def position(self, obj):
        if (obj.y > (GAME_HEIGHT/2)):
            if obj.x <= GAME_WIDTH/8 :
                return 1
            if obj.x <= GAME_WIDTH/4 :
                return 2
            if obj.x <= GAME_WIDTH/2 :
                return 3
            if obj.x <= (3*GAME_WIDTH)/4 :
                return 4
            if obj.x <= (7*GAME_WIDTH)/8 :
                return 5
            else :
                return 6
            
        else :
            if obj.x <= GAME_WIDTH/8 :
                return 7
            if obj.x <= GAME_WIDTH/4 :
                return 8
            if obj.x <= GAME_WIDTH/2 :
                return 9
            if obj.x <= (3*GAME_WIDTH)/4 :
                return 10
            if obj.x <= (7*GAME_WIDTH)/8 :
                return 11
            else :
                return 12
                
    @property
    def coepdevant(self):
        if self.id_team == 1:
            if self.id_player == 1:
                if self.state.player_state(self.id_team, 2).position.x >= self.player.x :
                    return 1 
                else:
                    return 0
            else :
                if self.state.player_state(self.id_team, 1).position.x >= self.player.x :
                    return 1 
                else:
                    return 0
        else :
            if self.id_player == 1:
                if self.state.player_state(self.id_team, 2).position.x <= self.player.x :
                    return 1 
                else:
                    return 0
            else :
                if self.state.player_state(self.id_team, 1).position.x <= self.player.x :
                    return 1 
                else:
                    return 0
            
        
        
    @property
    def pointattaquantgauche(self):
        if self.id_team == 1:
            return Vector2D(GAME_WIDTH*3/4, GAME_HEIGHT*3/4)
        else : 
            return Vector2D(GAME_WIDTH/4, GAME_HEIGHT*3/4)
        
    
    @property
    def pointattaquantdroit(self):
        if self.id_team == 1:
            return Vector2D(GAME_WIDTH*3/4, GAME_HEIGHT/4)
        else : 
            return Vector2D(GAME_WIDTH/4, GAME_HEIGHT/4)
        
    @property
    def pointcampeurdroit(self):
        if self.id_team == 1:
            return Vector2D(GAME_WIDTH*15/16, GAME_HEIGHT*3.5/8)
        else : 
            return Vector2D(GAME_WIDTH/16, GAME_HEIGHT*3.5/8)
        
        
    @property
    def pointcampeurgauche(self):
        if self.id_team == 1:
            return Vector2D(GAME_WIDTH*15/16, GAME_HEIGHT*5.5/8)
        else : 
            return Vector2D(GAME_WIDTH/16, GAME_HEIGHT*5.5/8)
        
    @property
    def poscoequippier(self):
        if self.id_player == 1:
            return self.state.player_state(self.id_team, 2).position
        else :
            return self.state.player_state(self.id_team, 1).position
            
            
    @property
    def campadversedroit(self):
        #if self.id_team == 1:
        if self.ball.y >= GAME_HEIGHT/2 :
            return 1
        else :return 0
                
       # else :
         #   return 0
    
    @property
    def campadversegauche(self):
        #if self.id_team == 1:
        if self.ball.y <= GAME_HEIGHT/2 :
            return 1
        else :return 0
        
       # else :
        #    return 0
            
        
        
    @property
    def positionadverse(self):
        if (self.playeradverse.y > (GAME_HEIGHT/2)):
            if self.playeradverse.x <= GAME_WIDTH/8 :
                return 1
            if self.playeradverse.x <= GAME_WIDTH/4 :
                return 2
            if self.playeradverse.x <= GAME_WIDTH/2 :
                return 3
            if self.playeradverse.x <= (3*GAME_WIDTH)/4 :
                return 4
            if self.playeradverse.x <= (7*GAME_WIDTH)/8 :
                return 5
            else :
                return 6
            
        else :
            if self.playeradverse.x <= GAME_WIDTH/8 :
                return 7
            if self.playeradverse.x <= GAME_WIDTH/4 :
                return 8
            if self.playeradverse.x <= GAME_WIDTH/2 :
                return 9
            if self.playeradverse.x <= (3*GAME_WIDTH)/4 :
                return 10
            if self.playeradverse.x <= (7*GAME_WIDTH)/8 :
                return 11
            else :
                return 12

    @property
    def coepball(self):
        
        for i in range(1, 4) : 
            if i == self.id_player :
                continue
            else :
                if self.state.player_state(self.id_team, i).position.distance(self.ball) < PLAYER_RADIUS + BALL_RADIUS:
                    return 1;
        return 0 ;    
            



    @property
    def possibtir(self):
        b = 0 
        return b