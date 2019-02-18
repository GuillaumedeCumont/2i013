# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import P_S_G
from P_S_G import GoStrategy, Strategy_Attaque, Strategy_Defense
from soccersimulator import Simulation, show_simu
from P_S_G import get_team

team1 = get_team(1)
team2 = get_team(1)
    
simu = Simulation(team1, team2)
show_simu(simu)