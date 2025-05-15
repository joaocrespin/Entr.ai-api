from flask import Flask, request

from models.user import User, db
from models.student import Student
from models.authorized_member import Authorized

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/meubanco'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return "Olá Flask"

# Terminar CRUDS 2

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
@app.route("/membros", methods=["GET"])
def get_members():
    authorized_members = Authorized.query.all()
    members_list = []
    for member in authorized_members:
        members_list.append({
            "id": member.authorized_id,
            "name": member.authorized_name,
            "cpf": member.cpf,
            "photo": member.photo
        })            
    
    return  members_list

@app.route("/membros", methods=["POST"])
def auth_member_signup():
    auth_name = request.form.get("name")
    cpf = request.form.get("cpf")
    photo = request.form.get("photo")

    # Verificar dados enviados
    member = Authorized(authorized_name=auth_name, cpf=cpf, photo=photo)
    db.session.add(member)
    db.session.commit()

    return "Cadastrado com sucesso!"

@app.route("/membros/<int:id>", methods=["GET"])
def get_member(id):
    member = Authorized.query.get(id)

    if member:
        return [{
            "id": member.authorized_id,
            "name": member.authorized_name,
            "cpf": member.cpf,
            "photo": member.photo
        }]
    
    return "Membro não encontrado!"

@app.route("/membros/update/<int:id>", methods=["POST"])
def update_member(id):
    member = Authorized.query.get(id)

    if not member:
        return "Não encontrado!"
    
    new_name = request.form.get("name")
    new_cpf = request.form.get("cpf")
    new_photo = request.form.get("photo")

    if not new_name or not new_cpf or not new_photo:
        return "Preencha todos os campos!"
    
    # Verifica se o novo CPF pertence a alguém já cadastrado
    if Authorized.query.filter(Authorized.cpf == new_cpf, member.authorized_id != id).first():
        return "CPF já cadastrado em outro membro autorizado!"
    
    member.authorized_name = new_name
    member.cpf = new_cpf
    member.photo = new_photo

    # TODO: Estudar transactions
    db.session.commit()
    
    return [{
            "id": member.authorized_id,
            "name": member.authorized_name,
            "cpf": member.cpf,
            "photo": member.photo
        }]

@app.route("/membros/delete/<int:id>", methods=["POST"])
def delete_member(id):
    member = Authorized.query.get(id)

    if not member:
        return "Membro não encontrado"
    
    db.session.delete(member)
    db.session.commit()

    return "Apagado com sucesso!"

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