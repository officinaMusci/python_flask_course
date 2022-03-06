
'''Fichier "app.py" à la racine du projet'''
# 1. On importe le module Flask
import flask

# 2. On déclare la variable globale pour l'application
app = flask.Flask(__name__)

# 3. On lance le serveur en mode dev pour avoir le debug
>>> export FLASK_ENV=development
>>> flask run

# 3.b Si on utilise un fichier différent (hello.py) :
>>> export FLASK_ENV=development
>>> export FLASK_APP=hello
>>> flask run
