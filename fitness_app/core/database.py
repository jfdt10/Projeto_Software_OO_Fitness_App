from tinydb import TinyDB, Query
from datetime import datetime
import os



os.makedirs('fitness_app/data', exist_ok=True)

db = TinyDB('fitness_app/data/fitness.json')


usuarios = db.table('usuarios')
planos_treino = db.table('planos_treino') 
wearable = db.table('wearable')
atividades = db.table('atividades')  
nutricao = db.table('nutricao')  
metas = db.table('metas')  
desafios = db.table('desafios')  
videos = db.table('videos')  
recomendacoes = db.table('recomendacoes')  
feedbacks = db.table('feedbacks')  
posts_forum = db.table('posts_forum')
comentarios_forum = db.table('comentarios_forum')




def inserir_registro(tabela, dados):
    dados['criado_em'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    return db.table(tabela).insert(dados)

def atualizar_usuario(email, dados_usuario):
    Q = Query()
    usuarios.update(dados_usuario, Q.email == email)
    return True

def obter_registros(tabela, query=None):
    if query:
        return db.table(tabela).search(query)
    return db.table(tabela).all()



def deletar_registro_por_id(tabela, id_model):
    Q = Query()
    results = db.table(tabela).search(Q.id == id_model)
    if results:
        doc_ids = [r.doc_id for r in results]
        db.table(tabela).remove(doc_ids=doc_ids)
        return True
    return False

def atualizar_registro_por_id(tabela, id_model, novos_dados):
    Q = Query()
    results = db.table(tabela).search(Q.id == id_model)
    if results:
        doc_ids = [r.doc_id for r in results]
        db.table(tabela).update(novos_dados, doc_ids=doc_ids)
        return True
    return False

def usuario_existe(nome=None, email=None):
    Usuario = Query()
    if nome and email:
        return usuarios.contains((Usuario.nome == nome) | (Usuario.email == email))
    elif nome:
        return usuarios.contains(Usuario.nome == nome)
    elif email:
        return usuarios.contains(Usuario.email == email)
    return False


def backup_banco(arquivo='backup_fitness_app.json'):
    dados = db.storage.read()
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(dados)
    print(f"Backup salvo em {arquivo}")


def importar_banco(arquivo='backup_fitness_app.json'):
    with open(arquivo, 'r', encoding='utf-8') as f:
        dados = f.read()
    db.storage.write(dados)
    print(f"Dados importados de {arquivo}")

__all__ = [
    "db", "usuarios", "planos_treino", "atividades", "nutricao", "metas",
    "desafios", "videos", "recomendacoes", "feedbacks", "forum", "wearable",
    "inserir_registro", "obter_registros", "atualizar_registro", "deletar_registro", "usuario_existe",
    "backup_banco", "importar_banco", "deletar_registro_por_id", "atualizar_registro_por_id"]
