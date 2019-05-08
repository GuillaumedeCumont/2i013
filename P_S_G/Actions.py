#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 11:02:09 2019

@author: 3535014
"""
import math
from .Tools import *
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH, GAME_GOAL_HEIGHT, maxPlayerAcceleration, maxPlayerShoot
from random import randint

class Move(object):
    def __init__(self, superstate):
        self.superstate = superstate
    def move(self, acceleration=None):
        return SoccerAction(acceleration = acceleration)
    
    def aller_vers(self, Vecteur):
        if((Vecteur - self.superstate.player).norm < PLAYER_RADIUS):
            return None
        return (Vecteur - self.superstate.player).normalize()*maxPlayerAcceleration

    @property
    def aller_vers_ballon(self):
        return self.aller_vers(self.superstate.ball)
    
    @property
    def aller_vers_anticiper_ballon(self):
        return (self.aller_vers(self.superstate.state.ball.position + 5*self.superstate.state.ball.vitesse))
    
    @property
    def aller_vers_but_allie(self):
        return self.aller_vers(self.superstate.but_allie)
    @property
    def aller_vers_but_ennemi(self):
        return self.aller_vers(self.superstate.but_ennemi).normalize()*maxPlayerAcceleration
    @property
    def aller_milieu(self):
        return (self.aller_vers_but_allie+self.aller_vers_but_ennemi)/2
    @property
    def allier_plus_proche_du_ballon_y_va(self):
        return self.aller_vers_anticiper_ballon
    @property
    def allerdef(self):
        return self.aller_vers(self.superstate.reste)
    @property
    def allermillieuzoneAretranche(self):
        return self.aller_vers(self.superstate.position_milieu_zone_Aretranche)
    @property
    def allermillieuzoneBretranche(self):
        return self.aller_vers(self.superstate.position_milieu_zone_Bretranche)
    @property
    def allerattaquantzoneCdepart(self):
        return self.aller_vers(self.superstate.position_attaquant_zone_C_depart)
    @property
    def allergoalzonegoaldepart(self):
        return self.aller_vers(self.superstate.position_goal_depart)
    
    @property
    def aller_vers_joueurennemiplusproche(self):
        return self.aller_vers(self.superstate.joueur_ennemi_le_plus_proche)
    
    """
    def __getattr__(self, name):
        return getattr(self.MyState, name)
    """
    
class Shoot(object):
    def __init__(self, superstate):
        self.superstate = superstate
    
    @property
    def tire_au_but_precision_chirurgicale_attaquant(self):
        #modifier en fonction de la distance
        #en fonction des positions joueurennemis
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.superstate.but-self.superstate.ball).normalize()*1.5)
        return vecteur_shoot
    
    @property
    def tire_au_but_si_peut_tirer(self):
        """Tire uniquement si il est à coté du ballon"""
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.superstate.but-self.superstate.ball).normalize()*1.5)
        return vecteur_shoot
    
    @property
    def tire_au_but_si_peut_tirer_doucement(self):
        """Tire uniquement si il est à coté du ballon"""
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.superstate.but-self.superstate.ball).normalize()*4.5)
        return vecteur_shoot    
    
    @property
    def tire_au_but_si_peut_tirer_2(self, strength):
        return self.tire_au_but_si_peut_tirer*strength
    
    @property
    def tire_au_but_si_peut_tirer_violent(self):
        """Tire fort uniquement si il est a côté du ballon"""
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.superstate.but-self.superstate.ball).normalize())*maxPlayerShoot
        return vecteur_shoot
    
    @property
    def passe_joueur_allier_forte(self):
        """Tire fort uniquement si il est a côté du ballon a son allier"""
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.superstate.position_joueur_allier_le_plus_proche-self.superstate.ball).normalize())*100
        return vecteur_shoot
    
    @property
    def passe_joueur_allier_faible(self):
        """Tire fort uniquement si il est a côté du ballon a son allier"""
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = ((self.superstate.position_joueur_allier_le_plus_proche-self.superstate.ball).normalize())
        return vecteur_shoot
    """
    def __getattr__(self, name):
        return getattr(self.MyState, name)
    """
    @property
    def degagement(self):
        vecteur_shoot = None
        if ((self.superstate.angle_de_degagement(self.superstate.but_ennemi-self.superstate.player,self.superstate.but_ennemi-self.superstate.joueur_ennemi_le_plus_proche) < 1.0) and (self.superstate.angle_de_degagement(self.superstate.but_ennemi-self.superstate.player,self.superstate.but_ennemi-self.superstate.joueur_ennemi_le_plus_proche) > 0)):
            if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = Vector2D(self.superstate.joueur_ennemi_le_plus_proche.x, self.superstate.joueur_ennemi_le_plus_proche.y-25)
        elif ((self.superstate.angle_de_degagement(self.superstate.but_ennemi-self.superstate.player,self.superstate.but_ennemi-self.superstate.joueur_ennemi_le_plus_proche) <= 0.0) and (self.superstate.angle_de_degagement(self.superstate.but_ennemi-self.superstate.player,self.superstate.but_ennemi-self.superstate.joueur_ennemi_le_plus_proche) > -1.0)):
            if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = Vector2D(self.superstate.joueur_ennemi_le_plus_proche.x, self.superstate.joueur_ennemi_le_plus_proche.y+25)
        
        elif self.superstate.zone_allie:
            if (self.superstate.joueur_ennemi_le_plus_proche-self.superstate.player).norm < 6 and (self.superstate.joueur_ennemi_le_plus_proche-self.superstate.player).norm > 2.5:
                vecteur_shoot = self.tire_au_but_si_peut_tirer_violent  
        return vecteur_shoot
    
    @property
    def passe_attaquant_faible(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_attaquant) == Vector2D):
                vecteur_shoot = ((self.superstate.position_attaquant-self.superstate.ball).normalize())
        return vecteur_shoot
    
    @property
    def passe_attaquant_faiblouille(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_attaquant) == Vector2D):
                vecteur_shoot = ((self.superstate.position_attaquant-self.superstate.ball).normalize())*4
        return vecteur_shoot
    
    @property
    def passe_attaquant_forte(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_attaquant) == Vector2D):
                vecteur_shoot = (self.superstate.ball-self.superstate.position_attaquant).normalize()*6 # self.superstate.position_attaquant-self.superstate.ball
        return vecteur_shoot

    @property
    def passe_milieu_A_faible(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_milieu_A) == Vector2D):
                vecteur_shoot = (self.superstate.position_milieu_A-self.superstate.ball).normalize()*2
        return vecteur_shoot   
    
    @property
    def passe_milieu_A_forte(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_milieu_A) == Vector2D):
                vecteur_shoot = (self.superstate.position_milieu_A-self.superstate.ball).normalize()*6
            else:
                vecteur_shoot = self.superstate.position_milieu_zone_Aretranche.normalize()*6
        return vecteur_shoot    

    @property
    def passe_milieu_B_forte(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_milieu_B) == Vector2D):
                vecteur_shoot = (self.superstate.position_milieu_B-self.superstate.ball).normalize()*6
        return vecteur_shoot
    
    @property
    def passe_milieu_B_faible(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_milieu_B) == Vector2D):
                vecteur_shoot = (self.superstate.position_milieu_B-self.superstate.ball).normalize()
        return vecteur_shoot
    

    
    ######################################################################################################
    #nouvelles passes 
    
    @property
    def passe_positionmoyenne_A_forte(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_moyenne_A_pourshoot) == Vector2D):
                vecteur_shoot = (self.superstate.position_milieu_A-self.superstate.ball).normalize()*6
            else:
                vecteur_shoot = self.superstate.position_milieu_zone_Aretranche.normalize()*6
        return vecteur_shoot    

    @property
    def passe_positionmoyenne_B_forte(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_moyenne_B_pourshoot) == Vector2D):
                vecteur_shoot = (self.superstate.position_moyenne_B_pourshoot-self.superstate.ball).normalize()*6 #moyennedelaouildevraitetre
            else:
                vecteur_shoot = self.superstate.position_milieu_zone_Bretranche.normalize()*6 #positiondedepart
        return vecteur_shoot
    
    
    @property
    def passe_positionmoyenneattaquant_faiblouille(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.position_moyenne_C_pourshoot) == Vector2D):
                vecteur_shoot = ((self.superstate.ball-self.superstate.position_moyenne_C_pourshoot).normalize())*4
            else:
                vecteur_shoot = self.superstate.position_moyenne_C_pourshoot.normalize()*6
        return vecteur_shoot
    
    @property
    def passesurquijetire_jesuisMA(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.surquijetire_jesuisMA) == Vector2D):
                vecteur_shoot = ((self.superstate.ball-self.superstate.surquijetire_jesuisMA).normalize())*4
            else:
                vecteur_shoot = self.superstate.surquijetire_jesuisMA.normalize()*6
        return vecteur_shoot
    
    #######################################################################################################################
    
    @property
    def shootsurpasse_intelligente_MilieuB(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.passe_intelligente_MilieuB) == Vector2D):
                vecteur_shoot = (self.superstate.passe_intelligente_MilieuB-self.superstate.ball).normalize()*4
        return vecteur_shoot
    
    @property
    def shootsurpasse_intelligente_goal(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.passe_intelligente_goal) == Vector2D):
                vecteur_shoot = (self.superstate.passe_intelligente_goal-self.superstate.ball).normalize()*6
        return vecteur_shoot
    
    @property
    def shootsurpasse_intelligente_MilieuA(self):
        vecteur_shoot = None
        if((self.superstate.player - self.superstate.ball).norm < PLAYER_RADIUS + BALL_RADIUS):
            if(type(self.superstate.passe_intelligente_MilieuA) == Vector2D):
                vecteur_shoot = (self.superstate.passe_intelligente_MilieuA-self.superstate.ball).normalize()*6
        return vecteur_shoot
    
    
    
    
    
    
    
    
    
    
    
    