#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 19:49:22 2019

@author: noe
"""

from .tools import *
from .actions import *
from .strategies import *
from .jouer import *
from .GoalSearch import *
from .QStrategy import *
from .QLearning import *
from .AttaquegaucheQ import *
from .AttaquedroiteQ import *
from .CampgaucheQ import *
from .CampdroiteQ import *
from .DefenseQ import *
from .OtherStratNasser import *
import pickle as pkl

def get_team(nb_players, name = "Barbès Football Club"):
    
    if name == "Barbès Football Club" :
        team = SoccerTeam(name="Barbès Football Club")
        if nb_players == 1:
            team.add("Attaquant", Attaquantsolo())
        if nb_players == 2:
            team.add("Gardien"  , Gardien()  )
            team.add("Attaquant", Attaquantduo())
        
        if nb_players == 3:
            team.add("Gardien"  , Gardien()  )
            team.add("Attaquantdroit", Attaquantdroit())
            team.add("Attaquantgauche", Attaquantgauche())
            
            
        if nb_players == 4:
            team.add("Gardien"  , Gardien4()  )
            team.add("Attaquantdroit", Ad())
            team.add("Attaquantgauche",Ag())
            #team.add("Attaquantgauche", QStrategy()) #Essai du QLearning
            team.add("Défenseur", Defenseur())
            return team
    
    else:
        
        team = SoccerTeam(name = "Nasser’s Team")
        if (nb_players == 1):
            team.add("One",SimpleStrategy(one,'One'))
        if (nb_players == 2):
            team.add("Attaquant",SimpleStrategy(attaquant2,'Att'))
            team.add("Défenseur",SimpleStrategy(defenseur2,'Def'))
        if (nb_players == 4): 
            team.add("Nasser0",SimpleStrategy(defenseur5,'Def5'))
            team.add("Nasser1",SimpleStrategy(milieu1,'m1'))
            team.add("Nasser2",SimpleStrategy(milieu2,'m2'))
            team.add("Nasser3",SimpleStrategy(attaquant5,'Att5'))
        return team
        
    
    
