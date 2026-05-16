""" ----------- Author : GREGOIRE Louna ------------- """
import numpy as np

#score=[(catégorie,0.5),(sous_catégorie,0.4),(genre,0.1),(taille,0.3),(couleur,0.2),(etat,0.4),(matiere,0.2)]
# Ce scoring sera utilisé si le reste fonctionne, nousnous concentrons d'abord sur une version du site plus simple mais fonctionnelle.
def scorer_articles(articles, criteres): 
    """

    :param articles:liste
    :param criteres:dictionnaire
    :return:liste
    """
    mapping = {"categorie": "categorie","sous_categorie": "sous_categorie","genre": "genre","taille": "taille","couleur": "couleur","marque": "marque","etat": "etat","matiere": "matiere"}
    criteres_actifs = {k : v for k, v in criteres.items() if k in mapping} #l'utilisateur ne peut pas inventer de catégorie
    if not criteres_actifs:
        return articles
    articles_dispo = [a for a in articles if not a.vendu] # rencensement des articles encore en stock
    cles = list(criteres_actifs)
    n = len(cles)
    #poidprim=np.array([0]*n)      #cette partie de la fonction correspond au scoring commenté en dessus
    #for c in range(n):
    #    for i in range(len (score)):
    #        if score[i][0]==cles[c]:
    #           poidprim[c]=score[i][1]
    #for p in poidprim:
    #        if p==0:
    #                   poidprim.remove(p)
    poid = np.array([1/n] * n) #on prend chaque catégorie le meme poids ici pour que ça soit plus facile c'est une matrice 1,n
    matrice = []

    for a in articles_dispo: #on parcours tous les articles disponibles
        ligne = []
        for cle in cles:
            if getattr(a, cle) == criteres_actifs[cle]:   #si la catégorie de l'article dans la base de données correspond à celle de l'article recherché
                ligne.append(1.0)
            else:
                ligne.append(0.0)
        matrice.append(ligne)  #on obtient une matrice n,1 avec des 1 si la catégorie est la bonne et des 0 sinon 

    matrice = np.array(matrice)
    scores = matrice @ poid   # on obtient une matrice 1,1 qu'on utilise comme un réel
    resultat = list(zip(articles_dispo, scores))
    resultat.sort(key=lambda x: x[1], reverse=True) #on trie les articles par score décroissant donc par pertinence (plus le score est haut, meilleure est la pertinence)
    return resultat


"""---------------------- OLD ------------------------------------------
Version lente qui ne sort pas une liste triée en fonction du score mais qui sort seulement les articles qui correspondent exactement aux
critères.
La version calcul matriciel ci-dessous est plus rapide et permet de trier les résultats en fonction du score obtenu."""


def rechercher(articles, criteres):
    """

    :param articles:liste
    :param criteres:dictionnaire
    :return:liste
    """
    resultats = []
    categorie = criteres.get('categorie')
    sous_categorie = criteres.get('sous_categorie')
    genre = criteres.get('genre')
    taille = criteres.get('taille')
    couleur = criteres.get('couleur')
    marque = criteres.get('marque')
    etat = criteres.get('etat')
    prix = criteres.get('prix')
    matiere = criteres.get('matiere')
    for a in articles:
        check = True
        if a.vendu:
            check = False
        if categorie is not None and a.categorie != categorie:
            check = False
        if sous_categorie is not None and a.sous_categorie != sous_categorie:
            check = False
        if genre is not None and a.genre != genre:
            check = False
        if taille is not None and a.taille != taille:
            check = False
        if couleur is not None and a.couleur != couleur:
            check = False
        if marque is not None and a.marque != marque:
            check = False
        if etat is not None and a.etat != etat:
            check = False
        if prix is not None and prix < a.prix_vendeur:
            check = False
        if matiere is not None and a.matiere != matiere:
            check = False
        if check:      #resultats est la liste des articles en stock dont les catégories correspondent à celles recherchées par l'utilisateur
            resultats.append(a)
    return resultats

def scorer_articles_python(articles, criteres):
    """

    :param articles:liste
    :param criteres:dictionnaire
    :return:liste
    """
    mapping = {"categorie": "categorie","sous_categorie": "sous_categorie","genre": "genre","taille": "taille","couleur": "couleur","marque": "marque","etat": "etat","matiere": "matiere"}
    criteres_actifs = {k: v for k, v in criteres.items() if k in mapping} #l'utilisateur ne peut pas inventer une catégorie
    if not criteres_actifs:             
        return articles                 si aucune catégorie n'est valable, aucun article n'est pertinent, la liste article n'a donc pas besoin d'etre triée par pertinence       
    cles = list(criteres_actifs)
    n = len(cles)
    resultats = []

    for a in articles:
        if a.vendu:
            continue
        matchs = 0
        for cle in cles:
            if getattr(a, cle) == criteres_actifs[cle]: # on augmente matchs a chaque critere correspondant
                matchs += 1
        score = matchs / n          # 0<=score<=1
        resultats.append((a, score))

    resultats.sort(key=lambda x: x[1], reverse=True) #on trie les résultats par pertinence décroissante
    return resultats
