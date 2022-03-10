
# ./routes/auth.py
import functools
import flask
from werkzeug import security

from database.db import get_db


# On déclare notre BP
blueprint = flask.Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)


# Route pour le form d'enregistrement et son submit
@blueprint.route('/register', methods=['GET', 'POST'])
def register():

    # Si "POST", il s'agit du submit
    if flask.request.method == 'POST':
        
        # 1. On récupère les data
        username = flask.request.form['username']
        password = flask.request.form['password']
        
        # 2. On contrôle les data
        error = None
        if not username:
            error = 'Le nom utilisateur est requis'
        elif not password:
            error = 'Le mot de passe est requis'

        # On continue seulement si les data sont là
        if error is None:

            # 3. On ouvre la BDD et on enregistre l'user
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user\
                        (username, password)\
                        VALUES (?, ?)",
                    (
                        username,
                        security.generate_password_hash(
                            password
                        )
                    ),
                )
                db.commit()

            # 3.b On ajoute une erreur si il existe déjà
            except db.IntegrityError:
                error = f"{username} existe déjà"

            # 4. Si tout va bien, on révient au login
            else:
                return flask.redirect(
                    flask.url_for("auth.login")
                )

        # 5. Sinon, on ajoute l'erreur au flash bag
        flask.flash(error)

    # On affiche le form si "GET"
    # ou si on a des erreurs à afficher
    return flask.render_template(
        'auth/register.html'
    )


# Route pour le form de login et son submit
@blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # Si "POST", il s'agit du submit
    if flask.request.method == 'POST':
            
        # 1. On récupère les data
        username = flask.request.form['username']
        password = flask.request.form['password']

        # 2. On ouvre la BDD et on cherche l'user
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()

        # 3. On contrôle les data
        error = None
        if (
            user is None or not security.check_password_hash(
                user['password'],
                password
            )
        ):
            error = 'Identifiants non valides'

        # 4. Si tout va bien, on nettoye la session,
        # on enregistre l'user (id) en session
        # et va à l'index
        if error is None:
            flask.session.clear()
            flask.session['user_id'] = user['id']
            
            return flask.redirect(
                flask.url_for('index')
            )

        # 5. Sinon, on ajoute l'erreur au flash bag
        flask.flash(error)
    
    # On affiche le form si "GET"
    # ou si on a des erreurs à afficher
    return flask.render_template(
        'auth/login.html'
    )


# On crée l'objet user pour chaque request
@blueprint.before_app_request
def load_logged_in_user():
    # 1. On récupère l'ID depuis la session
    user_id = flask.session.get('user_id')

    # 2.a Si il n'existe pas, ce sera None
    if user_id is None:
        flask.g.user = None

    # 2.b Si il existe, on le récupère depuis la BDD
    else:
        flask.g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()


# Au logout, on nettoye et on redirige
@blueprint.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect(
        flask.url_for('index')
    )


# 🆕 Notre premier décorateur !
# ici on en crée un pour protéger les pages

def login_required(view):           # (view = la fonction)
    
    @functools.wraps(view)          # On l'enveloppe
    def wrapped_view(**kwargs):     # avec une function
                                    # qui prend les kwargs

        # Si la view est ouverte par un user
        # non loggué, on le redirige ver le login
        if flask.g.user is None:
            return flask.redirect(
                flask.url_for('auth.login')
            )

        # Sinon on lance la bonne fonction
        # avec ses kwargs originaux
        return view(**kwargs)

    # On retourne la fonction enveloppée
    return wrapped_view

# Et voilà comment ce sera utilisé
@blueprint.route('/profile')
@login_required # 🆕
def profile():
    '''🤖'''



# ./__init__.py
def create_app():
    ...
    from routes import auth
    app.register_blueprint(auth.blueprint)
    ...