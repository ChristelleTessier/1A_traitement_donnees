import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def afficher_joueur(joueur):
    """
    Affiche les informations détaillées d'un joueur (prénom, nom, sexe, etc.).

    Paramètres :
        joueur (Joueur or None) :
            Objet représentant un joueur, ou None si le joueur
            n'est pas trouvé.

    Affiche :
        Détails du joueur tels que son nom, sexe, date de naissance, etc.
    """
    if joueur is None:
        print("❌ Joueur non trouvé.")
    else:
        print("\n✅ Joueur trouvé :")
        print(f"Nom : {joueur.prenom} {joueur.nom}")
        print(f"Sexe : {joueur.sexe}")
        print(f"Date de naissance : {joueur.date_nais}")
        print(f"Main : {joueur.main}")
        print(f"Nombre de tournois joués : {joueur.nb_tournois_joue}")
        print(f"Nombre de tournois gagnés : {joueur.nb_tournois_gagne}")
        print(
            f"Proportion victoires après set 1 perdu : "
            f"{round(joueur.prop_vic_set_1_perdu,2)} %"
            )
        print(
            f"Proportion balles de break sauvées :"
            f"{round(joueur.prop_balle_break_sauvee,2)} %"
            )
        print(f"Nombre de semaines classé : {joueur.nb_sem_classe}")
        print(f"Nombre de semaines 1-10 : {joueur.nb_sem_1_10}")
        print(f"Nombre de semaines 11-50 : {joueur.nb_sem_11_50}")
        print(f"Nombre de semaines 51-100 : {joueur.nb_sem_51_100}")
        print(f"Premier match : {joueur.pre_match}")
        print(f"Dernier match : {joueur.der_match}")

    input("\nAppuie sur Entrée pour continuer")


def afficher_tournoi(data, lignes_par_page=20):
    """
    Affiche les données d'un tournoi avec pagination.

    Paramètres :
        data (DataFrame) :
            Données des tournois à afficher.
        lignes_par_page (int) :
            Nombre de lignes à afficher par page (défaut : 20).

    Affiche :
        Les informations des tournois, une page à la fois.
    """

    n = len(data)
    for i in range(0, n, lignes_par_page):
        print(data.iloc[i:i+lignes_par_page].to_string(index=False))
        if i + lignes_par_page < n:
            input("\nAppuie sur Entrée pour voir la suite...")


def afficher_matchs(data):
    """
    Affiche un résumé des matchs, incluant le round, les gagnants,
    les perdants et le score.

    Paramètres :
        data (DataFrame) :
            Données des matchs à afficher.

    Affiche :
        Pour chaque match, les informations sur le round,
        le gagnant, le perdant et le score.
    """
    for index, row in data.iterrows():
        print(
            f"{row['round_label']} : Victoire de {row['winner_name']} "
            f"contre {row['loser_name']}, score de {row['score']}"
            )


def afficher_matchs_rencontre(data, lignes_par_page=25):
    """
    Affiche les détails des matchs entre deux joueurs, avec pagination.

    Paramètres :
        data (DataFrame) :
            Données des matchs entre deux joueurs à afficher.
        lignes_par_page (int) :
            Nombre de lignes à afficher par page (défaut : 25).

    Affiche :
        Les détails des matchs, y compris les dates, les tournois,
        les rounds, les scores et les vainqueurs.
    """

    n = len(data)

    for i in range(0, n, lignes_par_page):
        page = data.iloc[i:i + lignes_par_page]
        for index, row in page.iterrows():
            print(
                f"📅 {row['tourney_date']} - 🎾 Tournoi de "
                f"{row['tourney_name']}, 🌀 Round : {row['round']}\n"
                f"🏆 Victoire de {row['winner_name']} contre "
                f"{row['loser_name']}, 📊 Score : {row['score']}\n"
            )
        if i + lignes_par_page < n:
            input("Appuie sur Entrée pour voir la suite...")
            os.system('cls' if os.name == 'nt' else 'clear')

    input("Appuie sur Entrée pour continuer")


