#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:14:14 2019

@author: 3535014
"""

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
        team.add("Pavaaaaard", P_S_G.Strategy_Attaque())
        team.add("Defenseur", P_S_G.Strategy_Attaque())
    return team