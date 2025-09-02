"""
Serviço de Atividades para o aplicativo de fitness.
Este Módulo fornece funcionalidades para registrar atividades, listar atividades do usuário, atualizar e deletar atividades.
"""

from fitness_app.core.abc import ServicoBase
from fitness_app.core.models import Atividade
from fitness_app.core.database import RepositorioTinyDB
from tinydb import Query

class ServicoAtividade(ServicoBase):
    def __init__(self, repo = None):
        super().__init__(repo or RepositorioTinyDB('atividades'))
        # Aqui usei Composição: ServicoAtividade "possui" uma instância base de Atividade
        self.atividade_base = Atividade(
            usuario_email="",
            tipo="",
            data="",
            duracao=0,
            calorias=0,
            passos=0,
            ritmo=""
        )

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

    def criar(self, usuario_email, tipo, data, duracao, calorias=None, passos=None, ritmo=None, usuario=None):
        # Usa a classe da instância base para criar nova atividade
        nova_atividade = type(self.atividade_base)(
            usuario_email=usuario_email,
            tipo=tipo,
            data=data,
            duracao=duracao,
            calorias=calorias,
            passos=passos,
            ritmo=ritmo
        )
        if hasattr(nova_atividade, '__dict__'):
            nova_atividade.__dict__['_tipo'] = 'Atividade'
        try:
            tipo = nova_atividade.tipo.strip().lower()
            peso = float(usuario.peso) if usuario and hasattr(usuario, 'peso') else None
            altura = float(usuario.altura) / 100 if usuario and hasattr(usuario, 'altura') else None
            duracao_min = float(nova_atividade.duracao) if nova_atividade.duracao else None
            passos_val = int(nova_atividade.passos) if nova_atividade.passos else None
            if peso and duracao_min and not nova_atividade.calorias:
                nova_atividade.calorias = self.calcular_calorias(tipo, peso, duracao_min, ritmo, passos_val, altura)
        except Exception as e:
            print(f"Erro no cálculo de calorias: {e}")
        return self.repo.inserir(nova_atividade)

    def listar(self, usuario_email=None):
        if usuario_email:
            Q = Query()
            # Aqui utilizei a classe da instância base para o model_cls
            regs = self.repo.listar(query=Q.usuario_email == usuario_email, model_cls=type(self.atividade_base))
        else:
            regs = self.repo.listar(model_cls=type(self.atividade_base))
        return regs

    def atualizar(self, id, dados):
        return self.repo.atualizar(id, dados)

    def deletar(self, id):
        return self.repo.deletar(id)