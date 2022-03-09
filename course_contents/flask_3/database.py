
# ./routes/articles.py
import flask
from werkzeug import exceptions

from . import auth
from database.db import get_db

...

# La route pour afficher tous les articles
@blueprint.route('/')
def index():
    db = get_db()
    articles = db.execute(
        'SELECT p.id, title, body, created,\
            author_id, username'
        ' FROM article p JOIN user u\
            ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    # On affiche le template avec les articles
    return flask.render_template(
        'articles/index.html',
        articles=articles
    )


# La route pour créer un nouvel article
@blueprint.route('/create', methods=['GET', 'POST'])
@auth.login_required
def create():

    # Si "POST", il s'agit du submit
    if flask.request.method == 'POST':

        # 1. On récupère les data
        title = flask.request.form['title']
        body = flask.request.form['body']
        
        # 2. On contrôle les data
        error = None
        if not title:
            error = 'Le titre est requis'

        # On continue seulement si les data sont là
        if error is None:

            # 3. On ouvre la BDD et on enregistre l'art.
            db = get_db()
            db.execute(
                'INSERT INTO article\
                    (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, flask.g.user['id'])
            )
            db.commit()

            # 4. Si tout va bien, on révient à la liste
            return flask.redirect(
                flask.url_for('articles.index')
            )

        # 5. Sinon, on ajoute l'erreur au flash bag
        flask.flash(error)

    # On affiche le form si "GET"
    # ou si on a des erreurs à afficher
    return flask.render_template(
        'articles/create.html'
    )


# On crée un "helper" pour obtenir un article
# Cela nous servira pour "update" et "delete"
def get_article(id, check_author=True):
    article = get_db().execute(
        'SELECT\
            p.id, title, body, created,\
            author_id, username'
        ' FROM article p JOIN user u\
            ON p.author_id = u.id'
        ' WHERE p.id=?',
        (id,)
    ).fetchone()

    # On peut lever des erreurs HTTP
    if article is None:
        exceptions.abort(
            404,
            f"l'article {id} n'existe pas"
        )
    
    if check_author and (
        article['author_id'] != flask.g.user['id']
    ):
        exceptions.abort(403)

    # Si tout est ok, on retourne l'article
    return article


# La route pour mettre à jour un article
@blueprint.route(
    '/<int:id>/update',
    methods=['GET', 'POST']
)
@auth.login_required
def update(id):
    article = get_article(id)

    # Si "POST", il s'agit du submit
    if flask.request.method == 'POST':

        # 1. On récupère les data
        title = flask.request.form['title']
        body = flask.request.form['body']
        
        # 2. On contrôle les data
        error = None
        if not title:
            error = 'Title is required.'

        # On continue seulement si les data sont là
        if error is None:

            # 3. On ouvre la BDD et on enregistre l'art.
            db = get_db()
            db.execute(
                'UPDATE article SET title=?, body=?'
                ' WHERE id=?',
                (title, body, id)
            )
            db.commit()
            
            # 4. Si tout va bien, on révient à la liste
            return flask.redirect(
                flask.url_for('articles.index')
            )            

        # 5. Sinon, on ajoute l'erreur au flash bag
        flask.flash(error)

    # On affiche le form si "GET"
    # ou si on a des erreurs à afficher
    return flask.render_template(
        'articles/edit.html',
        article=article
    )


# La route pour effacer un article
@blueprint.route('/<int:id>/delete', methods=['POST'])
@auth.login_required
def delete(id):
    get_article(id)
    db = get_db()
    db.execute(
        'DELETE FROM article WHERE id=?',
        (id,)
    )
    db.commit()

    # On révient à la liste
    return flask.redirect(
        flask.url_for('articles.index')
    )