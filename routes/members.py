from flask import Blueprint, request, jsonify
from database import db
from models.authorized_member import Authorized
from helpers import login_required

members = Blueprint("members", __name__)

# Rotas parar membros autorizados
@members.route("/membros", methods=["GET"])
@login_required
def get_members():
    authorized_members = Authorized.query.all()

    if not authorized_members:
        return jsonify(message="Nenhum membro autorizado encontrado!"), 404

    members_list = []
    for member in authorized_members:
        members_list.append({
            "id": member.authorized_id,
            "name": member.authorized_name,
            "cpf": member.cpf,
            "photo": member.photo,
            "position": member.position
        })            
    
    return members_list

@members.route("/membros", methods=["POST"])
@login_required
def auth_member_signup():
    auth_name = request.form.get("name")
    cpf = request.form.get("cpf")
    position = request.form.get("position")
    photo = request.form.get("photo")

    if not auth_name or not cpf or not position:
        return jsonify(message="Preencha todos os campos!"), 400
    
    auth_name = auth_name.strip()
    
    position = position.strip()

    if len(cpf) != 11:
        print(len(cpf))
        return jsonify(message="CPF inválido!"), 400
    
    if Authorized.query.filter(Authorized.cpf == cpf).first():
        return jsonify(message="CPF já cadastrado em outro membro autorizado!"), 409

    member = Authorized(authorized_name=auth_name, cpf=cpf, position=position, photo=photo)
    db.session.add(member)
    db.session.commit()

    return jsonify(message="Autorizado cadastrado com sucesso!"), 201

@members.route("/membros/<int:id>", methods=["GET"])
@login_required
def get_member(id):
    member = Authorized.query.get(id)

    if member:
        return [{
            "id": member.authorized_id,
            "name": member.authorized_name,
            "cpf": member.cpf,
            "position": member.position,
            "photo": member.photo
        }]
    
    return jsonify(message="Membro não encontrado!"), 404

@members.route("/membros/<int:id>", methods=["PUT"])
@login_required
def update_member(id):
    member = Authorized.query.get(id)

    if not member:
        return jsonify(message="Não encontrado!"), 404
    
    new_name = request.form.get("name")
    new_cpf = request.form.get("cpf")
    new_position = request.form.get("position")
    new_photo = request.form.get("photo")

    if not new_name or not new_cpf or not new_position:
        return jsonify(message="Preencha todos os campos!"), 400
    
    new_name = new_name.strip()

    new_position = new_position.strip()
    
    if len(new_cpf) != 11:
        print(len(new_cpf))
        return jsonify(message="CPF inválido!"), 400
    
    # Verifica se o novo CPF pertence a alguém já cadastrado
    if Authorized.query.filter(Authorized.cpf == new_cpf, member.authorized_id != id).first():
        return jsonify(message="CPF já cadastrado em outro membro autorizado!"), 409
    
    member.authorized_name = new_name
    member.cpf = new_cpf
    member.photo = new_photo
    member.position = new_position

    db.session.commit()
    
    return jsonify(message="Alterações salvas com sucesso!")

@members.route("/membros/<int:id>", methods=["DELETE"])
@login_required
def delete_member(id):
    member = Authorized.query.get(id)

    if not member:
        return jsonify(message="Membro não encontrado"), 404
    
    db.session.delete(member)
    db.session.commit()

    return jsonify(message="Apagado com sucesso!"), 204