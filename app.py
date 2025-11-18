from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roupas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float)
    criado_em = db.Column(db.DateTime, default=db.func.current_timestamp())
    editado_em = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    tipo = db.Column(db.String(50))  # Campo para discriminar o tipo de produto

    __mapper_args__ = {
        'polymorphic_identity': 'produto',
        'polymorphic_on': tipo
    }

class Roupa(Produto):
    __mapper_args__ = {
        'polymorphic_identity': 'roupa',
    }
    tamanho = db.Column(db.String(10))

class Acessorios(Produto):
    __mapper_args__ = {
        'polymorphic_identity': 'acessorio',
    }
    tipo_acessorio = db.Column(db.String(50))

@app.route('/')
def main():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # quantidade de itens por página
    pagination = Roupa.query.paginate(page=page, per_page=per_page, error_out=False)
    roupas = pagination.items
    return render_template('index.html', roupas=roupas, pagination=pagination)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastrar.html')

@app.route('/editar')
def editar():
    produtos = Produto.query.all()
    return render_template('editar.html', produtos = produtos)

@app.route('/add', methods=['POST'])
def add_roupa():
    nome = request.form.get('nome')
    tamanho = request.form.get('tamanho')
    preco = request.form.get('preco')
    preco_limpo = preco.replace('R$', '').replace('.', '').replace(',', '.').strip()
    preco_float = float(preco_limpo)

    nova_roupa = Roupa(
        nome=nome,
        tamanho=tamanho,
        preco=preco_float,
        criado_em=db.func.current_timestamp(),
        editado_em=db.func.current_timestamp()
    )
    db.session.add(nova_roupa)
    db.session.commit()
    return redirect(url_for('cadastro', sucesso=True))

@app.route('/edit/<int:id>', methods=['POST'])
def editar_roupa(id):
    roupa = Roupa.query.get_or_404(id)
    nome = request.form.get('nome')
    tamanho = request.form.get('tamanho')
    preco = request.form.get('preco')
    preco = request.form.get('preco')
    if preco is None or preco.strip() == '':
        preco_float = roupa.preco  # mantém o valor antigo se não vier nada novo
    else:
        preco_limpo = preco.replace('R$', '').replace(',', '.').strip()
        preco_float = float(preco_limpo)

    roupa.nome = nome
    roupa.tamanho = tamanho
    roupa.preco = preco_float
    db.session.commit()
    return redirect(url_for('editar'))

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_roupa(id):
    roupa = Roupa.query.get_or_404(id)
    db.session.delete(roupa)
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/add_acessorio', methods=['POST'])
def add_acessorio():
    nome = request.form.get('nome')
    tipo_acessorio = request.form.get('tipo_acessorio')
    preco = request.form.get('preco')
    preco_limpo = preco.replace('R$', '').replace('.', '').replace(',', '.').strip()
    preco_float = float(preco_limpo)

    novo_acessorio = Acessorios(
        nome=nome,
        tipo_acessorio=tipo_acessorio,
        preco=preco_float,
        criado_em=db.func.current_timestamp(),
        editado_em=db.func.current_timestamp()
    )
    db.session.add(novo_acessorio)
    db.session.commit()
    return redirect(url_for('cadastro', sucesso=True))
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)