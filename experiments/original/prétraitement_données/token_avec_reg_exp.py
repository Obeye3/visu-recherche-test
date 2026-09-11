from nltk.tokenize  import RegexpTokenizer # this is for tokenization using regular expressions
 
 
 
#Structure generale :
exp_reg = r"\w+" #exemple d'expression regulière
#exp_reg = r"[\w']+"      cette expression dénote l'ensemble des mots contenant des apostrophes
#exp_reg = r'\d+'    cette expression dénote l'ensemble des numéros (one or more digit)
#exp_reg = r'\w+|\d+' les deux
#Si on veut diviser le texte selon les espaces et la ponctuation, on utilise gaps=True
#tokenizer = RegexpTokenizer(r'\s+', gaps=True)
tokenizer = RegexpTokenizer(exp_reg)
tokens = tokenizer.tokenize("Hello , c'est moi ")
print(tokens)
