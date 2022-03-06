
# Pour avoir accès au request object, on doit l'importer
import flask
from flask import request # 🆕

app = flask.Flask(__name__)

# Dans les routes on a acces au request object :
@app.route('/endpoint')
def endpoint():
    request.method  # POST, GET, PUT, DELETE
    request.args    # Les paramétres URL (?k=v)
    request.headers # Les en-têtes de la requête

    # Data reçues
    request.form       # Le contenu du form (si submitted)
    request.data       # Les data en format byte
    request.get_json() # Les data lues depuis le JSON
    