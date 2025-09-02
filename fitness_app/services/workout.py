"""
Serviço de Treino para o aplicativo de fitness.
Este módulo fornece funcionalidades para recomendar treinos, criar planos personalizados,
"""

from fitness_app.core.models import PlanoTreino
from fitness_app.core.abc import ServicoBase
from fitness_app.core.database import RepositorioTinyDB


class ServicoTreino(ServicoBase):
    def __init__(self, repo=None, repo_planos=None):
        super().__init__(repo or RepositorioTinyDB('treinos_prontos'))
        self.repo_planos = repo_planos or RepositorioTinyDB('planos_treino')
        # Aqui usei Composição: ServicoTreino "possui" uma instância base de PlanoTreino
        self.plano_treino_base = PlanoTreino(
            usuario_email="",
            nome="",
            exercicios=[],
            objetivo="",
            nivel=""
        )

    def recomendar_treinos(self, usuario):
        # Usa a classe da instância base para o model_cls
        treinos = self.repo.listar(model_cls=type(self.plano_treino_base))
        nivel_usuario = getattr(usuario, 'nivel_experiencia', None) or getattr(usuario, 'nivel_atividade', None)
        objetivo_usuario = getattr(usuario, 'objetivo', None)
        
        if nivel_usuario is None and objetivo_usuario is None:
            return treinos

        def valor_treino(t, campo):
            if isinstance(t, dict):
                return t.get(campo)
            return getattr(t, campo, None)

        recomendados = [
            t for t in treinos
            if (nivel_usuario is None or valor_treino(t, 'nivel') == nivel_usuario) and
               (objetivo_usuario is None or valor_treino(t, 'objetivo') == objetivo_usuario)
        ]
        return recomendados

    def criar(self, usuario_email, nome, exercicios, objetivo, nivel):
        # Usa a classe da instância base para criar novo plano
        plano = type(self.plano_treino_base)(
            usuario_email=usuario_email,
            nome=nome,
            exercicios=exercicios,
            objetivo=objetivo,
            nivel=nivel
        )
        self.repo_planos.inserir(plano)
        return plano

    def listar(self, usuario_email=None):
        # Usa a classe da instância base para o model_cls
        planos = self.repo_planos.listar(model_cls=type(self.plano_treino_base))
        if usuario_email:
            return [p for p in planos if getattr(p, 'usuario_email', None) == usuario_email]
        return planos

    def atualizar(self, id, dados: dict):
        return self.repo_planos.atualizar(id, dados)

    def deletar(self, id):
        return self.repo_planos.deletar(id)

    def add_exercicio(self, plano_id, exercicio):
        plano = self.repo_planos.obter(plano_id, model_cls=type(self.plano_treino_base))
        if plano:
            plano.add_exercicio(exercicio)
            # Atualiza no banco com a nova lista
            self.repo_planos.atualizar(plano_id, {'exercicios': plano.exercicios})
            print(f"Exercício '{exercicio}' adicionado ao plano '{getattr(plano, 'nome', 'Plano')}'!")
            return True
        print("Plano não encontrado.")
        return False

    def remove_exercicio(self, plano_id, exercicio):
        plano = self.repo_planos.obter(plano_id, model_cls=type(self.plano_treino_base))
        if plano:
            if exercicio in plano.exercicios:
                plano.remove_exercicio(exercicio)
                # Atualiza no banco com a nova lista
                self.repo_planos.atualizar(plano_id, {'exercicios': plano.exercicios})
                print(f"Exercício '{exercicio}' removido do plano '{getattr(plano, 'nome', 'Plano')}'!")
                return True
            else:
                print(f"Exercício '{exercicio}' não encontrado no plano.")
                return False
        print("Plano não encontrado.")
        return False

    def listar_exercicios(self, plano_id):
        plano = self.repo_planos.obter(plano_id, model_cls=type(self.plano_treino_base))
        if plano:
            return plano.exercicios
        return []