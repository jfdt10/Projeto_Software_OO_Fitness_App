"""
Serivço para manipular o fórum de discussões do aplicativo de fitness.
Este módulo fornece funcionalidades para criar posts, listar posts do usuário, comentar e exibir conteúdo.
"""

from fitness_app.core.models import PostForum, ComentarioForum, ConteudoForum
from fitness_app.core.database import inserir_registro, obter_registros, atualizar_registro, deletar_registro

class ServicoForum:
    def __init__(self):
        pass

    def criar_post(self, usuario_email, titulo, mensagem, data):
        post = PostForum(usuario_email=usuario_email, titulo=titulo, mensagem=mensagem, data=data)
        return inserir_registro('posts_forum', post.to_dict())

    def listar_posts(self):
        return [PostForum.from_dict(dado) for dado in obter_registros('posts_forum')]
    
    def comentar_post(self, post_id, usuario_email, mensagem, data):
        comentario = ComentarioForum(post_id=post_id, usuario_email=usuario_email, mensagem=mensagem, data=data)
        return inserir_registro('comentarios_forum', comentario.to_dict())
    
    def listar_comentarios(self, post_id):
        return [ComentarioForum.from_dict(dado) for dado in obter_registros('comentarios_forum') if dado.get('post_id') == post_id]
    
    def exibir_todos_conteudos(self, lista_conteudos):
        for conteudo in lista_conteudos:
            print(f"{conteudo.usuario_email}: {conteudo.mensagem} ({conteudo.data})")

    def exibir_conteudo_usuario(self, usuario_email):
        posts = [PostForum.from_dict(dado) for dado in obter_registros('posts_forum')] 
        comentarios = [ComentarioForum.from_dict(dado) for dado in obter_registros('comentarios_forum')]
        conteudos = posts + comentarios
        for conteudo in conteudos:
            if conteudo.usuario_email == usuario_email:
                print(f"{conteudo.usuario_email}: {conteudo.mensagem} ({conteudo.data})")

    def deletar_post(self, post_id):
        return deletar_registro('posts_forum', post_id)