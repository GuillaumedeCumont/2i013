#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 12:09:23 2019

@author: noe
"""

from sklearn.model_selection import ParameterGrid
def begin_match(self, team1, team2, state):
    self.last_step = 0 # Step of the last round
    self.criterion = 0 # Criterion to maximize (here, number of goals) 
    self.cpt_trials = 0 # Counter for trials
    # Set of chromosomes
    # self.param_grid = iter(ParameterGrid(self.params))
    self.cur_param = next(self.param_grid, None) # Current parameter 
    if self.cur_param is None:
        raise ValueError("no␣parameter␣given.") 
        self.res = dict() # Dictionary of results

    def end_round(self, team1, team2, state):
     # A round ends when there is a goal of if max step is achieved 
     if state.goal > 0:
         self.criterion += 1 # Increment criterions
    
    self.cpt_trials += 1  #Increment number of trials
    
    print(self.cur_param, end "    ")
    print("Crit:␣{}␣␣␣Cpt:␣{}".format(self.criterion , self.cpt_trials))
    
    if self.cpt_trials >= self.trials:
        # Save the result
    
    self.res[tuple(self.cur_param.items())] = self.criterion * 1. / self.cpt_trials
    
    # Reset parameters
    self.criterion = 0 
    self.cpt_trials = 0
    
    
    # Next parameter value
    self.cur_param = next(self.param_grid , None)
    if self.cur_param is None:
        # Update the set of chromosomes 
        # self.simu.end_match()
                      