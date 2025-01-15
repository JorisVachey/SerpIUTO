# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module IA.py
    Ce module implémente toutes les fonctions ainsi que l'IA de votre serpent
"""

import partie
import argparse
import client
import random
import arene
import serpent
direction_prec='X' # variable indiquant la décision précédente prise par le joueur. A mettre à jour soi-même

####################################################################
### A partir d'ici, implémenter toutes les fonctions qui vous seront 
### utiles pour prendre vos décisions
### Toutes vos fonctions devront être documentées
####################################################################

def directions_possibles(l_arene:dict,num_joueur:int)->str:
    """Indique les directions possible pour le joueur num_joueur
        c'est à dire les directions qu'il peut prendre sans se cogner dans
        un mur, sortir de l'arène ou se cogner sur une boîte trop grosse pour sa tête

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur

    Returns:
        str: une chaine composée de NOSE qui indique les directions
            pouvant être prise par le joueur. Attention il est possible
            qu'aucune direction ne soit possible donc la fonction peut retourner la chaine vide   """
    res=[]
    serp=arene.get_serpent(l_arene,num_joueur)[0]

    x,y=serp[0],serp[1]
    tete=arene.get_val_boite(l_arene,x,y)
    lgn,col=arene.get_dim(l_arene)
    if 0<=x-1<lgn and (not arene.est_mur(l_arene,x-1,y) or serpent.get_temps_mange_mur(l_arene["serpents"][num_joueur-1])>1) and (arene.get_val_boite(l_arene,x-1,y)<=tete or serpent.get_temps_surpuissance(l_arene["serpents"][num_joueur-1])>1):
        res+=["N"]
    if 0<=y-1<col and (not arene.est_mur(l_arene,x,y-1) or serpent.get_temps_mange_mur(l_arene["serpents"][num_joueur-1])>1) and (arene.get_val_boite(l_arene,x,y-1)<=tete or serpent.get_temps_surpuissance(l_arene["serpents"][num_joueur-1])>1): 
        res+=["O"]
    if 0<=x+1<lgn and (not arene.est_mur(l_arene,x+1,y) or serpent.get_temps_mange_mur(l_arene["serpents"][num_joueur-1])>1) and (arene.get_val_boite(l_arene,x+1,y)<=tete or serpent.get_temps_surpuissance(l_arene["serpents"][num_joueur-1])>1):
        res+=["S"]
    if col>y+1>=0 and (not arene.est_mur(l_arene,x,y+1) or serpent.get_temps_mange_mur(l_arene["serpents"][num_joueur-1])>1) and (arene.get_val_boite(l_arene,x,y+1)<=tete or serpent.get_temps_surpuissance(l_arene["serpents"][num_joueur-1])>1):
        res+=["E"]
    random.shuffle(res)
    return "".join(res)
    

def objets_voisinage(l_arene:dict, num_joueur, dist_max:int):
    """Retourne un dictionnaire indiquant pour chaque direction possibles, 
        les objets ou boites pouvant être mangés par le serpent du joueur et
        se trouvant dans voisinage de la tête du serpent 

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur considéré
        dist_max (int): le nombre de cases maximum qu'on s'autorise à partir du point de départ
    Returns:
        dict: un dictionnaire dont les clés sont des directions  et les valeurs une liste de triplets
            (distance,val_objet,prop) où distance indique le nombre de cases jusqu'à l'objet et id_objet
            val_obj indique la valeur de l'objet ou de la boite et prop indique le propriétaire de la boite
    """
    directions = directions_possibles(l_arene, num_joueur)
    serp = arene.get_serpent(l_arene,num_joueur)[0]
    x,y=serp[0],serp[1]
    voisinage = {direction: [] for direction in directions}
    queue = [(x, y, 0)]
    visited = set()

    while queue:
        x, y, dist = queue.pop(0)
        if dist > dist_max:
            continue
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if dist > 0:
            val_objet = arene.get_val_boite(l_arene, x, y)
            prop = arene.get_proprietaire(l_arene, x, y)
            for direction in directions:
                voisinage[direction].append((dist, val_objet, prop))

        for dx, dy, direction in [(-1, 0, 'N'), (1, 0, 'S'), (0, -1, 'E'), (0, 1, 'O')]:
            nx, ny = x + dx, y + dy
            lgn, col = arene.get_dim(l_arene)
            if 0 <= nx < lgn and 0 <= ny < col and not arene.est_mur(l_arene, nx, ny):
                queue.append((nx, ny, dist + 1))

    return voisinage


def choix_box(l_arene:dict,num_joueur:int,dist_max:int)->tuple:
    """Renvoie le choix de la cellule à récupérer selon les points, la distance, la distance avec d'autres serpents etc

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur considéré
        dist_max (int): le rayon de la zone à analyser

    Returns:
        tuple: la cellule qui nous intéresse le plus
    """  
    choix_direction=None
    directions=objets_voisinage(l_arene,num_joueur,dist_max)
    score_ch=0
    for x,y in directions.items():
        compteur=0
        score=0
        while compteur<len(y):
            score+=y[compteur][1]/y[compteur][0]
            if choix_direction is None or score>score_ch:
                choix_direction=x
                score_ch=score
            compteur+=1
    return choix_direction

def mon_IA2(num_joueur:int, la_partie:dict)->str:
    """Fonction qui va prendre la decision du prochain coup pour le joueur de numéro ma_couleur

    Args:
        num_joueur (int): un entier désignant le numero du joueur qui doit prendre la décision
        la_partie (dict): structure qui contient la partie en cours

    Returns:
        str: une des lettres 'N', 'S', 'E' ou 'O' indiquant la direction que prend la tête du serpent du joueur
    """
    direction=random.choice("NSEO")
    global direction_prec
    dir_pos=directions_possibles(partie.get_arene(la_partie),num_joueur)
    print(f'les directions possibles pour {num_joueur}:{dir_pos}')
    dir_pos=choix_box(partie.get_arene(la_partie),num_joueur,10)
    print(f'le joueur{num_joueur} a pris {dir_pos}')
    if not dir_pos:
        direction = direction_prec  # Continue dans la dernière direction viable
        if direction_prec=="N":
            direction="S"
        elif direction_prec=="S":
            direction="N"
        elif direction_prec=="E":
            direction="O"
        elif direction_prec=="O":
            direction="E"
    else:
        direction = random.choice(dir_pos)
    direction_prec = direction
    return direction
def mon_IA(num_joueur:int, la_partie:dict)->str:
    """Fonction qui va prendre la decision du prochain coup pour le joueur de numéro ma_couleur

    Args:
        num_joueur (int): un entier désignant le numero du joueur qui doit prendre la décision
        la_partie (dict): structure qui contient la partie en cours

    Returns:
        str: une des lettres 'N', 'S', 'E' ou 'O' indiquant la direction que prend la tête du serpent du joueur
    """
    direction=random.choice("NSEO")
    direction_prec=direction #La décision prise sera la direction précédente le prochain tour
    dir_pos=arene.directions_possibles(partie.get_arene(la_partie),num_joueur)
    if dir_pos=='':
        direction=random.choice('NOSE')
    else:
        direction=random.choice(dir_pos)
    return direction







if __name__=="__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu,_=le_client.prochaine_commande()
        if ok:
            la_partie=partie.partie_from_str(le_jeu)
            actions_joueur=mon_IA2(int(id_joueur),la_partie)
            le_client.envoyer_commande_client(actions_joueur)
    le_client.afficher_msg("terminé")


