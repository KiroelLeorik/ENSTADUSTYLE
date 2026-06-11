""" ----------- Author : GREGOIRE Louna ------------- """


def recommander(acheteur, tous_les_articles, n=5):
    """
    Recommande des articles à un acheteur en fonction de ses favoris.
    Construit un profil de préférences (catégorie, taille, couleur…) à partir des favoris
    et score chaque article disponible selon sa correspondance avec ce profil.

    :param acheteur: objet Acheteur avec ses favoris chargés
    :param tous_les_articles: liste de tous les articles de la plateforme
    :param n: nombre maximum de recommandations à retourner (défaut : 5)
    :return: liste de tuples (article, score) triés par pertinence décroissante
    """
    #Construction du profil
    categorie = {}
    sous_categorie = {}
    genre = {}
    taille = {}
    couleur = {}
    marque = {}
    matiere = {}

    for article in acheteur.favoris:
        categorie_fav = article.categorie
        sous_categorie_fav = article.sous_categorie
        genre_fav = article.genre
        taille_fav = article.taille
        couleur_fav = article.couleur
        marque_fav = article.marque
        matiere_fav = article.matiere

        categorie[categorie_fav] = categorie.get(categorie_fav, 0) + 1
        sous_categorie[sous_categorie_fav] = sous_categorie.get(sous_categorie_fav, 0) + 1
        genre[genre_fav] = genre.get(genre_fav, 0) + 1
        taille[taille_fav] = taille.get(taille_fav, 0) + 1
        couleur[couleur_fav] = couleur.get(couleur_fav, 0) + 1
        marque[marque_fav] = marque.get(marque_fav, 0) + 1
        matiere[matiere_fav] = matiere.get(matiere_fav, 0) + 1
    #On pourrait également agrémenter le profil acheteur avec les informations de ses achats précédents.

    resultat = []
    id_fav = [article.id for article in acheteur.favoris]
    for article in tous_les_articles:
        if article.id in id_fav:
            continue
        if article.vendu:
            continue
        article_score = 0
        if article.categorie in categorie:
            article_score += categorie[article.categorie] * 1
        if article.sous_categorie in sous_categorie:
            article_score += sous_categorie[article.sous_categorie] * 0.7
        if article.genre in genre:
            article_score += genre[article.genre] * 0.5
        if article.taille in taille:
            article_score += taille[article.taille] * 0.3
        if article.couleur in couleur:
            article_score += couleur[article.couleur] * 0.1
        if article.marque in marque:
            article_score += marque[article.marque] * 0.2
        if article.matiere in matiere:
            article_score += matiere[article.matiere] * 0.1
        resultat.append((article, article_score))
    resultat.sort(key=lambda x: x[1], reverse=True)
    return resultat[0:n]
