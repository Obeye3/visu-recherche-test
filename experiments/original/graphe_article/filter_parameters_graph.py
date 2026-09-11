#from load_data import load_data



#Dictionary = load_data()



def filtered_data(Dictionary, keywords=None, year=None, type=None, authors=None):
    """
    Filtre les données du dictionnaire en fonction des mots-clés, de l'année, du type et des auteurs.

    :param Dictionary: Dictionnaire contenant les données.
    :param keywords: Liste de mots-clés à filtrer (optionnel).
    :param year: Année à filtrer (optionnel).
    :param type: Type de publication à filtrer (optionnel).
    :param authors: Liste de noms d'auteurs à filtrer (optionnel).
    :return: Dictionnaire filtré.
    """
    filtered_dict = {}

    for hal_id, data in Dictionary.items():

        # Filtre par auteurs
        if authors:
            data_authors = data.get("authors") or []
            if not any(author.lower() in [da.lower() for da in data_authors] for author in authors):
                continue

        # Filtre par mots-clés
        data_keywords = data.get("keywords") or []
        if keywords:
            print(keywords)
            if not any(k.lower() in [dk.lower() for dk in data_keywords] for k in keywords):
                continue

        # Filtre par année
        if year and ( int(data.get("year")) > int(year[1]) or int(data.get("year")) <int(year[0])) :

            continue


        
        # Filtre par type
        if type and data.get("type") not in type:
            continue

       
        # Si tout passe → on ajoute
        filtered_dict[hal_id] = data

    return filtered_dict

'''
if __name__ == "__main__":
    # Exemple d'utilisation de la fonction filtered_data
    keywords = None

    #keywords = ["deep learning"]
    type = None
    authors = ["Slim  Essid", "Bertrand  David"]
      # None pour ne pas filtrer par auteurs
    #year = "2022"
    year = None  # None pour ne pas filtrer par année  
    print("test")
    filtered_results = filtered_data(Dictionary, keywords, year,  type, authors)
    print(" Done filtering data.")
    print(filtered_results)
    # Affichage des résultats filtrés
    for hal_id, data in filtered_results.items():
        print(f"HAL ID: {hal_id}")
        print(f"Title: {data.get('title')}")
        print(f"Authors: {data.get('authors')}")
        print(f"Keywords: {data.get('keywords')}")
        print(f"Year: {data.get('year')}")
        print(f"Type: {data.get('type')}")
        print(f"PDF Link: {data.get('pdf_link')}\n")
'''