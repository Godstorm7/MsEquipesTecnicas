from flask import Blueprint, request, jsonify, abort, current_app
from models import db
from models.EquipeTecnica import EquipeTecnica
from models.StatusEquipeEnum import StatusEquipeEnum
from models.MembroEquipe import MembroEquipe
import requests

equipe_bp = Blueprint('equipe', __name__)

    #    Rota de Create

##cria equipe
@equipe_bp.route('/api/v1/equipes', methods=['POST'])
def criar_equipe():
    data = request.get_json()
    nome = data.get('nome')
    especialidade = data.get('especialidade')
    status = data.get('status', 'ATIVA')
    membros = data.get('membros', [])

    if not nome or not especialidade:
        abort(400, 'Nome e especialidade são obrigatórios.')

    if len(membros) > 10:
        abort(400, 'Uma equipe não pode ter mais de 10 membros.')

    try:
        status_enum = StatusEquipeEnum[status.upper()]
    except KeyError:
        abort(400, 'Status inválido. Use "ativa" ou "inativa".')
    equipe = EquipeTecnica(nome=nome,
                           especialidade=especialidade,
                           status=status_enum
                           )
    db.session.add(equipe)
    db.session.flush()  # Para obter o ID da equipe
    for membro in membros:
        if not all(k in membro for k in ('nome', 'cargo', 'contato')):
            abort(400, 'Cada membro deve ter nome, cargo e contato.')
        m = MembroEquipe(
            nome=membro['nome'],
            cargo=membro['cargo'],
            contato=membro['contato'],
            equipe_id=equipe.id
        )
        db.session.add(m)
    db.session.commit()
    return jsonify({'id': equipe.id}), 201

###-------------------------------------------------------


    #       Rotas de Read


#consulta todas as equipes
@equipe_bp.route('/api/v1/equipes', methods=['GET'])
def listar_equipes():
    status = request.args.get('status')
    especialidade = request.args.get('especialidade')
    query = EquipeTecnica.query

    if status:
        try:
            status_enum = StatusEquipeEnum[status.upper()]
            query = query.filter_by(status=status_enum)
        except KeyError:
            abort(400, f'Status inválido: {status}. Use "ATIVA" ou "INATIVA".')

    if especialidade:
        query = query.filter(EquipeTecnica.especialidade.ilike(f'%{especialidade}%'))

    equipes = query.all()
    result = []
    for equipe in equipes:
        membros = [
            {'id': m.id, 'nome': m.nome, 'cargo': m.cargo, 'contato': m.contato}
            for m in equipe.membros
        ]
        result.append({
            'id': equipe.id,
            'nome': equipe.nome,
            'especialidade': equipe.especialidade,
            'status': equipe.status.value,
            'membros': membros
        })
    return jsonify(result)


#-------------------------------------------------------

#consulta equipe por id
@equipe_bp.route('/api/v1/equipes/<int:id>', methods=['GET'])
def consultar_equipe(id):
    equipe = EquipeTecnica.query.get_or_404(id)
    membros = [
        {'id': m.id, 'nome': m.nome, 'cargo': m.cargo, 'contato': m.contato}
        for m in equipe.membros
    ]
    return jsonify({
        'id': equipe.id,
        'nome': equipe.nome,
        'especialidade': equipe.especialidade,
        'status': equipe.status.value,
        'membros': membros
    })

#-------------------------------------------------------

##consultar status da equipe com id
@equipe_bp.route('/api/v1/equipes/status/ativa/<int:id>', methods=['GET'])
def consultar_equipe_ativa(id):
    equipe = EquipeTecnica.query.filter_by(id=id, status=StatusEquipeEnum.ATIVA).first_or_404()
    membros = [
        {'id': m.id, 'nome': m.nome, 'cargo': m.cargo, 'contato': m.contato}
        for m in equipe.membros
    ]
    return jsonify({
        'id': equipe.id,
        'nome': equipe.nome,
        'especialidade': equipe.especialidade,
        'status': equipe.status.value,
        'membros': membros
    })

