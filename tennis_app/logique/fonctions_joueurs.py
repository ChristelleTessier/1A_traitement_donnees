import os
import datetime

from ..joueur.creer_joueur import creer_joueur
from ..affichage.afficher import (
    afficher_joueur,
    afficher_nuage_point,
    afficher_tournoi,
    afficher_matchs,
    afficher_nuage_point_deux_joueurs,
    afficher_matchs_rencontre
)
from ..menus.menu import (
    sous_menu_4,
    menu_joueur,
    sous_menu_3,
    sous_menu_32
)
from ..affichage.zoom import (
    zoom_graph,
    chercher_parcours,
    zoomer_tab_tournoi
)
from .fonctions_divers import (
    choix_invalide,
    boucle_01
)
from .fonctions_enregistrement import (
    sauvegarder_texte,
    sauvegarder_data,
    sauvegarder_figure
)


def creer_joueur_bis():
    """
    Permet de créer un nouveau joueur en demandant son prénom et nom.

    Returns:
        Joueur: L'instance du joueur nouvellement créé.
    """
    print("\n_____________________________________________________")
    prenom = input("\nEntrez le prénom du joueur : ")
    nom = input("Entrez le nom du joueur : ")
    joueur = creer_joueur(prenom=prenom, nom=nom)
    return joueur


def adversaire(joueur):
    """
    Affiche les adversaires les plus fréquents d'un joueur et permet de
    comparer avec un autre joueur.

    Cette fonction affiche un sous-menu qui permet à l'utilisateur
    de sélectionner un joueur adverse et de comparer leurs statistiques,
    parcours et confrontations.

    Args:
        joueur (Joueur):
            Instance du joueur principal avec lequel effectuer la comparaison.
    """
    while True:

        sous_menu_3(joueur)
        choix = input("Entrez votre choix : ")

        if choix == "1":
            joueur2 = creer_joueur_bis()

            if joueur2 is not None:
                print("Le joueur n'a pas été trouvé")
                input("Appuyer sur entrer pour continuer")
                comparaison(joueur, joueur2)

        elif choix == "10":
            break

        else:
            choix_invalide()


def comparaison(joueur1, joueur2):
    """
    Compare deux joueurs de tennis sur différents aspects (statistiques,
    confrontations, classement).

    Propose un sous-menu pour :
    - Afficher les fiches des deux joueurs.
    - Voir leurs matchs communs.
    - Visualiser leurs classements dans le temps (avec zoom possible).

    Args:
        joueur1 (Joueur):
            Premier joueur à comparer.
        joueur2 (Joueur):
            Deuxième joueur à comparer.
    """
    while True:
        sous_menu_32(joueur1, joueur2)
        choix = input("Entrez votre choix : ")

        if choix == "1":
            afficher_joueur(joueur1)
            afficher_joueur(joueur2)

            # Proposition enregistrement
            print(
                "\nVoulez-vous sauvegarder les informations sur les joueurs ?"
                )
            enregistrement = boucle_01()
            if enregistrement == "1":
                # Créer le dossier principal si nécessaire
                dossier_principal = "enregistrement"
                os.makedirs(dossier_principal, exist_ok=True)

                # Créer le dossier spécifique au joueur si nécessaire
                nom_sous_dossier = (
                    f"{joueur1.nom}_{joueur1.prenom}_VS_"
                    f"{joueur2.nom}_{joueur2.prenom}"
                )
                dossier = os.path.join(dossier_principal, nom_sous_dossier)

                # Creation du nom
                nom = "Comparaison_info_deux_joueurs"

                sauvegarder_texte([joueur1, joueur2], dossier, nom)
                input("\nAppuie sur Entrée pour continuer")

        elif choix == "2":
            data = joueur1.chercher_match_adversaire(joueur2)
            afficher_matchs_rencontre(data)

            # Proposer un enregistrement
            print("\nSouhaitez-vous enregistrer ce palmarès ? (0/1) : ")
            choix = boucle_01()
            if choix == "1":
                # Créer le dossier principal si nécessaire
                dossier_principal = "enregistrement"
                os.makedirs(dossier_principal, exist_ok=True)

                # Créer le dossier spécifique au joueur si nécessaire
                nom_sous_dossier = (
                    f"{joueur1.nom}_{joueur1.prenom}_VS_"
                    f"{joueur2.nom}_{joueur2.prenom}"
                )
                dossier = os.path.join(dossier_principal, nom_sous_dossier)

                # Creation du nom
                now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                nom = f"Evolution_des_rangs_des_deux_joueurs_{now}"

                # Enregistrement
                sauvegarder_data(data, dossier, nom)
                input("\nAppuie sur Entrée pour continuer")

        elif choix == "3":
            data = joueur1.comparer_rang(joueur2)
            fig = afficher_nuage_point_deux_joueurs(data, joueur1, joueur2)
            fig.show()

            # Proposer un enregistrement
            print("\nSouhaitez-vous enregistrer ce palmarès ? (0/1) : ")
            choix = boucle_01()
            if choix == "1":
                # Créer le dossier principal si nécessaire
                dossier_principal = "enregistrement"
                os.makedirs(dossier_principal, exist_ok=True)

                # Créer le dossier spécifique au joueur si nécessaire
                nom_sous_dossier = (
                    f"{joueur1.nom}_{joueur1.prenom}_VS_"
                    f"{joueur2.nom}_{joueur2.prenom}"
                )
                dossier = os.path.join(dossier_principal, nom_sous_dossier)

                # Creation du nom
                nom = "Rencontre_des_deux_joueurs"

                # Enregistrement
                sauvegarder_figure(fig, dossier, nom)
                input("\nAppuie sur Entrée pour continuer")

            print("Voulez-vous zommer sur une période ?")
            zoomer = boucle_01()
            while zoomer == '1':
                data2 = zoom_graph(data)
                fig = afficher_nuage_point_deux_joueurs(
                    data2,
                    joueur1,
                    joueur2
                    )
                fig.show()

                # Proposer un enregistrement
                print("\nSouhaitez-vous enregistrer ce palmarès ? (0/1) : ")
                choix = boucle_01()
                if choix == "1":
                    # Créer le dossier principal si nécessaire
                    dossier_principal = "enregistrement"
                    os.makedirs(dossier_principal, exist_ok=True)

                    # Créer le dossier spécifique au joueur si nécessaire
                    nom_sous_dossier = (
                        f"{joueur1.nom}_{joueur1.prenom}_VS_"
                        f"{joueur2.nom}_{joueur2.prenom}"
                    )
                    dossier = os.path.join(dossier_principal, nom_sous_dossier)

                    # Creation du nom
                    nom = "Rencontre_des_deux_joueurs"

                    # Enregistrement
                    sauvegarder_figure(fig, dossier, nom)
                    input("\nAppuie sur Entrée pour continuer")

                print("\nVoulez-vous effectuer un nouveau zoom ?")
                zoomer = boucle_01()

        elif choix == "10":
            break

        else:
            choix_invalide()


