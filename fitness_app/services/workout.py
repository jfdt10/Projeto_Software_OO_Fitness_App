"""
Serviço de Treino para o aplicativo de fitness.
Este módulo fornece funcionalidades para recomendar treinos, criar planos personalizados,
"""

from fitness_app.core.models import PlanoTreino
from fitness_app.core.database import inserir_registro, obter_registros, atualizar_registro_por_id, deletar_registro_por_id


class ServicoTreino:
    def __init__(self):
        pass
    
    def recomendar_treinos(self, usuario):
        treinos = obter_registros('treinos_prontos')
        recomendados = [
            t for t in treinos
            if t["nivel"] == usuario.nivel_experiencia and t["objetivo"] == usuario.objetivo
        ]
        return recomendados

    def criar_plano_personalizado(self, usuario_email, nome, exercicios, objetivo, nivel):
        plano = PlanoTreino(
            usuario_email=usuario_email,
            nome=nome,
            exercicios=exercicios,
            objetivo=objetivo,
            nivel=nivel
        )
        return inserir_registro('planos_treino', plano.to_dict())

    def listar_planos_usuario(self, usuario_email):
        return [
            PlanoTreino.from_dict(dado)
            for dado in obter_registros('planos_treino')
            if dado.get('usuario_email') == usuario_email
        ]

    def atualizar_plano(self, plano_id, novos_dados: dict):
        return atualizar_registro_por_id('planos_treino', plano_id, novos_dados)

    def deletar_plano(self, plano_id):
        return deletar_registro_por_id('planos_treino', plano_id)