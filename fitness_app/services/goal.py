"""
Serviço de Treino para o aplicativo de fitness.
Este módulo fornece funcionalidades para criar metas personalizadas, listas metas do usuário e verfificar progresso.
"""

from fitness_app.core.models import Meta
from fitness_app.core.database import atualizar_registro_por_id, deletar_registro_por_id, inserir_registro, obter_registros

class ServicoMeta:
    def __init__(self):
        pass
    
    def criar_meta(self, usuario_email, tipo, valor, data_inicio, data_fim):
        meta = Meta(
            usuario_email=usuario_email,
            tipo=tipo,        
            valor=valor,        
            data_inicio=data_inicio,
            data_fim=data_fim,
            atingida=False
        )
        return inserir_registro('metas', meta.to_dict())

    def listar_metas_usuario(self, usuario_email):
        return [
            Meta.from_dict(dado)
            for dado in obter_registros('metas')
            if dado.get('usuario_email') == usuario_email
        ]

    def atualizar_meta(self, meta_id, novos_dados: dict):
        return atualizar_registro_por_id('metas', meta_id, novos_dados)

    def deletar_meta(self, meta_id):
        return deletar_registro_por_id('metas', meta_id)

    def verificar_progresso(self, usuario_email):
        metas = self.listar_metas_usuario(usuario_email)
        atingidas = [m for m in metas if m.atingida]
        pendentes = [m for m in metas if not m.atingida]
        return {"atingidas": atingidas, "pendentes": pendentes}
    
    def concluir_meta(self, meta_id):
        return self.atualizar_meta(meta_id, {"atingida": True})
