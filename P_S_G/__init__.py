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

def get_team(nb_players):
    team = SoccerTeam(name="pSG")
    if nb_players == 1:
        team.add("Benjamin Pavard", P_S_G.Strategy_Attaque_Solo())
    if nb_players == 2:
        team.add("Pavardoff", P_S_G.Strategy_Attaque())
        team.add("def", P_S_G.Strategy_Attaque())
    return team

def get_team1(nb_players):
    team = SoccerTeam(name="pSG")
    if nb_players == 1:
        team.add("Benjamin Pavard", P_S_G.Strategy_Attaque_Solo())
    if nb_players == 2:
        team.add("Pavarddef", P_S_G.Strategy_Defense())
        team.add("Mbappé", P_S_G.Strategy_Defense())
    return team