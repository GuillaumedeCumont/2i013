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
    def anticiper_ball_position(self):
        return self.state.ball.position + 5*self.state.ball.vitesse
    
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
    def zone_allie(self):
        if(self.id_team==1):
            if((Vector2D(0,GAME_HEIGHT/2.) - self.state.ball.position).norm < (Vector2D(GAME_WIDTH,GAME_HEIGHT/2.) - self.state.ball.position).norm):
                return True
            else:
                return False
        if(self.id_team==2):
            if((Vector2D(0,GAME_HEIGHT/2.) - self.state.ball.position).norm > (Vector2D(GAME_WIDTH,GAME_HEIGHT/2.) - self.state.ball.position).norm):
                return True
            else:
                return False
    
    @property
    def zone_ennemi(self):
        """A TESTER"""
        return not(self.zone_allie) 
    
    @property
    def allie_1(self):
        if(self.id_team == 1):
            if(self.state.player_state(self.id_team, self.id_player).position.x < GAME_WIDTH/4):
                return True
        if(self.id_team == 2):
            if(self.state.player_state(self.id_team, self.id_player).position.x > 3*GAME_WIDTH/4):
                return True
        return False
    
    @property
    def ennemi_1(self):
        if(self.id_team == 2):
            if(self.state.player_state(self.id_team, self.id_player).position.x < GAME_WIDTH/4):
                return True
        if(self.id_team == 1):
            if(self.state.player_state(self.id_team, self.id_player).position.x > 3*GAME_WIDTH/4):
                return True
        return False 
    
    @property
    def allie_2(self):
        if(self.zone_allie and self.allie_1):
            return False
        if(self.zone_allie):
            return True
        return False
    
    @property
    def ennemi_2(self):
        if(self.zone_allie):
            return False
        if(self.zone_ennemi_1):
            return False
        return True
    
    @property
    def but_allie(self):
        if(self.id_team == 1):
            position_but = Vector2D(0,GAME_HEIGHT/2.)
        elif(self.id_team == 2):
            position_but = Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
        return position_but
    
    @property
    def but_ennemi(self):
        if(self.id_team == 2):
            position_but = Vector2D(0,GAME_HEIGHT/2.)
        elif(self.id_team == 1):
            position_but = Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
        return position_but        
    
    @property
    def distance_but_ennemi(self):
        """distance du but
            utile pour augmenter sa puissance si proche du but"""
        return (self.but-self.player).norm
    
    def aller_vers(self, Vecteur):
        if((Vecteur - self.player).norm < PLAYER_RADIUS):
            return None
        return (Vecteur - self.player).normalize()
    
    @property
    def aller_vers_ballon(self):
        return self.aller_vers(self.ball)
    
    @property
    def aller_vers_anticiper_ballon(self):
        return self.aller_vers(self.state.ball.position + 5*self.state.ball.vitesse)
    
    @property
    def aller_vers_but_allie(self):
        return self.aller_vers(self.but_allie)
    @property
    def aller_vers_but_ennemi(self):
        return self.aller_vers(self.but_ennemi)
    
    @property
    def tire_au_but_si_peut_tirer(self):
        """Tire uniquement si il est à coté du ballon"""
        vecteur_shoot = None
        if((self.player - self.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.but-self.ball).normalize())
        return vecteur_shoot
    
    @property
    def tire_au_but_si_peut_tirer_violent(self):
        """Tire fort uniquement si il est a côté du ballon"""
        vecteur_shoot = None
        if((self.player - self.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.but-self.ball).normalize())*1000
        return vecteur_shoot
    
    @property
    def passe_joueur_allier_forte(self):
        """Tire fort uniquement si il est a côté du ballon a son allier"""
        vecteur_shoot = None
        if((self.player - self.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.position_joueur_allier_le_plus_proche-self.ball).normalize())*1000
        return vecteur_shoot
    
    @property
    def passe_joueur_allier_faible(self):
        """Tire fort uniquement si il est a côté du ballon a son allier"""
        vecteur_shoot = None
        if((self.player - self.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.position_joueur_allier_le_plus_proche-self.ball).normalize())
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
    def position_joueur_allier_le_plus_proche(self):
        minimum = (self.player-self.liste_des_positions_joueurs_equipe_allie[0]).norm
        position = self.liste_des_positions_joueurs_equipe_allie[0]
        for i in self.liste_des_positions_joueurs_equipe_allie:
            if((self.player-i).norm < minimum):
                minimum = (self.player-i).norm
                position = i
        return position 
    
    @property
    def tout_le_monde_est_sur_le_ballon(self):
        if((self.player - self.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if((self.joueur_ennemi_le_plus_proche - self.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                return True
        return False
    
    @property
    def allier_plus_proche_du_ballon(self):
        minimum = self.ball - self.liste_des_positions_joueurs_equipe_allie[0]
        for position in self.liste_des_positions_joueurs_equipe_allie:
            if((self.liste_des_positions_joueurs_equipe_allie[position]).norm<minimum.norm):
                minimum = self.ball - self.liste_des_positions_joueurs_equipe_allie[position]
        return minimum
        
    @property
    def allier_plus_proche_du_ballon_y_va(self):
        return self.aller_vers_anticiper_ballon
        
        
        
        
        
        
    
    