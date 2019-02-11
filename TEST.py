#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 17:36:06 2019

@author: 3535014
"""

import module
from module import GoStrategy, Strategy_Attaque, Strategy_Defense

from soccersimulator import SoccerTeam

def get_team(nb_players):
    team = SoccerTeam(name="Guillaume's Team")
    if nb_players == 1:
        team.add("Attaquant", module.Strategy_Attaque_Solo())
    if nb_players == 2:
        team.add("Attaquant", module.Strategy_Attaque())
        team.add("Defenseur", module.Strategy_Attaque())
    return team

if __name__ == '__main__':
    from soccersimulator import Simulation, show_simu
    team1 = get_team(2)
    team2 = get_team(2)

    
    
    simu = Simulation(team1,team2)
    show_simu(simu)