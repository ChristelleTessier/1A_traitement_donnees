# clustering_module.py
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from ..joueur.creer_joueur import creer_joueur
from ..menus.menu import (
    menu_classification,
    sous_menu_classification
)
from ..affichage.afficher import (
    k_means_visualisation,
    plot_clusters,
    show_cluster_centroids
)
from .fonctions_divers import (
    sortie,
    boucle_01
)
from .fonctions_enregistrement import (
    sauvegarder_resultats_clustering
)
from .preparation_classification import (
    preaprer_liste_id,
    choix_features,
    choix_nb_individu_groupe,
    preparer_joueurs,
    preparer_donnees,
    preparer_features
)


def preparer_classification(X):
    """
    Affiche la courbe du coude pour aider à déterminer le nombre
    optimal de clusters.

    Args:
        X (np.ndarray): Matrice des caractéristiques des joueurs.

    Returns:
        int or None: Nombre de clusters choisi par l'utilisateur,
        ou None si aucun joueur valide.
    """
    nb_joueurs_trouves = len(X)

    if nb_joueurs_trouves > 0:
        # Graphique pour visualisation coude
        k_means_visualisation(X)

        while True:
            print("_____________________________________________________")
            k_optimal = input("Combien de classe ? ")
            try:
                k_optimal_int = int(k_optimal)
                if 1 <= k_optimal_int <= nb_joueurs_trouves:
                    # Si valeur est un indice de la liste on sort
                    break

                else:
                    print(
                        "Valeur invalide (valeur attendue entre 1 et "
                        f"{nb_joueurs_trouves})"
                        )
            except ValueError:
                print(
                    "Erreur : Veuillez entrer indice entre 1 et "
                    f"{nb_joueurs_trouves} (un nombre entier)."
                    )

        return k_optimal_int
    else:
        print("Aucun joueur valide trouvé, impossible de continuer")
        input("Pressez entrer pour continuer")

        k_optimal_int = None

    return k_optimal_int


def clustering(X, noms_joueurs, k_optimal, features):
    """
    Effectue l'algorithme de clustering K-Means sur les données des joueurs.

    Args:
        X (np.ndarray):
            Matrice des caractéristiques des joueurs.
        noms_joueurs (list):
            Liste des noms des joueurs correspondant aux lignes de X.
        k_optimal (int):
            Nombre de clusters à créer.
        features (list):
            Liste des noms des caractéristiques utilisées pour le clustering.

    Returns:
        tuple: Un tuple contenant :
            - df_result (pd.DataFrame):
                DataFrame avec les joueurs, leurs clusters assignés et
                les composantes PCA.
            - df_centroids (pd.DataFrame):
                DataFrame des centroïdes de chaque cluster.
            - kmeans (sklearn.cluster.KMeans):
                L'objet KMeans entraîné.
    """
    kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)
    X_pca = PCA(n_components=2).fit_transform(X)

    df_result = pd.DataFrame({
        'Joueur': noms_joueurs,
        'Cluster': clusters,
        'PCA1': X_pca[:, 0],
        'PCA2': X_pca[:, 1]
    })

    colonnes = []
    mapping = {
        "pourcentage_victoire": 'Ratio victoires',
        "pourcentage_victoire_set1_perdu": 'Remontées après set perdu',
        "pourcentage_balle_break_sauvée": 'Balles de break sauvées',
        "pourcentage_sem_top_1_10": 'Temps top 10',
        "pourcentage_sem_top_11_50": 'Temps top 11-50',
        "pourcentage_sem_top_51_100": 'Temps top 51-100',
        "main_dominante": ['Main Droite', 'Main Gauche'],
        "genre": ["Sexe Homme", "Sexe Femme"]
    }
    for feat in features:
        val = mapping.get(feat)
        if isinstance(val, list):
            colonnes.extend(val)
        elif val:
            colonnes.append(val)

    df_centroids = pd.DataFrame(kmeans.cluster_centers_, columns=colonnes)
    df_centroids.index = [f'Cluster {i}' for i in range(k_optimal)]

    return df_result, df_centroids, kmeans


