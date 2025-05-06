import os

from ..logique.fonctions_divers import effacer_terminal


def menu_principal():
    """
    Affiche le menu principal de l'application.

    Propose à l'utilisateur les options suivantes :
    - Étude de données d'un joueur.
    - Lancer une classification de groupes de joueurs.
    - Quitter l'application.
    """
    effacer_terminal()
    print("\n ########## Menu Principal ########## \n")

    print("\n1. Faire de l'étude de données")
    print("2. Faire de la classification")

    print("\n ############################## \n")

    print("10. Quitter")

    print("\n ############################## \n")


def menu_joueur(joueur):
    """
    Affiche le menu principal de l'application.

    En fonction de la présence ou non d'un joueur sélectionné,
    le menu propose différentes options (sélection, affichage d'infos,
    analyses, prédiction, etc.).

    Args:
        joueur (Joueur or None):
            Le joueur sélectionné dont on souhaite analyser les adversaires.
    """
    effacer_terminal()
    print("\n ########## Menu JOUEUR ########## \n")

    if joueur is None:
        print("\n1. Saisir le nom/prenom d'un joueur")
    else:
        print(f"\nJoueur Sélectionné : {joueur.prenom} {joueur.nom}")
        print("1. Choisir un autre joueur ")
        print("2. Les informations du joueur")
        print("3. Les adversaires")
        print("4. Le palmares du joueur par tournois")
        print("5. L'évolution du rangs sur la carrière")

    print("\n ############################## \n")

    print("10. Revenir au menu principal")

    print("\n ############################## \n")


def sous_menu_3(joueur):
    """
    Affiche le sous-menu lié à l'analyse des adversaires d'un joueur.

    Ce menu affiche la liste des 10 adversaires les plus fréquents
    pour le joueur sélectionné. Si aucune donnée n'est trouvée,
    un message s'affiche.

    Args:
        joueur (Joueur):
            Le joueur sélectionné dont on souhaite analyser les adversaires.
    """
    from ..affichage.afficher import afficher_tournoi
    from ..logique.fonctions_divers import boucle_01
    from ..logique.fonctions_enregistrement import sauvegarder_data

    effacer_terminal()
    print("\n ########## Menu comparaison ########## \n")

    data = joueur.cherche_10_joueur()

    if data is not None and not data.empty:
        print(f"Sous menu : Les adversaires de {joueur.prenom} {joueur.nom} ?")
        afficher_tournoi(data)

        print("\nVoulez-vous sauvegarder la liste des adversaires ?")
        choix = boucle_01()
        if choix == "1":
            # Créer le dossier principal si nécessaire
            dossier_principal = "enregistrement"
            os.makedirs(dossier_principal, exist_ok=True)

            # Créer le dossier spécifique au joueur si nécessaire
            dossier = os.path.join(
                dossier_principal,
                f"{joueur.nom}_{joueur.prenom}"
                )

            # Creation du nom
            nom = f"Adversaires_de_{joueur.nom}_{joueur.prenom}"

            # Enregistrement
            sauvegarder_data(data, dossier, nom)

    else:
        print("Aucun adversaire trouvé.")

    print("1. Saisir un deuxième joueur")

    print("\n ############################## \n")

    print("10. Revenir au menu joueur")

    print("\n ############################## \n")


def sous_menu_32(joueur1, joueur2):
    """
    Affiche le sous-menu permettant de comparer deux joueurs.

    Options disponibles :
    - Comparaison des statistiques individuelles.
    - Historique des confrontations.
    - Évolution des rangs au cours de leur carrière.

    Args:
        joueur1 (Joueur): Premier joueur à comparer.
        joueur2 (Joueur): Deuxième joueur à comparer.
    """
    effacer_terminal()

    print(
        "########## "
        f"Sous menu : Comparer {joueur1.prenom} {joueur1.nom} "
        f"et {joueur2.prenom} {joueur2.nom}"
        " ##########\n"
    )
    print("1. Les statistiques des deux joueurs")
    print("2. Les rencontres des deux joueurs")
    print("3. L'évolution des rangs des deux joueurs")

    print("\n ############################## \n")

    print("10. Revenir au menu joueur")

    print("\n ############################## \n")


def sous_menu_4(joueur):
    """
    Affiche le sous-menu relatif au palmarès du joueur.

    Options disponibles :
    - Résultats généraux dans les tournois.
    - Nombre de victoires par tournoi.

    Args:
        joueur (Joueur):
            Le joueur sélectionné dont on souhaite afficher le palmares.
    """
    effacer_terminal()

    print("\n ########## Menu PALMARES ########## \n")

    print(f"Sous menu : Le palmares de {joueur.prenom} {joueur.nom}\n")

    print("\n1. Les résultats aux différents tournois (général)")
    print("2. Les victoires aux différents tournois (général)")

    print("\n ############################## \n")

    print("10. Revenir au menu joueur")

    print("\n ############################## \n")


def menu_classification():
    """
    Affiche le menu principal des options de classification.

    Propose à l'utilisateur de choisir le type de groupe de joueurs
    à classifier (hommes, femmes, mixte, classés ou non).
    """
    effacer_terminal()

    print("\n ########## Menu CLASSIFICATION ########## \n")

    print('Que voulez vous classifier :')
    print("1. Un groupe d'homme quelconque")
    print("2. Un groupe d'homme classé")
    print("3. Un groupe de femme quelconque")
    print("4. Un groupe de femme classée")
    print("5. Un groupe mixte quelconque")
    print("6. un groupe mixte classe")

    print("\n ############################## \n")

    print("10. Revenir au menu principal")

    print("\n ############################## \n")


def sous_menu_classification():
    """
    Affiche le sous-menu permettant de travailler sur la classification.

    Propose à l'utilisateur les options pour afficher le graphique de
    classification, le tableau de répartition, trouver la classe d'un
    nouveau joueur et enregistrer la classification.
    """
    effacer_terminal()
    print("\n ########## Travailler sur la classification ########## \n")

    print("1. Afficher le graphique de classification")
    print("2. Afficher le tableau des centroïdes")
    print("3. Trouver la classe d'un nouveau joueur")
    print("4. Enregistrer la classification")

    print("\n ############################## \n")

    print("10. Revenir au menu classification")

    print("\n ############################## \n")
