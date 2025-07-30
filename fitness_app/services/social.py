"""
Serviço de Treino para o aplicativo de fitness.
Este Módulo fornece  funciionalidades de social  como compartilhar progresso e participar de desafios
"""

from fitness_app.core.models import Desafio
from fitness_app.core.database import inserir_registro, obter_registros, atualizar_registro, deletar_registro

class ServicoSocial:
    def __init__(self):
        pass
    
    def criar_desafio(self, nome, descricao, data_inicio, data_fim, participantes=None):
        desafio = Desafio(
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            participantes=participantes or []
        )
        return inserir_registro('desafios', desafio.to_dict())

    def listar_desafios(self):
        return [
            Desafio.from_dict(dado)
            for dado in obter_registros('desafios')
        ]

    def participar_desafio(self, doc_id, usuario_email):
        desafios = obter_registros('desafios')
        for desafio in desafios:
            if desafio.doc_id == doc_id:
                participantes = desafio.get('participantes', [])
                if usuario_email not in participantes:
                    participantes.append(usuario_email)
                    atualizar_registro('desafios', doc_id, {"participantes": participantes})
                break

    def deletar_desafio(self, doc_id):
        return deletar_registro('desafios', doc_id)