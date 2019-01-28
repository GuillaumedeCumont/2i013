from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH
from Tools import *
   
    
class GoStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        print(s.joueur_ennemi_le_plus_proche)
        if(id_player == 0):
            return SoccerAction(s.aller_vers_ballon,s.tire_au_but_si_peut_tirer)
        if (id_player == 1):
            return SoccerAction(s.aller_vers_but_allie,None)
        
    
    
# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")
# Add players
team1.add("Zlatan", GoStrategy())
team1.add("Mbappé", GoStrategy())  
team2.add("Static", Strategy())   
team2.add("Static", Strategy())

# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)
