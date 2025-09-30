from models import db
from models.StatusEquipeEnum import StatusEquipeEnum

class EquipeTecnica(db.Model):
    __tablename__ = 'equipe_tecnica'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(StatusEquipeEnum), nullable=False, default=StatusEquipeEnum.ATIVA)
    membros = db.relationship('MembroEquipe', backref='equipe', cascade='all, delete-orphan')

    def __init__(self, nome, especialidade, status=StatusEquipeEnum.ATIVA):
        self.nome = nome
        self.especialidade = especialidade
        self.status = status

    def __repr__(self):
        return f'<EquipeTecnica {self.nome}>'
