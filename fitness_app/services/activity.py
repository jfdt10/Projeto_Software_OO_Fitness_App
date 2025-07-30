"""
Serviço de Treino para o aplicativo de fitness.
Este Módulo fornece funcionalidades para registrar atividades, listar atividades do usuário, atualizar e deletar atividades.
"""

from fitness_app.core.models import Atividade
from fitness_app.core.database import inserir_registro, obter_registros, atualizar_registro, deletar_registro

class ServicoAtividade:
    def __init__(self):
        pass
    
    def calcular_calorias(self, tipo, peso, duracao_min, ritmo=None, passos=None, altura=None):
        """
        tipo: caminhada, corrida, ciclismo, etc.
        peso: em kg
        duracao_min: duração em minutos
        ritmo: lento, medio, rapido
        passos: número de passos (opcional)
        altura: em metros (opcional)
        """
        METS = {
            'caminhada': {'lento': 2.8, 'medio': 3.5, 'rapido': 5.0},
            'corrida': {'lento': 7.0, 'medio': 9.8, 'rapido': 11.0},
            'ciclismo': {'lento': 4.0, 'medio': 8.0, 'rapido': 10.0},
            'musculacao': {'medio': 6.0},
        }
        tipo = tipo.strip().lower()
        ritmo = (ritmo or 'medio').lower()
      
        if tipo in ['caminhada', 'corrida', 'ciclismo'] and passos and altura:
            passada = altura * 0.414
            distancia = passada * passos  
            velocidades = {'lento': 0.9, 'medio': 1.34, 'rapido': 1.79}  
            v = velocidades.get(ritmo, 1.34)
            tempo_seg = distancia / v 
            duracao_min = tempo_seg / 60  
            met = METS[tipo].get(ritmo, list(METS[tipo].values())[0])
            calorias = (met * 3.5 * peso / 200) * duracao_min
            return round(calorias, 2)
        if tipo in METS:
            met = METS[tipo].get(ritmo, list(METS[tipo].values())[0])
        else:
            met = METS['musculacao']['medio']
        calorias = (met * 3.5 * peso / 200) * duracao_min
        return round(calorias, 2)
    def registrar_atividade(self, atividade: Atividade, usuario=None, ritmo=None):
        try:
            tipo = atividade.tipo.strip().lower()
            peso = float(usuario.peso) if usuario and hasattr(usuario, 'peso') else None
            altura = float(usuario.altura) / 100 if usuario and hasattr(usuario, 'altura') else None
            duracao = float(atividade.duracao) if atividade.duracao else None
            passos = int(atividade.passos) if atividade.passos else None
            if peso and duracao and not atividade.calorias:
                atividade.calorias = self.calcular_calorias(tipo, peso, duracao, ritmo, passos, altura)
        except Exception:
            pass
        return inserir_registro('atividades', atividade.to_dict())

    def listar_atividades_usuario(self, usuario_email):
        return [
            Atividade.from_dict(dado)
            for dado in obter_registros('atividades')
            if dado.get('usuario_email') == usuario_email
        ]

    def atualizar_atividade(self, doc_id, novos_dados: dict):
        return atualizar_registro('atividades', doc_id, novos_dados)

    def deletar_atividade(self, doc_id):
        return deletar_registro('atividades', doc_id)