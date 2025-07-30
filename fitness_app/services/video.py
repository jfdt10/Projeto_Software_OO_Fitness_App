"""
Servico de Video para o aplicativo de fitness.
Este módulo fornece funcionalidades para pesquisar videos de treino e videos de orientação fitness, deletar videos.
"""
from youtubesearchpython import VideosSearch
from fitness_app.core.database import db, inserir_registro, obter_registros, deletar_registro
from fitness_app.core.models import Video
import requests

class ServicoVideo:

    def __init__(self):
        pass

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
            videos.append(Video.from_dict(video_data))
        return videos
    
    def registrar_video(self, video: Video, usuario_email=None):
        dados = video.to_dict()
        if usuario_email:
            dados['usuario_email'] = usuario_email
        inserir_registro('videos', dados)
        return True
    
    def listar_videos(self, usuario_email=None):
        registros = obter_registros('videos')
        if usuario_email:
            registros = [r for r in registros if r.get('usuario_email') == usuario_email]
        return [Video.from_dict(dado) for dado in registros]
    
    def deletar_video(self, doc_id):
        return deletar_registro('videos', doc_id)
    
    def buscar_exercicios(self, termo, limit=10, offset=0, threshold=0.3):
        url = "https://exercisedb-90c85o35g-jfdt10s-projects.vercel.app/api/v1/exercises/search"
        params = {
            "q": termo,
            "limit": limit,
            "offset": offset,
            "threshold": threshold
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            raise Exception("Erro ao buscar exercícios: " + response.text)

