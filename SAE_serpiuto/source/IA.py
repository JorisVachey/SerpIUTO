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

# Variable indiquant la décision précédente prise par le joueur. A mettre à jour soi-même
direction_prec = 'X'

####################################################################
### A partir d'ici, implémenter toutes les fonctions qui vous seront 
### utiles pour prendre vos décisions
### Toutes vos fonctions devront être documentées
####################################################################

def get_tout_serpent(arene, num_joueur):
    """
    Renvoie le dictionnaire entier du serpent du numéro choisi.

    Args:
        arene (dict): arène considérée
        num_joueur (int): le numéro du joueur choisi

    Returns:
        dict: Dictionnaire du serpent du joueur choisi
    """
    return arene["serpents"][num_joueur - 1]

def est_sur_arene(l_arene, pos):
    """
    Indique si la position pos est sur l'arène.

    Args:
        l_arene (dict): l'arène considérée
        pos (tuple): la position à tester

    Returns:
        bool: True si la position est sur l'arène, False sinon
    """
    lgn, col = arene.get_dim(l_arene)
    return 0 <= pos[0] < lgn and 0 <= pos[1] < col

def directions_possibles(l_arene, num_joueur):
    """
    Indique les directions possibles pour le joueur num_joueur.

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur

    Returns:
        str: Une chaîne composée de NOSE indiquant les directions possibles
    """
    res = []
    serp = arene.get_serpent(l_arene, num_joueur)[0]
    x, y = serp[0], serp[1]
    tete = arene.get_val_boite(l_arene, x, y)
    lgn, col = arene.get_dim(l_arene)

    directions = {
        "N": (x - 1, y),
        "O": (x, y - 1),
        "S": (x + 1, y),
        "E": (x, y + 1)
    }

    for dir, (nx, ny) in directions.items():
        if est_sur_arene(l_arene, (nx, ny)) and (
            not arene.est_mur(l_arene, nx, ny) or serpent.get_temps_mange_mur(l_arene["serpents"][num_joueur - 1]) > 1
        ) and (
            arene.get_val_boite(l_arene, nx, ny) <= tete or serpent.get_temps_surpuissance(l_arene["serpents"][num_joueur - 1]) > 1
        ):
            res.append(dir)

    random.shuffle(res)
    return "".join(res)

def get(l_arene, pos):
    """
    Retourne la valeur de la case à la position donnée.

    Args:
        l_arene (dict): l'arène considérée
        pos (tuple): la position à tester

    Returns:
        int: La valeur de la case à la position donnée ou None si la position n'est pas sur l'arène
    """
    if est_sur_arene(l_arene, pos):
        return arene.get_val_boite(l_arene, pos[0], pos[1])

def fabriquer_calque(l_arene, num_joueur):
    """
    Fabrique le calque de l'arène en utilisant l'inondation.

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur considéré

    Returns:
        matrice.Matrice: Le calque de l'arène créé à partir de l'inondation
    """
    lgn, col = arene.get_dim(l_arene)
    calque = matrice.Matrice(lgn, col)
    serp = arene.get_serpent(l_arene, num_joueur)[0]
    matrice.set_val(calque, serp[0], serp[1], 0)
    i = 0
    charge = True

    while charge:
        charge = False
        for ligne in range(lgn):
            for colonne in range(col):
                pos = (ligne, colonne)
                voisins_calque = [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]), (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]
                for voisin in voisins_calque:
                    if est_sur_arene(l_arene, voisin) and matrice.get_val(calque, voisin[0], voisin[1]) == i and matrice.get_val(calque, pos[0], pos[1]) is None and not arene.est_mur(l_arene, pos[0], pos[1]):
                        matrice.set_val(calque, pos[0], pos[1], i + 1)
                        charge = True
        i += 1

    return calque

def objets_voisinage(l_arene, num_joueur, dist_max):
    """
    Retourne un dictionnaire indiquant pour chaque direction possible,
    les objets ou boîtes pouvant être mangés par le serpent du joueur et
    se trouvant dans le voisinage de la tête du serpent.

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur considéré
        dist_max (int): le nombre de cases maximum qu'on s'autorise à partir du point de départ

    Returns:
        dict: Un dictionnaire dont les clés sont des directions et les valeurs une liste de triplets
              (distance, val_objet, prop)
    """
    dire = directions_possibles(l_arene, num_joueur)
    res = {d: [] for d in dire}
    serp = arene.get_serpent(l_arene, num_joueur)[0]
    val_tete = arene.get_val_boite(l_arene, serp[0], serp[1])
    calque = fabriquer_calque(l_arene, num_joueur)
    directions = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "O": (0, -1)}
    directions = {d: (dx, dy) for d, (dx, dy) in directions.items() if d in dire}

    for direction, (dx, dy) in directions.items():
        for dist in range(1, dist_max + 1):
            pos = (serp[0] + dx * dist, serp[1] + dy * dist)
            if est_sur_arene(l_arene, pos):
                if 0 < arene.get_val_boite(l_arene, pos[0], pos[1]) <= val_tete:
                    res[direction].append((dist, arene.get_val_boite(l_arene, pos[0], pos[1]), arene.get_proprietaire(l_arene, pos[0], pos[1])))

    return res

