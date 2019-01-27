from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu
from soccersimulator import PLAYER_RADIUS, BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH

   
    
class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        
        if(id_team == 2):
            position_but = Vector2D(0,GAME_HEIGHT/2.)
        if(id_team == 1):
            position_but = Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
        
        vecteur_acceleration = state.ball.position - state.player_state(id_team,id_player).position
        vecteur_shoot = None
        
        if((state.player_state(id_team,id_player).position - state.ball.position).norm < PLAYER_RADIUS + BALL_RADIUS):
                vecteur_shoot = (position_but - state.ball.position)
        return SoccerAction(vecteur_acceleration,vecteur_shoot)
    
    
# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")
# Add players
team1.add("Zlatan", Strategy())
team1.add("Mbappé", Strategy())  
team2.add("Static", RandomStrategy())   
team2.add("Static", RandomStrategy())

# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)
