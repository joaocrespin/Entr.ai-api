from flask import Blueprint
from helpers import login_required
from models.user import User

main = Blueprint("main", __name__)

@main.route("/")
@login_required
def index():
    return "Olá Flask"

@main.route("/usuarios")
@login_required
def get_users():
    users = User.query.all()

    if not users:
        return "Nenhum membro autorizado encontrado!", 404

    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "access_level": user.access_level,
        })            
    
    return user_list