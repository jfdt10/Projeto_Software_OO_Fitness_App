from tinydb import TinyDB, Query
from datetime import datetime
import os
from .abc import RepositorioBase
os.makedirs('fitness_app/data', exist_ok=True)

db = TinyDB('fitness_app/data/fitness.json')

# Herança de Classe Abstrata
class RepositorioTinyDB(RepositorioBase):
    def __init__(self, tabela, db_path='fitness_app/data/fitness.json'):
        super().__init__(tabela)
        self._db = TinyDB(db_path)
        self._table = self._db.table(tabela) 

    def inserir(self, obj):
        if hasattr(obj, 'to_dict'): ## qualquer objeto pode ser chamado aqui de forma uniforme
            data = obj.to_dict()
        elif isinstance(obj, dict):
            data = obj
        else:
            raise TypeError('obj devem ser dicionários ou modelos com to_dict()')
        data['criado_em'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        return self._table.insert(data)

    def insert_multiple(self, items):
        prepared = []
        for obj in items:
            if hasattr(obj, 'to_dict'):
                prepared.append(obj.to_dict()) # Duck typing adicionado uso de função sem verificar qual classe para inserção múltipla no Banco
            elif isinstance(obj, dict):
                prepared.append(obj)
            else:
                raise TypeError('items devem ser dicionários ou modelos com to_dict()')
        return self._table.insert_multiple(prepared)

    def listar(self, query=None, model_cls=None):
        if query:
            regs = self._table.search(query)
        else:
            regs = self._table.all()
        
        if model_cls and hasattr(model_cls, 'from_dict'):
            tipo_esperado = model_cls.__name__
            regs_filtrados = [r for r in regs if r.get('_tipo') == tipo_esperado or '_tipo' not in r]
            return [model_cls.from_dict(r) for r in regs_filtrados]
        return regs

    def obter(self, id, model_cls=None):
        Q = Query()
        results = self._table.search(Q.id == id)
        if not results:
            return None
        rec = results[0]
        if model_cls and hasattr(model_cls, 'from_dict'):
            return model_cls.from_dict(rec)
        return rec

    def atualizar(self, id, data):
        Q = Query()
        results = self._table.search(Q.id == id)
        if results:
            doc_ids = [r.doc_id for r in results]
            self._table.update(data, doc_ids=doc_ids)
            return True
        return False

    def deletar(self, id):
        Q = Query()
        results = self._table.search(Q.id == id)
        if results:
            doc_ids = [r.doc_id for r in results]
            self._table.remove(doc_ids=doc_ids)
            return True
        return False

    def truncate(self):
        self._table.truncate()

    def usuario_existe(self, field, value):
        Q = Query()
        return self._table.contains(Q[field] == value)


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

# Encapsulamento para controle de acesso do módulo
__all__ = [
    "db", "RepositorioTinyDB", "backup_banco", "importar_banco"
]
