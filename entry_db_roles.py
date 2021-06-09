from app import create_app
from app.models import db, Roles

app = create_app()
app.app_context().push()

roles = ["Admin", "Almoxarife", "Nutricionista", "Escola"]

for i in roles:
    role = Roles()
    role.nome = i 
    db.session.add(role)
    db.session.commit() 