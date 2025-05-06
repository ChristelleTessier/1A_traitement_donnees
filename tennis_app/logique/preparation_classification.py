import pandas as pd


def preaprer_liste_id(genre, type=None, rang_max=None):
    """
    Prépare une liste d'identifiants de joueurs en fonction de leur genre et
    du type de données souhaitées (tous les joueurs ou seulement les classés).

    Args:
        genre (str):
            Genre des joueurs
            ('H' pour hommes, 'F' pour femmes, 'M' pour mixtes).
        type (str, optional):
            Type de joueurs à considérer.
            - None :
                tous les joueurs ayant joué en 2024.
            - 'classe' :
                uniquement les joueurs classés.
        rang_max (int, optional):
            Rang maximal pour filtrer les joueurs classés.

    Returns:
        list:
            Liste d'identifiants uniques des joueurs filtrés.
    """
    if type is None:

        if genre == "H":
            liste_fichier = [
                "Donnees/atp_matches_1968_2024.csv",
                "Donnees/atp_matches_futures_1992_2024.csv",
                "Donnees/atp_matches_qual_1978_2024.csv"
                ]
        elif genre == "F":
            liste_fichier = [
                "Donnees/wta_matches_1968_2024.csv",
                "Donnees/wta_matches_qual_1968_2024.csv"
                ]
        else:
            liste_fichier = [
                "Donnees/atp_matches_1968_2024.csv",
                "Donnees/atp_matches_futures_1992_2024.csv",
                "Donnees/atp_matches_qual_1978_2024.csv",
                "Donnees/wta_matches_1968_2024.csv",
                "Donnees/wta_matches_qual_1968_2024.csv"
                ]

        data = pd.DataFrame()
        for fichier in liste_fichier:
            data_temp = pd.read_csv(fichier, low_memory=False)
            data = pd.concat([data, data_temp], axis=0)

        data = data[data["annee"] == 2024]

        # Récupération d'un liste d'Id_joueur
        liste_id_win = list(data["winner_id"].unique())
        liste_id_los = list(data["loser_id"].unique())
        liste_id = list(set(liste_id_win + liste_id_los))

    else:
        if genre == "H":
            data = pd.read_csv("Donnees/atp_rankings.csv")
        elif genre == "F":
            data = pd.read_csv("Donnees/wta_rankings.csv")
        else:
            dataH = pd.read_csv("Donnees/atp_rankings.csv")
            dataF = pd.read_csv("Donnees/wta_rankings.csv")
            data = pd.concat([dataH, dataF], axis=0)

        date = (data["ranking_date"].unique()).max()
        data = data[data["ranking_date"] == date].copy()

        if rang_max is not None:
            data = data[data["rank"] < rang_max]

        # Récupération d'un liste d'Id_joueur
        liste_id = list(data["player"].unique())

    return liste_id


def choix_features(genre):
    """
    Permet à l'utilisateur de choisir les caractéristiques à utiliser
    pour la classification des joueurs.

    Args:
        genre (str):
            Genre des joueurs ('H', 'F' ou 'M').

    Returns:
        list:
            Liste des noms des caractéristiques sélectionnées.
    """
    from .fonctions_divers import boucle_01, choix_dans_liste, choix_invalide

    liste_possible = [
        "pourcentage_victoire_matchs",
        "pourcentage_victoire_tournois", "pourcentage_victoire_set1_perdu",
        "pourcentage_balle_break_sauvée", "pourcentage_sem_top_1_10",
        "pourcentage_sem_top_11_50", "pourcentage_sem_top_51_100",
        "main_dominante"
    ]
    if genre == 'M':
        liste_possible.append("genre")

    print(
        "Voulez-vous : \n"
        "prendre toutes les caractéristiques (0)"
        "\nchoisir des caractéristiques particulières (1)?"
    )
    choix = boucle_01()
    liste_choisie = []
    while True:
        if choix == "0":
            liste_choisie = liste_possible
            break
        elif choix == "1":
            liste_choisie = choix_dans_liste(liste_possible, liste_choisie)
            if len(liste_choisie) < 2:
                print("Il faut choisir au moins 2 caractéristiques")
            else:
                break
        else:
            choix_invalide()
            boucle_01()
    print(liste_choisie)

    return liste_choisie


def choix_nb_individu_groupe(liste_id):
    """
    Permet à l'utilisateur de choisir le nombre d'individus à inclure7
    dans l'analyse.

    Args:
        liste_id (list):
            Liste des identifiants de joueurs disponibles.

    Returns:
        int:
            Nombre d'individus sélectionnés pour l'analyse.
    """
    # Choix de nb_element pour construire la classification
    while True:
        print("_____________________________________________________")
        nb_element = input(
            f"saisir le nombre d'individu (max {len(liste_id)}) : "
            )
        try:
            nb_element_int = int(nb_element)
            if 11 <= nb_element_int <= len(liste_id):
                # Si valeur est un indice de la liste on sort
                break

            else:
                print(
                    "Valeur invalide (valeur attendue entre 11 et "
                    f"{len(liste_id)})"
                    )
        except ValueError:
            print(
                "Erreur : Veuillez entrer indice entre 11 et "
                f"{len(liste_id)} (un nombre entier)."
                )

    return nb_element_int


