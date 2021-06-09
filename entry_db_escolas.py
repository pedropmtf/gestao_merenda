import pandas as pd
from app import create_app
from app.models import db, Escolas

app = create_app()
app.app_context().push()

df = pd.read_csv('escolas.csv', sep=';', encoding='windows-1252')

for index, row in df.iterrows():
    escola = Escolas()
    escola.nome = row['Escola']
    escola.bairro = row['Bairro']
    escola.endereco = row['Endereco']
    escola.alunos = row['Alunos']
    with app.app_context():
        db.session.add(escola)
        db.session.commit()