def palmares(joueur):
    """
    Affiche le palmarès d'un joueur, avec ses tournois joués et gagnés.

    Cette fonction permet de visualiser les tournois joués ou gagnés,
    de consulter le parcours d'un joueur dans un tournoi spécifique et
    d'afficher les matchs associés.

    Args:
        joueur (Joueur): Instance du joueur concerné par le palmarès.
    """
    while True:
        sous_menu_4(joueur)
        choix = input("Entrez votre choix : ")

        if choix == "1" or choix == "2":
            if choix == "2":
                victoire = True
                type = "victoire"
            else:
                victoire = False
                type = "participation"

            data = zoomer_tab_tournoi(joueur, victoire)

            if data is not None and not data.empty:
                data = data.sort_values(by="tourney_date")
                afficher_tournoi(data)

                # Proposer un enregistrement
                print("\nSouhaitez-vous enregistrer ce palmarès ? (0/1) : ")
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
                    now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                    nom = (
                        f"Palmares_de_{type}_de_{joueur.nom}_"
                        f"{joueur.prenom}_{now}"
                    )

                    # Enregistrement
                    sauvegarder_data(data, dossier, nom)
                    input("\nAppuie sur Entrée pour continuer")

                data2 = chercher_parcours(joueur, data)
                if data2 is not None:
                    afficher_matchs(data2)
                    # Proposer un enregistrement
                    print(
                        "\nSouhaitez-vous enregistrer le parcours ? (0/1) : "
                        )
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
                        now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                        nom = (
                            f"Parcours_dans_un_tournoi_de_{joueur.nom}_"
                            f"{joueur.prenom}_{now}"
                        )

                        # Enregistrement
                        sauvegarder_data(data, dossier, nom)
                    input("Cliquer sur entrer pour continuer")

                break
            else:
                print("Aucun résultat trouvé.")

        elif choix == "10":
            break

        else:
            choix_invalide()


