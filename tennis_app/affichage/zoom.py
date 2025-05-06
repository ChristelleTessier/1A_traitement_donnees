import pandas as pd


def zoom_annee(data):
    """
    Filtre les données en fonction d'une ou plusieurs années sélectionnées
    par l'utilisateur.

    Paramètres:
        data (pd.DataFrame): Le DataFrame contenant une colonne 'annee'
        (années des tournois).

    Returns:
        pd.DataFrame:
            Un sous-ensemble du DataFrame original, filtré selon
            les années choisies.
    """
    from ..logique.fonctions_divers import choix_dans_liste

    annee_liste = sorted(data['annee'].unique())

    print("=== Filtrage des années ===")
    annees_choisies = choix_dans_liste(annee_liste, [])

    data_filtrée = data[data['annee'].isin(annees_choisies)].copy()
    return data_filtrée


def zoom_level(data):
    """
    Filtre les données en fonction des niveaux de tournoi sélectionnés
    par l'utilisateur.

    Paramètres:
        data (pd.DataFrame): Le DataFrame contenant une colonne
        'tourney_level' (niveau de tournoi).

    Returns:
        pd.DataFrame: Un sous-ensemble du DataFrame filtré par les
         niveaux de tournoi choisis.
    """
    from ..logique.fonctions_divers import choix_dans_liste

    level_liste = sorted(data['tourney_level'].dropna().unique())
    print("=== Filtrage par niveau de tournoi ===")
    niveaux_choisis = choix_dans_liste(level_liste, [])

    data_filtrée = data[data['tourney_level'].isin(niveaux_choisis)].copy()
    return data_filtrée


def zoom_surface(data):
    """
    Filtre les données en fonction des types de surface sélectionnés
    par l'utilisateur.

    Paramètres:
        data (pd.DataFrame):
            Le DataFrame contenant une colonne 'surface'
            (type de surface des tournois).

    Returns:
        pd.DataFrame:
            Un sous-ensemble du DataFrame filtré selon les surfaces choisies.
    """
    from ..logique.fonctions_divers import choix_dans_liste

    surface_liste = sorted(data['surface'].dropna().unique())
    print("=== Filtrage par type de surface ===")
    surfaces_choisies = choix_dans_liste(surface_liste, [])

    data_filtrée = data[data['surface'].isin(surfaces_choisies)].copy()
    return data_filtrée


def zoomer_tab_tournoi(joueur, victoire):
    """
    Filtre les résultats d'un joueur selon différents critères :
    année, niveau de tournoi, et surface.

    Paramètres:
        joueur (Joueur):
            L'objet représentant un joueur, utilisé pour récupérer
            ses résultats de tournois.
        victoire (bool):
            Si True, filtre uniquement les victoires.
            Si False, affiche tous les résultats.

    Returns:
        pd.DataFrame:
            Le DataFrame des résultats filtrés selon les critères choisis
            (année, niveau de tournoi, surface).
    """
    from ..logique.fonctions_divers import boucle_01

    data = joueur.chercher_resultat(victoire)
    print("\n_____________________________________________________")
    print("Voulez-vous préciser des informations ?")
    choix = boucle_01()

    if choix == '1':
        print("\n_____________________________________________________")
        print("Voulez-vous préciser la/les année(s) ?")
        choix = boucle_01()
        if choix == '1':
            data = zoom_annee(data)

        print("\n_____________________________________________________")
        print("Voulez-vous préciser le(s) niveaux de tournois ?")
        choix = boucle_01()
        if choix == '1':
            data = zoom_level(data)

        print("\n_____________________________________________________")
        print("Voulez-vous préciser les surface ?")
        choix = boucle_01()
        if choix == '1':
            data = zoom_surface(data)

    return data