def afficher_nuage_point(data):
    """
    Crée et retourne un nuage de points représentant l'évolution des
    classements des joueurs dans le temps, sans l'afficher directement.

    Paramètres :
        data (DataFrame) :
            Données de classement avec les colonnes 'ranking_date' et 'rank'.

    Retourne :
        fig (Figure) : L'objet matplotlib de la figure.
    """
    data = data.copy()
    data['ranking_date'] = pd.to_datetime(data['ranking_date'])

    fig, ax = plt.subplots(figsize=(10, 6))

    conditions = [
        (data["rank"] >= 1) & (data["rank"] <= 10),
        (data["rank"] >= 11) & (data["rank"] <= 50),
        (data["rank"] >= 51) & (data["rank"] <= 100),
        (data["rank"] > 100)
    ]
    couleurs = ['black', 'green', 'blue', 'orange']
    labels = ['Top 10', '11-50', '51-100', 'Au-delà de 100']

    for condition, couleur, label in zip(conditions, couleurs, labels):
        subset = data[condition]
        ax.scatter(
            subset['ranking_date'],
            subset['rank'],
            color=couleur,
            label=label,
            s=10
            )

    ax.set_title("Nuage de points : Classement par Date")
    ax.set_xlabel("Année")
    ax.set_ylabel("Classement")
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())

    fig.autofmt_xdate()
    ax.grid(True)
    ax.legend()
    fig.tight_layout()

    return fig


def afficher_nuage_point_deux_joueurs(data, joueur1, joueur2):
    """
    Compare graphiquement les classements de deux joueurs au fil du temps.

    Paramètres :
        data (DataFrame) :
            Données de classement avec les colonnes 'ranking_date',
            'rankjoueur1', et 'rankjoueur2'.
        joueur1 (Joueur) :
            Premier joueur à comparer.
        joueur2 (Joueur) :
            Deuxième joueur à comparer.

    Retourne :
        fig (matplotlib.figure.Figure) : L'objet matplotlib de la figure.
    """
    # S'assurer que la colonne 'ranking_date' est bien au format datetime
    data['ranking_date'] = pd.to_datetime(data['ranking_date'])

    # Créer le graphique
    fig, ax = plt.subplots(figsize=(12, 6))

    # Tracer les deux courbes
    ax.plot(
        data['ranking_date'],
        data['rankjoueur1'],
        label=joueur1.nom,
        color='blue',
        marker='o',
        linewidth=1
    )
    ax.plot(
        data['ranking_date'],
        data['rankjoueur2'],
        label=joueur2.nom,
        color='red',
        marker='o',
        linewidth=1
    )

    # Titre et axes
    ax.set_title(
        f"Comparaison des Classements : {joueur1.nom} vs {joueur2.nom}"
        )
    ax.set_xlabel("Date")
    ax.set_ylabel("Classement")
    ax.invert_yaxis()  # meilleur classement en haut
    ax.grid(True)

    # Formater les dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()

    ax.legend()
    fig.tight_layout()

    return fig


def k_means_visualisation(X):
    """
    Affiche la courbe d'inertie pour différents nombres de clusters
    (méthode du coude).

    Args:
        X (np.ndarray): Matrice des caractéristiques des joueurs.
    """
    from sklearn.cluster import KMeans
    # Déterminer le nombre optimal de clusters avec la méthode du coude
    inertias = []
    K_range = range(1, 11)

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)

    # Visualiser la courbe du coude
    plt.figure(figsize=(10, 6))
    plt.plot(K_range, inertias, 'bo-')
    plt.xlabel('Nombre de clusters (k)')
    plt.ylabel('Inertie')
    plt.title('Méthode du coude pour déterminer k optimal')
    plt.grid(True)
    plt.show()


def plot_clusters(df_result, k_optimal):
    """
    Affiche un graphique de dispersion des joueurs colorés par cluster
    après réduction de dimensionnalité par PCA.

    Args:
        df_result (pd.DataFrame):
            DataFrame contenant les joueurs, leurs clusters
            assignés et les deux premières composantes PCA
            (colonnes 'PCA1', 'PCA2', 'Cluster', 'Joueur').
        k_optimal (int):
            Le nombre optimal de clusters déterminé.
    """
    plt.figure(figsize=(12, 8))
    for cluster in range(k_optimal):
        cluster_data = df_result[df_result['Cluster'] == cluster]
        plt.scatter(cluster_data['PCA1'],
                    cluster_data['PCA2'],
                    label=f'Cluster {cluster}',
                    alpha=0.7)
        for _, row in cluster_data.iterrows():
            plt.annotate(row['Joueur'], (row['PCA1'], row['PCA2']), fontsize=8)

    plt.title('Clusters de joueurs de tennis')
    plt.xlabel('Première composante principale')
    plt.ylabel('Deuxième composante principale')
    plt.legend()
    plt.grid(True)
    plt.show()


def afficher_cluster_centroids(df_centroids):
    """
    Affiche les caractéristiques moyennes de chaque cluster (les centroïdes).

    Args:
        df_centroids (pd.DataFrame):
            DataFrame contenant les centroïdes de chaque
            cluster, où chaque ligne représente un cluster
            et chaque colonne une caractéristique.
    """
    print("Caractéristiques moyennes des clusters:")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(df_centroids.round(0))
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    input("Presser entrer pour continuer")
