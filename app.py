from flask import Flask
from models import db
from routes.equipe import equipe_bp as equipe_bp
from routes.membro import membro_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345@localhost:5432/equipes-tecnicas'
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(equipe_bp)
app.register_blueprint(membro_bp)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