#-------------------------------------------------------

##consultar status da equipe com id
@equipe_bp.route('/api/v1/equipes/<int:id>/status', methods=['GET'])
def consultar_status_equipe(id):
    equipe = EquipeTecnica.query.get_or_404(id)
    return jsonify({'id': equipe.id, 'status': equipe.status.value})

#-------------------------------------------------------


#       Rotas de Update


#atualiza equipe
@equipe_bp.route('/api/v1/equipes/<int:id>', methods=['PUT'])
def atualizar_equipe(id):
    equipe = EquipeTecnica.query.get_or_404(id)
    data = request.get_json()
    equipe.nome = data.get('nome', equipe.nome)
    equipe.especialidade = data.get('especialidade', equipe.especialidade)
    if 'status' in data:
        try:
            equipe.status = StatusEquipeEnum[data['status'].upper()]
        except KeyError:
            abort(400, 'Status inválido. Use "ativa" ou "inativa".')
    membros = data.get('membros')
    if membros is not None:
        if len(membros) > 10:
            abort(400, 'Uma equipe não pode ter mais de 10 membros.')
        for m in equipe.membros:
            db.session.delete(m)
        for membro in membros:
            if not all(k in membro for k in ('nome', 'cargo', 'contato')):
                abort(400, 'Cada membro deve ter nome, cargo e contato.')
            m = MembroEquipe(
                nome=membro['nome'],
                cargo=membro['cargo'],
                contato=membro['contato'],
                equipe_id=equipe.id
            )
            db.session.add(m)
    db.session.commit()
    return jsonify({'message': 'Equipe atualizada com sucesso.'})


###-------------------------------------------------------

#atualiza status da equipe
@equipe_bp.route('/api/v1/equipes/<int:id>/<status>', methods=['PATCH'])
def atualizar_status_equipe(id, status):
    equipe = EquipeTecnica.query.get_or_404(id)
    try:
        equipe.status = StatusEquipeEnum[status.upper()]
    except KeyError:
        abort(400, 'Status inválido. Use "ativa" ou "inativa".')
    db.session.commit()
    return jsonify({'message': 'Status da equipe atualizado com sucesso.'})

###-------------------------------------------------------


    #       Rota de Delete


#deleta equipe ou desativa
@equipe_bp.route('/api/v1/equipes/<int:id>', methods=['DELETE'])
def desativar_ou_deletar_equipe(id):
    token = request.headers.get("Authorization")
    headers = {
        "Authorization": token
    }
    equipe = EquipeTecnica.query.get_or_404(id)
    url_ordens = current_app.config["MS_ORDEM_SERVICE_URL"] + f'/orders/filter?teamId={id}'
    try:
        response = requests.get(url_ordens,headers=headers, timeout=3)
        response.raise_for_status()
        ordens = response.json()
        #feito isso abaixo porque os cara usaram umas page ai da vida
        ordens = ordens['content']
    # em caso de erro faz o L
    except Exception as e:
        return jsonify({'error': 'Não foi possível consultar o microserviço de ordens de serviço.', 'detalhe': str(e)}), 503
    if ordens:
        #print(f'Ordens de serviço associadas encontradas para a equipe {id}: {ordens}')
        equipe.status = StatusEquipeEnum.INATIVA  # Desativação lógica
        db.session.commit()
        return jsonify({'message': 'Equipe desativada (existem ordens de serviço associadas).'}), 200
    else:
        db.session.delete(equipe)
        db.session.commit()
        return jsonify({'message': 'Equipe excluída com sucesso.'}), 200

    # else:
    #     return jsonify({'message': 'Equipe não possui ordens de serviço associadas. Exclusão física não permitida pela política atual.'}), 200
    # db.session.delete(equipe)
    # db.session.commit()
    # return jsonify({'message': 'Equipe excluída com sucesso.'}), 200