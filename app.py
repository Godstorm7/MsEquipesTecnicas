from flask import Flask, request
from config import Config
from models import db
from models.auth import jwt_required
from routes.equipe import equipe_bp
from routes.membro import membro_bp

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

@app.before_request
def check_token_before_request():
    public_paths = ['/']
    if request.path in public_paths:
        return

    auth_error = jwt_required()

    if auth_error:
        return auth_error

with app.app_context():
    db.create_all()

app.register_blueprint(equipe_bp)
app.register_blueprint(membro_bp)

def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()