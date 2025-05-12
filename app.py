from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from models.user import User, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/meubanco'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return "Olá Flask"

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Nome de usuário e senha são obrigatórios!"
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return 'Logado com sucesso'
    else:
        return 'Credenciais incorretas'


@app.route("/cadastro", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not password:
        return "Nome de usuário e senha são obrigatórios!"
    
    if not email:
        return "Email é obrigatório!"
    
    if User.query.filter_by(username=name).first():
        return "Nome de usuário já existe!"
    
    user = User(username=name, email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return 'ok'