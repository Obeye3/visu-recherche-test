import requests
import io   


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
        