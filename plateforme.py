
class Plateforme:
    def __init__(self):
        self.utilisateurs = []    # composition
        self.articles = []        # composition
        self.transactions = []    # composition

    def creer_utilisateur(self, pseudo, nom, prenom, mail, mot_de_passe, est_pro=False, evaluation=0, localisation=None, date_inscription=None):
        '''
        :param pseudo:
        :param nom:
        :param prenom:
        :param mail:
        :param mot_de_passe:
        :param est_pro:
        :param evaluation:
        :param localisation:
        :param date_inscription:
        :return:
        '''
        for user in self.utilisateurs:
            if pseudo == user.pseudo:
                print('blabla')
                return False
        from models.utilisateur import Utilisateur
        nouveau_id = len(self.utilisateurs) + 1
        self.utilisateurs.append(Utilisateur(nouveau_id, pseudo, nom, prenom, mail, mot_de_passe, est_pro, evaluation, localisation, date_inscription))
        return True
        # Crée un nouvel utilisateur
        # Vérifie que le pseudo n'est pas déjà pris
        # Ajoute à self.utilisateurs


    def charger_depuis_bdd(self):
        # Charge les utilisateurs et articles depuis marche.db
        # Utilise get_all_utilisateurs() et get_all_articles()
        from db.db import get_all_utilisateurs, get_all_articles
        from models.utilisateur import Utilisateur
        from models.article import Vetement
        utilisateurs_bdd = get_all_utilisateurs()
        self.utilisateurs = [Utilisateur(*u) for u in utilisateurs_bdd]
        articles_bdd = get_all_articles()
        self.articles = [Vetement(*a) for a in articles_bdd]
        #manque un get_all_transactions ??
        return True

    def trouver_utilisateur(self, pseudo):
        for user in self.utilisateurs:
            if pseudo == user.pseudo:
                return user
        return None

    def ajouter_article(self, article):
        if article not in self.articles:
            self.articles.append(article)
            return True
        return False

    def afficher_catalogue(self):
        for a in self.articles:
            if not a.vendu:
                print(f"{a.nom} — {a.prix_vendeur}€ ({a.sous_categorie})")
            else:
                print(f"{a.nom} — {a.prix_vendeur}€ ({a.sous_categorie}) — Vendu")
    #Je me suis rendu compte qu'on utilisait que des utilisateurs mais qu'on avait besoin d'acheteur et de vendeur
    #Le problème c'est que tout le monde est à la fois acheteur et vendeur, mais on ne peut pas instancier
    #Un utilisateur, vendeur, acheteur sous la même bannière
    #Donc on charge tout le monde en utilisateur, puis on les transforment en acheteur/vendeur au bon moment
    def en_tant_que_acheteur(self, utilisateur):
        from models.utilisateur import Acheteur
        return Acheteur(utilisateur.id, utilisateur.pseudo, utilisateur.nom,
                        utilisateur.prenom, utilisateur.mail, utilisateur.mot_de_passe,
                        utilisateur.est_pro, utilisateur.evaluation,
                        utilisateur.localisation, utilisateur.date_inscription)

    def en_tant_que_vendeur(self, utilisateur):
        from models.utilisateur import Vendeur
        return Vendeur(utilisateur.id, utilisateur.pseudo, utilisateur.nom,
                       utilisateur.prenom, utilisateur.mail, utilisateur.mot_de_passe,
                       utilisateur.est_pro, utilisateur.evaluation,
                       utilisateur.localisation, utilisateur.date_inscription)

