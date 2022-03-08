
# ./routes/articles.py
import flask
blueprint = flask.Blueprint(
    'articles',             # Nom
    __name__,               # Nom pour l'import
    url_prefix='/articles'
)

@blueprint.route('/new') # == '/articles/new'
def new_article():
    '''🤖'''


# ./__init__.py
def create_app():
    ...
    # On peut ajouter nos routes sous forme de blueprints
    from routes import articles # 🆕
    app.register_blueprint(articles.blueprint) # 🆕
    ...