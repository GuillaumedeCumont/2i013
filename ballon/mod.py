#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 19:06:37 2019

@author: 3670841
"""

strat:
    
    
    #attaquant 4v4 v2        
class attaquant1(Strategy):
     def __init__(self):
        Strategy.__init__(self, "Attaquant")
        
     def compute_strategy(self, state, id_team, id_player):
        s=SuperState(state,id_team,id_player)
        i=s.goal.x
        if id_team==1:
            if s.milieu:
                return SoccerAction((s.ball-s.player),(Vector2D(s.posxatk+30,s.posyatk)-s.player).normalize()*2)
            elif s.ball.x<GAME_WIDTH/2:
                return SoccerAction(Vector2D(s.unedeux.x+20,GAME_HEIGHT/4)-s.player,Vector2D())
            elif s.possede:
                if s.abnorme :
                    if s.cannot:
                        return SoccerAction((s.ball-s.player),Vector2D())
                    elif s.gnorme<30 and s.player.y>20 and s.player.y<70:
                        return SoccerAction((s.ball-s.player),(Vector2D(i,GAME_HEIGHT/2)-s.player).normalize()*4)
                    else:
                        return SoccerAction((s.ball-s.player),(Vector2D(s.unedeux.x+15,s.unedeux.y)-s.player))
                else:
                    return SoccerAction(Vector2D(s.unedeux.x+10,GAME_HEIGHT/4)-s.player,Vector2D())
            else:
                if s.abnorme:
                    if s.cannot:
                        return SoccerAction((s.ball-s.player),Vector2D())
                    elif s.gnorme<30 and s.player.y>20 and s.player.y<70:
                        return SoccerAction((s.ball-s.player),(Vector2D(i,GAME_HEIGHT/2)-s.player).normalize()*4)
                    else:
                        return SoccerAction((s.ball-s.player),(Vector2D(s.unedeux.x+15,s.unedeux.y)-s.player))
                    
    




#attanquant 4v4 v2 bis
class attaquant2(Strategy):
     def __init__(self):
        Strategy.__init__(self, "Attaquant")
        
     def compute_strategy(self, state, id_team, id_player):
        s=SuperState(state,id_team,id_player)
        i=s.goal.x
        if id_team==1:
            if s.milieu:
                return SoccerAction((Vector2D(GAME_WIDTH/2+20,3*GAME_HEIGHT/4)-s.player),Vector2D())
            elif s.ball.x<GAME_WIDTH/2:
                    return SoccerAction(Vector2D(s.ball.x+30,3*GAME_HEIGHT/4)-s.player,Vector2D())
            elif s.possede: 
                if s.abnorme :
                    if s.cannot:
                        return SoccerAction((s.ball-s.player),Vector2D())
                    elif s.gnorme<30 and (s.player.y>20 or s.player.y<70):
                        return SoccerAction((s.ball-s.player),(Vector2D(i,GAME_HEIGHT/2)-s.player).normalize()*4)
                    else:
                        return SoccerAction((s.ball-s.player),(Vector2D(s.unedeux.x+15,s.unedeux.y)-s.player))                
                else:
                    return SoccerAction(Vector2D(s.unedeux.x-10,3*GAME_HEIGHT/4)-s.player,Vector2D())
            else:
                if s.abnorme:
                    if s.cannot:
                        return SoccerAction((s.ball-s.player),Vector2D())
                    elif s.gnorme<30 and (s.player.y>20 or s.player.y<70):
                        return SoccerAction((s.ball-s.player),(Vector2D(i,GAME_HEIGHT/2)-s.player).normalize()*4)
                    else:
                        return SoccerAction((s.ball-s.player),(Vector2D(s.unedeux.x+15,s.unedeux.y)-s.player)) 
                else:
                    return SoccerAction(Vector2D(GAME_WIDTH/2,3*GAME_HEIGHT/4)-s.player,Vector2D())

    
    
tools :
    
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