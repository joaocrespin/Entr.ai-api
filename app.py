from flask import Flask
from database import db

from routes.main import main
from routes.auth import auth
from routes.members import members
from routes.students import students

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/meubanco'

app.secret_key = "segredo"

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(members)
app.register_blueprint(students)