def predire_nouveau_joueur(kmeans, genre, df_result):
    """
    Permet de prédire le cluster d'un nouveau joueur en saisissant son nom.

    Args:
        kmeans (sklearn.cluster.KMeans):
            L'objet KMeans entraîné.
        genre (str):
            Le genre des joueurs considérés ('H', 'F', 'M').
        df_result (pd.DataFrame):
            DataFrame contenant les résultats du clustering.
    """
    prenom, nom = input("Saisir prénom : "), input("Saisir nom : ")
    joueur = creer_joueur(nom=nom, prenom=prenom)

    if joueur is None:
        print("Le joueur n'a pas été trouvé")
        return input("Presser entrer pour continuer")

    nom_complet = f"{joueur.prenom} {joueur.nom}"

    if nom_complet in df_result["Joueur"].values:
        cluster = df_result[
            df_result['Joueur'] == nom_complet
            ]['Cluster'].values[0]
        print(f"{nom_complet} est déjà dans les données (Cluster {cluster})")
    else:
        features = preparer_features(joueur, genre)
        prediction = kmeans.predict(np.array(features).reshape(1, -1))[0]
        print(f"{nom_complet} serait classé dans le cluster : {prediction}")

    input("Presser entrer pour continuer")


def interpretation(df_centroids, df_result, kmeans, genre, k_optimal):
    """
    Gère l'interaction utilisateur pour l'interprétation des résultats
    du clustering.

    Permet d'afficher les clusters, les centroïdes, de prédire le cluster
    d'un nouveau joueur et de sauvegarder les résultats.

    Args:
        df_centroids (pd.DataFrame):
            DataFrame des centroïdes de chaque cluster.
        df_result (pd.DataFrame):
            DataFrame avec les joueurs et leurs clusters.
        kmeans (sklearn.cluster.KMeans):
            L'objet KMeans entraîné.
        genre (str):
            Le genre des joueurs considérés ('H', 'F', 'M').
        k_optimal (int):
            Le nombre optimal de clusters.
    """
    while True:
        sous_menu_classification()
        choix = input("Entrez votre choix : ")
        if choix == "10":
            return sortie()
        elif choix == '1':
            plot_clusters(df_result, k_optimal)
        elif choix == "2":
            show_cluster_centroids(df_centroids)
        elif choix == "3":
            predire_nouveau_joueur(kmeans, genre, df_result)
        elif choix == "4":
            sauvegarder_resultats_clustering(df_result, df_centroids)
        else:
            print("Choix invalide. Veuillez réessayer.")


def classification(genre, type_, rang_max):
    """
    Orchestre le processus de classification des joueurs.

    Gère la préparation des données, le clustering et l'interprétation
    des résultats.

    Args:
        genre (str):
            Le genre des joueurs à classifier ('H', 'F', 'M').
        type_ (str or None):
            Le type de groupe ('classe' pour les joueurs classés,
            None pour tous).
        rang_max (int or None):
            Le rang maximal à considérer pour les joueurs classés.
    """
    liste_id = preaprer_liste_id(genre, type_, rang_max)
    features = choix_features(genre)
    nb_element = choix_nb_individu_groupe(liste_id)
    joueurs = preparer_joueurs(liste_id, genre, nb_element)
    X, noms_joueurs = preparer_donnees(joueurs, features)
    k_optimal = preparer_classification(X)

    if k_optimal is None:
        return fonction_classification()

    df_result, df_centroids, kmeans = clustering(
        X,
        noms_joueurs,
        k_optimal,
        features
        )
    interpretation(df_centroids, df_result, kmeans, genre, k_optimal)


def fonction_classification():
    """
    Affiche le menu principal de la fonctionnalité de classification
    et lance le processus de classification en fonction du choix
    de l'utilisateur.
    """
    while True:
        menu_classification()
        choix = input("Entrez votre choix : ")

        if choix == '10':
            return sortie()

        options = {
            '1': ('H', None),
            '2': ('H', 'classe'),
            '3': ('F', None),
            '4': ('F', 'classe'),
            '5': ('M', None),
            '6': ('M', 'classe')
        }

        if choix in options:
            genre, type_ = options[choix]
            rang_max = None
            if type_ == 'classe':
                print("\nSouhaitez-vous définir un rang maximal ?")
                if boucle_01() == '1':
                    while True:
                        rang_input = input(
                            "Saisir le rang_max (supérieur à 20): "
                            )
                        try:
                            rang_max = int(rang_input)
                            if rang_max > 20:
                                break
                        except ValueError:
                            pass
                        print("Entrée invalide. Essayez encore.")
            classification(genre, type_, rang_max or 2500)
        else:
            print("Choix invalide. Veuillez réessayer.")
