import os
import datetime
import matplotlib.pyplot as plt


def sauvegarder_resultats_clustering(df_result, df_centroids):
    """
    Sauvegarde les résultats du clustering dans un sous-dossier horodaté.

    Les résultats incluent :
    - Un graphique de dispersion des clusters (PNG).
    - Les données des joueurs avec leur cluster assigné (CSV).
    - Les caractéristiques des centroïdes de chaque cluster (CSV).

    Args:
        df_result (pd.DataFrame):
            DataFrame contenant les joueurs, leurs clusters et
            les composantes PCA.
        df_centroids (pd.DataFrame):
            DataFrame des centroïdes de chaque cluster.
    """
    # Créer le dossier principal si nécessaire
    dossier_principal = "enregistrement"
    os.makedirs(dossier_principal, exist_ok=True)

    # Créer un sous-dossier unique par sauvegarde
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    dossier_sauvegarde = os.path.join(dossier_principal, f"clustering_{now}")
    os.makedirs(dossier_sauvegarde, exist_ok=True)

    # 1. Graphique des clusters
    plt.figure(figsize=(12, 8))
    for cluster in sorted(df_result['Cluster'].unique()):
        cluster_data = df_result[df_result['Cluster'] == cluster]
        plt.scatter(
            cluster_data['PCA1'],
            cluster_data['PCA2'],
            label=f'Cluster {cluster}',
            alpha=0.7
            )
        for _, row in cluster_data.iterrows():
            plt.annotate(row['Joueur'], (row['PCA1'], row['PCA2']), fontsize=8)

    plt.title('Clusters de joueurs de tennis')
    plt.xlabel('PCA1')
    plt.ylabel('PCA2')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        os.path.join(dossier_sauvegarde, "graphique_clustering.png"),
        dpi=300
        )
    plt.close()

    # 2. Sauvegarde des résultats en CSV
    df_result.to_csv(
        os.path.join(dossier_sauvegarde, "classification_joueurs.csv"),
        index=False
        )
    df_centroids.to_csv(
        os.path.join(dossier_sauvegarde, "caracteristiques_clusters.csv"),
        index=True
        )

    print(f"\n✅ Résultats sauvegardés dans le dossier : {dossier_sauvegarde}")
    input("Appuyer sur Entrer pour continuer")


def sauvegarder_texte(liste_joueur, dossier, nom):
    """
    Sauvegarde les informations statistiques d'une liste de joueurs
    dans un fichier texte.

    Args:
        liste_joueur (list):
            Une liste d'objets représentant les joueurs.
        dossier (str):
            Le chemin du dossier où enregistrer le fichier.
        nom (str):
            Le nom du fichier à créer.
    """
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom)

    with open(chemin, "w", encoding="utf-8") as f:
        for joueur in liste_joueur:
            f.write("\n=== Informations du joueur ===\n")
            f.write(f"Nom : {joueur.nom}\n")
            f.write(f"Prénom : {joueur.prenom}\n")
            f.write(f"Sexe : {joueur.sexe}\n")
            f.write(f"Main : {joueur.main}\n")
            f.write(f"Date de naissance : {joueur.date_nais}\n")
            f.write(f"Nombre de tournois joués : {joueur.nb_tournois_joue}\n")
            f.write(
                f"Nombre de tournois gagnés : {joueur.nb_tournois_gagne}\n"
                )
            f.write(
                f"Proportion victoires après set 1 perdu : "
                f"{round(joueur.prop_vic_set_1_perdu,2)} %\n"
                )
            f.write(
                f"Proportion balles de break sauvées :"
                f"{round(joueur.prop_balle_break_sauvee,2)} %\n"
                )
            f.write(f"Nombre de semaines classé : {joueur.nb_sem_classe}\n")
            f.write(f"Nombre de semaines 1-10 : {joueur.nb_sem_1_10}\n")
            f.write(f"Nombre de semaines 11-50 : {joueur.nb_sem_11_50}\n")
            f.write(f"Nombre de semaines 51-100 : {joueur.nb_sem_51_100}\n")
            f.write(f"Premier match : {joueur.pre_match}\n")
            f.write(f"Dernier match : {joueur.der_match}\n")

    print(f"✅ Informations enregistrées dans : {chemin}")


def sauvegarder_data(data, fichier, nom):
    """
    Sauvegarde un DataFrame pandas au format CSV.

    Args:
        data (pd.DataFrame):
            Le DataFrame à sauvegarder.
        fichier (str):
            Le chemin du dossier où enregistrer le fichier.
        nom (str):
            Le nom du fichier (sans extension).
    """
    os.makedirs(fichier, exist_ok=True)

    # Ajouter l'extension .csv au nom du fichier
    chemin_enregistrement = os.path.join(fichier, f"{nom}.csv")

    try:
        data.to_csv(chemin_enregistrement, index=False, encoding="utf-8")
        print(
            "\n✅ Données enregistrées au format CSV dans : "
            f"{chemin_enregistrement}"
            )
    except Exception as e:
        print(
            "Une erreur s'est produite lors de l'enregistrement des données "
            f"CSV : {e}"
            )


def sauvegarder_figure(fig, fichier, nom):
    """
    Sauvegarde une figure matplotlib dans un fichier PNG.

    Args:
        fig (matplotlib.figure.Figure):
            L'objet figure à sauvegarder.
        fichier (str):
            Le chemin du dossier où enregistrer le fichier.
        nom (str):
            Le nom du fichier
            (avec extension, par exemple 'mon_graphique.png').
    """
    os.makedirs(fichier, exist_ok=True)

    chemin_enregistrement = os.path.join(fichier, nom)

    try:
        fig.savefig(chemin_enregistrement, dpi=300, bbox_inches='tight')
        print(
            "La figure a été enregistrée sous le nom : "
            f"{chemin_enregistrement}"
            )
    except Exception as e:
        print(
            "Une erreur s'est produite lors de l'enregistrement de la "
            f"figure : {e}"
            )
