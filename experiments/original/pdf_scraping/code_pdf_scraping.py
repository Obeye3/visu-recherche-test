import fitz  # PyMuPDF
import requests
import io

def extract_text_from_pdf_url(pdf_url):
    # Télécharger le PDF en tant que contenu binaire
    response = requests.get(pdf_url)
    response.raise_for_status()  # Vérifie que la requête s'est bien déroulée
    
    # Créer un objet BytesIO à partir du contenu du PDF
    pdf_stream = io.BytesIO(response.content)
    
    # Ouvrir le PDF depuis le flux
    document = fitz.open("pdf", pdf_stream)
    
    text = ""
    # Parcourir chaque page du PDF
    for page in document:
        text += page.get_text()
    return text

    
def extract_date(pdf_txt):
    parts = pdf_txt.split("\n\n")
    for part in parts:
        lines = part.split("\n")
        for line in lines:
            start = line[:9]
            if start=="Submitted":
                motif = r'\b\d{1,2} [A-Za-z]{3} \d{4}\b'
                dates = re.findall(motif, pdf_txt)
                print(dates)
                return dates # renvoie [date de soumission de l'article; date de dernière révision]
        

# Exemple d'utilisation
pdf_url = "https://hal.science/hal-04762097v1/file/main.pdf"  # Remplacez par l'URL réelle du PDF
contenu_pdf = extract_text_from_pdf_url(pdf_url)

with open("pdf_content.txt", "w", encoding="utf-8") as file:
    file.write(contenu_pdf)
        
print("Les informations de la page ont été stockées dans 'pdf_content.txt'.")