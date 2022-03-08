
#./database/db.py
import sqlite3
import click
import flask
from flask.cli import with_appcontext


def get_db():
    if 'db' not in flask.g: # "g" est la var de session
        flask.g.db = sqlite3.connect(
            flask.current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        flask.g.db.row_factory = sqlite3.Row

    return flask.g.db


def close_db(e=None):
    db = flask.g.pop('db', None) # Détache la BDD

    if db is not None:
        db.close()



#./database/schema.sql
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS article;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE article (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);



#./database/db.py
def init_db():
    db = get_db()

    with flask.current_app.open_resource(
        'database/schema.sql'
    ) as schema:
        db.executescript(
            schema.read().decode('utf8')
        )


@click.command('init-db') # $ flask init-db
@with_appcontext
def init_db_command():
    """Efface et récrée la BDD"""
    init_db()
    click.echo('BDD initialisée')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)



#./__init__.py
def create_app():
    ...
    # On peut initialiser la BDD dans la factory
    from database import db
    db.init_app(app)
    ...