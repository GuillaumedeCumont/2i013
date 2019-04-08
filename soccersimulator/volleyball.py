from .mdpsoccer import PlayerState, SoccerState, Simulation, Ball, SoccerAction, SoccerTeam
from . import settings
from .utils import Vector2D
import random
from copy import deepcopy
from .gui import SimuGUI, FPS, pyg_start
from .guiutils import Primitive2DGL, ObjectSprite, BackgroundSprite, get_hud_prims, Hud
from .guisettings import *
import pyglet


###############################################################################
# PlayerState
###############################################################################
class VolleyPlayerState(PlayerState):
    def next(self, ball, action=None):
        """ Calcul le prochain etat en fonction de l'action et de la position de la balle
        :param ball:
        :param action:
        :return: Action shoot effectue
        """
        if not (hasattr(action, "acceleration") and hasattr(action, "shoot")):
            action = SoccerAction()
        self.action = action.copy()
        self.vitesse *= (1 - settings.playerBrackConstant)
        self.vitesse = (self.vitesse + self.acceleration).norm_max(settings.maxPlayerSpeed)
        self.position += self.vitesse
        if self.position.x < 0 or self.position.x > settings.GAME_WIDTH \
                or self.position.y < 0 or self.position.y > settings.GAME_HEIGHT:
            self.position.x = max(0, min(settings.GAME_WIDTH, self.position.x))
            self.position.y = max(0, min(settings.GAME_HEIGHT, self.position.y))
            self.vitesse = Vector2D()

        if self._id_team == 1 and self.position.x > settings.GAME_WIDTH / 2:
            self.position.x = settings.GAME_WIDTH / 2 - settings.PLAYER_RADIUS
            self.vitesse = Vector2D()
        elif self._id_team == 2 and self.position.x < settings.GAME_WIDTH / 2:
            self.position.x = settings.GAME_WIDTH / 2 + settings.PLAYER_RADIUS
        if self.shoot.norm == 0 or not self.can_shoot():
            self._dec_shoot()
            return Vector2D()
        self._reset_shoot()
        if self.position.distance(ball.position) > (settings.PLAYER_RADIUS + settings.BALL_RADIUS):
            return Vector2D()

        # If there is an actual shoot
        ball.previous_team_owner = deepcopy(ball.team_owner)
        ball.team_owner = self._id_team
        return self._rd_angle(self.shoot,(self.vitesse.angle-self.shoot.angle)*(0 if self.vitesse.norm==0 else 1),\
                    self.position.distance(ball.position)/(settings.PLAYER_RADIUS+settings.BALL_RADIUS))


###############################################################################
# SoccerState
###############################################################################
class VolleySoccerState(SoccerState):
    def apply_actions(self, actions=None, strategies=None):
        if strategies: self.strategies.update(strategies)
        sum_of_shoots = Vector2D()
        self.goal = 0
        if actions:
            for k, c in self.states.items():
                if k in actions:
                    sum_of_shoots += c.next(self.ball, actions[k])
        self.ball.next(sum_of_shoots)
        self.step += 1

        if self.ball.off_the_field():
            self._do_goal(3 - self.ball.team_owner)
        if self.ball.exceed_hits():
            self._do_goal(3 - self.ball.team_owner)

        if self.ball.on_ground():
            if self.ball.position.x < settings.GAME_WIDTH / 2:
                self._do_goal(2)
            else:
                self._do_goal(1)

    def reset_state(self, nb_players_1=0, nb_players_2=0):
        if nb_players_1 == 0 and self.nb_players(1) > 0:
            nb_players_1 = self.nb_players(1)
        if nb_players_2 == 0 and self.nb_players(2) > 0:
            nb_players_2 = self.nb_players(2)
        quarters = [i * settings.GAME_HEIGHT / 4. for i in range(1, 4)]
        rows = [settings.GAME_WIDTH * 0.1, settings.GAME_WIDTH * 0.35, settings.GAME_WIDTH * (1 - 0.35),
                settings.GAME_WIDTH * (1 - 0.1)]
        if nb_players_1 == 1:
            self.states[(1, 0)] = VolleyPlayerState(position=Vector2D(rows[0], quarters[1]))
        if nb_players_2 == 1:
            self.states[(2, 0)] = VolleyPlayerState(position=Vector2D(rows[3], quarters[1]))
        if nb_players_1 == 2:
            self.states[(1, 0)] = VolleyPlayerState(position=Vector2D(rows[0], quarters[0]))
            self.states[(1, 1)] = VolleyPlayerState(position=Vector2D(rows[0], quarters[2]))
        if nb_players_2 == 2:
            self.states[(2, 0)] = VolleyPlayerState(position=Vector2D(rows[3], quarters[0]))
            self.states[(2, 1)] = VolleyPlayerState(position=Vector2D(rows[3], quarters[2]))
        if nb_players_1 == 3:
            self.states[(1, 0)] = VolleyPlayerState(position=Vector2D(rows[0], quarters[1]))
            self.states[(1, 1)] = VolleyPlayerState(position=Vector2D(rows[0], quarters[0]))
            self.states[(1, 2)] = VolleyPlayerState(position=Vector2D(rows[0], quarters[2]))
        if nb_players_2 == 3:
            self.states[(2, 0)] = VolleyPlayerState(position=Vector2D(rows[3], quarters[1]))
            self.states[(2, 1)] = VolleyPlayerState(position=Vector2D(rows[3], quarters[0]))
            self.states[(2, 2)] = VolleyPlayerState(position=Vector2D(rows[3], quarters[2]))
        if nb_players_1 == 4:
            self.states[(1, 0)] = VolleyPlayerState(position=Vector2D(rows[0], quarters[0]))
            self.states[(1, 1)] = VolleyPlayerState(position=Vector2D(rows[0], quarters[2]))
            self.states[(1, 2)] = VolleyPlayerState(position=Vector2D(rows[1], quarters[0]))
            self.states[(1, 3)] = VolleyPlayerState(position=Vector2D(rows[1], quarters[2]))
        if nb_players_2 == 4:
            self.states[(2, 0)] = VolleyPlayerState(position=Vector2D(rows[3], quarters[0]))
            self.states[(2, 1)] = VolleyPlayerState(position=Vector2D(rows[3], quarters[2]))
            self.states[(2, 2)] = VolleyPlayerState(position=Vector2D(rows[2], quarters[0]))
            self.states[(2, 3)] = VolleyPlayerState(position=Vector2D(rows[2], quarters[2]))

        # Give an id_team to player state
        for key in self.states.keys():
            self.states[key]._id_team = key[0]

        # Here change ball initialization
        server = random.randint(1, 2)
        self.ball = Ball(deepcopy(self.states[(server, 0)].position), Vector2D())
        self.goal = 0


