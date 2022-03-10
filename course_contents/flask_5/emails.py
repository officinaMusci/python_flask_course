
# $ pip install Flask-Mail



# ./__init__.py
...
def create_app():
    ...
    app.config.from_mapping(
        ...
        MAIL_DEFAULT_SENDER='gatekeeper@website.web'
        SECURITY_PASSWORD_SALT='utilisée_pour_le_cryptage_token'
        ...
    )



# ./services/email.py 🆕
import flask
import flask_mail

# On crée un helper pour envoyer les emails
def send_email(to, subject, body):
    app = flask.current_app
    mail = flask_mail.Mail(app)
    
    # 1. On compose le message avec les args
    message = flask_mail.Message(
        subject,
        recipients=[to],
        html=body,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    
    # On envoie le message
    mail.send(message)



#./services/database/schema.sql
# On met à jour le schema SQL
...
CREATE TABLE user (
  ...
  email TEXT UNIQUE NOT NULL,
  confirmed INTEGER(1) DEFAULT 0
);



#./services/auth.py
import flask
from itsdangerous import URLSafeTimedSerializer


# On crée un helper pour générer les tokens
def generate_confirmation_token(email):
    app = flask.current_app

    # 1. On initialise le serializer
    serializer = URLSafeTimedSerializer(
        app.config['SECRET_KEY']
    )
    
    # 2. On encrypte l'email
    return serializer.dumps(
        email,
        salt=app.config['SECURITY_PASSWORD_SALT']
    )


# On crée un helper pour confirmer les tokens 
def confirm_token(token, expiration=3600):
    app = flask.current_app

    # 1. On initialise le serializer
    serializer = URLSafeTimedSerializer(
        app.config['SECRET_KEY']
    )
    
    # 2. On essaye de décrypter
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    
    # 3.a On retourne False en cas de échec
    except:
        return False
    
    # 3.b Si tout va bien, on retourne l'email
    return email



#./routes/auth.py
from services import email


# Route pour vérifier un token
@blueprint.route('/confirm/<token>')
@auth.login_required
def confirm_token(token):
    db = get_db()

    # 1. On essaye de décrypter
    email = auth.confirm_token(token)

    # 2.a En cas d'echéc
    if not email:
        flask.flash(
            'Le lien de confirmation est invalide ou a expiré'
        )

    # 2.b En cas de succés
    else:
        user = db.execute(
            'SELECT * FROM user WHERE email=?',
            (email,)
        ).fetchone()
        
        # 3.a Si l'user est confirmé déjà
        if user.confirmed:
            flask.flash(
                'Compte déjà confirmé. Veuillez vous connecter.'
            )
        
        # 3.b Tout va bien, on met à jour et on remercie
        else:
            db.execute(
                'UPDATE user SET confirmed=1'
                ' WHERE id=?',
                (user['id'],)
            )
            db.commit()
            
            flask.flash(
                'You have confirmed your account. Thanks!',
                'success'
            )
    
    # En tout cas, on redirige vers le login
    return flask.redirect(
        flask.url_for('auth.login')
    )


# On met à jour la route d'enregistrement
@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    ...
    # Dans l'étape 4.
    else:
        # 1. On crée un token
        token = auth.generate_confirmation_token(
            email
        )

        # 2. On crée le URL de confirmation
        confirm_url = flask.url_for(
            'auth.confirm_email',
            token=token,
            _external=True
        )

        # 3. On crée un message
        email_body = f'''
            <p>Veuillez suivre ce lien pour activer votre compte :</p>
            <p><a href="{confirm_url}">{confirm_url}</a></p>
        '''

        # 4. On ajoute un objet
        subject = 'Veuillez confirmer votre email'

        # 5. On enoie l'email
        email.send_email(email, subject, email_body)

        # 6. On communique au front end
        flask.flash(
            'A confirmation email has been sent via email',
            'success'
        )
        ...