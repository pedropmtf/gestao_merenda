
from app import create_app
from app.models import db, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()



nome = input("Nome: ")
email = input("Email: ")
senha = input("Senha: ")


user = User()
user.name = nome
user.email = email
user.password = generate_password_hash(senha)

with app.app_context():
        db.session.add(user)
        db.session.commit()