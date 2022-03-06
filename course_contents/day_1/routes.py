
import flask
app = flask.Flask(__name__)

# Une route est exposée par ce décorateur :
@app.route('/endpoint', methods=['GET', 'POST'])
def my_endpoint():
    '''🤖'''

# Si plusieurs routes doivent pointer vers le même output
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index')
@app.route('/index-post', methods=['POST'])
def home():
    '''🤖'''

# La route peut passer des arguments à la fonction
@app.route('/books/<title>')
def books(title):
    '''🤖'''

# ... préciser les types
@app.route('/articles/<int:year>/<int:month>')
def articles(year, month):
    '''🤖'''

# Et la fonction peut en définir les défauts
@app.route('/reviews/<int:year>/<int:month>/<str:title>')
def reviews(year=2021, month=12, title=None):
    '''🤖'''
