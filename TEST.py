#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 18:47:15 2019

@author: 3535014
"""

import P_S_G
from soccersimulator import Simulation, show_simu
from P_S_G import get_team, get_team1

team1 = get_team(2)
team2 = get_team1(2)
    
simu = Simulation(team1, team2)
show_simu(simu)