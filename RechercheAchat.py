import sqlite3
k=0.1 # 10% au dessus du budget
# Connexion à la base de données (créée si elle n'existe pas)
bdd = sqlite3.connect("basededonnee.db")
cursor = bdd.cursor()
Criteres={}
#exemple: critere={categorie:mateaux, couleur:bleu, taille:XL, matière:laine}
Acheteur= cursor.execute("SELECT id FROM utilisateur")# à voir comment on ecrit
A_acheter=[None for i in range 30]
objets=cursor.execute ("SELECT id FROM objet")
liste_objet=[]
for x in objets:
    cat=cursor.execute ("SELECT categorie FROM objet WHERE id=x")
    coul=cursor.execute ("SELECT couleur FROM objet WHERE id=x")#à voir ecriture
    tai=cursor.execute ("SELECT taille FROM objet WHERE id=x")
    mat=cursor.execute ("SELECT matiere FROM objet WHERE id=x")
    if cat==Criteres["categorie"] and coul==Criteres["couleur"] and tai==Criteres["taille"] and mat==Criteres["matiere"]:
        liste_objet.append(x)
meilleur_offre=0
liste_nego=[]
L=[]
    for x in liste_objet:
        prix=cursor.execute ("SELECT prix FROM objet WHERE id=x")
        budget_max_a=cursor.execute ("SELECT budget_max FROM utilisateur WHERE id=Acheteur")
        if meilleur_offre!=0:
            prix_meilleur_offre=cursor.execute ("SELECT prix FROM objet WHERE id=meilleur_offre")
        if prix<=budget_max_a:
            L.append(prix)
            L.sort()
            meilleur_offre=meilleur_offre+1

    elif prix<budget_max_a*(1+k):
        liste_nego.append(x)

if meilleur_offre!=0:
    prix_min_meill_offre=cursor.execute ("SELECT prix_min FROM objet WHERE id=meilleur_offre")
    if prix_meilleur_offre>= prix_min_meill_offre:
        print('achat direct réussi!')
else:
    for x in liste_nego:
        prix_propose=budget_max_a
        prix_min_x=cursor.execute ("SELECT prix_min FROM objet WHERE id=x")
        if prix_propose >= prix_min_x:
            print('achat négocié réussi!')#on prend le premier au hasard de la liste nego
    print('aucun achat')


#autre proposition de la derniere partie
prix_ok=[]
else:
    for x in liste_nego:
        prix_propose=budget_max_a
        if prix_propose >= prix_min_x:
            prix_ok.append(x)
            m=min (prix_ok[prix])
            print ('on a acheté à prix négocié')
    print('aucun achat')


