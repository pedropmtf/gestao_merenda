
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.core import IntegerField, FloatField, SelectField
from wtforms.fields.html5 import SearchField 


 
db = SQLAlchemy(session_options={"autoflush": False})
login_manager = LoginManager()

@login_manager.user_loader
def current_user(id):
    return User.query.get(id)

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable = False)
    email = db.Column(db.String(84), nullable= False, unique= True, index=True)
    password = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name
"""
pratos_alimentos = db.Table("pratos_alimentos",
                            db.Column("pratos_id", db.Integer, db.ForeignKey('Pratos.pratos_id'), primary_key=True),
                            db.Column("alimentos_id", db.Integer, db.ForeignKey('Alimentos.alimentos_id'), primary_key=True)
                            )

"""                            

class pratos_alimentos(db.Model, UserMixin):
    __tablename__ = "pratos_alimentos_association"
    Pratos_id = db.Column(db.Integer, db.ForeignKey('Pratos.pratos_id', ondelete="CASCADE"), primary_key=True)
    Alimentos_id = db.Column(db.Integer, db.ForeignKey('Alimentos.alimentos_id'), primary_key=True)
    quantidade = db.Column(db.Integer)
    alimentos = db.relationship('Alimentos', back_populates = "")
    pratos = db.relationship('Pratos', back_populates ="alimentos_relat")


class Movimentos(db.Model, UserMixin):
    __tablename__ = 'Movimentos'
    id = db.Column(db.Integer, primary_key=True)
    Alimentos_id = db.Column(db.Integer, db.ForeignKey('Alimentos.alimentos_id'), primary_key=True)
    origem_id = db.Column(db.Integer, db.ForeignKey('Escolas.id'), primary_key=True)
    destino_id = db.Column(db.Integer, db.ForeignKey('Escolas.id'), primary_key=True)
    nota_fiscal = db.Column(db.Integer)
    quantidade = db.Column(db.Integer)
    alimentos = db.relationship('Alimentos', back_populates="alimentos_relat")
    origem = db.relationship('Escolas', foreign_keys=[origem_id])
    destino = db.relationship('Escolas', foreign_keys=[destino_id])
    
class Estoque(db.Model, UserMixin):
    __tablename__ = 'Estoque'
    id = db.Column(db.Integer, primary_key=True)
    alimento_id = db.Column(db.Integer, db.ForeignKey('Alimentos.alimentos_id'), primary_key=True)
    escola_id = db.Column(db.Integer, db.ForeignKey('Escolas.id'), primary_key=True)
    quantidade = db.Column(db.Integer)
    alimentos = db.relationship('Alimentos', back_populates="alimentos_estocados")
    escolas = db.relationship('Escolas', back_populates="escolas_estoques")

class Pratos(db.Model, UserMixin):
    __tablename__ = "Pratos"
    pratos_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(84))
    descricao = db.Column(db.String(200))
    #alimentos_relat = db.relationship('Alimentos', secondary=pratos_alimentos, backref=db.backref('alimentos_usados', lazy='dynamic'))
    alimentos_relat = db.relationship("pratos_alimentos", back_populates="pratos", cascade="all, delete", passive_deletes=True)


class Alimentos(db.Model, UserMixin):
    __tablename__ = "Alimentos"
    alimentos_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(84), nullable = False)
    energia = db.Column(db.Float)
    proteina = db.Column(db.Float)
    lipideos = db.Column(db.Float)
    carboidratos = db.Column(db.Float)
    calcio = db.Column(db.Float)
    ferro = db.Column(db.Float)
    retinol = db.Column(db.Float)
    vitamina_c = db.Column(db.Float)
    sodio = db.Column(db.Float)
    restricao = db.Column(db.Integer)
    pratos_relat = db.relationship("pratos_alimentos", back_populates="alimentos")
    alimentos_relat = db.relationship("Movimentos", back_populates="alimentos")
    alimentos_estocados = db.relationship("Estoque", back_populates="alimentos")

class Roles(db.Model, UserMixin):
    __tablename__ = "Roles"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(84), nullable = False)

class Setores(db.Model, UserMixin):
    __tablename__ = 'Setores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(84))
    
class Escolas(db.Model, UserMixin):
    __tablename__ = 'Escolas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(84))
    bairro = db.Column(db.String(84))
    endereco = db.Column(db.String(84))
    alunos = db.Column(db.Integer)
    escolas_estoques = db.relationship("Estoque", back_populates="escolas")


class Satisfacao(db.Model, UserMixin):
    __tablename__ = 'Satisfacao'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)





#######################################################
#               FORMS
#######################################################

class LoginForm(FlaskForm):
    login = StringField('login')
    password = PasswordField('password')

class NovoAlimentoForm(FlaskForm):
    nome = StringField('nome')
    energia = FloatField('energia')
    proteina = FloatField('proteina')
    lipideos = FloatField('lipideos')
    carboidratos = FloatField('carboidratos')
    calcio = FloatField('calcio')
    ferro = FloatField('ferro')
    retinol = FloatField('retinol')
    vitamina_c = FloatField('vitamina_c')
    sodio = FloatField('sodio')
    restricao = IntegerField('restricao')

class EntradaProdutos(FlaskForm):
    origem = SelectField('origem')
    destino = SelectField('destino')
    quantidade = FloatField('quantidade')
    alimento = SelectField('alimento')
    notaFiscal = IntegerField('notaFiscal')

class novaEscolaForm(FlaskForm):
    nome = StringField('nome')
    endereco = StringField('endereco')
    bairro = StringField('bairro')
    alunos = IntegerField('alunos')

class novoPratoForm(FlaskForm):
    nome = StringField('nome')
    descricao = StringField('descricao')
    

class selectFieldAlimento(FlaskForm):
    alimento_select = SelectField('alimento', choices=[])
    search = SearchField('search')
    quantidade_select = IntegerField('quantidade')

class selectEscolaQRCode(FlaskForm):
    escola_select = SelectField('escola', choices=[])






