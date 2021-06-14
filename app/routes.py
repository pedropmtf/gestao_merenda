#from flask.app.models import current_user
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Alimentos, EntradaProdutos, LoginForm, NovoAlimentoForm, Escolas, novaEscolaForm, novoPratoForm, Pratos, selectEscolaQRCode, selectFieldAlimento, pratos_alimentos, selectEscolaQRCode
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
        a = Pratos.query.filter_by(pratos_id=id).join(pratos_alimentos).join(Alimentos).first()

        if a != None:
            todos_alimentos = a.alimentos_relat

        if form.validate_on_submit():
            alimento_escolhido_id = form.alimento_select.data
            quant = pratos_alimentos(quantidade = form.quantidade_select.data)
            quant.alimentos = Alimentos.query.filter_by(alimentos_id = alimento_escolhido_id).first()
            pratos = Pratos.query.filter_by(pratos_id = id).first()
            pratos.alimentos_relat.append(quant)
            db.session.commit()
            return redirect(url_for('prato_nome', id=id))
        return render_template("prato_nome.html", nome = pratos.nome, form = form, todos_alimentos=todos_alimentos)



    @app.route('/info_prato/<id>', methods=['GET', 'POST'])
    def info_prato(id):
        #######
        a = Pratos.query.filter_by(pratos_id=id).join(pratos_alimentos).join(Alimentos).first()
        b =[]
        if a != None:
            for i in a.alimentos_relat:
                b.append(i.alimentos)
        ######
        graphJSON = createGraphs(b)
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
        form.origem.choices = [ (escola.id, escola.nome) for escola in Escolas.query.all()]
        form.destino.choices = [ (escola.id, escola.nome) for escola in Escolas.query.all()]
        form.alimento.choices = [ (alimento.alimentos_id, alimento.nome) for alimento in Alimentos.query.all()]
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
        form = selectEscolaQRCode()
        form.escola_select.choices = [ (escola.id, escola.nome) for escola in Escolas.query.all()]
        return render_template('qrcode.html', form=form)

    @app.route('/qrcode/<escola>', methods=["GET", "POST"])
    def qrcode_escola(escola):
        makeQRCode()
        return render_template('')

    @app.route('/pesquisa')
    def pesquisa():
        return render_template('pesquisa.html')

    @app.route('/avaliacao')
    def avaliacao():
        return render_template('avaliacao.html')

    @app.route('/movimentos')
    def movimentos():
        return render_template('movimentos.html')

    @app.route('/delete/<id>')
    def delete_prato(id):
        prato = Pratos.query.filter_by(pratos_id=id).first()
        association_prato = pratos_alimentos.query.filter_by(Pratos_id=id).all()
        for i in association_prato:
            db.session.delete(i)
            db.session.commit()
        db.session.delete(prato)
        db.session.commit()
        return redirect(url_for("pratos"))