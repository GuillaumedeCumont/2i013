"""
Created on Mon Mar 25 16:06:38 2019

@author: root
"""

from soccersimulator import QLearning, RandomPos
from soccersimulator import GAME_HEIGHT, GAME_WIDTH
from soccersimulator import Vector2D, Strategy, SoccerAction
from .Tools import *


class QStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Q-Learning")
        self.strategies = dict()
        self.current_strategy = None
        self.qtable = None
        
    def add(self, name, strategy):
        self.strategies[name] = strategy
        if not self.current_strategy:
            self.current_strategy = name
            
            
    def get_state(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        x = int(s.player.x / GAME_WIDTH *3)
        y = int(s.player.y / GAME_HEIGHT *5)
        return x,y, state.goal>0
    
    def compute_strategy(self, state, id_team, id_player):
        if self.qtable is None:
            strat = self.strategies[self.current_strategy]
            return strat.compute_strategy(state, id_team, id_player)
        else:
            qstate = self.get_state(state, id_team, id_player)
            strategy = max([(q, key[1]) for key, q in self.qtable.items() if key[0]==qstate], default=(None, None))[1]
            if strategy is not None:
                strat = self.strategies[strategy]
                return strat.compute_strategy(state, id_team, id_player)
            else:
                return SoccerAction()
            
    @property
    def strategy_names(self):
        return self.strategies.keys()
    @property
    def strategy(self):
        return self.current_strategy
    @strategy.setter
    def strategy(self, name):
        self.current_strategy=name













