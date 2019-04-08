#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:36:26 2019

@author: noe
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS

from .tools   import SuperState
from .actions import Actions
import math



class Strategies(object) : 
    
    def __init__(self, state, id_team, id_player):
    
        self.state     = state 
        self.id_team   = id_team 
        self.id_player = id_player
    

    
    def attaquesolo(self, force, distance, forcedr, angledr, distadverse):
            
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS:
            if s.opposantsplusproche[1].distance(s.player) < (PLAYER_RADIUS*distadverse):
                return a.dr2(forcedr, angledr)
            elif  s.player.distance(s.goaladverse) < (PLAYER_RADIUS * distance) :#Si il est dans la surface de tir : shoot, sinon avance
                
                return a.shootbut(force)
            
            else :
                return a.avanceravecballe
        else:
            return a.deplacement(a.directionball)
        
        
    
    @property
    def attaque2(self):
            
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        if s.player.distance(s.ball) < PLAYER_RADIUS*10:
            return a.deplacement(a.directionball)
        elif s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS:
            if s.player.distance(s.goaladverse) < (PLAYER_RADIUS * 15):
                return a.shootbut
            elif s.coepdevant == 1 :
                return a.tircoequippier
            else : 
                return a.avanceravecballe
                    
                
                
            
        else:
            return a.deplacement(s.pointattaquant2)
        
    @property
    def attaque1(self):
            
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        if s.poscoequippier.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS : #SI le coequippier a la balle
            
            return a.deplacement(s.pointcampeurgauche)
        
        elif s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS:
            if s.player.distance(s.poscoequippier) < PLAYER_RADIUS*25 :
                if s.coepdevant == 1 :
                    return a.tircoequippier 
            elif  s.player.distance(s.goaladverse) < (PLAYER_RADIUS * 15) :#Si il est dans la surface de tir : shoot
                return a.shootbut
            elif s.playeradverse.distance(s.player) < (PLAYER_RADIUS*8):
                return a.dr2
            else :
                
                return a.avanceravecballe
        else:
            
            return a.deplacement(s.ball)
       
        
        
    @property
    def attaquedroit(self): #essai
            
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        if s.poscoequippier.distance(a.directionball) < PLAYER_RADIUS + BALL_RADIUS : #SI le coequippier a la balle
            
            return a.deplacement(s.pointcampeurdroit)
        
        elif s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS:
            if s.opposantsplusproche[1].distance(s.player)< PLAYER_RADIUS *10:
                
            #if s.player.distance(s.poscoequippier) < PLAYER_RADIUS*25 :
                if s.coepdevant == 1 :
                    
                    return a.tircoequippier + a.deplacement(s.pointattaquantdroit)
            elif  s.player.distance(s.goaladverse) < (PLAYER_RADIUS * 25) :#Si il est dans la surface de tir : shoot
                return a.shootbut
            elif s.playeradverse.distance(s.player) < (PLAYER_RADIUS*8):
                return a.dr2
            else :
                
                return a.avanceravecballe
        else:
            
            return a.deplacement(a.directionball)
        
    @property
    def attaquegauche(self): #essai
            
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        if s.poscoequippier.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS : #SI le coequippier a la balle
            
            return a.deplacement(s.pointcampeurgauche)
        
        elif s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS: 
            if s.opposantsplusproche[1].distance(a.directionball)< PLAYER_RADIUS *10:
                
                
            #if s.player.distance(s.poscoequippier) < PLAYER_RADIUS*25 :
                if s.coepdevant == 1 :
                    
                    return a.tircoequippier + a.deplacement(s.pointattaquantgauche)
            elif  s.player.distance(s.goaladverse) < (PLAYER_RADIUS * 25) :#Si il est dans la surface de tir : shoot
                return a.shootbut
            elif s.playeradverse.distance(s.player) < (PLAYER_RADIUS*8):
                return a.dr2
            else :
                
                return a.avanceravecballe
        else:
            
            return a.deplacement(a.directionball)
        
        

    @property
    def defensesolo(self):

        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
       
        return a.deplacement(s.pointdefensesolo)
      
    
    @property
    def defenseduo(self) :
        s = SuperState(self.state, self.id_team, self.id_player)
        
        return SoccerAction(acceleration = s.pointdefenseduo - s.player)
        
    
    @property
    def defensesolo2(self):

        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        if self.id_team == 1 :
            if s.position(s.ball) == 1 or s.position(s.ball) == 2 or s.position(s.ball) == 7 or s.position(s.ball) == 8 :
                return a.deplacement(s.ball) + a.shootbut
            else :
                return a.deplacement(s.pointdefensesolo)

        if self.id_team == 2 :
            if s.position(s.ball) == 5 or s.position(s.ball) == 6 or s.position(s.ball) == 11 or s.position(s.ball) == 12 :
                return a.deplacement(s.ball) + a.shootbut
            else :
                return a.deplacement(s.pointdefensesolo)
    
        
            
      
            
        
    
    @property
    def gardien(self):
            
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        

        
        if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS :
            return a.shootdefenseduo
            
        
        elif s.player.distance(s.ball) < PLAYER_RADIUS*10 :
            return a.deplacement(a.directionball)
        
        else:
            return a.deplacementlateral
        
    @property
    def gardien4(self):
            
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        
        
        if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS :
            return a.shootdefensemilieu
            
        
        elif s.player.distance(s.ball) < PLAYER_RADIUS*15 :
            return a.deplacement(a.directionball)
        
        else:
            return a.deplacementlateral












    @property
    def gardien2(self):
       
       
       
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions (self.state, self.id_team, self.id_player)
        id_team = self.id_team
        state = self.state
        id_player = self.id_player
       
        if id_team == 1:
            if s.ball.x >= GAME_WIDTH/2 :
                if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS :
                    shoot = (s.goaladverse - s.player)
                    #return SoccerAction(shoot = shoot.normalize()*1500)
                    return a.shootbut
               
                elif s.player.distance(s.ball) < PLAYER_RADIUS*3  : #Ne se déplace que si la balle est proche de lui
                    return a.deplacement(s.ball)
               
                else:
                    return a.deplacement(s.goalequipe)
            elif s.ball.x < GAME_WIDTH/2 :
                if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS :
                    shoot = (s.goaladverse - s.player)
                    #return SoccerAction(shoot = shoot.normalize()*1500)
                   
                else :
                    deplacement = state.ball.position - state.player_state(id_team,id_player).position
                    tir = Vector2D(150,45) - state.ball.position
                    return SoccerAction(deplacement, tir)

        else:
            if s.ball.x <= GAME_WIDTH/2 :
                if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS :
                    shoot = (s.goaladverse - s.player)
                    return SoccerAction(shoot = shoot.normalize()*1500)
                   
                elif s.player.distance(s.ball) < PLAYER_RADIUS*3  : #Ne se déplace que si la balle est proche de lui
                    return SoccerAction(acceleration = s.deplacement(s.ball))
                   
                else:
                    return a.deplacement(s.goalequipe)
            elif s.ball.x > GAME_WIDTH/2 :
                    deplacement = state.ball.position - state.player_state(id_team,id_player).position
                    tir = Vector2D(0,45) - state.ball.position
                    return SoccerAction(deplacement, tir)
                    


    @property
    def fonceur(self):
        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions (self.state, self.id_team, self.id_player)
        # id_team is 1 or 2
        # id_player starts at 0
        
        #SI C'EST DANS SON CAMP : FONCEUR. SINON : POSDÉFENSEDUO
     
        if s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS :
            return a.tircoequippier
        else :
            return a.deplacement(a.directionball)
       

    @property
    def campdroit(self):

        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)

        return a.deplacement(s.pointattaquantdroit)
    
    @property
    def campgauche(self):

        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)

        return a.deplacement(s.pointattaquantgauche)
    

    @property
    def milieu(self):

        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        if s.player.distance(s.ball) < PLAYER_RADIUS*10:
            return a.deplacement(s.ball)
        elif s.player.distance(s.ball) < PLAYER_RADIUS + BALL_RADIUS:
            return a.shoot(s.pointattaquantgauche)
        
        else:
            return a.deplacementlateralmilieu
        
    @property
    def AttaquePasseDroit (self):

        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        b = 0 ;
        
        #if b == 1 :
         #   b = 0 #Pour savoir si la passe vient juste d'être faite
          #  return a.shootbut
        #elif s.estderriere == 0:
        if s.opposantsplusproche[1].distance(s.player)< PLAYER_RADIUS *10: #Si un adversaire est proche de nous
            print("1D")
            return a.tircoequippier + a.deplacement(s.pointcampeurdroit) #Tir au coep
         
        elif  s.player.distance(s.goaladverse) < (PLAYER_RADIUS * 20) :#Si il est dans la surface de tir : shoot
            return a.shootbut
        
        else :
            return a.avanceravecballe
    
    @property
    def AttaquePasseGauche (self):

        s = SuperState(self.state, self.id_team, self.id_player)
        a = Actions(self.state, self.id_team, self.id_player)
        
        b = 0 ;
        
        #if b == 1 :
         #   b = 0 #Pour savoir si la passe vient juste d'être faite
          #  return a.shootbut
        #elif s.estderriere == 0:
        if s.opposantsplusproche[1].distance(s.player)< PLAYER_RADIUS *10: #Si un adversaire est proche de nous
            print("1G")
            return a.tircoequippier + a.deplacement(s.pointcampeurgauche) #Tir au coep
     
        elif  s.player.distance(s.goaladverse) < (PLAYER_RADIUS * 20) :#Si il est dans la surface de tir : shoot
            return a.shootbut
    
        else :
            return a.avanceravecballe
        
