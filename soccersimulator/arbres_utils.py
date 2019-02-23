import numpy as np
from sklearn.tree import DecisionTreeClassifier,export_graphviz


def build_apprentissage(states_tuple,get_features):
    """ transforme une liste de couples ((etat,idteam,idplayer),strategie) en ensemble d'apprentissage, deux matrices l'une avec la description des etats, l'autre avec les labels. get_feature transforme l'etat en une liste de variables
    """
    res = []
    labels = []
    for state,info in states_tuple:
        res.append(get_features(state,info[0],info[1]))
        labels.append(info[2])
    """ transformation en matrice numpy """
    return np.array(res),np.array(labels)

def genere_dot(tree,fn):
    """ Genere un fichier .dot qui permet de visualiser un arbre """
    with open(fn,"w") as f:
            export_graphviz(tree,f,class_names = tree.classes_,feature_names=getattr(tree,"feature_names",None), filled = True,rounded=True)
    print("Use dot -Tpdf %s -o %spdf to generate pdf" % (fn,fn[:-3]))

def apprend_arbre(train,labels,depth=10,min_samples_leaf=2,min_samples_split=2,feature_names=None):
    """ Apprend un arbre de decision """
    tree = DecisionTreeClassifier(max_depth=depth,min_samples_leaf=min_samples_leaf,min_samples_split=min_samples_split)
    tree.fit(train,labels)
    if feature_names is not None:
        tree.feature_names=feature_names
    return tree