def preparer_joueurs(liste_id, genre, nb_element):
    """
    Prépare une liste d'objets Joueur valides à partir des identifiants
    fournis.

    Args:
        liste_id (list): Identifiants de joueurs.
        genre (str): Genre des joueurs ('H', 'F' ou 'M').
        nb_element (int): Nombre de joueurs souhaité.

    Returns:
        list: Liste d'objets Joueur valides.
    """
    from ..joueur.creer_joueur import creer_joueur
    import math
    import random

    if genre == 'H':
        data = [pd.read_csv("Donnees/atp_players.csv")]
    elif genre == 'F':
        data = [pd.read_csv("Donnees/wta_players.csv")]
    else:
        dataH = pd.read_csv("Donnees/atp_players.csv")
        dataF = pd.read_csv("Donnees/wta_players.csv")
        data = [dataH, dataF]

    joueurs = []  # Liste d'objets Joueur
    ids_utilisés = set()

    attributs_numeriques_a_verifier = [
        "nb_matchs_joue",
        "nb_tournois_joue",
        "prop_vic_set_1_perdu",
        "prop_balle_break_sauvee",
        "nb_sem_classe"
    ]

    # Recherche aléatoire de nb_element par découpage en groupe pour
    # par calculer tous les joueurs
    while len(joueurs) < nb_element:
        # Prendre des IDs qu'on n'a pas encore essayés
        ids_restants = [id for id in liste_id if id not in ids_utilisés]

        if not ids_restants:
            print(
                f"Plus de joueurs disponibles. Seulement {len(joueurs)} "
                "joueurs valides trouvés.")
            return joueurs

        # Prendre un lot de joueurs à essayer
        taille_lot = min(50, len(ids_restants), nb_element - len(joueurs))
        lot_ids = random.sample(ids_restants, taille_lot)

        for id in lot_ids:
            ids_utilisés.add(id)
            joueur = creer_joueur(id=id, info=(data, genre))

            if joueur is not None:
                est_valide = True
                for attribut in attributs_numeriques_a_verifier:
                    try:
                        valeur_attribut = getattr(joueur, attribut)
                        if math.isnan(valeur_attribut):
                            est_valide = False
                            break
                    except AttributeError:
                        est_valide = False
                        break

                if est_valide:
                    joueurs.append(joueur)
                    if len(joueurs) >= nb_element:
                        break

    return joueurs


def preparer_features(joueur, features_choisies):
    """
    Extrait les caractéristiques numériques d’un joueur selon les
    features choisies.

    Args:
        joueur (object):
            Instance d’un joueur.
        features_choisies (list):
            Noms des caractéristiques à extraire.

    Returns:
        list:
            Valeurs numériques correspondant aux caractéristiques
            sélectionnées.
    """
    features = []

    if "pourcentage_victoire_matchs" in features_choisies:
        # Pourcentage victoires/tournois
        features.append(
            joueur.nb_matchs_gagne / joueur.nb_matchs_joue*100
            if joueur.nb_matchs_joue != 0 else 0
            )

    if "pourcentage_victoire_tournois" in features_choisies:
        # Pourcentage victoires/tournois
        features.append(
            joueur.nb_tournois_gagne / joueur.nb_tournois_joue*100
            if joueur.nb_tournois_joue != 0 else 0
            )

    if "pourcentage_victoire_set1_perdu" in features_choisies:
        features.append(joueur.prop_vic_set_1_perdu)

    if "pourcentage_balle_break_sauvée" in features_choisies:
        features.append(joueur.prop_balle_break_sauvee)

    if "pourcentage_sem_top_1_10" in features_choisies:
        features.append(
            joueur.nb_sem_1_10 / joueur.nb_sem_classe * 100
            if joueur.nb_sem_classe != 0 else 0
        )

    if "pourcentage_sem_top_11_50" in features_choisies:
        features.append(
            joueur.nb_sem_11_50 / joueur.nb_sem_classe * 100
            if joueur.nb_sem_classe != 0 else 0
        )

    if "pourcentage_sem_top_51_100" in features_choisies:
        features.append(
            joueur.nb_sem_51_100 / joueur.nb_sem_classe * 100
            if joueur.nb_sem_classe != 0 else 0
        )

    if "main_dominante" in features_choisies:
        if joueur.main == 'R':
            features.extend([100, 0])  # [est_droitier, est_gaucher]
        elif joueur.main == 'L':
            features.extend([0, 100])
        else:
            features.extend([0, 0])

    if "genre" in features_choisies:
        if joueur.sexe == 'F':
            features.extend([0, 100])
        else:
            features.extend([100, 0])

    return features


def preparer_donnees(joueurs, features):
    """
    Prépare les données pour l'algorithme de clustering.

    Args:
        joueurs (list):
            Liste d'objets Joueur.
        features (list):
            Caractéristiques sélectionnées.

    Returns:
        tuple:
            - X (np.ndarray):
                Matrice des caractéristiques.
            - noms_joueurs (list):
                Liste des noms complets des joueurs.
    """
    import numpy as np

    X = []
    noms_joueurs = []

    for joueur in joueurs:
        features_joueur = preparer_features(joueur, features)
        X.append(features_joueur)
        noms_joueurs.append(f"{joueur.prenom} {joueur.nom}")

    # Convertir en array numpy
    X = np.array(X)

    return X, noms_joueurs
