from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH
from .Tools import *
from .Actions import Move, Shoot    

class GoStrategy(Strategy):
    def __init__(self, strength):
        Strategy.__init__(self, "Random")
        self.strength = strength
        
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        move = Move(s)
        shoot = Shoot(s)
        return move.aller_vers_ballon + shoot.tire_au_but_si_peut_tirer(self.strenght)
    