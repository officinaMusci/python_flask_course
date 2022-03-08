
# ./__init__.py

import os
import flask

def create_app():
    app = flask.Flask(__name__)

    # Configuration de l'app
    app.config.from_mapping(
        SECRET_KEY='utilisée_pour_le_cryptage',
        DATABASE=os.path.join(
            app.instance_path,
            'database',
            'project.sqlite'
        ) # Génère la path pour la BDD
    )

    # Ici on mettra nos routes
    ...

    return app