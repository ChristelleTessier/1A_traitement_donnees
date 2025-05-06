import pandas as pd
from .class_joueur import Joueur


def creer_joueur(*, id=None, prenom=None, nom=None, data=None, info=None):
    """
    Crée un objet Joueur à partir de son ID, ou de son prénom et nom.
    Si les informations sont manquantes, la fonction effectue une recherche
    dans les données disponibles.

    Les arguments sont des arguments de type "keyword-only"
    (doivent être spécifiés par leur nom).

    Args:
        id (str, optional):
            L'identifiant unique du joueur. Si non fourni, une recherche par
            prénom et nom est effectuée.
        prenom (str, optional):
            Le prénom du joueur. Doit être spécifié si l'ID n'est pas fourni.
        nom (str, optional):
            Le nom de famille du joueur. Doit être spécifié si l'ID n'est
            pas fourni.
        data (optional):
            Une structure de données (par exemple, un DataFrame) contenant les
            informations des joueurs. Non utilisé directement dans cette
            version de la fonction.
        info (tuple, optional):
            Un tuple contenant des données supplémentaires, sous forme de
            liste de DataFrames et du sexe ('H' ou 'F').

    Returns:
        Joueur or None:
            Retourne un objet Joueur si les informations sont trouvées et
            valides, sinon None si aucune correspondance n'est trouvée.

    Notes:
        - Si un `id` est fourni, la fonction recherche dans les fichiers CSV
        des joueurs ATP/WTA pour récupérer les données correspondantes.
        - Si ni l'ID, ni le prénom/nom ne sont fournis,
        la fonction retourne `None`.
        - La fonction peut rechercher un joueur parmi deux DataFrames,
        un pour les hommes et un pour les femmes (ATP/WTA).
    """

    if id is None and (prenom is None or nom is None):
        return None

    ligne_joueur = None

    # Récupération de la bonne ligne
    if id is not None:
        if info is None:
            print("Chargement des données.")
            # Chargement des joueurs ATP/WTA
            data_homme = pd.read_csv(
                "Donnees/atp_players.csv", low_memory=False
                )
            data_femme = pd.read_csv(
                "Donnees/wta_players.csv", low_memory=False
                )

            if id in data_homme["player_id"].values:
                ligne_joueur = data_homme[data_homme["player_id"] == id]
                genre = "H"
            elif id in data_femme["player_id"].values:
                ligne_joueur = data_femme[data_femme["player_id"] == id]
                genre = "F"
            else:
                genre = None

        else:
            liste_data, genre = info
            if len(liste_data) == 1:
                data = liste_data[0]
                ligne_joueur = data[data["player_id"] == id]
            else:
                dataH = liste_data[0]
                dataF = liste_data[1]
                if id in list(dataH["player_id"].unique()):
                    genre = "H"
                    ligne_joueur = dataH[dataH["player_id"] == id]
                elif id in list(dataF["player_id"].unique()):
                    genre = "F"
                    ligne_joueur = dataF[dataF["player_id"] == id]

    elif (prenom is not None) and (nom is not None):

        data_homme = pd.read_csv("Donnees/atp_players.csv", low_memory=False)
        data_femme = pd.read_csv("Donnees/wta_players.csv", low_memory=False)

        # Recherche chez les hommes
        ligne_joueur = data_homme[
            (data_homme["name_last"] == nom) &
            (data_homme["name_first"] == prenom)
        ]

        if not ligne_joueur.empty:
            genre = "H"
        else:
            # Recherche chez les femmes
            ligne_joueur = data_femme[
                (data_femme["name_last"] == nom) &
                (data_femme["name_first"] == prenom)
            ]
            if not ligne_joueur.empty:
                genre = "F"

    # Création du joueur
    if not ligne_joueur.empty:
        joueur = Joueur(
            id_joueur=ligne_joueur["player_id"].values[0],
            prenom=ligne_joueur["name_first"].values[0],
            nom=ligne_joueur["name_last"].values[0],
            sexe=genre,
            date_nais=ligne_joueur['dob'].values[0],
            main=ligne_joueur['hand'].values[0],
            nb_tournois_joue=ligne_joueur['nb_tournois_joue'].values[0],
            nb_tournois_gagne=ligne_joueur['nb_tournois_gagne'].values[0],
            nb_matchs_joue=ligne_joueur['nb_matchs_joue'].values[0],
            nb_matchs_gagne=ligne_joueur['nb_matchs_gagne'].values[0],
            prop_vic_set_1_perdu=(
                ligne_joueur["prop_vic_set_1_perdu"].values[0]
            ),
            prop_balle_break_sauvee=(
                ligne_joueur["prop_balle_break_sauvee"].values[0]
            ),
            nb_sem_classe=ligne_joueur["nb_sem_classe"].values[0],
            nb_sem_1_10=ligne_joueur["nb_sem_1_10"].values[0],
            nb_sem_11_50=ligne_joueur["nb_sem_11_50"].values[0],
            nb_sem_51_100=ligne_joueur["nb_sem_51_100"].values[0],
            date1=ligne_joueur['first_match_date'].values[0],
            date2=ligne_joueur['last_match_date'].values[0])
    else:
        joueur = None

    return joueur
