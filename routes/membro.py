from flask import Blueprint, request, jsonify, abort
from models import db
from models.MembroEquipe import MembroEquipe
from models.EquipeTecnica import EquipeTecnica

membro_bp = Blueprint('membro', __name__)

@membro_bp.route('/membros', methods=['POST'])
def criar_membro():
    data = request.get_json()
    nome = data.get('nome')
    cargo = data.get('cargo')
    contato = data.get('contato')
    equipe_id = data.get('equipe_id')
    if not all([nome, cargo, contato, equipe_id]):
        abort(400, 'Nome, cargo, contato e equipe_id são obrigatórios.')
    equipe = EquipeTecnica.query.get(equipe_id)
    if not equipe:
        abort(404, 'Equipe não encontrada.')
    if len(equipe.membros) >= 10:
        abort(400, 'Uma equipe não pode ter mais de 10 membros.')
    membro = MembroEquipe(nome=nome, cargo=cargo, contato=contato, equipe_id=equipe_id)
    db.session.add(membro)
    db.session.commit()
    return jsonify({'id': membro.id}), 201

@membro_bp.route('/membros', methods=['GET'])
def listar_membros():
    membros = MembroEquipe.query.all()
    result = []
    for m in membros:
        result.append({
            'id': m.id,
            'nome': m.nome,
            'cargo': m.cargo,
            'contato': m.contato,
            'equipe_id': m.equipe_id
        })
    return jsonify(result)

@membro_bp.route('/membros/<int:id>', methods=['GET'])
def consultar_membro(id):
    m = MembroEquipe.query.get_or_404(id)
    return jsonify({
        'id': m.id,
        'nome': m.nome,
        'cargo': m.cargo,
        'contato': m.contato,
        'equipe_id': m.equipe_id
    })

@membro_bp.route('/membros/<int:id>', methods=['PUT'])
def atualizar_membro(id):
    m = MembroEquipe.query.get_or_404(id)
    data = request.get_json()
    m.nome = data.get('nome', m.nome)
    m.cargo = data.get('cargo', m.cargo)
    m.contato = data.get('contato', m.contato)
    db.session.commit()
    return jsonify({'message': 'Membro atualizado com sucesso.'})

@membro_bp.route('/membros/<int:id>', methods=['DELETE'])
def remover_membro(id):
    m = MembroEquipe.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': 'Membro removido com sucesso.'})

