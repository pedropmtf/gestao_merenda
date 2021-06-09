#from flask.app.models import current_user
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Alimentos, EntradaProdutos, LoginForm, NovoAlimentoForm, Escolas, novaEscolaForm, novoPratoForm, Pratos, selectFieldAlimento
from makeqrcode import makeQRCode
from app import db
from app.models import User
from graphs import createGraphs

def init_app(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        form = LoginForm()
        if form.validate_on_submit():
            login = form.login.data
            password = form.password.data
            user = User.query.filter_by(email=login).first()
            if not user:
################################ Flash nao esta funcionando
                flash("Login ou Senha incorreta")
################################
                return redirect(url_for('index'))
            if not check_password_hash(user.password, password):
################################ Flash nao esta funcionando
                flash("Login ou Senha incorreta")
################################
                return redirect(url_for('index'))
            login_user(user)
            return redirect(url_for('home'))
        return render_template("index.html", form=form)


    @app.route('/home', methods=['GET', "POST"])
    @login_required
    def home():
        return render_template('home.html')

    @app.route('/estoque')
    def estoque():
        return render_template('estoque.html')

    @app.route('/novos_produtos')
    def novos_produtos():
        return render_template('novosprodutos.html')

    @app.route('/pratos')
    def pratos():
        todos_pratos = Pratos.query.all() 
        return render_template('pratos.html', todos_pratos = todos_pratos)

    @app.route('/cardapio')
    def cardapio():
        return render_template('cardapio.html')

    ROWS_PER_PAGE = 10
    @app.route('/alimentos')
    def alimentos():
        page = request.args.get('page', 1, type=int)
        alimentos = Alimentos.query.order_by(Alimentos.nome).paginate(page=page, per_page=ROWS_PER_PAGE)
        return render_template('alimentos.html', alimentos=alimentos)

    @app.route('/novo_prato', methods=['GET', 'POST'])
    def novo_prato():
        form = novoPratoForm()
        if form.validate_on_submit():
            prato = Pratos()
            prato.nome = form.nome.data
            prato.descricao = form.descricao.data
            db.session.add(prato)
            db.session.commit()
            id = prato.pratos_id
            return redirect(url_for('prato_nome', id=id))
        return render_template('novo_prato.html', form=form)

    @app.route('/prato_nome/<int:id>', methods=["GET", "POST"])
    def prato_nome(id):
        pratos = Pratos.query.filter_by(pratos_id= id).first()
        form = selectFieldAlimento()
        form.alimento_select.choices = [ (alimento.alimentos_id, alimento.nome) for alimento in Alimentos.query.all()]
        if form.validate_on_submit():
            alimento_escolhido_id = form.alimento_select.data
            alimento_escolhido = Alimentos.query.filter_by(alimentos_id = alimento_escolhido_id).first()
            prato = Pratos.query.filter_by(pratos_id = id).first()
            alimento_escolhido.alimentos_usados.append(prato)
            db.session.commit()
            return redirect(url_for('prato_nome', id=id))
        return render_template("prato_nome.html", nome = pratos.nome, form = form, todos_alimentos = pratos.alimentos_relat)

    @app.route('/info_prato/<id>', methods=['GET', 'POST'])
    def info_prato(id):
        alimentos = Pratos.query.filter_by(pratos_id=id).first().alimentos_relat
        graphJSON = createGraphs(alimentos)
        return render_template('info_prato.html', id=id, graphJSON=graphJSON)


    @app.route('/escolas')
    def escolas():
        escolas = Escolas.query.all()
        return render_template('escolas.html', escolas=escolas)

    @app.route('/nova_escola')
    def nova_escola():
        form = novaEscolaForm()
        return render_template('nova_escola.html', form=form)

    @app.route('/financeiro')
    def financeiro():
        return render_template('financeiro.html')

    @app.route('/entrada_produtos')
    def entrada_produtos():
        form = EntradaProdutos()
        return render_template('entrada_produtos.html', form=form)

    @app.route('/saida_produtos')
    def saida_produtos():
        return render_template('saida_produtos.html')

    @app.route('/novo_alimento', methods=['GET', 'POST'])
    def novo_alimento():
        form = NovoAlimentoForm()
        if form.validate_on_submit():
            alimento = Alimentos()
            alimento.nome = form.nome.data
            alimento.energia = form.energia.data
            alimento.proteina = form.proteina.data
            alimento.lipideos = form.lipideos.data
            alimento.carboidratos = form.carboidratos.data
            alimento.calcio = form.calcio.data
            alimento.ferro = form.ferro.data
            alimento.retinol = form.retinol.data
            alimento.vitamina_c = form.vitamina_c.data
            alimento.sodio = form.sodio.data
            alimento.restricao = form.restricao.data
            db.session.add(alimento)
            db.session.commit()

        return render_template('novo_alimento.html', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/qrcode')
    def qrcode():
        makeQRCode()
        return render_template('qrcode.html')

    @app.route('/pesquisa')
    def pesquisa():
        return render_template('pesquisa.html')