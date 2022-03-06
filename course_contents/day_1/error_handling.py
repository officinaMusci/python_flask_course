
import flask
app = flask.Flask(__name__)

'''
Des réponses spécifiques peuvent être retournées
dans le cas où une requête renvoie une erreur
'''
@app.errorhandler(404)
def not_found():
    '''🤖'''

@app.errorhandler(400)
def bad_request():
    '''🤖'''

@app.errorhandler(500)
def server_error():
    '''🤖'''