from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from models.user import User, db
from models.student import Student

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/meubanco'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return "Olá Flask"

# Terminar CRUDS

# Rotas para autenticação
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
    username = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not password:
        return "Nome de usuário e senha são obrigatórios!"
    
    if not email:
        return "Email é obrigatório!"
    
    if User.query.filter_by(username=username).first():
        return "Nome de usuário já existe!"
    
    user = User(username=username, email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return 'Registrado com sucesso'

# Rotas parar membros autorizados
# Rota básica para testes
@app.route("/teste/cad", methods=["POST"])
def auth_member_signup():
    auth_name = request.form.get("name")
    cpf = request.form.get("cpf")
    photo = "simulação de foto"

    # Verificar dados enviados

    return "Cadastrado com sucesso!"

# Rotas de aluno
@app.route("/aluno/cadastro", methods=["POST"])
def student_signup():
    id = request.form.get("id")
    name = request.form.get("name")
    school_class = request.form.get("class")

    if not id:
        return "Insira o id do aluno!"
    
    if not name or not school_class:
        return "Nome e classe são obrigatórios!"
    
    student = Student(student_id=id, student_name=name, school_class=school_class)
    db.session.add(student)
    db.session.commit()

    return "Aluno cadastrado com sucesso!"