def calculer_score_direction(l_arene, num_joueur, serp, objets):
    """
    Calcule le score pour une direction donnée en fonction des objets dans cette direction.

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur considéré
        serp (tuple): position de la tête du serpent
        objets (list): liste des objets dans cette direction

    Returns:
        int: Le score calculé pour la direction
    """
    score_dist = {1: 100, 2: 80, 3: 60, 4: 40, 5: 30, 6: 20, 7: 16, 8: 12, 9: 8, 10: 6, 11: 4, 12: 4, 13: 2, 14: 2, 15: 2}
    val_par_obj = {0: 2, 1: 10, 2: 20, -1: 16, -2: 24, -3: 12}
    score = 0

    for dist, val_obj, prop in objets:
        if val_obj in val_par_obj.keys() and prop != arene.get_proprietaire(l_arene, serp[0], serp[1]):
            score += score_dist[dist] * val_par_obj[val_obj] / dist
        elif val_obj >= 3:
            if (arene.get_val_boite(l_arene, serp[0], serp[1]) > arene.get_val_boite(l_arene, dist, val_obj) or serpent.get_temps_surpuissance(l_arene["serpents"][num_joueur - 1]) > dist) and serpent.get_temps_protection(get_tout_serpent(l_arene, num_joueur)) < dist:
                score += (val_obj / dist) * 6
        else:
            score -= 20

    return score

def choix_box(l_arene, num_joueur, dist_max):
    """
    Renvoie le choix de la cellule à récupérer selon les points, la distance, la distance avec d'autres serpents, etc.

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur considéré
        dist_max (int): le rayon de la zone à analyser

    Returns:
        str: La direction qui nous intéresse le plus
    """
    directions = objets_voisinage(l_arene, num_joueur, dist_max)
    serp = arene.get_serpent(l_arene, num_joueur)[0]
    choix_direction, score_ch = None, float('-inf')

    for direction, objets in directions.items():
        score = calculer_score_direction(l_arene, num_joueur, serp, objets)
        if choix_direction is None or score > score_ch:
            choix_direction, score_ch = direction, score
        print(f'La direction {direction} a un score de {score}')

    return choix_direction

def mon_IA2(num_joueur, la_partie):
    """
    Fonction qui va prendre la décision du prochain coup pour le joueur de numéro ma_couleur.

    Args:
        num_joueur (int): un entier désignant le numéro du joueur qui doit prendre la décision
        la_partie (dict): structure qui contient la partie en cours

    Returns:
        str: une des lettres 'N', 'S', 'E' ou 'O' indiquant la direction que prend la tête du serpent du joueur
    """
    global direction_prec
    dir_pos = directions_possibles(partie.get_arene(la_partie), num_joueur)
    print(f'Les directions possibles pour {num_joueur}: {dir_pos}')
    dir_choisie = choix_box(partie.get_arene(la_partie), num_joueur, 14)
    print(f'Le joueur {num_joueur} a pris {dir_choisie}')

    if dir_choisie is None:
        if direction_prec == "N":
            dir_choisie = "S"
        elif direction_prec == "S":
            dir_choisie = "N"
        elif direction_prec == "E":
            dir_choisie = "O"
        elif direction_prec == "O":
            dir_choisie = "E"
    else:
        dir_choisie = random.choice(dir_choisie)

    direction_prec = dir_choisie  # La décision prise sera la direction précédente le prochain tour
    return dir_choisie

def mon_IA(num_joueur, la_partie):
    """
    Fonction qui va prendre la décision du prochain coup pour le joueur de numéro ma_couleur.

    Args:
        num_joueur (int): un entier désignant le numéro du joueur qui doit prendre la décision
        la_partie (dict): structure qui contient la partie en cours

    Returns:
        str: une des lettres 'N', 'S', 'E' ou 'O' indiquant la direction que prend la tête du serpent du joueur
    """
    direction = random.choice("NSEO")
    direction_prec = direction  # La décision prise sera la direction précédente le prochain tour
    dir_pos = arene.directions_possibles(partie.get_arene(la_partie), num_joueur)

    if dir_pos == '':
        direction = random.choice('NOSE')
    else:
        direction = random.choice(dir_pos)

    return direction

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)

    args = parser.parse_args()
    le_client = client.ClientCyber()
    le_client.creer_socket(args.serveur, args.port)
    le_client.enregistrement(args.nom_equipe, "joueur")
    ok = True

    while ok:
        ok, id_joueur, le_jeu, _ = le_client.prochaine_commande()
        if ok:
            la_partie = partie.partie_from_str(le_jeu)
            actions_joueur = mon_IA2(int(id_joueur), la_partie)
            le_client.envoyer_commande_client(actions_joueur)

    le_client.afficher_msg("terminé")
