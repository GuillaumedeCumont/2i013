#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:06:38 2019

@author: root
"""

from soccersimulator import QLearning, RandomPos, QStrategy
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH
from soccersimulator import Vector2D, Strategy, SoccerAction

#Strategy
QTestStrategy = QStrategy()
QTestStrategy.add('right', SimpleStrategy(shoot_right, ''))
QTestStrategy.add('left', SimpleStrategy(shoot_right, ''))
QTestStrategy.add('up', SimpleStrategy(shoot_right, ''))
QTestStrategy.add('down', SimpleStrategy(shoot_right, ''))
#Learning
expe = QLearning(strategy=QTestStrategy, monte_carlo=False)
expe.start(fps=1500)

with open('qstrategy.pkl', 'wb') as fo:
    QTestStrategy.qtable = expe.qtable
    pkl.dump(QTestStrategy, fo)

#Test
with open('qstrategy.pkl.351', 'rb') as fi:
    QStrategy = pkl.load(fi)
    #Simulate and display the match
    simu = RandomPos(QStrategy)
    simu.start()











def begin_match(self, team1, team2, state):
    self.last_step = 0 #Step of the last round
    self.qtable = dict() #qtable

def begin_round(self, team1, team2, state):
    ball = Vector2D.create_random(low=0, high=1)
    ball.x *= GAME_WIDTH
    ball.y *= GAME_HEIGHT
    
    #player and ball position(random)
    self.simu.state.states[(1,0)].position = ball.copy() #player position
    self.simu.state.states[(1,0)].vitesse = Vector2D() #player acceleration
    self.simu.state.ball.position = ball.copy() #ball position
    
    #last step of the game
    self.last_step = self.simu.step
    self.last_state = None
    self.last_score = self.simu.score[1] #score of team 1
    self.cur_state = self.strategy.get_state(state, id_team=1, id_player=0)
    self.rewards = []

def update_round(self, team1, team2, state):
    #Q learning update 
    self.qupdate(state)
    
    if state.step > self.last_step + self.max_round_step:
        #Change action when state doesn't change
        if self.cur_state == self.last_state:
            self.strategy.strategy = self.next_action(self.cur_state)
    self.last_state = self.cur_state
    
def qupdate(self, state):
    qstate_next = self.strategy.get_state(state, id_team=1, id_player=0)
    if self.cur_state != qstate_next:
        qaction = self.strategy.strategy #strategy name
        key = (self.cur_state, qaction)
        
        #Future Q value
        qvalues_next = [q for k, q in self.qtable.items() if k[0] == qstate_next]
        qnext=max(qvalues_next, default=0)
        
        #Reinforcement
        score = state.score[1]
        if score > self.last_score:
            self.last_score = score
            r = 0
        else:
            r = -1 if state.goal==0 else -10
        qvalue = r+0.9 * qnext
        
        # Update Q table
        self.rewards.append((key, r))
        if not self.monte_carlo:
            if key in self.qtable:
                self.qtable[key] = 0.5 * self.qtable[key] + 0.5 * qvalue
            else:
                self.qtable[key] = qvalue
        
        #Change action
        self.strategy.strategy = self.next_action(qstate_next)
        #Update current state
        self.cur_state = qstate_next
        

def next_action(self, qstate_next):
    minq = min([q for key, q in self.qtable.items() if key[0] == qstate_next], default=0)
    minq = min(minq, 0)
    
    prob = [0.1 if (qstate_next, name) not in self.qtable else self.qtable[(qstate_next, name)] - minq + 0.1 for name in self.strategy.strategy_names]
    prob = np.asarray(prob)
    if prob.sum() < 1e-15:
        prob = None
    else:
        prob /= prob.sum()
    
    return choice(list(self.strategy.strategy_names), p=prob)
