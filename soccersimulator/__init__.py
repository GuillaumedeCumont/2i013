from .utils import  dump_jsonz, load_jsonz, fmt,clean_fn, to_json, to_jsonz, from_json, from_jsonz,dict_to_json
from .utils import  Vector2D, MobileMixin
from .strategies import Strategy,  KeyboardStrategy, DTreeStrategy
from .mdpsoccer import SoccerAction, Ball, PlayerState,SoccerState
from .mdpsoccer import  Player, SoccerTeam, Simulation
from .matches import Score, SoccerTournament
from .gui import SimuGUI, show_simu, show_state, pyg_start, pyg_stop, pyglet
from .challenges import *
from . import  settings
from . import gitutils
from .arbres_utils import apprend_arbre,build_apprentissage,genere_dot
import logging
__version__ = '1.2018.02.01'
__project__ = 'soccersimulator'

logging.basicConfig(format='%(name)s:%(levelname)s - %(message)s', level=logging.DEBUG)
