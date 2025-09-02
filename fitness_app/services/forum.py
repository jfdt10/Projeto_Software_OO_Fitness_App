"""
Serviço para manipular o fórum de discussões do aplicativo de fitness.
Este módulo fornece funcionalidades para criar posts, listar posts do usuário, comentar e exibir conteúdo.
"""
from fitness_app.core.database import RepositorioTinyDB
from fitness_app.core.abc import ServicoBase
from fitness_app.core.models import PostForum, ComentarioForum, ConteudoForum

class ServicoForum(ServicoBase):
    def __init__(self, repo=None):
        super().__init__(repo or RepositorioTinyDB('forum'))
        # Aqui usei Composição: ServicoForum "possui" instâncias base dos modelos
        self.post_base = PostForum(
            usuario_email="",
            titulo="",
            mensagem="",
            data=""
        )
        self.comentario_base = ComentarioForum(
            post_id="",
            usuario_email="",
            mensagem="",
            data=""
        )
        self.conteudo_base = ConteudoForum(
            usuario_email="",
            mensagem="",
            data=""
        )

    def criar(self, usuario_email, titulo, mensagem, data=None):
        # Usa a classe da instância base para criar novo post
        post = type(self.post_base)(
            usuario_email=usuario_email, 
            titulo=titulo, 
            mensagem=mensagem, 
            data=data
        )
        return self.repo.inserir(post)
    
    def listar(self, usuario_email=None):
        # Usa as classes das instâncias base para os model_cls
        posts = self.repo.listar(model_cls=type(self.post_base))
        comentarios = self.repo.listar(model_cls=type(self.comentario_base))
        conteudos = posts + comentarios
        if usuario_email:
            conteudos = [c for c in conteudos if c.usuario_email == usuario_email]
        return conteudos

    def comentar_post(self, post_id, usuario_email, mensagem, data=None):
        # Usa a classe da instância base para criar novo comentário
        comentario = type(self.comentario_base)(
            post_id=post_id, 
            usuario_email=usuario_email, 
            mensagem=mensagem, 
            data=data
        )
        return self.repo.inserir(comentario)

    def listar_posts(self, usuario_email=None):
        posts = self.repo.listar(model_cls=type(self.post_base))
        if usuario_email:
            posts = [p for p in posts if p.usuario_email == usuario_email]
        return posts

    def listar_comentarios(self, post_id=None, usuario_email=None):
        comentarios = self.repo.listar(model_cls=type(self.comentario_base))
        if usuario_email:
            comentarios = [c for c in comentarios if c.usuario_email == usuario_email]
        if post_id is not None:
            comentarios = [c for c in comentarios if getattr(c, 'post_id', None) == post_id]
        return comentarios
    
    def atualizar(self, id, dados: dict):
        return self.repo.atualizar(id, dados)

    def deletar(self, id):
        return self.repo.deletar(id)