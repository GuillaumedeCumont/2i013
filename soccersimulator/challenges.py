from .settings import *
from .mdpsoccer import *
from .utils import *
from .matches import SoccerTournament, Score
import logging

logger = logging.getLogger("soccersimulator.challenges")

class ChallengeFonceurButeur(Simulation):
    def __init__(self,team1,max_but=20,max_steps=5*settings.MAX_GAME_STEPS,initial_state=None,**kwargs):
        super(ChallengeFonceurButeur,self).__init__(team1,None,max_steps,initial_state,**kwargs)
        self.name = self.__class__.__name__
        self.resultats = []
        self._last_step = 0
        self.max_but = max_but
        self.stats_score = 0
    def begin_round(self):
        self._last_step = self.state.step
        super(ChallengeFonceurButeur,self).begin_round()
    def update_round(self):
        super(ChallengeFonceurButeur,self).update_round()
    def end_round(self):
        if self.state.goal==1:
            self.resultats.append(self.state.step-self._last_step)
        super(ChallengeFonceurButeur,self).end_round()
    def stop(self):
        return super(ChallengeFonceurButeur,self).stop() or self.state.get_score_team(1) >=self.max_but
    def end_match(self):
        if len(self.resultats)>0:
            self.stats_score = sum(self.resultats)/len(self.resultats)
        super(ChallengeFonceurButeur,self).end_match()
        
class Challenge(SoccerTournament):
    def __init__(self,idchal,**kwargs):
        super(Challenge,self).__init__(**kwargs)
        self.idchal = idchal
        self.chal = get_challenge(self.idchal)

    def add_team(self,team,score=None):
        if score is None:
            score = Score()
        self.teams[self.nb_teams] = team
        self.scores[self.nb_teams-1] =score
        self.matches[self.nb_teams-1] = None

    def play_next(self):
        if self.stop():
            return
        self.cur_i = self._get_next()
        self.cur_match = self.chal(self.get_team(self.cur_i))
        self.cur_match.listeners += self
        self.cur_match.start()
    def __str__(self):
        return "Challenge %d,  %d equipes, %d matches" %(self.idchal,self.nb_teams,self.nb_matches)

    def begin_match(self, *args, **kwargs):
        logger.info("\033[33mDebut challenge : \033[0m%d/%d : \033[94m%s (%s) \033[0m" % (len(self.played)+1, self.nb_matches,
                                                    self.cur_match.get_team(1).name,self.cur_match.get_team(1).login))
        self.listeners.begin_match(*args, **kwargs)

    def end_match(self, *args, **kwargs):
        if not self._replay:
            self.scores[self.cur_i].add(self.cur_match.stats_score,0)
            self.matches[self.cur_i]=to_jsonz(self.cur_match)
        logger.info("\033[93mResultat : \033[37m%s (%s) \033[0m : %f" % 
            (self.cur_match.get_team(1).name, self.cur_match.get_team(1).login,self.cur_match.stats_score))
        self.listeners.end_match(*args, **kwargs)
        self.cur_match.listeners -= self
        self.cur_i = -1
    
    
def get_challenge(id):
    return CHALLENGES[id]

CHALLENGES = dict({1:ChallengeFonceurButeur})
