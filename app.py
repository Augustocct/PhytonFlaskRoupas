from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roupas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Roupa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tamanho = db.Column(db.String(10))
    preco = db.Column(db.Float)

@app.route('/')
def main():
    roupas = Roupa.query.all()
    return render_template('index.html', roupas=roupas)

@app.route('/add', methods=['POST'])
def add_roupa():
    data = request.get_json()

    nova_roupa = Roupa(
        nome=data['nome'],
        tamanho=data['tamanho'],
        preco=data['preco']
    )
    db.session.add(nova_roupa)
    db.session.commit()

    return jsonify({'message': 'Roupa adicionada com sucesso!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)