def chercher_parcours(joueur, data):
    """
    Permet à l'utilisateur de consulter le parcours détaillé d'un joueur
    dans un tournoi spécifique.

    Paramètres:
        joueur (Joueur):
            L'objet représentant un joueur, utilisé pour récupérer
            ses résultats de tournois.
        data (pd.DataFrame):
            Les résultats des tournois à parcourir, qui peuvent être filtrés.

    Returns:
        pd.DataFrame or None:
            Le DataFrame des matchs dans le tournoi sélectionné, ou None si
            aucune sélection n'est faite.
    """
    from ..logique.fonctions_divers import boucle_01

    print(
        "Voulez vous connaitre le parcours du joueur sur un tournoi"
        " en particulier ?"
        )
    choix = boucle_01()

    if choix == "1":
        tournoi_id_liste = list(data["tourney_id"].unique())
        while True:
            tournoi_id = input(
                "Saisir l'indentificant du tournois (colonne 1) : "
                )
            if tournoi_id in tournoi_id_liste:
                break
            else:
                print("L'identificant du tournoi doit apartenir à la liste :")
                print(tournoi_id_liste)

        info_tournoi = data[data["tourney_id"] == tournoi_id].values[0]
        print(
            f"{info_tournoi[2]}, nom : {info_tournoi[3]}, "
            f"surface {info_tournoi[5]}, level {info_tournoi[4]}"
            )
        data2 = joueur.chercher_parcours_tournoi(tournoi_id)
    else:
        data2 = None

    return data2


def zoom_graph(data):
    """
    Permet à l'utilisateur de zoomer sur un intervalle de classement
    entre deux années.

    Paramètres:
        data (pd.DataFrame):
            Le DataFrame contenant une colonne 'ranking_date'
            (date de classement).

    Returns:
        pd.DataFrame:
            Le DataFrame filtré entre les deux années choisies
            par l'utilisateur.
    """
    from ..logique.fonctions_divers import boucle_01
    # S'assurer que 'ranking_date' est bien de type datetime
    data['ranking_date'] = pd.to_datetime(data['ranking_date'])

    # Extraire les années uniques et les trier
    annee_liste = sorted(data['ranking_date'].dt.year.unique())

    annees = []

    while len(annees) != 2:

        if annees == []:
            print("Année de départ :")
        else:
            print("Année de fin :")

        texte_liste = [
            f" {k+1} : {date}," for k, date in enumerate(annee_liste)
            ]
        texte = "".join(texte_liste) + ".\nIndiquer l'indice en réponse : "

        # Saisi de l'année
        while True:
            indice_annee_str = input(texte)
            try:
                annee_indice = int(indice_annee_str)
                if 1 <= annee_indice <= len(annee_liste):
                    # Si valeur est un indice de la liste on sort
                    break

                else:
                    print(
                        "Valeur invalide (valeur attendue entre 1 "
                        f"et {len(annee_liste)})"
                        )
            except ValueError:
                print(
                    "Erreur : Veuillez entrer indice entre 1 et "
                    f"{len(annee_liste)} (un nombre entier)."
                    )

        # Validation de l'annee
        if annees == []:
            print(
                "Vous souhaitez que le graphique commence pour l'annee : "
                f"{annee_liste[annee_indice - 1]} ?"
                )
        else:
            print(
                "Vous souhaitez que le graphique se termine pour l'annee : "
                f"{annee_liste[annee_indice - 1]} ?"
                )

        valide = boucle_01()
        if valide == "1":
            annees.append(annee_liste[annee_indice-1])
            annee_liste = annee_liste[annee_indice-1:]

        if len(annees) == 2:
            # Créer les bornes avec mois et jour au minimum / maximum
            date_debut = pd.to_datetime(f'{annees[0]}-01-01')
            date_fin = pd.to_datetime(f'{annees[1]}-12-31')

            # Filtrer le DataFrame
            data = data[
                (data['ranking_date'] >= date_debut) &
                (data['ranking_date'] <= date_fin)
                ]

    return data
