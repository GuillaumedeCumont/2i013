#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 16:05:58 2019

@author: 3700351
"""
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu, math
from soccersimulator.settings import *

class SuperState(object):
        def __init__(self,state,id_team,id_player):
            self.state = state
            self.id_team = id_team
            self.id_player = id_player
        @property
        def cannot(self):
            if self.norme>PLAYER_RADIUS+BALL_RADIUS:
                return True
            else:
                return False
        @property
        def milieu(self):
            if self.ball.x==GAME_WIDTH/2 and self.ball.y==GAME_HEIGHT/2:
                return True 
            else:
                return False
        @property
        def ide(self):
            return self.id_player
        @property
        def step(self):
            return self.state.step
        @property
        def ball(self):
            return self.state.ball.position
        @property
        def vball(self):
            return self.state.ball.vitesse
        @property
        def player(self):
            return self.state.player_state(self.id_team, self.id_player).position
        @property
        def goal(self):
            return Vector2D((self.id_team%2)*GAME_WIDTH,GAME_HEIGHT/2)
        @property
        def norme(self): #distance entre le joueur et la balle
            return math.sqrt((self.ball.x-self.player.x)**2+(self.ball.y-self.player.y)**2)
        @property
        def gnorme(self): #distance joueur et goal adverse
            return math.sqrt(((self.id_team%2)*GAME_WIDTH-self.player.x)**2+(45-self.player.y)**2)
        @property
        def cnorme(self): #distance entre l'attaquant adverse le plus proche et nos cages
            i=0
            n=len(self.state.players)/2
            v=Vector2D(GAME_WIDTH,GAME_HEIGHT)
            while i<n:
                if 0<(math.sqrt((self.state.player_state(self.id_team%2+1,i).position.x-(self.id_team%2+1)*GAME_WIDTH)**2+(self.state.player_state(self.id_team%2+1,i).position.y-GAME_HEIGHT/2)**2)) and (math.sqrt((self.state.player_state(self.id_team%2+1,i).position.x-(self.id_team%2+1)*GAME_WIDTH)**2+(self.state.player_state(self.id_team%2+1,i).position.y-GAME_HEIGHT/2)**2))<math.sqrt(v.x**2+v.y**2):
                    v=Vector2D(self.state.player_state(self.id_team%2+1,i).position.x-(self.id_team%2+1)*GAME_WIDTH,self.state.player_state(self.id_team%2+1,i).position.y-GAME_HEIGHT/2)
                i=i+1
            return math.sqrt(v.x**2+v.y**2)
        @property
        def fnorme(self): #distance entre le joueur et l'allier le plus proche
            i=0
            n=len(self.state.players)/2
            v=Vector2D(GAME_WIDTH,GAME_HEIGHT)
            while i<n:
                if 0<(math.sqrt((self.state.player_state(self.id_team,i).position.x-self.ball.x)**2+(self.state.player_state(self.id_team,i).position.y-self.ball.y)**2) and (math.sqrt((self.state.player_state(self.id_team,i).position.x-self.player.x)**2+(self.state.player_state(self.id_team,i).position.y-self.player.y)**2)<math.sqrt(v.x**2+v.y**2))):
                    v=Vector2D(self.state.player_state(self.id_team,i).position.x-self.ball.x,self.state.player_state(self.id_team,i).position.y-self.ball.y)
                i=i+1
            return math.sqrt(v.x**2+v.y**2)
        @property
        def fbnorme(self): #distance la plus courte entre la balle et un alliee 
            i=0
            n=len(self.state.players)/2
            v=Vector2D(GAME_WIDTH,GAME_HEIGHT)
            while i<n:
                if (math.sqrt((self.state.player_state(self.id_team,i).position.x-self.ball.x)**2+(self.state.player_state(self.id_team,i).position.y-self.ball.y)**2)<math.sqrt(v.x**2+v.y**2)):
                    v=Vector2D(self.state.player_state(self.id_team,i).position.x-self.ball.x,self.state.player_state(self.id_team,i).position.y-self.ball.y)
                i=i+1
            return math.sqrt(v.x**2+v.y**2)
        @property
        def enorme(self): #distance balle et adversaire
            i=0
            n=len(self.state.players)/2
            v=Vector2D(GAME_WIDTH,GAME_HEIGHT)
            while i<n:
                if (math.sqrt((self.state.player_state(self.id_team%2+1,i).position.x-self.ball.x)**2+(self.state.player_state(self.id_team%2+1,i).position.y-self.ball.y)**2)<math.sqrt(v.x**2+v.y**2)):
                    v=Vector2D(self.state.player_state(self.id_team%2+1,i).position.x-self.ball.x,self.state.player_state(self.id_team%2+1,i).position.y-self.ball.y)
                i=i+1
            return math.sqrt(v.x**2+v.y**2)
        @property
        def eproche(self): #distance entre nous et l'adversaire le plus proche
            i=0
            n=len(self.state.players)/2
            v=Vector2D(GAME_WIDTH,GAME_HEIGHT)
            while i<n:
                if (math.sqrt((self.state.player_state(self.id_team%2+1,i).position.x-self.player.x)**2+(self.state.player_state(self.id_team%2+1,i).position.y-self.player.y)**2)<math.sqrt(v.x**2+v.y**2)):
                    v=Vector2D(self.state.player_state(self.id_team%2+1,i).position.x-self.player.x,self.state.player_state(self.id_team%2+1,i).position.y-self.player.y)
                i=i+1
            return math.sqrt(v.x**2+v.y**2)
        
        @property
        def pos_eproche(self): # retourne la position de l'ennemie le plus proche
            i=0
            n=len(self.state.players)/2
            v=Vector2D(GAME_WIDTH,GAME_HEIGHT)
            while i<n:
                if (math.sqrt((self.state.player_state(self.id_team%2+1,i).position.x-self.player.x)**2+(self.state.player_state(self.id_team%2+1,i).position.y-self.player.y)**2)<math.sqrt(v.x**2+v.y**2)):
                    v=Vector2D(self.state.player_state(self.id_team%2+1,i).position.x-self.player.x,self.state.player_state(self.id_team%2+1,i).position.y-self.player.y)
                    j=self.state.player_state(self.id_team%2+1,i).position
                i=i+1
            return j
                
            
        @property 
        def fproche(self): #donne le vecteur position de l'allier le plus proche
            i=0
            n=len(self.state.players)/2
            dmax=math.sqrt((GAME_WIDTH)**2+(GAME_HEIGHT)**2)
            if self.id_team==1:  
                while i<n:
                    if dmax>math.sqrt((self.state.player_state(self.id_team,i).position.x-self.player.x)**2+(self.state.player_state(self.id_team,i).position.y-self.player.y)**2) and i!=self.id_player and self.state.player_state(self.id_team,i).position.x>self.player.x:
                        v=Vector2D(self.state.player_state(self.id_team,i).position.x-self.player.x,self.state.player_state(self.id_team,i).position.y-self.player.y)
                        dmax=math.sqrt((self.state.player_state(self.id_team,i).position.x-self.player.x)**2+(self.state.player_state(self.id_team,i).position.y-self.player.y)**2)
                    i=i+1
            else:
                while i<n:
                    if dmax>math.sqrt((self.state.player_state(self.id_team,i).position.x-self.player.x)**2+(self.state.player_state(self.id_team,i).position.y-self.player.y)**2) and i!=self.id_player and self.state.player_state(self.id_team,i).position.x<self.player.x:
                        v=Vector2D(self.state.player_state(self.id_team,i).position.x-self.player.x,self.state.player_state(self.id_team,i).position.y-self.player.y)
                        dmax=math.sqrt((self.state.player_state(self.id_team,i).position.x-self.player.x)**2+(self.state.player_state(self.id_team,i).position.y-self.player.y)**2)
                    i=i+1
            return v
        @property
        def fprocheatk(self): #donne le vecteur position de l'attaquant le plus proche
            i=2 # a partir des 2 attaquant
            n=4
            j=0
            while i<n:
                
                ve=Vector2D(GAME_WIDTH,GAME_HEIGHT)
                while j<n:
                   if (math.sqrt((self.state.player_state(self.id_team%2+1,j).position.x-self.state.player_state(self.id_team,i).position.x)**2+(self.state.player_state(self.id_team%2+1,j).position.y-self.state.player_state(self.id_team,i).position.y)**2)<math.sqrt(ve.x**2+ve.y**2)):
                       ve=Vector2D(self.state.player_state(self.id_team%2+1,j).position.x-self.state.player_state(self.id_team,i).position.x,self.state.player_state(self.id_team%2+1,j).position.y-self.state.player_state(self.id_team,i).position.y)
                       j=j+1
                j=0
                
                if i==2:
                   tmp=Vector2D(self.state.player_state(self.id_team,i).position.x-self.player.x,self.state.player_state(self.id_team,i).position.y-self.player.y)
                   distfe=math.sqrt(ve.x**2+ve.y**2) 
                else :
                   tmp2=Vector2D(self.state.player_state(self.id_team,i).position.x-self.player.x,self.state.player_state(self.id_team,i).position.y-self.player.y)
                   distfe2=math.sqrt(ve.x**2+ve.y**2)
                    
            if tmp<tmp2:
                if distfe>15:
                    return tmp
                else:
                    return tmp2
            else:
                if distfe2>15:
                    return tmp2
                else:
                    return tmp
        @property
        def aligne_def(self): #s'aligne entre la balle et les cage pour un x donné : y=ax+b
            if self.id_team==1:
                a=(self.ball.y-45)/self.ball.x
                b=45
            else:
                a=(self.ball.y-45)/(self.ball.x-150)
                b=45-150*a
            return a*self.player.x+b
        
        @property
        def aligne_def_y(self): #s'aligne entre la balle et les cage pour un y donné : x=y-b/a
            if self.id_team==1:
                a=(self.ball.y-45)/self.ball.x
                b=45
            else:
                a=(self.ball.y-45)/(self.ball.x-150)
                b=45-150*a
            return (self.player.y-b)/a
        
        @property
        def defadv(self): #retourne la position du defenseur adverse
            i=0
            n=len(self.state.players)/2
            v=Vector2D(GAME_WIDTH,GAME_HEIGHT)
            while i<n:
                if math.sqrt((self.state.player_state(self.id_team%2+1,i).position.x-((self.id_team%2+1)%2)*GAME_WIDTH)**2+(self.state.player_state(self.id_team%2+1,i).position.y-GAME_HEIGHT/2)**2) < math.sqrt(v.x**2+v.y**2):
                    v=Vector2D(self.state.player_state(self.id_team%2+1,i).position.x-((self.id_team%2+1)%2)*GAME_WIDTH,self.state.player_state(self.id_team%2+1,i).position.y-GAME_HEIGHT/2)
                    res=self.state.player_state(self.id_team%2+1,i).position
                i=i+1
            return res
        
        @property
        def distgb(self): #retourne la distance entre la balle et notre goal
            return math.sqrt((self.state.player_state(self.id_team,3).position.x-self.ball.x)**2+(self.state.player_state(self.id_team,3).position.y-self.ball.y)**2)
        
        @property
        def enemy1v1(self): #renvoi la position de l'adversaire dans le cas d'un 1vs1
            if self.id_team==1:
                return self.state.player_state(2,0).position
            else:
                return self.state.player_state(1,0).position
        @property
        def unedeux(self):
            if self.id_team==1:
                if(self.id_player==2):
                    return self.state.player_state(1,3).position
                else:
                    return self.state.player_state(1,2).position
            else:
                if(self.id_player==2):
                    return self.state.player_state(2,3).position
                else:
                    return self.state.player_state(2,2).position
        @property
        def posxatk(self):
            if self.id_player==2:
                return self.state.player_state(self.id_team,3).position.x
            else:
                return self.state.player_state(self.id_team,2).position.x
        @property
        def posyatk(self):
            if self.id_player==2:
                return self.state.player_state(self.id_team,3).position.y
            else:
                return self.state.player_state(self.id_team,2).position.y
        @property
        def posdef(self):
            return self.state.player_state(self.id_team,1).position
        @property
        def possede(self):#retourne true si la balle est plus proche d'un membre de notre equipe ou false sinon
            i=0
            j=1
            dmax=math.sqrt((GAME_WIDTH)**2+(GAME_HEIGHT)**2)
            while j<3:
                while i<4:
                    if math.sqrt((self.state.player_state(j,i).position.x-self.ball.x)**2+(self.state.player_state(j,i).position.y-self.ball.y)**2)<dmax:
                        dmax=math.sqrt((self.state.player_state(j,i).position.x-self.ball.x)**2+(self.state.player_state(j,i).position.y-self.ball.y)**2)
                        equipe=j
                    i=i+1
                j=j+1
                i=0
            if equipe==self.id_team:
                return True
            return False
        @property
        def abnorme(self):# retourne true si on est le plus proche de la balle
            i=0
            v=Vector2D(GAME_WIDTH,GAME_HEIGHT)
            while i<4:
                if (math.sqrt((self.state.player_state(self.id_team,i).position.x-self.ball.x)**2+(self.state.player_state(self.id_team,i).position.y-self.ball.y)**2)<math.sqrt(v.x**2+v.y**2)):
                    v=Vector2D(self.state.player_state(self.id_team,i).position.x-self.ball.x,self.state.player_state(self.id_team,i).position.y-self.ball.y)
                    j=i
                i=i+1
            if j==self.id_player:
                return True
            return False
        @property
        def defadv4(self):#retourne la position du defenseur adverse dans le cas d'un 4V4
            v=Vector2D(GAME_WIDTH,GAME_HEIGHT)
            s=(self.id_team%2+1)-1
            j0=math.sqrt((self.state.player_state(self.id_team%2+1,0).position.x-s*GAME_WIDTH)**2+(self.state.player_state(self.id_team%+1,0).position.y-GAME_HEIGHT/2)**2)
            j1=math.sqrt((self.state.player_state(self.id_team%2+1,1).position.x-s*GAME_WIDTH)**2+(self.state.player_state(self.id_team%+1,1).position.y-GAME_HEIGHT/2)**2)
            j2=math.sqrt((self.state.player_state(self.id_team%2+1,2).position.x-s*GAME_WIDTH)**2+(self.state.player_state(self.id_team%+1,2).position.y-GAME_HEIGHT/2)**2)
            j3=math.sqrt((self.state.player_state(self.id_team%2+1,3).position.x-s*GAME_WIDTH)**2+(self.state.player_state(self.id_team%+1,3).position.y-GAME_HEIGHT/2)**2)
            if j0<j1 and j0<j2 and j0<j3:
                if j1<j2 and j1<j3:
                    return self.state.player_state(self.id_team%2+1,1).position
                elif j2<j1 and j2<j3:
                    return self.state.player_state(self.id_team%2+1,2).position
                else:
                    return self.state.player_state(self.id_team%2+1,3).position
            elif j2<j1 and j2<j0 and j2<j3:
                if j1<j0 and j1<j3:
                    return self.state.player_state(self.id_team%2+1,1).position
                elif j0<j1 and j0<j3:
                    return self.state.player_state(self.id_team%2+1,0).position
                else:
                    return self.state.player_state(self.id_team%2+1,3).position
            elif j1<j0 and j1<j2 and j1<j3:
                if j0<j2 and j0<j3:
                    return self.state.player_state(self.id_team%2+1,0).position
                elif j2<j0 and j2<j3:
                    return self.state.player_state(self.id_team%2+1,2).position
                else:
                    return self.state.player_state(self.id_team%2+1,3).position
            else:
                if j0<j2 and j0<j1:
                    return self.state.player_state(self.id_team%2+1,0).position
                elif j2<j0 and j2<j1:
                    return self.state.player_state(self.id_team%2+1,2).position
                else:
                    return self.state.player_state(self.id_team%2+1,1).position
        #@property
        """def pgoal(self):
            if self.id_team==1:
                yb=self.ball.y
                ya=GAME_HEIGHT/2
                xb=self.ball.x
                xa=0
                
                a=(yb-ya)/(xb-xa)
                b=yb/xb*a
                print(a,b)
                #y=ax+b
                delta=(2*a*b-90*a)**2-4*(1+a)*(b**2-90*b+1961)
                x=(-(2*a*b-90*a)+math.sqrt(delta))/2*(1+a)
                if(x<0):
                    x=(-(a*b-90*a)-math.sqrt(delta))/2*(1+a)
                y=a*x+b
            else:
                yb=self.ball.y
                ya=GAME_HEIGHT/2
                xb=self.ball.x
                xa=GAME_WIDTH
                
                a=(yb-ya)/(xb-xa)
                b=yb/xb*a
                
                delta = (-300+2*a*b-90*a)-4*(1+a)*(24461+b**2+90*b)
                x=(-(-300+2*a*b-90*a))+math.sqrt(delta)/2*(1+a)
                if x>150:
                    x=(-(-300+2*a*b-90*a))-math.sqrt(delta)/2*(1+a)
                y=ax+b
                
            return Vector2D(x,y)"""
            
class Decorator():
    def __init__ ( self , state ):
            self.state = state
    def __getattr__ ( self , attr ):
            return getattr ( self . state , attr )
class Shoot ( Decorator ):
    def __init__ ( self , state ):
        self.state=state
    def shoot ( self , p ):
        dist=self.norme
        if dist<PLAYER_RADIUS+BALL_RADIUS:
            return SoccerAction ( shoot=p)
        else:
            return SoccerAction()
    def to_goal(self, strength):
        return self.shoot((self.state.goal-self.state.player).normalize()*strength)
class Passe ( Decorator ):
    def __init__ ( self , state ):
        Decorator . __init__ ( self , state )        
    #   def passe ( self , p ):
        #return SoccerAction ( Vector2D (...))
class Move(object):
    def __init__(self,state):
        self.state=state
    def move(self,acceleration=None):
        return SoccerAction(acceleration=acceleration)
    def to_ball(self):
        return self.move(self.state.ball-self.state.player)