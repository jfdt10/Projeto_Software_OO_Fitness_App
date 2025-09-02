"""
Serviço de Vídeo para o aplicativo de fitness.
Este módulo fornece funcionalidades para pesquisar vídeos de treino e vídeos de orientação fitness, registrar, listar e deletar vídeos.
"""

from youtubesearchpython import VideosSearch
from fitness_app.core.abc import ServicoBase
from fitness_app.core.database import RepositorioTinyDB
from fitness_app.core.models import Video


class ServicoVideo(ServicoBase):
    def __init__(self, repo=None):
        super().__init__(repo or RepositorioTinyDB('videos'))
        # Aqui usei Composição: ServicoVideo "possui" uma instância base de Video
        self.video_base = Video(
            titulo="",
            descricao="",
            url="",
            thumbnail="",
            duracao="",
            data_publicacao="",
            usuario_email=""
        )

    def pesquisar_videos(self, query, max_results=10):
        search_videos = VideosSearch(query, limit=max_results)
        resultados = search_videos.result().get('result', [])
        videos = []
        for video in resultados:
            video_data = {
                'titulo': video.get('title'),
                'descricao': video.get('descriptionSnippet', ''),
                'url': video.get('link'),
                'thumbnail': video.get('thumbnails', [{}])[0].get('url', ''),
                'duracao': video.get('duration'),
                'data_publicacao': video.get('publishedTime')
            }
            # Usa a classe da instância base para criar vídeos
            videos.append(type(self.video_base).from_dict(video_data)) 
        return videos

    def criar(self, video_data, usuario_email=None):
        if not video_data:
            raise ValueError('video_data é obrigatório')
        
        if hasattr(video_data, 'to_dict'):
            dados = video_data.to_dict()
        elif isinstance(video_data, dict):
            dados = video_data
        else:
            raise TypeError('video_data deve ser um objeto ou dict')

        if usuario_email:
            dados['usuario_email'] = usuario_email
        
        # Usa a classe da instância base para criar novo vídeo
        video = type(self.video_base).from_dict(dados)
        return self.repo.inserir(video)

    def listar(self, usuario_email=None):
        query = None
        if usuario_email:
            from tinydb import Query as Q
            q = Q()
            query = q.usuario_email == usuario_email
        
        # Usa a classe da instância base para o model_cls
        return self.repo.listar(query=query, model_cls=type(self.video_base))

    def atualizar(self, id, dados):
        return self.repo.atualizar(id, dados)

    def deletar(self, id):
        return self.repo.deletar(id)