#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:43:02 2019

@author: root
"""

from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH


class SuperState(object):
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        
    @property
    def ball(self):
        return self.state.ball.position
    
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position

    @property
    def but(self):
        if(self.id_team == 2):
            position_but = Vector2D(0,GAME_HEIGHT/2.)
        elif(self.id_team == 1):
            position_but = Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
        return position_but
    
    @property
    def but_allie(self):
        if(self.id_team == 1):
            position_but = Vector2D(0,GAME_HEIGHT/2.)
        elif(self.id_team == 2):
            position_but = Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
        return position_but

    def aller_vers(self, Vecteur):
        return (Vecteur - self.player).normalize()
    
    @property
    def aller_vers_ballon(self):
        return self.aller_vers(self.ball)
    
    @property
    def aller_vers_but_allie(self):
        return self.aller_vers(self.but_allie)
    
    @property
    def tire_au_but_si_peut_tirer(self):
        vecteur_shoot = None
        if((self.player - self.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.but-self.ball).normalize())
        return vecteur_shoot
    
    @property
    def liste_joueur(self):
        return self.state.players
    
    @property
    def liste_joueur_equipe_allie(self):
        """retourne liste[tuple(equipe,joueur)]"""
        L = list()
        cpt = 0
        if(self.id_team == 1):
            for i in self.liste_joueur:
                a,b = i
                if (a == 1):
                    L.append(self.liste_joueur[cpt])
                cpt+=1
        if(self.id_team == 2):
            for i in self.liste_joueur:
                a,b = i
                if(a == 2):
                    L.append(self.liste_joueur[cpt])
                cpt+=1
        return L      
    
    @property
    def liste_joueur_ennemis(self):
        """retourne liste[tuple(equipe,joueur)]"""
        L = list()
        cpt = 0
        if(self.id_team == 1):
            for i in self.liste_joueur:
                a,b = i
                if (a == 2):
                    L.append(self.liste_joueur[cpt])
                cpt+=1
        if(self.id_team == 2):
            for i in self.liste_joueur:
                a,b = i
                if(a == 1):
                    L.append(self.liste_joueur[cpt])
                cpt+=1
        return L
    
    @property
    def liste_des_positions_joueurs_equipe_allie(self):
        L = list()
        for i in self.liste_joueur_equipe_allie:
            numero_equipe,numero_joueur = i
            L.append((self.state.player_state(numero_equipe, numero_joueur)).position)
        return L       
    
    @property
    def liste_des_positions_joueurs_ennemis(self):
        L = list()
        for i in self.liste_joueur_ennemis:
            numero_equipe,numero_joueur = i
            L.append((self.state.player_state(numero_equipe, numero_joueur)).position)
        return L
    
    @property
    def joueur_ennemi_le_plus_proche(self):
        minimum = (self.player-self.liste_des_positions_joueurs_ennemis[0]).norm
        position = self.liste_des_positions_joueurs_ennemis[0]
        for i in self.liste_des_positions_joueurs_ennemis:
            if((self.player-i).norm < minimum):
                minimum = (self.player-i).norm
                position = i
        return position
    
    
    @property
    
    
