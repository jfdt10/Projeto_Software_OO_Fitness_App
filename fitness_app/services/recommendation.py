"""
Serviço de Recomendação para Treinos e Alimentos
Este módulo fornece funcionalidades para recomendar treinos e alimentos com base nas preferências do usuário.
"""

from fitness_app.core.models import Recomendacao
from fitness_app.core.database import obter_registros

class ServicoRecomendacao:
    def __init__(self):
        pass

    def recomendar_treinos_sugestoes(self, preferencia_usuario):
        treinos = obter_registros('treinos_prontos')
        recomendacoes = [
            Recomendacao(tipo='treino', dados=treino)
            for treino in treinos
            if self.verificar_preferencia(treino, preferencia_usuario)
        ]
        return recomendacoes

    def recomendar_alimentos_sugestoes(self, preferencia_usuario):
        alimentos = obter_registros('alimentos')
        recomendacoes = [
            Recomendacao(tipo='alimento', dados=alimento)
            for alimento in alimentos
            if self.verificar_preferencia(alimento, preferencia_usuario)
        ]
        return recomendacoes


    def recomendar_diretrizes_gerais(self, preferencia_usuario):
        diretrizes = obter_registros('diretrizes_gerais')
        recomendacoes = [
            Recomendacao(tipo='diretriz_geral', dados=d)
            for d in diretrizes
            if self.verificar_preferencia(d, preferencia_usuario)
        ]
        return recomendacoes

    def recomendar_grupos_musculares(self, preferencia_usuario):
        grupos = obter_registros('grupos_musculares')
        recomendacoes = [
            Recomendacao(tipo='grupo_muscular', dados=g)
            for g in grupos
            if self.verificar_preferencia(g, preferencia_usuario)
        ]
        return recomendacoes

    def recomendar_mobilidade(self, preferencia_usuario):
        mobilidade = obter_registros('mobilidade')
        recomendacoes = [
            Recomendacao(tipo='mobilidade', dados=m)
            for m in mobilidade
            if self.verificar_preferencia(m, preferencia_usuario)
        ]
        return recomendacoes

    def recomendar_divisoes_semanais(self, preferencia_usuario):
        divisoes = obter_registros('divisoes_semanais')
        recomendacoes = [
            Recomendacao(tipo='divisao_semanal', dados=d)
            for d in divisoes
            if self.verificar_preferencia(d, preferencia_usuario)
        ]
        return recomendacoes

    def recomendar_progressao(self, preferencia_usuario):
        progressao = obter_registros('progressao')
        recomendacoes = [
            Recomendacao(tipo='progressao', dados=p)
            for p in progressao
            if self.verificar_preferencia(p, preferencia_usuario)
        ]
        return recomendacoes

    def recomendar_consideracoes_finais(self, preferencia_usuario):
        consideracoes = obter_registros('consideracoes_finais')
        recomendacoes = [
            Recomendacao(tipo='consideracao_final', dados=c)
            for c in consideracoes
            if self.verificar_preferencia(c, preferencia_usuario)
        ]
        return recomendacoes

    def verificar_preferencia(self, item, preferencia_usuario):
        for chave, valor in preferencia_usuario.items():
            if valor == "Nenhuma":
                if chave in item:
                    campo = item[chave]
                    if isinstance(campo, list):
                        if any(r != "Nenhuma" for r in campo):
                            return False
                    else:
                        if campo != "Nenhuma":
                            return False
            else:
                if chave in item:
                    campo = item[chave]
                    if isinstance(campo, list):
                        if valor not in campo:
                            return False
                    else:
                        if campo != valor:
                            return False
        return True