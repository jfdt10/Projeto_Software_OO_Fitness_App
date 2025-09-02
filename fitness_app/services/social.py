"""
Serviço Social para o aplicativo de fitness.
Este Módulo fornece funcionalidades de social como compartilhar progresso e participar de desafios
"""

from fitness_app.core.models import Desafio
from fitness_app.core.database import RepositorioTinyDB
from fitness_app.core.abc import ServicoBase


class ServicoSocial(ServicoBase):
    def __init__(self, repo=None):
        super().__init__(repo or RepositorioTinyDB('desafios'))
        # Aqui usei Composição: ServicoSocial "possui" uma instância base de Desafio
        self.desafio_base = Desafio(
            nome="",
            descricao="",
            data_inicio="",
            data_fim="",
            participantes=[]
        )

    def criar(self, nome, descricao, data_inicio, data_fim, participantes=None):
        # Usa a classe da instância base para criar novo desafio
        desafio = type(self.desafio_base)(
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            participantes=participantes or []
        )
        self.repo.inserir(desafio)
        return desafio

    def listar(self, usuario_email=None):
        # Usa a classe da instância base para o model_cls
        desafios = self.repo.listar(model_cls=type(self.desafio_base))
        if usuario_email:
            return [d for d in desafios if usuario_email in getattr(d, 'participantes', [])]
        return desafios

    def participar_desafio(self, desafio_id, usuario_email):
        # Usa a classe da instância base para o model_cls
        desafio = self.repo.obter(desafio_id, model_cls=type(self.desafio_base))
        if desafio:
            desafio.add_participante(usuario_email)
            self.repo.atualizar(desafio_id, {'participantes': desafio.participantes})
            print("Inscrição no desafio realizada com sucesso!")
            return True
        print("Desafio não encontrado.")
        return False

    def sair_desafio(self, desafio_id, usuario_email):
        # Usa a classe da instância base para o model_cls
        desafio = self.repo.obter(desafio_id, model_cls=type(self.desafio_base))
        if desafio:
            desafio.remove_participante(usuario_email)
            self.repo.atualizar(desafio_id, {'participantes': desafio.participantes})
            print("Você saiu do desafio.")
            return True
        print("Desafio não encontrado.")
        return False

    def atualizar(self, id, dados: dict):
        campos_permitidos = ['nome', 'descricao', 'data_inicio', 'data_fim']
        dados_validos = {k: v for k, v in dados.items() if k in campos_permitidos and v}

        if not dados_validos:
            print("Nenhum dado válido para atualização.")
            return False

        if self.repo.atualizar(id, dados_validos):
            print("Desafio atualizado com sucesso!")
            return True
        
        print("Falha ao atualizar o desafio.")
        return False

    def deletar(self, id):
        return self.repo.deletar(id)

 