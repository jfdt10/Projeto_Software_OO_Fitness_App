"""
Serviço para gerenciar feedbacks dos usuários na aplicação de fitness.
Este módulo fornece funcionalidades para criar, listar, atualizar e deletar feedbacks.

"""
from datetime import datetime
from tinydb import Query as Q
from fitness_app.core.abc import ServicoBase
from fitness_app.core.database import RepositorioTinyDB
from fitness_app.core.models import Feedback

class ServicoFeedback(ServicoBase):
    def __init__(self, repo=None):
        super().__init__(repo or RepositorioTinyDB('feedbacks'))
        # Aqui usei Composição: ServicoFeedback "possui" uma instância base de Feedback
        self.feedback_base = Feedback(
            usuario_email="",
            texto="",
            nota=1,
            data=""
        )

    def criar(self, usuario_email, texto, nota, data):
        try:
            if nota is None:
                raise ValueError("A nota é obrigatória")
            nota = int(nota)
        except (TypeError, ValueError):
            raise ValueError("A nota deve ser um número inteiro entre 1 e 5")
        if nota < 1 or nota > 5:
            raise ValueError("A nota deve ser um número inteiro entre 1 e 5")
        
        # Usa a classe da instância base para criar novo feedback
        feedback = type(self.feedback_base)(
            usuario_email=usuario_email, 
            texto=texto, 
            nota=nota, 
            data=data or datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        return self.repo.inserir(feedback)

    def listar(self, usuario_email=None):
        query = None
        if usuario_email:
            q = Q()
            query = q.usuario_email == usuario_email
        # Usa a classe da instância base para o model_cls
        return self.repo.listar(query=query, model_cls=type(self.feedback_base))
    
    def deletar(self, id):
        q = Q()
        if isinstance(id, str) and "@" in id:
            registros = self.repo.listar(query=(q.usuario_email == id))
            if not registros:
                return False
            feedback_id = registros[0].get("id")
            if not feedback_id:
                return False
            return self.repo.deletar(feedback_id)
        return self.repo.deletar(id)

    def atualizar(self, id, dados=None, novo_texto=None, nova_nota=None, nova_data=None):
        q = Q()
        if isinstance(id, str) and "@" in id:
            registros = self.repo.listar(query=(q.usuario_email == id))
            if not registros:
                return False
            id = registros[0].get("id")

        if dados:
            if "nota" in dados and dados["nota"] is not None:
                try:
                    n = int(dados["nota"])
                except (TypeError, ValueError):
                    raise ValueError("Nota deve ser um inteiro entre 1 e 5.")
                if not (1 <= n <= 5):
                    raise ValueError("Nota deve estar entre 1 e 5.")
                dados["nota"] = n
            return self.repo.atualizar(id, dados)

        novos_dados = {}
        if novo_texto is not None:
            novos_dados["texto"] = novo_texto
        if nova_nota is not None:
            try:
                n = int(nova_nota)
            except (TypeError, ValueError):
                raise ValueError("Nota deve ser um inteiro entre 1 e 5.")
            if not (1 <= n <= 5):
                raise ValueError("Nota deve estar entre 1 e 5.")
            novos_dados["nota"] = n
        if nova_data is not None:
            novos_dados["data"] = nova_data

        if not novos_dados:
            return False

        return self.repo.atualizar(id, novos_dados)