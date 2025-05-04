def application_tennis():
    """
    Lance l'application de gestion et d'analyse de joueurs de tennis.

    Fonctionnalités proposées via un menu :
    - Gérer ou consulter un joueur (statistiques, évolution...).
    - Lancer une analyse de type classification (clustering).
    - Quitter proprement l'application.

    La fonction utilise une boucle principale qui oriente l'utilisateur
    selon son choix. Elle importe dynamiquement les modules nécessaires
    à l'exécution des différentes fonctionnalités.
    """
    """
    Lance l'application de gestion et d'analyse de joueurs de tennis.
    """

    # Importations
    from tennis_app.menus.menu import menu_principal
    from tennis_app.logique.fonctions_joueurs import (
        fonction_joueur,
        creer_joueur_bis
    )
    from tennis_app.logique.fonctions_classification import fonction_classification
    from tennis_app.logique.fonctions_divers import sortie


    print("=== Bienvenue sur l'application Joueur Tennis ===")

    appli_marche = True
    joueur = None

    while appli_marche:
        menu_principal()
        choix = input("Entrez votre choix : ")

        if choix == "10":
            print("Merci d'avoir utilisé l'application ! À bientôt 👋")
            appli_marche = sortie()

        elif choix == "1":
            joueur = creer_joueur_bis()
            fonction_joueur(joueur)

        elif choix == "2":
            fonction_classification()

        else:
            print("\n ❌ Choix invalide. Veuillez réessayer.\n")


# Point d'entrée de l'application
if __name__ == "__main__":
    application_tennis()
