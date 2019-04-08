#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 16:42:00 2019

@author: noe
"""
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS, BALL_RADIUS
from .tools      import SuperState
from .actions    import Actions
from .strategies import Strategies

class Attaquantsolo(Strategy):
    def __init__(self, force = 5, distance = 25, forcedr = 1, angledr = 3.14/5, distadverse = 5):
        
        Strategy.__init__(self, "Fonceur")
        self.force = force
        self.distance = distance
        self.angledr = angledr
        self.forcedr = forcedr
        self.distadverse = distadverse
        
    def compute_strategy(self, state, id_team, id_player):
        
        # id_team is 1 or 2
        # id_player starts at 0
        
       s = Strategies(state, id_team, id_player)
       v = SuperState(state, id_team, id_player)
       a = Actions(state, id_team, id_player)
        
       defense = s.defensesolo
       attaque = s.attaquesolo(self.force, self.distance, self.forcedr, self.angledr, self.distadverse)
       
       #if  v.playeradverse.distance(v.player) < PLAYER_RADIUS*10:
           #return attaque
       if  v.playeradverse.distance(v.ball) < PLAYER_RADIUS + BALL_RADIUS:#Défense si l'adversaire à la balle
       
           return defense
                
       else : 
           return attaque
           

          
            
class Attaquantduo(Strategy):
    def __init__ (self, force = 5, distance = 25, forcedr = 2, angledr = 3.14/4, distadverse = 12):
        Strategy.__init__(self, "Fonceur")
        self.force = force
        self.distance = distance
        self.angledr = angledr
        self.forcedr = forcedr
        self.distadverse = distadverse
        
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        
       s = Strategies(state, id_team, id_player)
       v = SuperState(state, id_team, id_player)
       a = Actions(state, id_team, id_player)
        
       defense = s.defenseduo
       attaque = s.attaquesolo(self.force, self.distance, self.forcedr, self.angledr, self.distadverse)
       
       #if  v.playeradverse.distance(v.player) < PLAYER_RADIUS*10:
           #return attaque
       if  v.ballecampadverse == 1 :  #Défense si l'adversaire à la balle
           return defense
                
       else : 
           return attaque
       

class Attaquantgauche(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")
        
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        
       s = Strategies(state, id_team, id_player)
       v = SuperState(state, id_team, id_player)
       a = Actions(state, id_team, id_player)
        
       defense = s.fonceur
       camp    = s.campgauche
       attaque = s.attaquegauche
       
       
       if  v.ballecampadverse == 1 :
           if v.campadversegauche == 1 : #Défense si l'adversaire à la balle
               
               return defense
           else : 
              
               return camp
    
        
       elif  v.campadversegauche == 0 : #si la balle n'est pas dans son camp, va se placer
           
           return camp
                
       else : 
           
           return attaque
       
       
class Attaquantdroit(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")
        
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        
       s = Strategies(state, id_team, id_player)
       v = SuperState(state, id_team, id_player)
       a = Actions(state, id_team, id_player)
        
       defense = s.fonceur #il suit la balle
       attaque = s.attaquedroit
       camp    = s.campdroit
       
    
       if  v.ballecampadverse == 1 :
           if v.campadversedroit == 1 : #Défense si l'adversaire à la balle
           
               return defense
           else : 
               
               return camp
               #break 
       elif  v.campadversedroit == 0 : #si la balle n'est pas dans son camp, va se placer
           
           return camp
                
       else : 
           
           return attaque
        
        
class Defenseur(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")
        
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        
       s = Strategies(state, id_team, id_player)
       v = SuperState(state, id_team, id_player)
       a = Actions(state, id_team, id_player)
       
       defense = s.fonceur
       
       if v.player.distance(v.ball) < PLAYER_RADIUS + BALL_RADIUS*32 :
           return defense
       
      #elif v.estballderrierelegoal == 1 :
       #    print("je vais au milieu")
        #   return a.deplacement(v.pointmilieu)"""
       
       else : 
           return s.milieu
       

class Gardien(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")
        
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        
       s = Strategies(state, id_team, id_player)
       t = SuperState(state, id_team, id_player)
       

      
       if t.estballderriere == 1 :
           
           return s.fonceur
       else :
          
           return s.gardien
       
class Gardien4(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")
        
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        
       s = Strategies(state, id_team, id_player)
       t = SuperState(state, id_team, id_player)
       

      
       if t.estballderriere == 1 :
           
           return s.fonceur
       else :
          
           return s.gardien4
   
    
class Ad(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaquant Droit")
        
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        
       s = Strategies(state, id_team, id_player)
       v = SuperState(state, id_team, id_player)
       a = Actions(state, id_team, id_player)
        
       defense = s.fonceur #il suit la balle
       #attaque = s.attaquedroit
        
        
       if v.player.distance(v.ball) < PLAYER_RADIUS + BALL_RADIUS: #J'ai la 
           if  v.player.distance(v.goaladverse) < (PLAYER_RADIUS * 30) :#Si il est dans la surface de tir : shoot
               print("shoot2")
               return a.shootbut() 
           else :
               return s.AttaquePasseDroit 
       else:
           if v.ballecampadverse == 0: #balle camps adverse
               if v.coepball == 1 :   # # mon coep a la balle 
                   return a.deplacementCampDroit # Je me positionne en position buteur 
               else:
                   if v.campadversegauche == 1: # Si je suis le plus proche 
                       return a.deplacement(a.directionball) #je recupere la balle
                   else:
                       return a.deplacement(v.pointcampeurdroit) # Je me positionne en position buteur 
           
           else :
               #if v.campadversedroit == 1: # Si je suis le plus proche 
                #   return defense
               #else :
               return a.deplacement(v.pointattaquantdroit) # Je me positionne en position buteur """

class Ag(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaquant Droit")
        
    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        
        s = Strategies(state, id_team, id_player)
        v = SuperState(state, id_team, id_player)
        a = Actions(state, id_team, id_player)
        
        defense = s.fonceur 
        
        if v.player.distance(v.ball) < PLAYER_RADIUS + BALL_RADIUS: #J'ai la 
            if  v.player.distance(v.goaladverse) < (PLAYER_RADIUS * 30) :#Si il est dans la surface de tir : shoot
                print("shoot1")
                return a.shootbut()
            else :
                return s.AttaquePasseGauche 
        else:
            if v.ballecampadverse == 0: #balle camps adverse
                if v.coepball == 1 :  # si mon coep a la balle 
                    return a.deplacementCampGauche # Je me positionne en position buteur 
                else:
                    if v.campadversedroit == 1: # Si je suis le plus proche 
                        return a.deplacement(a.directionball) #je recupere la balle
                    else:
                        return a.deplacement(v.pointcampeurgauche) # Je me positionne en position buteur 
                #return a.deplacement(v.pointattaquantgauche)

            else :
               #if v.campadversegauche == 1: # Si je suis le plus proche 
                #   return defense
               #else :
               return a.deplacement(v.pointattaquantgauche) # Je me positionne en position buteur """