def fonction_joueur(joueur_actuel):
    """
    Gère le sous-menu et les actions liées à un joueur.

    En fonction de l'action choisie, cette fonction permet de créer un joueur,
    afficher ses informations, comparer avec un adversaire,
    consulter son palmarès, ou explorer son classement.

    Args:
        joueur_actuel (Joueur or None):
            L'instance du joueur actuellement sélectionné
            (peut être None au début).

    Returns:
        Joueur or None:
            Le joueur sélectionné ou créé, ou None si l'action
            retourne au menu principal.
    """
    while True:
        menu_joueur(joueur_actuel)
        choix = input("Entrez votre choix : ")

        if choix == "10":
            return joueur_actuel  # Retourne au menu principal

        elif choix == "1":

            joueur = creer_joueur_bis()
            if joueur:
                joueur_actuel = joueur
            else:
                print("❌ Aucun joueur trouvé !")
                input("\nAppuie sur Entrée pour continuer")

        elif choix == "2":
            if joueur_actuel:
                afficher_joueur(joueur_actuel)

                # Proposition enregistrement
                print(
                    "\nVoulez-vous sauvegarder les informations du joueurs ?"
                    )
                enregistrement = boucle_01()
                if enregistrement == "1":
                    # Créer le dossier principal si nécessaire
                    dossier_principal = "enregistrement"
                    os.makedirs(dossier_principal, exist_ok=True)

                    # Créer le dossier spécifique au joueur si nécessaire
                    dossier = os.path.join(
                        dossier_principal,
                        f"{joueur_actuel.nom}_{joueur_actuel.prenom}"
                        )

                    # Creation du nom
                    nom = (
                        f"Evolution du rang_de_{joueur_actuel.nom}_"
                        f"{joueur_actuel.prenom}"
                    )

                    sauvegarder_texte([joueur_actuel], dossier, nom)
                    input("\nAppuie sur Entrée pour continuer")

            else:
                print("❌ Aucun joueur sélectionné. Créez un joueur d'abord !")
                input("\nAppuie sur Entrée pour continuer")

        elif choix == "3":
            if joueur_actuel:
                adversaire(joueur_actuel)
            else:
                print("❌ Aucun joueur sélectionné. Créez un joueur d'abord !")
                input("\nAppuie sur Entrée pour continuer")

        elif choix == "4":
            if joueur_actuel:
                palmares(joueur_actuel)
            else:
                print("❌ Aucun joueur sélectionné. Créez un joueur d'abord !")
                input("\nAppuie sur Entrée pour continuer")

        elif choix == "5":
            if joueur_actuel:
                data = joueur_actuel.chercher_rang()
                if data is not None and not data.empty:
                    data = data.sort_values(by="ranking_date")
                    fig = afficher_nuage_point(data)
                    fig.show()

                    # Proposition enregistrement
                    print("\nVoulez-vous sauvegarder le graphique ?")
                    enregistrement = boucle_01()
                    if enregistrement == "1":
                        # Créer le dossier principal si nécessaire
                        dossier_principal = "enregistrement"
                        os.makedirs(dossier_principal, exist_ok=True)

                        # Créer le dossier spécifique au joueur si nécessaire
                        dossier = os.path.join(
                            dossier_principal,
                            f"{joueur_actuel.nom}_{joueur_actuel.prenom}"
                            )

                        # Creation du nom
                        now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                        nom = (
                            f"Evolution du rang_de_{joueur_actuel.nom}_"
                            f"{joueur_actuel.prenom}_{now}"
                        )

                        sauvegarder_figure(fig, dossier, nom)
                        input("\nAppuie sur Entrée pour continuer")

                    print("Voulez-vous zommer sur une période ?")
                    zoomer = boucle_01()
                    while zoomer == '1':
                        data2 = zoom_graph(data)
                        fig = afficher_nuage_point(data2)
                        fig.show()

                        # Proposition enregistrement
                        print("\nVoulez-vous sauvegarder le graphique ?")
                        enregistrement = boucle_01()
                        if enregistrement == "1":
                            # Créer le dossier principal
                            dossier_principal = "enregistrement"
                            os.makedirs(dossier_principal, exist_ok=True)

                            # Créer le dossier spécifique au joueur
                            dossier = os.path.join(
                                dossier_principal,
                                f"{joueur_actuel.nom}_{joueur_actuel.prenom}"
                                )

                            # Creation du nom
                            now = datetime.datetime.now().strftime(
                                "%Y%m%d_%H%M"
                                )
                            nom = (
                                f"Evolution du rang_de_{joueur_actuel.nom}_"
                                f"{joueur_actuel.prenom}_{now}"
                            )

                            sauvegarder_figure(fig, dossier, nom)
                            input("\nAppuie sur Entrée pour continuer")

                        print("\nVoulez-vous effectuer un nouveau zoom ?")
                        zoomer = boucle_01()
                else:
                    print("Aucun classement trouvé pour ce joueur.")
            else:
                print("❌ Aucun joueur sélectionné. Créez un joueur d'abord !")
                input("\nAppuie sur Entrée pour continuer")

        else:
            choix_invalide()
