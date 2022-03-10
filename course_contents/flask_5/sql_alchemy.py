
# $ pip install sqlalchemy



# ./services/database/db.py
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()


# On déclare le type de DB
Base = declarative_base()


# On crée l'helper pour les sessions DB
def create_session(engine=None):
    engine = create_engine(
        engine
        or os.getenv('DB_ENGINE')
        # f"sqlite:///{db_path}"
    )
    
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    Session = sessionmaker(bind=engine)
    
    return Session



#  ./classes/user
from dataclasses import dataclass
from sqlalchemy import Column as ORMColumn
from sqlalchemy import String as ORMString
from sqlalchemy import Integer as ORMInteger
from sqlalchemy import Boolean as ORMBoolean

from services.database import db


# On déclare le schema pour les utilisateurs
class UserRow(db.Base):
    __tablename__ = 'user'

    id = ORMColumn(ORMInteger, primary_key=True)
    username = ORMColumn(ORMString, nullable=False)
    password = ORMColumn(ORMString, nullable=False)
    email = ORMColumn(ORMString, nullable=False)
    confirmed = ORMColumn(ORMBoolean, default=False)


# On crée une dataclass pour les utilisateurs
@dataclass
class User:
    id:int
    username:str
    password:str
    email:str
    confirmed:bool

    # Méthode pour avoir un User depuis la DB
    @classmethod
    def from_row(cls, row:UserRow):
        return User(
            id=row.id,
            username=row.username,
            password=row.password,
            email=row.email,
            confirmed=row.confirmed
        )
    
    # ... et pour l'avoir avec juste l'id
    @classmethod
    def from_row_id(cls, id:int):
        with db.create_session().begin() as db_session:
            user_row = db_session.query(UserRow).get(id)
            user = User.from_row(user_row)
            db_session.close()
        
        return user
    
    # Méthode pour convertir un User pour la DB
    def to_row(self) -> UserRow:
        return UserRow(
            id=self.id,
            username=self.username,
            password=self.password,
            email=self.email,
            confirmed=self.confirmed
        )
    
    # ... et pour l'enregistrer
    def store_row(self) -> int:
        user_row = self.to_row()

        with db.create_session().begin() as db_session:
            db_session.add(user_row)
            db_session.flush()
            id = user_row.id
        
        return id