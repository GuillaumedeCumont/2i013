#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:14:14 2019

@author: 3535014
"""

from P_S_G import Strategy_Attaque, Strategy_Defense

from .MyStrategy import *
from .Strategy_Attaque import *
from .Strategy_Defense import *
from .Tools import *
from .Actions import *


import P_S_G
from soccersimulator import SoccerTeam

def get_team1(nb_players):
    team = SoccerTeam(name="pSG")
    if nb_players == 1:
        team.add("defenseur/attaquant", P_S_G.Nouvelle_Strategie_Solo())
    if nb_players == 2:
        team.add("Attaquant", P_S_G.Strategy_Attaque_Solo())
        team.add("Defenseur+attaquesurprise", P_S_G.Defenseur())
    if nb_players == 4:
        team.add("Goal", P_S_G.Defenseur())
        team.add("Attaquant", P_S_G.Strategy_Attaque_Solo())
        team.add("Defenseurs", P_S_G.Strategy_Defense())
        team.add("Defenseurs", P_S_G.Strategy_Defense())        
    return team

def get_team(nb_players):
    team = SoccerTeam(name="pSG")
    if nb_players == 1:
        team.add("Attaquant", P_S_G.Strategy_Attaque_Solo())
    if nb_players == 2:
        team.add("Goal", P_S_G.Strategy_GardienStock())
        team.add("Milieu", P_S_G.Strategy_AttaquantStock())
    return team