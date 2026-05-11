
def proposer_achat(acheteur, article, prix_acheteur, marge_max=0.1):
                """
            
            :param acheteur: 
            :param article: 
            :param prix_acheteur: 
            :param marge_max: 
            :return: 
            """
    prix_min = article.prix_min
    prix_vendeur = article.prix_vendeur
    budget_elargi = prix_acheteur * (1 + marge_max)

    if prix_acheteur >= prix_vendeur:
        return "acceptee"
    elif prix_acheteur >= prix_min and prix_vendeur <= budget_elargi:
        return "negociation"
    else:
        return "refusee"
