


test=["Je","suis","Rayané","et","je","ne","sais","pas","qui","est","ce","rayanÉ","dans","la","cuisine"]

nom_fichier = "exemple.txt"

def conversion_txt_string(nom_fichier):
    try:
        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            contenu = fichier.read()
        return contenu
    except FileNotFoundError:
        return "Erreur : fichier non trouvé."
    except Exception as e:
        return f"Erreur : {e}"


def vocabularisation(tokens): #tokens est le résultat de la tokenisation du texte
    vocab_occ = {}
    liste_mots=[]
    for elt in tokens :
        if elt.casefold() in vocab_occ :
            vocab_occ[elt.casefold()] += 1
        else:
            vocab_occ[elt.casefold()] = 1
            liste_mots.append(elt.casefold())
    return liste_mots,vocab_occ

