from flask import Blueprint, request,jsonify
from database import db
from models.student import Student
from helpers import login_required

students = Blueprint("student", __name__)

# Rotas de aluno
@students.route("/aluno/cadastro", methods=["POST"])
@login_required
def student_signup():
    id = request.form.get("id")
    name = request.form.get("name")
    school_class = request.form.get("class")

    if not id:
        return jsonify(message="Insira o id do aluno!"), 400
    
    if not id.isdigit():
        return jsonify(message="O id do aluno precisa ser um número!"), 400
    
    if not name or not school_class:
        return jsonify(message="Nome e classe são obrigatórios!"), 400
    
    student = Student(student_id=id, student_name=name, school_class=school_class)
    db.session.add(student)
    db.session.commit()

    return jsonify(message="Aluno cadastrado com sucesso!"), 201