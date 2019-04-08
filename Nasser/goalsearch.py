from soccersimulator import SoccerTeam, Strategy, Simulation
from soccersimulator import Vector2D, show_simu
from sklearn.model_selection import ParameterGrid
from soccersimulator.settings  import GAME_WIDTH, GAME_HEIGHT,PLAYER_RADIUS,BALL_RADIUS,maxPlayerShoot



class GoalSearch (object):
    def __init__ (self, strategy, params, simu = None, trials =20, max_steps =1000000, max_round_step =40):
        self.strategy = strategy
        self.params = params.copy()
        self.simu = simu
        self.trials = trials
        self.max_steps = max_steps
        self.max_round_step = max_round_step

    def start (self, show = True):
        if not self.simu :
            team1 = SoccerTeam("Team␣1")
            team2 = SoccerTeam("Team␣2")
            team1.add(self.strategy.name, self.strategy)
            team2.add(Strategy().name, Strategy())
            self.simu = Simulation(team1, team2, max_steps = self.max_steps)
        self.simu.listeners += self

        if show :
            show_simu(self.simu)
        else :
            self.simu.start()

    def begin_match (self, team1, team2, state):
        self.last_step = 0 # Step of the last round
        self.criterion = 0 # Criterion to maximize ( here , number of goals )
        self.cpt_trials = 0 # Counter for trials
        self.param_grid = iter(ParameterGrid(self.params)) # Iterator for the g
        self.cur_param = next(self.param_grid, None) # Current parameter
        if self.cur_param is None :
            raise ValueError('no␣parameter␣given.')
        self.res = dict() # Dictionary of results

    def begin_round (self, team1, team2, state):
        ball = Vector2D.create_random(low=0,high=1) 
        ball.y = ball.y*GAME_HEIGHT
        ball.x = ball.x*GAME_WIDTH*(3/5) + GAME_WIDTH*(3/5) 
        

        # Player and ball postion ( random )
        self.simu.state.states[(1,0)].position = ball.copy() # Player position
        self.simu.state.states[(1,0)].vitesse = Vector2D() # Player acceleration
        self.simu.state.ball.position = ball.copy() # Ball position
        
        self.last_step = self.simu.step # Last step of the game

        # Set the current value for the current parameters
        for key, value in self.cur_param.items():
            setattr(self.strategy, key, value)
    
    def end_round (self, team1, team2, state):
        # A round ends when there is a goal of if max step is achieved
        if state.goal > 0:
            self.criterion += 1 # Increment criterion

        self.cpt_trials += 1 # Increment number of trials

        print(self.cur_param, end = " ␣ ␣ ␣ ␣ ")
        print("Crit: {}   Cpt: {}".format(self.criterion, self.cpt_trials))

        if self.cpt_trials >= self.trials :
            # Save the result
            self.res[tuple(self.cur_param.items())] = (self.criterion*1.)/(self.cpt_trials*1.)
            # Reset parameters
            self.criterion = 0
            self.cpt_trials = 0

            # Next parameter value
            self.cur_param = next(self.param_grid, None)
            if self.cur_param is None:
                self.simu.end_match()
        
    def update_round (self, team1, team2, state):
        # Stop the round if it is too long
        if state.step > self.last_step + self.max_round_step: 
            self.simu.end_round()

    def get_res(self):
        return self.res

    def get_best(self):
        return max(self.res, key=self.res.get)