
# $ pip install python-dotenv



# ./.env 🆕 (à ajouter au .gitignore)

SECRET_KEY='utilisée_pour_le_cryptage'
JWT_SECRET_KEY='utilisée_pour_le_cryptage_jwt'
ENV='development'



# ./__init__.py
...
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    ...
    app.config.from_mapping(
        ENV=os.getenv('ENV'),
        SECRET_KEY=os.getenv('SECRET_KEY'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        ...
    )
    ...