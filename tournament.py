# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 16:14:40 2019

@author: root
"""

import P_S_G
from soccersimulator import Simulation, show_simu
from P_S_G import get_team, get_team1

team1 = get_team(4)
team2 = get_team(4)

simu = Simulation(team1, team2)
show_simu(simu)