#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 18:47:15 2019

@author: 3535014
"""

from P_S_G.Strategy_4_joueurs import Attaquant_4_joueurs
from P_S_G.GoalSearch import *

expe = GoalSearch(strategy = Attaquant_4_joueurs(), params={"strength": [15]})
expe.start()
print(expe.get_res())
print(expe.get_best())