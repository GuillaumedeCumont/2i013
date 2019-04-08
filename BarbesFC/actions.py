#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 16:04:42 2019

@author: noe
"""
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS
from .tools  import SuperState

class Actions(object):
    
    def __init__(self, state, id_team, id_player):
    
        self.state     = state 
        self.id_team   = id_team 
        self.id_player = id_player
    
    
    def shootbut(self, force = 2) :
        s = SuperState(self.state, self.id_team, self.id_player) 
        shoot = s.goaladverse - s.player
        return SoccerAction(shoot = shoot.normalize()*force)
    

    def shoot(self, obj) :
        s = SuperState(self.state, self.id_team, self.id_player) 
        shoot = obj - s.player
        return SoccerAction(shoot = shoot.normalize()*10)
    
    @property
    def shootdefenseduo(self) :
        s = SuperState(self.state, self.id_team, self.id_player) 
        shoot = s.pointdefenseduo - s.player
        return SoccerAction(shoot = shoot.normalize()*155)
    
    @property
    def shootdefensemilieu(self) :
        s = SuperState(self.state, self.id_team, self.id_player) 
        shoot = s.pointmilieu - s.player
        return SoccerAction(shoot = shoot.normalize()*155)
    
    @property
    def dribble(self) :
        s = SuperState(self.state, self.id_team, self.id_player) 
        if s.playeradverse.y > s.player.y : #Si le joueur vient par la droite
            return SoccerAction(shoot = Vector2D(s.goaladverse.x, 0).normalize()*0.5) #On avance par la gauche
        else :  
            return SoccerAction(shoot = Vector2D(s.goaladverse.x, 0).normalize()*0.5)#On avance par la droite
    """@property
    def dr2(self) :
        s = SuperState(self.state, self.id_team, self.id_player) 
        if s.estderriere == 0 : #ssi l'&dversaire est derrière on dribble 
            if s.playeradverse.y >= s.player.y : #Si le joueur vient par la droite
                return SoccerAction(shoot = Vector2D(s.goaladverse.x - s.player.x, s.playeradverse.y-30 - s.player.y).normalize()*2) #+ self.avanceravecballe #On avance par la gauche
        
            else :  
                return SoccerAction(shoot = Vector2D(s.goaladverse.x - s.player.x, s.playeradverse.y+30 - s.player.y).normalize()*2) #+ self.avanceravecballe #On avance par la gauche
        else : 
            return self.avanceravecballe"""
        
   
    def dr2(self, forcedr, angledr) :
        s = SuperState(self.state, self.id_team, self.id_player) 
        if s.estderriere == 0 : #ssi l'&dversaire est derrière on dribble 
            if s.opposantsplusproche[1].y > s.player.y or s.opposantsplusproche[1].y == s.player.y : #Si le joueur vient par la droite
                
                dir = (s.goaladverse - s.player).normalize() * forcedr
                dir.angle -= angledr #3.14/6
                return SoccerAction(shoot = dir)
                #return SoccerAction(shoot = Vector2D(s.goaladverse.x - s.player.x, s.opposantsplusproche[1].y-15 - s.player.y).normalize()*1.1) #+ self.avanceravecballe #On avance par la gauche
                    
            else : 
                
                dir = (s.goaladverse - s.player).normalize() * forcedr
                dir.angle += angledr #3.14/6
                return SoccerAction(shoot = dir)
                #return SoccerAction(shoot = Vector2D(s.goaladverse.x - s.player.x, s.opposantsplusproche[1].y+15 - s.player.y).normalize()*1.1) #+ self.avanceravecballe #On avance par la gauche
                
        else : 
            
            return self.avanceravecballe 

   

# Aller vers un point

    def deplacement(self, obj): 
        s = SuperState(self.state, self.id_team, self.id_player)
        dep = obj - s.player
        de = dep.normalize()* 1500
        return SoccerAction(acceleration = de)
    
    @property
    def allerdefensesolo(self) :
        s = SuperState(self.state, self.id_team, self.id_player) 
        return self.deplacement(s.pointdefensesolo)
    
    @property
    def allergoalequipe(self):
        s = SuperState(self.state, self.id_team, self.id_player) 
        dep = s.goalequipe - s.player
        de = dep.normalize()* 1500
        return SoccerAction(acceleration = de)
    
    @property
    def tircoequippier(self):
        s = SuperState(self.state, self.id_team, self.id_player)
        tir = s.poscoequippier - s.player
        if s.id_team == 1 : #Différenciation de la position du joueur pour la force de frappe
            if s.player.x >= (3*GAME_WIDTH)/4 :
                return SoccerAction(shoot = tir.normalize()*2.5)
        else :
            if s.player.x <= (GAME_WIDTH)/4 :
                return SoccerAction(shoot = tir.normalize()*2.5 )
        return SoccerAction(shoot = tir.normalize()*5 )
    
    
    @property
    def tircampeur(self):
        s = SuperState(self.state, self.id_team, self.id_player)
        tir = s.pointcampeur - s.player
        return SoccerAction(shoot = tir.normalize()*25 )
    
    
    @property
    def avancertoutdroit(self):
        s = SuperState(self.state, self.id_team, self.id_player) 
        if self.id_team == 1 :
            shoot = Vector2D(GAME_WIDTH, s.player.y) - s.player
        else :
            shoot = Vector2D(0, s.player.y) - s.player
            
        return SoccerAction(shoot = shoot.normalize()*1)
    
    @property
    def allerpositiongardien(self):
       s = SuperState(self.state, self.id_team, self.id_player) 
       dep = s.pointdefensesolo - s.player
       de = dep.normalize()* 150
       return SoccerAction(acceleration = de)
        
    @property
    def avanceravecballe(self):
        s = SuperState(self.state, self.id_team, self.id_player) 
        shoot = s.goaladverse - s.player
        return SoccerAction(shoot = shoot.normalize()*1)
    
    @property
    def deplacementlateral(self):
        s = SuperState(self.state, self.id_team, self.id_player)
        return SoccerAction(acceleration = Vector2D(s.pointdefensesolo.x - s.player.x, s.ball.y - s.player.y))
    
    @property
    def deplacementlateralmilieu(self):
        s = SuperState(self.state, self.id_team, self.id_player)
        return SoccerAction(acceleration = s.pointmilieu - s.player)
    
    @property
    def directionball(self) :
        s = SuperState(self.state, self.id_team, self.id_player)
        #return Vector2D(s.ball + self.state.ball.vitesse*1.5*s.player.distance(s.ball))
        return s.ball + self.state.ball.vitesse*5
      

    @property
    def deplacementCampDroit(self):
        s = SuperState(self.state, self.id_team, self.id_player)
        return SoccerAction(acceleration = Vector2D(s.ball.x - s.player.x, s.pointattaquantdroit.y - s.player.y))
    @property
    def deplacementCampGauche(self):
        s = SuperState(self.state, self.id_team, self.id_player)
        return SoccerAction(acceleration = Vector2D(s.ball.x - s.player.x, s.pointattaquantgauche.y - s.player.y))