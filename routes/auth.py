from flask import Blueprint, request, session
from models.user import db, User
from helpers import login_required

auth = Blueprint("auth", __name__)

 #Rotas para autenticação
@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Nome de usuário e senha são obrigatórios!", 400
    
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session["user_id"] = user.id
        session["access_level"] = user.access_level
        return "Logado com sucesso", 200
    else:
        return "Credenciais incorretas", 401
    
@auth.route("/cadastro", methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    access_level = request.form.get("access")

    if not username or not password:
        return "Nome de usuário e senha são obrigatórios!", 400
    
    if not email:
        return "Email é obrigatório!", 400
    
    if not access_level:
        return "Selecione um nível de acesso!", 400
    
    if User.query.filter_by(username=username).first():
        return "Nome de usuário já existe!", 409
    
    match access_level:
        case 'Administrador':
            access_level='a'
        case 'Porteiro':
            access_level='p'
        case _:
            return "Inválido!", 400
    
    user = User(username=username, email=email, access_level=access_level)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return "Registrado com sucesso", 201

@auth.route("/logout")
@login_required
def logout():
    session.clear()
    return "Sessão Limpa.", 204

@auth.route("/nivel-acesso")
@login_required
def get_access_level():
    access_level = session.get("access_level")
    return access_level