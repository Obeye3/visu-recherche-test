import re

def parse_bibtex_entries(text):
    entries = re.findall(r'@inproceedings\{.*?\n\}', text, re.DOTALL)
    title_author_dict = {}
    
    for entry in entries:
        title_match = re.search(r'title\s*=\s*\{(.+?)\}', entry)
        author_match = re.search(r'author\s*=\s*\{(.+?)\}', entry)
        
        if title_match and author_match:
            title = title_match.group(1)
            authors = [author.strip() for author in author_match.group(1).split(' and ')]
            title_author_dict[title] = authors
    
    return title_author_dict

def invert_title_author_dict(title_author_dict):
    author_title_dict = {}
    for title, authors in title_author_dict.items():
        for author in authors:
            if author not in author_title_dict:
                author_title_dict[author] = []
            author_title_dict[author].append(title)
    return author_title_dict

# Exemple d'utilisation
bibtex_string = """ texte après scrapping   """
titles_authors = parse_bibtex_entries(bibtex_string)
authors_titles = invert_title_author_dict(titles_authors)
print(authors_titles)