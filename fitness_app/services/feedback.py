"""
Serviço para gerenciar feedbacks dos usuários na aplicação de fitness.
Este módulo fornece funcionalidades para criar, listar, atualizar e deletar feedbacks.

"""

from fitness_app.core.database import inserir_registro, obter_registros, deletar_registro_por_id, atualizar_registro_por_id
from fitness_app.core.models import Feedback

class ServicoFeedback:
    def __init__(self):
        pass

    def criar_feedback(self, usuario_email, texto, nota, data):
        feedback = Feedback(usuario_email=usuario_email, texto=texto, nota=nota, data=data)
        inserir_registro("feedbacks", feedback.to_dict()) 

    def listar_feedback(self):
        return [Feedback.from_dict(dado) for dado in obter_registros("feedbacks")]
    
    def deletar_feedback(self, feedback_id):
        return deletar_registro_por_id("feedbacks", feedback_id)

    def atualizar_feedback(self, feedback_id, novo_texto, nova_nota, nova_data):
        novos_dados = {"texto": novo_texto, "nota": nova_nota, "data": nova_data}
        return atualizar_registro_por_id("feedbacks", feedback_id, novos_dados)

    