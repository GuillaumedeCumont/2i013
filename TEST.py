#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 18:47:15 2019

@author: 3535014
"""

from P_S_G.Strategy_4_joueurs import Strategy_4_joueurs_attaquant
from P_S_G.GoalSearch import *

expe = GoalSearch(strategy = Strategy_4_joueurs_attaquant(), params={"strength": [2,3,5,8]})
expe.start()
print(expe.get_res())
print(expe.get_best())



