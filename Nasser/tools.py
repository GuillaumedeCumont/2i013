from soccersimulator import Ball, settings, Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator.settings  import GAME_WIDTH, GAME_HEIGHT, PLAYER_RADIUS,BALL_RADIUS
import math


class SuperState (object):
    def __init__ (self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        
    def __getattr__ (self , attr):
        return getattr (self.state , attr)
        
    @property
    def ball(self):
        return self.state.ball.position
    
    @property
    def player(self):
        return self.state.player_state (self.id_team, self.id_player).position
    
    @property
    def goal(self):
        if(self.id_team == 2):
            return Vector2D(0,GAME_HEIGHT/2)
        else :
            return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        
    @property
    def angle(self):
        return math.atan2(self.y, self.x)
    
    @property
    def listeop(self):
        return [self.state.player_state(id_team, id_player).position for (id_team , id_player) in self.state.players if id_team != self.id_team]
    
    @property
    def near(self):
        opponent = self.listeop
        return min([(self.player.distance (player), player) for player in opponent])[1]
        
    @property 
    def ballameliorer(self):
        return self.state.ball.position + 5 * self.state.ball.vitesse
    
    @property
    def teamdef(self):
        if self.id_team == 1 :
            (posdef,condition) = (1/4, self.ballameliorer.x > GAME_WIDTH*(1/3))
        else : 
            (posdef, condition) = (3/4, self.ballameliorer.x < GAME_WIDTH*(2/3))
        return (posdef,condition)
        
    @property
    def teammil(self):
        if self.id_team == 1 :
            return self.ball.x <= GAME_WIDTH*(1/2) 
        else : 
            return self.ball.x >= GAME_WIDTH*(1/2) 
        
    @property
    def teamatt(self):
        if self.id_team == 1 :
            (posattx,nextpos,defe) = (self.player.x < GAME_WIDTH*(1/2), GAME_WIDTH*(3/5),self.ballameliorer.x < GAME_WIDTH*(1/4))
        else : 
            (posattx,nextpos,defe) = (self.player.x > GAME_WIDTH*(1/2), GAME_WIDTH*(2/5),self.ballameliorer.x > GAME_WIDTH*(3/4))
        return (posattx,nextpos,defe)
    @property
    def teamatt2(self):
        if self.id_team == 1 :
            (un,deux)=(self.ball.x >= GAME_WIDTH*(2/3), GAME_WIDTH*(2/3))
        else : 
            (un,deux)=(self.ball.x <= GAME_WIDTH*(1/3),GAME_WIDTH*(1/3))
        return  (un,deux)
    
    @property
    def v4v4(self):
        if self.id_team == 1 :
            (def3, def4, att3, att4) = (self.ball.y <= GAME_HEIGHT*(1/2), self.ball.y >= GAME_HEIGHT*(1/2), self.ball.y <= GAME_HEIGHT*(1/2), self.ball.y >= GAME_HEIGHT*(1/2))
        else : 
            (def3, def4, att3, att4) = (self.ball.y <= GAME_HEIGHT*(1/2), self.ball.y >= GAME_HEIGHT*(1/2), self.ball.y <= GAME_HEIGHT*(1/2), self.ball.y >= GAME_HEIGHT*(1/2))
        return (def3, def4, att3, att4)
        
    @property
    def coequipier(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player): 
                return self.state.player_state(id_team, id_player).position
            
    @property 
    def oneatt(self): 
        if self.id_team == 1 :
            return (self.near.x < self.player.x)
        else : 
            return (self.near.x > self.player.x)
    
    @property 
    def devant(self):
        if(self.goal.distance(self.player) < self.goal.distance(self.near)):
            return True 
        else : 
            return False
         
    @property 
    def bouge(self) : 
        if self.goal.distance(self.near)<20:
            return False 
        else : 
            return True
    
    @property
    def coequipier0(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and (id_player == 0): 
                return self.state.player_state(id_team, id_player).position
            
    @property
    def coequipier1(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and (id_player == 1): 
                return self.state.player_state(id_team, id_player).position
        
    @property
    def coequipier22(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and (id_player == 2): 
                return self.state.player_state(id_team, id_player).position
        
    @property
    def coequipier2(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and ((id_player == 1) or (id_player == 2)): 
                return self.state.player_state(id_team, id_player).position
            
  
    
    @property
    def coequipier3(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and (id_player == 3): 
                return self.state.player_state(id_team, id_player).position
    
    @property
    def coequipieratt(self):   
        for (id_team, id_player) in self.state.players :
            if (id_team == self.id_team) and (id_player != self.id_player) and ((id_player == 2) or (id_player == 3)):
                return self.state.player_state(id_team, id_player).position
            
    @property 
    def distancemil(self):
        if self.ball.distance(self.player) > self.ball.distance(self.coequipier2) :
            return True 
        else :
            return False 
            
    @property
    def devantmil(self):
        if self.goal.distance(self.player) > self.goal.distance(self.coequipier2) :
            return True
        else:
            return False
    
    @property
    def devantatt(self):
        if self.goal.distance(self.player) < self.goal.distance(self.coequipieratt) :
            return True
        else:
            return False
     
    @property   
    def milieuproche(self):
        if self.player.distance(self.coequipier1) < self.player.distance(self.coequipier22):
            return self.coequipier1
        else:
            return self.coequipier22
    
      
    @property   
    def milieuloin(self):
        if self.player.distance(self.coequipier1) < self.player.distance(self.coequipier22):
            return self.coequipier22
        else:
            return self.coequipier1
           
        


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