import pandas as pd
from app import create_app
from app.models import db, Alimentos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = create_app()
app.app_context().push()




df = pd.read_csv('tabela_nutricional.csv', sep=";" , encoding='windows-1252')

for index, row in df.iterrows():
    alimento = Alimentos()
    alimento.nome = row['Tabela de composicao em 100g de alimento']
    alimento.energia = row['Energia (kcal)']
    alimento.proteina = row['Proteina (g)']
    alimento.lipideos = row['Lipideos (g)']
    alimento.carboidratos = row['Carboidratos (g)']
    alimento.calcio = row['Calcio (mg)']
    alimento.ferro = row['Ferro (mg)']
    alimento.retinol = row['Retinol (mcg)']
    alimento.vitamina_c = row['Vitamina C (mg)']
    alimento.sodio = row['Sodio  (mg)']
    alimento.restricao = row['Cod.']
    with app.app_context():
        db.session.add(alimento)
        db.session.commit()
