#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:43:02 2019

@author: root
"""
import random
import math
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH, GAME_GOAL_HEIGHT


class SuperState(object):
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        
    def __getattr__(self, attr):
        return getattr(self.state, attr)
    
    """Tout ce qui est relatif a la position"""
    
    @property
    def ball(self):
        return self.state.ball.position

    @property
    def anticiper_ball_position(self):
        return self.state.ball.position + 5*self.state.ball.vitesse
    
    """
    @property
    def anticiper_ball_positionv2(self, distance):
    """
    
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position

    @property
    def but(self):
        if(self.id_team == 2):
            position_but = Vector2D(0,(GAME_HEIGHT/2.)+random.randint(-GAME_GOAL_HEIGHT/2,GAME_GOAL_HEIGHT/2))
        elif(self.id_team == 1):
            position_but = Vector2D(GAME_WIDTH,(GAME_HEIGHT/2.)+random.randint(-GAME_GOAL_HEIGHT/2,GAME_GOAL_HEIGHT/2))
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
    def zone_attaque(self):
        if self.allie_2 or self.zone_ennemi:
            return True
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
    def reste(self):
        if(self.id_team == 2):
            positiondef = Vector2D(140.0, self.anticiper_ball_position.y)
        else:
            positiondef = Vector2D(20.0, self.anticiper_ball_position.y)
        return positiondef
            
    @property
    def but_allie(self):
        if(self.id_team == 1):
            position_but = Vector2D(10,GAME_HEIGHT/2.)
        elif(self.id_team == 2):
            position_but = Vector2D(GAME_WIDTH-10,GAME_HEIGHT/2.)
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
            if((self.player-i).norm > minimum):
                minimum = (self.player-i).norm
                position = i
        return position
        
    @property
    def distance_entre_joueur_allier_proche(self):
        """renvoie la distance entre self joueur et son ami le plus proche"""
        return self.player.distance(self.position_joueur_allier_le_plus_proche)
    
    @property
    def distance_entre_joueur_ennemi_proche(self):
        """renvoie la distance entre self joueur et son ami le plus proche"""
        return self.player.distance(self.joueur_ennemi_le_plus_proche)
    
    @property
    def tout_le_monde_est_sur_le_ballon(self):
        if((self.player - self.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if((self.joueur_ennemi_le_plus_proche - self.ball).norm < 3*(PLAYER_RADIUS + BALL_RADIUS)):
                return True
        return False
    
    @property
    def impasse(self):
        if self.distance_entre_joueur_ennemi_proche<5:
            return True
        return False
    
    @property
    def allier_plus_proche_du_ballon(self):
        minimum = self.ball - self.liste_des_positions_joueurs_equipe_allie[0]
        for position in self.liste_des_positions_joueurs_equipe_allie:
            if((self.liste_des_positions_joueurs_equipe_allie[position]).norm<minimum.norm):
                minimum = self.ball - self.liste_des_positions_joueurs_equipe_allie[position]
        return minimum
    
        
    """
    @property
    def liste_opposants(self):
        return [self.state.player_state(id_team, id_player).position for (id_team,id_player) in self.state.players if id_team != self.id_team]
    @property
    def opposant_plus_proche(self):
        return [min(self.player.distance(player), player) for player in self.liste_opposants]
    """
    
    @property
    def g_le_ballon(self):
        """return bool"""
        if((self.player -self.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            return True
        return False
    
    @property
    def si_ballon_proche_zone_def(self):
        if((self.player - self.ball).norm <35):
            return True
        return False
    
    @property
    def champ_libre(self):
        if self.g_le_ballon:
            for i in self.liste_des_positions_joueurs_ennemis:
                if self.but_ennemi.distance(self.player) < self.but_ennemi.distance(i):
                    return True
        return False
    
    
    """pour ma fonction degagement"""
    def angle_de_degagement(self, Vecteur_1, Vecteur_2):
        return math.acos((Vecteur_1.dot(Vecteur_2))/(Vecteur_1.norm*Vecteur_2.norm))*(180/math.pi)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    