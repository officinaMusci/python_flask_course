
import flask
app = flask.Flask(__name__)

@app.route('/')
def home():
    # A. Gabarit HTML
    html = flask.render_template(
        'index.html',
        title='Bienvenue sur ma page web !',
        visits=10
    )

    response = flask.make_response(
        html,                  # body
        200,                   # status
        {'X-Foo': 'blah blah'} # headers
    )

    # B. Réponse JSON
    json = flask.jsonify({
        'results': [1, 2, 3],
        'error': None
    })

    response = flask.make_response(
        json,                                 # body
        200,                                  # status
        {'Content-Type': 'application/json'}  # headers
    )

    # C. Rédirection
    response = flask.redirect(
        flask.url_for(
            'dashboard', # Nom de la fonction
            visits=11    # /?visits=11 || /&#60;visits=11&#62;
        ),
        code=302
    )

    # On retourne la réponse
    return response