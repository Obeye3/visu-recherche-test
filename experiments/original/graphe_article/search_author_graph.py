import networkx as nx

def create_gephi_graph(graph: dict, auteur_dict: dict, auteur_cible: str, file_name: str):
    G = nx.Graph()

    for source, voisins in graph.items():
        for target in voisins:
            G.add_edge(source, target)

    for node in G.nodes:
        auteurs = auteur_dict.get(node, "")
        cible = "oui" if auteur_cible.lower() in auteurs.lower() else "non"

        # Ajout d'attributs au nœud
        G.nodes[node]['auteurs'] = auteurs
        G.nodes[node]['auteur_cible'] = cible
        G.nodes[node]['label'] = node

        # Optionnel : couleur personnalisée (rouge si cible, gris sinon)
        if cible == "oui":
            G.nodes[node]['viz'] = {
                'color': {'r': 255, 'g': 80, 'b': 80, 'a': 1.0}
            }
        else:
            G.nodes[node]['viz'] = {
                'color': {'r': 180, 'g': 180, 'b': 180, 'a': 0.7}
            }

    nx.write_gexf(G, f"graphes/{file_name}.gexf")

def test():
    my_graph = {
        "A1": ["A2", "A3"],
        "A2": ["A1"],
        "A3": ["A1", "A4"],
        "A4": ["A3"]
    }

    auteur_dict = {
        "A1": "Dupont;Martin",
        "A2": "Durand",
        "A3": "Tremblay;Dupont",
        "A4": "Leclerc"
    }

    create_gephi_graph(my_graph, auteur_dict, auteur_cible="Dupont", file_name="test_gephi")
print("heu")
test()
print("heinn")