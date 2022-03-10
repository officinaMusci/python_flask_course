
# $ pip install flask-jwt-extended



# ./__init__.py
...
import flask_jwt_extended as flask_jwt
...
def create_app():
    ...
    app.config.from_mapping(
        ...
        JWT_SECRET_KEY='utilisée_pour_le_cryptage_jwt'
        ...
    )
    jwt = flask_jwt.JWTManager(app)
    ...



# ./routes/api.py 🆕
import flask
from werkzeug import security

import flask_jwt_extended as flask_jwt

from database.db import get_db


# On déclare le blueprint
blueprint = flask.Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)


# Route pour le login
@blueprint.route('/login', methods=['POST'])
def login():

    # 1. On récupère les data
    request = flask.request.get_json()
    username = request['username']
    password = request['password']

    # 2. On ouvre la BDD et on cherche l'user
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ?',
        (username,)
    ).fetchone()

    # 3. On contrôle les data
    # 3.a Identifiants non valides
    if (
        user is None or not flask.check_password_hash(
            user['password'],
            password
        )
    ):
        response = flask.jsonify({
            'error': 'Identifiants non valides'
        })
        code = 401
    
    # 3.b Identifiants valides, on crée un JWT
    else:
        access_token = flask_jwt.create_access_token(
            identity=user['id']
        )
        response = flask.jsonify({
            'access_token': access_token
        })
        code = 200

    # 4. On envoi la réponse
    return flask.make_response(
        response,
        code,
        {'Content-Type': 'application/json'}
    )


# Exemple de route protégée
@blueprint.route('/protected')
@flask_jwt.jwt_required() # On protège la route, notre
def protected():          # requête devra avoir en header :
                          # {Authorization: "Bearer $JWT"}
    # 1. On récupère le user
    user_id = flask_jwt.get_jwt_identity()
    user = get_db().execute(
        'SELECT * FROM user WHERE id = ?',
        (user_id,)
    ).fetchone()
    
    # 2. Pour démo, on retourne le username
    response = flask.jsonify({
        'logged_in_as': user['username']
    })
    return flask.make_response(
        response,
        200,
        {'Content-Type': 'application/json'}
    )