###############################################################################
# Simulation
###############################################################################
class VolleySimulation(Simulation):
    def __init__(self, team1=None, team2=None, max_steps = settings.MAX_GAME_STEPS, initial_state=None, **kwargs):
        team1, team2 = team1 or SoccerTeam(), team2 or SoccerTeam()
        initial_state = initial_state or VolleySoccerState.create_initial_state(team1.nb_players,
                                                                                team2.nb_players, max_steps)
        super().__init__(team1=team1, team2=team2, max_steps=max_steps, initial_state=initial_state, **kwargs)

    def get_initial_state(self):
        return VolleySoccerState.create_initial_state(self.team1.nb_players, self.team2.nb_players, self.max_steps)


###############################################################################
# get_field_prims
###############################################################################
def get_volley_field_prims():
    field = Primitive2DGL([(0, 0), (0, settings.GAME_HEIGHT),
                           (settings.GAME_WIDTH, settings.GAME_HEIGHT),
                           (settings.GAME_WIDTH, 0)], VOLLEY_FIELD_COLOR)
    bandes_1 = Primitive2DGL([(0, 0), (settings.GAME_WIDTH, 0),
                              (settings.GAME_WIDTH, settings.GAME_HEIGHT),
                              (0, settings.GAME_HEIGHT), (0, 0)], LINE_COLOR, pyglet.gl.GL_LINE_STRIP)
    bandes_2 = Primitive2DGL([(settings.GAME_WIDTH / 2, settings.GAME_HEIGHT),
                              (settings.GAME_WIDTH / 2, 0)], LINE_COLOR, pyglet.gl.GL_LINE_STRIP)
    bandes_3 = Primitive2DGL([(6 / 18 * settings.GAME_WIDTH, settings.GAME_HEIGHT),
                              (6 / 18 * settings.GAME_WIDTH, 0)], LINE_COLOR, pyglet.gl.GL_LINE_STRIP)
    bandes_4 = Primitive2DGL([(12 / 18 * settings.GAME_WIDTH, settings.GAME_HEIGHT),
                              (12 / 18 * settings.GAME_WIDTH, 0)], LINE_COLOR, pyglet.gl.GL_LINE_STRIP)
    # y1 = (settings.GAME_HEIGHT - settings.GAME_GOAL_HEIGHT) / 2
    # y2 = (settings.GAME_HEIGHT + settings.GAME_GOAL_HEIGHT) / 2
    # xend = settings.GAME_WIDTH
    # goals_1 = Primitive2DGL([(0, y1), (0, y2), (2, y2), (2, y1)], GOAL_COLOR)
    # goals_2 = Primitive2DGL([(xend, y2), (xend, y1), (xend - 2, y1), (xend - 2, y2)], GOAL_COLOR)
    return [field, bandes_1, bandes_2, bandes_3, bandes_4]


###############################################################################
# BackgroundSprite
###############################################################################
class VolleyBackgroundSprite(BackgroundSprite):
    def __init__(self):
        ObjectSprite.__init__(self)
        self.add_primitives(get_volley_field_prims())
        self.add_primitives(get_hud_prims())


###############################################################################
# SimuGUI
###############################################################################
class VolleySimuGUI(SimuGUI):
    def __init__(self, simu=None, width=1400, height=700, fps=None):
        pyglet.window.Window.__init__(self, width=width, height=height, resizable=True)
        self.set_size(width, height)
        self.focus()
        self.clear()
        self._fps = FPS if fps is None else fps
        self._sprites = dict()
        self._background = VolleyBackgroundSprite()
        self._state = None
        self._mode_next = self.AUTO
        self._waiting_key = False
        self._hud_names = True
        self.hud = Hud()
        pyglet.clock.schedule_interval(self.update, 1. / 25)
        self.set(simu)
        if simu:
            self.play()

###############################################################################
# volley_show_simu
###############################################################################
def volley_show_simu(simu, fps=None):
    gui = VolleySimuGUI(simu, fps=fps)
    pyg_start()
