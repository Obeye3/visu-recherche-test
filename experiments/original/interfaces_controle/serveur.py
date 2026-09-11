from flask import Flask, render_template, request, send_file
from flask_cors import CORS
import topic_modeling as tm
import nouvelle_anc as kw_anc
import threading
app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin si besoin

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualiser1', methods=['POST'])
def visualiser1():
    data = request.get_json()
    print("Reçu :", data)
    # Générez ici votre image (ex: 'result.png') à partir des données
   
    #tm.run_topic_modeling(data['keywords'], [data['start_year'],data['end_year']])
    return send_file("result_ac.png", mimetype="image/png")

@app.route('/visualiser2', methods=['POST'])
def visualiser2():

    data = request.get_json()
    
    print("Reçu :", data)
    # Générez ici votre image (ex: 'result.png') à partir des données

    #kw_anc.run_topic_modeling(data['keywords'], [data['start_year'],data['end_year']])
    return send_file("result_nouvelle_anc.png", mimetype="image/png")




if __name__ == '__main__':
    app.run(debug=True , port=5050)
