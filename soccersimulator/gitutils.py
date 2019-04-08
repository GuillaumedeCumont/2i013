#-*- coding: utf-8 -*-

import os
import sys
# import imp
import shutil
# import argparse
# import pickle
from collections import namedtuple
import traceback
import logging
from soccersimulator import SoccerTeam, Strategy, Simulation
# import glob
# import importlib

logger = logging.getLogger("soccersimulator.gitutils")

MAX_TEST_STEPS = 50
Groupe = namedtuple("Groupe",["login","projet","module","noms"])

def dl_from_github(groupe, path):
    path = os.path.abspath(path)
    if type(groupe)==list:
        if os.path.exists(path):
            os.system('rm -rf %s/*' % path)
        for g in groupe:
            if g.module:
                dl_from_github(g,path)
            else:
                logger.info("\033[93m Module inconnu pour \033[94m%s : \033[91m%s \033[0m" % (g.login, g.projet))
        return
    logger.info("Debut import github %s %s" % (groupe.login, groupe.projet))
    if not os.path.exists(path):
        os.mkdir(path)
    tmp_path = os.path.join(path, groupe.login)
    shutil.rmtree(tmp_path, ignore_errors=True)
    os.mkdir(tmp_path)
    os.system("git clone https://github.com/%s/%s %s 2> /dev/null" % (groupe.login, groupe.projet, tmp_path))
    os.system("mv %s/%s %s/%s" % (tmp_path, groupe.module, path, 'temp_dir'))
    os.system("rm -rf %s" % tmp_path)
    os.system("mv %s/%s %s/%s" % (path, 'temp_dir', path, groupe.module))
#    try:
#        initdir = os.path.abspath(os.path.dirname(sorted(glob.glob(tmp_path+"/**/__init__.py",recursive=True),key=lambda x:len(x))[0]))
#    except Exception:
#           logger.info("Pas de __init__.py trouvé pour %s %s" % (groupe.login,groupe.projet))
#           return
#    if initdir != tmp_path:
#        logger.info("__init__.py pas a la racine, mv %s -- %s" % (initdir,tmp_path))
#        os.system("mv %s %s" %(initdir+"/*",tmp_path+"/"))

    

def check_date(groupe, path):
    if type(groupe)==list:
        for g in groupe: check_date(g,path)
        return
    print(groupe.login)
    os.system("git --git-dir=%s/.git log  --format=\"%%Cgreen%%cd %%Creset \"| cut -d \" \" -f 1-3,7| uniq" %
              (os.path.join(path, groupe.login),))


def check_team(team):
    teamDefault = SoccerTeam()
    for nb in range(team.nb_players):
        teamDefault.add(str(nb),Strategy())
    if Simulation(team,teamDefault,max_steps=MAX_TEST_STEPS).start().error or \
            Simulation(teamDefault,team,max_steps=MAX_TEST_STEPS).start().error:
        return False
    return True

def load_teams(path,login, nbps,cmd="get_team",filename='tournament.py'):
    mymod = None
    if not os.path.exists(os.path.join(path,login,"__init__.py")):
        logger.info("\033[93m Erreur pour \033[94m%s : \033[91m%s \033[0m" % (login, "__init__.py non trouve"))
    # if not os.path.exists(os.path.join(path, login, filename)):
    #     logger.info("\033[93m Erreur pour \033[94m%s : \033[91m%s \033[0m" % (login, filename+" non trouve"))
    #     return None
    try:
        sys.path.insert(0, path)
        mymod = __import__(login)

        #cpcmd = 'cp init.py {}/__init__.py'.format(os.path.join(path, login))
        #print(cpcmd)
        #os.system(cpcmd)
        #sys.path.insert(0, path)
        #mymod = __import__(login)

        # Delete modules in github...
        # sys.path.insert(0, os.path.join(path, login))
        # files = [f for f in os.listdir(os.path.join(path, login)) if '.py' not in f and f != 'soccersimulator' and f != '.git' and '.md' not in f and f != '.ipynb_checkpoints' and f != '__pycache__']
        # if not files:
        #     logger.info("\033[93m Erreur pour \033[94m%s : \033[91m%s \033[0m" % (login, "module non trouve"))
        #     return None
        # key_del = []
        # for name in files:
        #     for key in sys.modules.keys():
        #         if name in key:
        #     #if name in sys.modules:
        #         #del sys.modules[name]
        #             key_del.append(key)
        # for key in key_del:
        #     del sys.modules[key]
        # mymod = __import__(filename[:-3])
        # mymod = importlib.reload(mymod)

        #spec = importlib.util.spec_from_file_location('tournament', os.path.join(path, login, filename))
        #mymod = importlib.util.module_from_spec(spec)
        #spec.loader.exec_module(mymod)
        #print(dir(mymod))
    except Exception as e:
        logger.debug(traceback.format_exc())
        logger.info("\033[93m Erreur pour \033[94m%s : \033[91m%s \033[0m" % (login, e))
    finally:
        del sys.path[0]
    if mymod is None:
        return None
    teams = dict()
    if not hasattr(mymod,cmd):
        logger.info("\033[93m Pas de get_team pour \033[94m%s\033[0m" % (login,))
        return teams
    for nbp in nbps:
        try:
            tmpteam = mymod.__getattribute__(cmd)(nbp)
            if tmpteam is None or not hasattr(tmpteam,"nb_players"):
                logger.info("\033[93m Pas d'equipe %s pour \033[94m%s\033[0m" % (cmd+"("+str(nbp)+")",login))
                continue
            if not check_team(tmpteam):
                logger.info("\033[93m Error for \033[91m(%s,%d)\033[0m" % (login,nbp))
                continue
            tmpteam.login = login
            teams[nbp] = (tmpteam,mymod.__getattribute__(cmd))
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.info("\033[93m Erreur pour \033[94m%s: \033[91m%s \033[0m" % (login,e))
    logger.info("Equipes de \033[92m%s\033[0m charge, \033[92m%s equipes\033[0m" % (login, len(teams)))
    return teams



def import_directory(path,nbps,logins = None,cmd="get_team"):
    teams = dict()
    for i in nbps:
        teams[i] = []
    path = os.path.realpath(path)
    logins = [login for login in os.listdir(path)\
              if os.path.isdir(os.path.join(path,login)) and (logins is None or login in logins)]
    for l in sorted(logins,key=lambda x : x.lower()):
        tmp=load_teams(path,l,nbps,cmd)
        if tmp is not None:
            for nbp in tmp.keys():
                teams[nbp].append(tmp[nbp])
    return teams
