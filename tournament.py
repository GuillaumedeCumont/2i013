# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import module
from module import GoStrategy, Strategy_Attaque

from soccersimulator import SoccerTeam

def get_team(nb_players):
    team = SoccerTeam(name="Guillaume's Team")
    if nb_players == 1:
        team.add("Attaquant", module.Strategy_Attaque())
    if nb_players == 2:
        team.add("Attaquant", module.Strategy_Attaque())
        team.add("Defenseur", module.Strategy_Attaque())
    return team

if __name__ == '__main__':
    from soccersimulator import Simulation, show_simu
    team1 = get_team(1)
    team2 = get_team(1)
    
    simu = Simulation(team1,team2)
    show_simu(simu)
