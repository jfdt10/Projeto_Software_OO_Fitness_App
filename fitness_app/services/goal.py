"""
Serviço de Metas para o aplicativo de fitness.
Este módulo fornece funcionalidades para criar metas personalizadas, listas metas do usuário e verfificar progresso.
"""

from fitness_app.core.abc import ServicoBase
from fitness_app.core.models import Meta
from fitness_app.core.database import RepositorioTinyDB

class ServicoMeta(ServicoBase):
    def __init__(self, repo=None):
        super().__init__(repo or RepositorioTinyDB('metas'))
        # Aqui usei Composição: ServicoMeta "possui" uma instância base de Meta
        self.meta_base = Meta(
            usuario_email="",
            tipo="",
            valor=0,
            data_inicio="",
            data_fim="",
            atingida=False
        )

    def criar(self, usuario_email, tipo, valor, data_inicio, data_fim):
        # Usa a classe da instância base para criar nova meta
        meta = type(self.meta_base)(
            usuario_email=usuario_email,
            tipo=tipo,        
            valor=valor,        
            data_inicio=data_inicio,
            data_fim=data_fim,
            atingida=False
        )
        return self.repo.inserir(meta)

    def listar(self, usuario_email):
        # Usa a classe da instância base para o model_cls
        metas = self.repo.listar(model_cls=type(self.meta_base))
        if usuario_email:
            metas = [m for m in metas if m.usuario_email == usuario_email]
        return metas

    def atualizar(self, id, dados: dict):
        return self.repo.atualizar(id, dados)

    def deletar(self, id):
        return self.repo.deletar(id)

    def verificar_progresso(self, usuario_email):
        metas = self.listar(usuario_email)
        atingidas = [m for m in metas if getattr(m, 'atingida', False)]
        pendentes = [m for m in metas if not getattr(m, 'atingida', False)]
        return {"atingidas": atingidas, "pendentes": pendentes}
    
    def concluir_meta(self, id):
        return self.atualizar(id, {"atingida": True})