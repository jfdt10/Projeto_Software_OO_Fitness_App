"""
Serviço de Treino para o aplicativo de fitness.
Este módulo fornece funcionalidades para wearables, registrar dados manuais, gerar simulações de dados de um wearable, listar e deletar dados.
"""

from fitness_app.core.models import DadoWearable
from fitness_app.core.database import inserir_registro, obter_registros, deletar_registro
import random
from datetime import datetime
import csv

class ServicoWearable:
    def __init__(self):
        pass

    def registrar_dado_manual(self, usuario_email, tipo, valor, data=None):
        dado = DadoWearable(
            usuario_email=usuario_email,
            data=data or datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            tipo=tipo,  
            valor=valor
        )
        return inserir_registro('wearable', dado.to_dict())

    def gerar_dado_aleatorio(self, usuario_email, tipo, data=None):
        if tipo == "passos":
            valor = random.randint(3000, 15000)
        elif tipo == "batimentos":
            valor = random.randint(60, 180)
        elif tipo == "sono":
            valor = round(random.uniform(5, 9), 1)  
        else:
            valor = random.randint(1, 100)
        return self.registrar_dado_manual(usuario_email, tipo, valor, data)

    def listar_dados_usuario(self, usuario_email):
        return [
            DadoWearable.from_dict(dado)
            for dado in obter_registros('wearable')
            if dado.get('usuario_email') == usuario_email
        ]

    def deletar_dado(self, doc_id):
        return deletar_registro('wearable', doc_id)
    
    def exportar_dados_csv(self, usuario_email, caminho_csv):
        dados = self.listar_dados_usuario(usuario_email)
        with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['usuario_email', 'data', 'tipo', 'valor'])
            for d in dados:
                writer.writerow([d.usuario_email, d.data, d.tipo, d.valor])

    def importar_dados_csv(self, usuario_email, caminho_csv):
        with open(caminho_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.registrar_dado_manual(
                    usuario_email=usuario_email,
                    tipo=row['tipo'],
                    valor=row['valor'],
                    data=row['data']
                )