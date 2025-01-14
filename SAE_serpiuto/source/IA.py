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
import matrice
direction_prec='X' # variable indiquant la décision précédente prise par le joueur. A mettre à jour soi-même

####################################################################
### A partir d'ici, implémenter toutes les fonctions qui vous seront 
### utiles pour prendre vos décisions
### Toutes vos fonctions devront être documentées
####################################################################

def est_sur_arene(l_arene,pos):
    """Fonction qui indique si la position pos est sur l'arène
        
        Args:
            l_arene (dict): l'arène considérée
            pos (tuple): la position à tester

        Returns:
            (bool): True si la position est sur l'arène, False sinon
    """
    lgn,col=arene.get_dim(l_arene)
    if 0<=pos[0]<lgn and 0<=pos[1]<col:
        return True
    return False

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
            qu'aucune direction ne soit possible donc la fonction peut retourner la chaine vide
    """    
    res=""
    serp=[arene.get_serpent[l_arene,num_joueur][0],arene.get_serpent[l_arene,num_joueur][1]]
    val_tete=arene.get_val_boite(l_arene,serp[0],serp[1])
    lgn,col=arene.get_dim(arene)
    if 0<=serp[0]-1 <= lgn and not arene.est_mur(serp[1],serp[0]-1)  and arene.get_val_boite(l_arene,serp[0]-1,serp[1])<=val_tete:
        res+="N"
    if col>=serp[1]+1 >= 0 and not arene.est_mur(serp[0],serp[1]+1) and arene.get_val_boite(l_arene,serp[0],serp[1]+1)<=val_tete: 
        res+="O"
    if 0<=serp[0]+1 <= lgn and not arene.est_mur(serp[1],serp[0]+1) and arene.get_val_boite(l_arene,serp[0]+1,serp[1])<=val_tete:
        res+="S"
    if col>=serp[1]-1 >= 0 and not arene.est_mur(serp[0],serp[1]-1) and arene.get_val_boite(l_arene,serp[0],serp[1]-1)<=val_tete:
        res+="E"

def get(l_arene,pos):
    if est_sur_arene(l_arene,pos):
        return matrice.get_val(l_arene["matrice"], pos[0], pos[1])

def calque(l_arene,num_joueur:int):
    """Fabrique le calcque de l'arene en utilisant l'inondation
    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur considéré

    Returns:
        matrice: le calcque de l'arène créé à partir de l'inondation
    """
    lgn,col=arene.get_dim(l_arene)
    calque=matrice.Matrice(lgn,col)
    i=0
    fin=(lgn-1,col-1)
    while get(l_arene,fin) is None or charge is True :
        charge=False
        for ligne in range(lgn):
            for colonne in range(col):
                pos=(ligne,colonne)
                voisins_calque=((pos[0]-1,pos[1]),(pos[0]+1,pos[1]),(pos[0],pos[1]-1),(pos[0],pos[1]+1))
                for voisin in voisins_calque:
                    if est_sur_arene(l_arene, voisin) and get(calque, voisin) == i and get(calque, pos) is None and not arene.est_mur(l_arene, pos[0], pos[1]):
                        matrice.set_val(calque,pos[0],pos[1],i+1)
                        charge=True
        i+=1
    return calque

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
    res={"N":[],"S":[],"E":[],"O":[]}
    serp=arene.get_serpent(l_arene, num_joueur)[0]
    tete=serp["pos"][0]
    calque=calque(l_arene, num_joueur)
    directions={"N":(-1, 0),"S":(1, 0),"E":(0, -1),"O":(0, +1)}
    for direction,(dx, dy) in directions.items():
        for dist in range(1,dist_max+1):
            pos=(tete[0]+dx*dist,tete[1]+dy*dist)
            if est_sur_arene(l_arene,pos):
                val=get(calque,pos)
                if val is not None:
                    obj=arene.get_objet(l_arene, pos)
                    if obj:
                        res[direction].append((dist,obj["valeur"],obj["proprietaire"]))
                    elif arene.est_boite(l_arene,pos):
                        boite=arene.get_boite(l_arene,pos)
                        res[direction].append((dist,boite["valeur"],boite["proprietaire"]))
    return res

def mon_IA2(num_joueur:int, la_partie:dict)->str:
    return 'N'

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
            actions_joueur=mon_IA(int(id_joueur),la_partie)
            le_client.envoyer_commande_client(actions_joueur)
    le_client.afficher_msg("terminé")