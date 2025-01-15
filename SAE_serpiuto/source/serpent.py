# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module serpent.py
    Ce module implémente l'API permettant de gérer les informations des joueurs (idenfier à leur serpent)
"""
import arene

def Serpent(nom_joueur:str, num_joueur:int,points:int=0,positions:list=None,tps_s:int=0,tps_p:int=0,tps_m:int=0,direction:str='N')->dict:
    """Créer un joueur avec toutes les informations le concernant.

    Args:
        nom_joueur (str): nom du joueur
        num_joueur (int): numero du joueur
        points (int, optional): nombre de points attribués au joueur. Defaults to 0.
        positions (list, optional): la liste des positions occupées par le serpent sur l'arène. Defaults to None.
        tps_s (int, optional): temps restant pour le bonus surpuissance. Defaults to 0.
        tps_p (int, optional): temps restant pour le bonus protection. Defaults to 0.
        tps_m (int, optional): temps restant pour le bonus mange-mur. Defaults to 0.
        direction (str, optional): dernière direction prise par le serpent. Defaults to 'N'.

    Returns:
        dict: une dictionnaire contenant les informations du serpent
    """    
    return {"nom":nom_joueur,"num_joueur":num_joueur, "points":points,"liste_pos":positions,"temps_surpuissance":tps_s,
            "temps_protection":tps_p,"temps_mange_mur":tps_m, "derniere_direction":direction}

def get_nom(serpent:dict)->str:
    """retourne le nom du joueur associé au serpent

    Args:
        serpent (dict): le serpent considéré

    Returns:
        str: le nom du joueur associé à ce serpent
    """    
    return serpent["nom"]

def get_num_joueur(serpent:dict)->int: #Erika
    """retourne le numéro du joueur associé au serpent

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le numéro du joueur associé à ce serpent
    """   
    return serpent["num_joueur"]

def get_points(serpent:dict)->int: #Erika
    """retourne le nombre de points du joueur associé au serpent

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de points du joueur associé à ce serpent
    """   
    return serpent["points"]

def get_liste_pos(serpent:dict)->list:
    """retourne la liste des positions occupées par le serpent sur l'arène. La première position étant la tête du serpent

    Args:
        serpent (dict): le serpent considéré

    Returns:
        list: la liste des positions occupées par le serpent
    """    
    return serpent["liste_pos"]

def get_queue(serpent:dict)->list[int,int]:
    """retourne la position (lig,col) de la queue du serpent dans l'arène

    Args:
        serpent (dict): le serpent considéré

    Returns:
        [int,int]: la position lig,col du la queue du serpent
    """    
    return serpent["liste_pos"][-1]

def get_derniere_direction(serpent:dict)->str:
    """retourne la dernière direction choisie par le joueur pour se déplacer

    Args:
        serpent (dict): le serpent considéré

    Returns:
        str: un des caractère N S E O
    """    
    return serpent["derniere_direction"]

def get_bonus(serpent:dict)->list:
    """retourne une liste contenant les bonus obtenus par le joueur
        c'est-à-dire ceux pour lesquels le temps restant est supérieur à 0

    Args:
        serpent (dict): le serpent considéré

    Returns:
        list: la liste des bonus du joueur
    """    
    res=[]
    if serpent["temps_surpuissance"]>0:
        res.append(arene.SURPUISSANCE)
    if serpent["temps_protection"]>0:
        res.append(arene.PROTECTION)
    if serpent["temps_mange_mur"]>0:
        res.append(arene.MANGE_MUR)
    return res



def ajouter_points(serpent:dict,nb_points:int): #Erika
    """ajoute (ou enlève) des points à un serpent

    Args:
        serpent (dict): le serpent considéré
        nb_points (int): le nombre de points à ajouter (si négatif enlève des points)
    """    
    serpent["points"]+=nb_points

def set_liste_pos(serpent:dict, tete:list): #Erika
    """initialise la liste des positionsd'un serpent

    Args:
        serpent (dict): le serpent considéré
        tete (list): la liste des positions occupées par ce serpent
    """    
    serpent["liste_pos"]=tete

def set_derniere_direction(serpent:dict, direction:str):
    """Met à jout la dernière direction utilisée par le serpent (utile pour l'affichage)

    Args:
        serpent (dict): le serpent considéré
        direction (str): un des caractère N S E O
    """    
    serpent["derniere_direction"]=direction

def to_str(serpent:dict)->str:
    """produit une chaine de caractères contenant les informations principales d'un serpent sour la forme
    Joueur 1 -> 143 s:0 m:4 p:0
    où Joueur 1 est le nom du joueur, après la flèche se trouve le nombre de point
    puis le temps restant de chaque bonus (supuissante, mange mur et protection)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        str: la chaine de caractères donnant les informations principales d'un serpent 
    """    
    return serpent["nom"]+ " -> " + str(serpent["points"]) + \
                    " s:"+str(serpent["temps_surpuissance"]) +\
                    " m:"+str(serpent["temps_mange_mur"])+\
                    " p:"+str(serpent["temps_protection"])

def get_temps_protection(serpent:dict)->int:
    """indique le temps restant pour le bonus protection

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de tours restant pour ce bonus
    """    
    return serpent["temps_protection"]

def get_temps_mange_mur(serpent:dict)->int:
    """indique le temps restant pour le bonus mange mur

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de tours restant pour ce bonus
    """   
    return serpent["temps_mange_mur"]

def get_temps_surpuissance(serpent:dict)->int: #Erika
    """indique le temps restant pour le bonus surpuissance

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de tours restant pour ce bonus
    """   
    return serpent["temps_surpuissance"]

def ajouter_temps_protection(serpent:dict, temps:int)->int: #Erika
    """ajoute du temps supplémentaire pour le bonus protection

    Args:
        serpent (dict): le serpent considéré
        temps (int): le nombre de tours à ajouter

    Returns:
        int: le nombre de tours total restant pour ce bonus
    """    
    serpent["temps_protection"]+=temps
    return serpent["temps_protection"]

def ajouter_temps_mange_mur(serpent:dict, temps:int)->int:
    """ajoute du temps supplémentaire pour le bonus mange mur

    Args:
        serpent (dict): le serpent considéré
        temps (int): le nombre de tours à ajouter

    Returns:
        int: le nombre de tours total restant pour ce bonus
    """    
    serpent["temps_mange_mur"]+=temps
    return serpent["temps_mange_mur"]

def ajouter_temps_surpuissance(serpent:dict, temps:int)->int:
    """ajoute du temps supplémentaire pour le bonus surpuissance

    Args:
        serpent (dict): le serpent considéré
        temps (int): le nombre de tours à ajouter

    Returns:
        int: le nombre de tours total restant pour ce bonus
    """    
    serpent["temps_surpuissance"]+=temps
    return serpent["temps_surpuissance"]

def maj_temps(serpent:dict):
    """Décrémente les temps restant pour les bonus de ce serpent
    Attention les temps ne peuvent pas être négatif

    Args:
        serpent (dict): le serpent considéré
    """    
    if serpent["temps_protection"]>0:
        serpent["temps_protection"]-=1
    if serpent["temps_mange_mur"]>0:
        serpent["temps_mange_mur"]-=1
    if serpent["temps_surpuissance"]>0:
        serpent["temps_surpuissance"]-=1

def serpent_2_str(serpent:dict, sep=";")->str:
    """Sérialise un serpent sous la forme d'une chaine de caractères
    contenant 2 lignes.
    nom_j;num_j;nb_point;tps_surpuissance;tps_mange_mur;tps_protection
    lig1;col1;lig2;col2;...
    La première ligne donne les informations autres que la liste des positions du serpent
    la deuxième ligne donné la liste des position du serpent en commençant par la tête
    Args:
        serpent (dict): le serpent considéré
        sep (str, optional): le caractère séparant les informations du serpent. Defaults to ";".

    Returns:
        str: la chaine de caractères contenant les toutes informations du serpent
    """    
    res= serpent["nom"]+sep+str(serpent["num_joueur"])+sep+str(serpent["points"])+sep+\
           str(serpent["temps_surpuissance"])+ sep + str(serpent["temps_protection"])+sep+\
           str(serpent["temps_mange_mur"])+sep+serpent["derniere_direction"]+"\n"
    if serpent["liste_pos"] is None:
        return res+'\n'
    prec=''
    for lig,col in serpent["liste_pos"]:
        res+=prec+str(lig)+sep+str(col)
        prec=sep
    return res+'\n'

def serpent_from_str(la_chaine, sep=";")->dict: #Erika
    """Reconstruit un serpent à partir d'une chaine de caractères
       telle que celle produite par la fonction précédente

    Args:
        la_chaine (_type_): la chaine de caractères contenant les informations du serpent
        sep (str, optional): le caractère servant à séparer les informations du serpent. Defaults to ";".

    Returns:
        dict: Le serpent représenté dans la chaine de caractères
    """    
    # nom_joueur,num_joueur,nb_points,positions,tps_s,tps_p,tps_m,direction=la_chaine.split(sep)
    # positions=eval(positions)
    # return {"nom":nom_joueur, "numero":int(num_joueur), "points":int(nb_points), "pos":positions,"temps_surp":int(tps_s),
    #         "temps_protec":int(tps_p),"temps_mange":int(tps_m),"der_direction":direction}
    lignes=la_chaine.split("\n")
    try:
       nom,num_joueur,points,temps_surpuissance,temps_protection,temps_mange_mur,derniere_direction=\
       lignes[0].split(sep)

    except:
        raise Exception("Problème construction serpent sur la 1ere ligne")
    try:
        coord=lignes[1].split(sep)
        pair=False
        les_coord=[]
        lig=None
        for val in coord:
            if pair:
                col=int(val)
                les_coord.append((lig,col))
            else:
                lig=int(val)
            pair=not(pair)
        if pair:
            raise Exception
    except:
        raise Exception("Problème construction serpent sur la 2eme ligne")
    return Serpent(nom,int(num_joueur),int(points),les_coord,int(temps_surpuissance),int(temps_protection),int(temps_mange_mur),derniere_direction)

def copy_serpent(serpent:dict)->dict: #Erika
    """fait une copie du serpent passer en paramètres
    Attention à bien faire une copie de la liste des positions
        
    Args:
        serpent (dict): le serpent à recopier

    Returns:
        dict: la copie du serpent passé en paramètres
    """ 
    # return {"nom":get_nom(serpent),"numero":get_num_joueur(serpent),"points":get_points(serpent),"positions":get_liste_pos,"temps_surp":get_temps_surpuissance(serpent),"temps_protec":get_temps_protection(serpent),"temps":(serpent),"temps_mange":get_temps_mange_mur(serpent),"der_direction":get_derniere_direction(serpent)}
    copie_pos=[]
    for [lin,col] in serpent["liste_pos"]:
        copie_pos.append([lin,col])
    return {"nom":serpent["nom"],"num_joueur":serpent["num_joueur"], "points":serpent["points"],
            "liste_pos":copie_pos,"temps_surpuissance":serpent["temps_surpuissance"],
            "temps_protection":serpent["temps_protection"], "temps_mange_mur":serpent["temps_mange_mur"],
            "derniere_direction":serpent["derniere_direction"]}
