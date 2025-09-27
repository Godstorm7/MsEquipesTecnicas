from models import db

class MembroEquipe(db.Model):
    __tablename__ = 'membro_equipe'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(100), nullable=False)
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipe_tecnica.id'), nullable=False)

    def __init__(self, nome, cargo, contato, equipe_id):
        self.nome = nome
        self.cargo = cargo
        self.contato = contato
        self.equipe_id = equipe_id

    def __repr__(self):
        return f'<MembroEquipe {self.nome}>'