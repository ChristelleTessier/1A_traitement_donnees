import os


def boucle_01():
    """
    Demande à l'utilisateur de répondre par oui (1) ou non (0).

    Utilisée comme confirmation binaire dans différents menus.

    Returns:
        str: '1' si l'utilisateur choisit oui, '0' sinon.
    """

    while True:
        rep = input("0 : non, 1: oui. Votre choix ?")
        if rep == '0' or rep == '1':
            # Réponse valide
            break
        else:
            print("Valeur saisie invalide (0 ou 1 attendu).")

    return rep


def sortie():
    """
    Permet de sortir proprement d'une boucle ou d'une application.

    Returns:
        bool: Toujours False, utilisé pour indiquer une sortie.
    """
    return False


def effacer_terminal():
    """
    Efface le terminal pour améliorer la lisibilité de l'affichage.

    Compatible uniquement avec les systèmes Windows ('cls').
    """
    os.system('cls')


def choix_invalide():
    """
    Affiche un message d'erreur pour un choix utilisateur invalide,
    puis demande d'appuyer sur Entrée pour continuer.
    """
    print("\n ❌ Choix invalide. Veuillez réessayer. \n")
    input("\nAppuie sur Entrée pour continuer")


def choix_dans_liste(liste, liste_choix=[]):
    """
    Permet à l'utilisateur de choisir plusieurs éléments dans une liste.

    L'utilisateur peut sélectionner un ou plusieurs éléments en saisissant
    leurs indices, avec confirmation. L'entrée '0' termine la sélection.
    Si aucun élément n'est sélectionné, la liste complète est retournée.

    Args:
        liste (list): Liste d'éléments à proposer.
        liste_choix (list optionelle): liste des elements deja_choisis

    Returns:
        list: Liste des éléments sélectionnés par l'utilisateur.
    """

    while True:
        effacer_terminal()
        print("\nMenu de choix dans la liste :\n")
        texte_liste = [
            f" {k+1} : {elt},\n" for k, elt in enumerate(liste)
        ]
        texte = "".join(texte_liste)
        texte += "\nIndiquer l'indice à ajouter (ou '0' pour terminer) : "
        elt = '...'

        print(liste_choix)
        indice_str = input(texte)

        if indice_str == '0':
            if len(liste_choix) == 0:
                liste_choix = liste
            break  # Sortir de la boucle de saisie d'indice
        else:

            try:
                indice = int(indice_str)
                if 1 <= indice <= len(liste):
                    elt = liste[indice - 1]
                    if elt not in liste_choix:
                        # Demander validation
                        print(f"Vous voulez ajouter '{elt}' ?")
                        print("Confirmer votre choix !")
                        choix = boucle_01()
                        if choix == '1':
                            print(f"Element '{elt}' ajoutée.")
                            liste_choix.append(elt)
                    else:
                        print("Cette caractéristique est déjà sélectionnée.")

                else:
                    print(
                        "Valeur invalide (valeur attendue entre 1 et "
                        f"{len(liste)} ou 0 pour terminer)"
                    )
            except ValueError:
                print(
                    "Erreur : Veuillez entrer un nombre entier valide."
                )
        input("Appuyer sur Entrer pour continuer...")

    return liste_choix
