# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import P_S_G
from soccersimulator import Simulation, show_simu
from P_S_G import get_team, get_team1

team1 = get_team1(4)
team2 = get_team(4)

simu = Simulation(team1, team2)
show_simu(simu)