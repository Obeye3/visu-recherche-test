import re

def remove_sections(text, start_markers, end_markers):
    """
    Supprime toutes les sections du texte comprises entre un des start_markers et un des end_markers.
    """
    # Créer une expression régulière combinée pour tous les cas
    pattern = '|'.join(
        rf'{re.escape(start)}.*?{re.escape(end)}'
        for start in start_markers
        for end in end_markers
    )
    # Remplacer les correspondances par une chaîne vide
    cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
    return cleaned_text

# Liste des débuts et fins à utiliser pour repérer les blocs à supprimer
start_markers = [
    "HAL is a"]

end_markers = [ "ou privés."]

# Charger le fichier original
with open("articles_cleaned_2.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Nettoyer le texte
cleaned = remove_sections(content, start_markers, end_markers)

# Sauvegarder dans un nouveau fichier texte
with open("articles_cleaned_3.txt", "w", encoding="utf-8") as f:
    f.write(cleaned)

print("✅ Nettoyage terminé. Fichier sauvegardé sous 'articles_cleaned.txt'.")
