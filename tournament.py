# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 16:14:40 2019

@author: root
"""

import P_S_G, Nasser, ballon, BarbesFC
from soccersimulator import Simulation, show_simu, SoccerTournament
from P_S_G import get_team, get_team1

team1 = Nasser.get_team(4)
team2 = BarbesFC.get_team(4)
team3 = ballon.get_team(4)
#simu = Simulation(team2, team1)
#simu = Simulation(team1, team2)


match = Simulation(team1, team2, 2000)
show_simu(match)
