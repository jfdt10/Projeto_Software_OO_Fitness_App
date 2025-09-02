"""
Serviço de Wearable para o aplicativo de fitness.
Este módulo fornece funcionalidades para wearables, registrar dados manuais, gerar simulações de dados de um wearable, listar e deletar dados.
"""

from fitness_app.core.models import DadoWearable
from fitness_app.core.database import RepositorioTinyDB
from fitness_app.core.abc import ServicoBase
import random
from datetime import datetime
import csv


class ServicoWearable(ServicoBase):
    def __init__(self, repo=None):
        super().__init__(repo or RepositorioTinyDB('wearable'))
        # Aqui usei Composição: ServicoWearable "possui" uma instância base de DadoWearable
        self.wearable_base = DadoWearable(
            usuario_email="",
            data="",
            tipo="",
            valor=0
        )

    def criar(self, usuario_email, tipo, valor, data=None):
        # Usa a classe da instância base para criar novo dado
        dado = type(self.wearable_base)(
            usuario_email=usuario_email,
            data=data or datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            tipo=tipo,
            valor=valor
        )
        self.repo.inserir(dado)
        return dado

    def gerar_dado_aleatorio(self, usuario_email, tipo, data=None):
        if tipo == "passos":
            valor = random.randint(3000, 15000)
        elif tipo == "batimentos":
            valor = random.randint(60, 180)
        elif tipo == "sono":
            valor = round(random.uniform(5, 9), 1)
        else:
            valor = random.randint(1, 100)
        return self.criar(usuario_email, tipo, valor, data)

    def listar(self, usuario_email=None):
        # Usa a classe da instância base para o model_cls
        dados = self.repo.listar(model_cls=type(self.wearable_base))
        if usuario_email:
            return [d for d in dados if getattr(d, 'usuario_email', None) == usuario_email]
        return dados

    def atualizar(self, id, dados: dict):
        return self.repo.atualizar(id, dados)

    def deletar(self, id):
        return self.repo.deletar(id)

    def exportar_dados_csv(self, usuario_email, caminho_csv):
        dados = self.listar(usuario_email)
        with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['usuario_email', 'data', 'tipo', 'valor'])
            for d in dados:
                writer.writerow([d.usuario_email, d.data, d.tipo, d.valor])

    def importar_dados_csv(self, caminho_csv, usuario_email):
        with open(caminho_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.criar(
                    usuario_email=usuario_email,
                    tipo=row['tipo'],
                    valor=row['valor'],
                    data=row['data']
                )