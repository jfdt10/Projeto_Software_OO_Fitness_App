from abc import ABC, abstractmethod

# Classe Abstrata para uso Herança Abstratas
class RepositorioBase(ABC):

    def __init__(self, tabela=None):
        self.tabela = tabela

    @abstractmethod
    def inserir(self, obj):
        pass

    @abstractmethod
    def listar(self, query=None):
        pass

    @abstractmethod
    def obter(self, id):
        pass

    @abstractmethod
    def atualizar(self, id, data):
        pass

    @abstractmethod
    def deletar(self, id):
        pass

# Outra Classe Abstrata para usar em todos os Serviços(Isto é Classes que implementam lógica principal do sistema)
class ServicoBase(ABC):

    def __init__(self, repo):
        self.repo = repo

    @abstractmethod
    def listar(self, usuario_email=None):
        pass

    @abstractmethod
    def criar(self, *args, **kwargs):
        pass

    @abstractmethod
    def deletar(self, id):
        pass

    @abstractmethod
    def atualizar(self, id, dados):
        pass
