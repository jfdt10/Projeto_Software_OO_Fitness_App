"""
Serviço de Treino para o aplicativo de fitness.
Este Módulo fornece funcionalidades para registrar atividades, listar atividades do usuário, atualizar e deletar atividades.
"""

from fitness_app.core.models import RegistroNutricional
from fitness_app.core.database import db, inserir_registro, obter_registros, atualizar_registro, deletar_registro
from tinydb import Query

class ServicoNutricional:
    def __init__(self):
        pass
    
    def registrar_refeicao(self, usuario_email, data, alimentos):
        tabela_alimentos = db.table('alimentos')
        alimentos_final = []
        for item in alimentos:
            nome = item['alimento']
            alimento = self.buscar_alimento(nome)
            if not alimento:
                macros = {
                    "calorias": item.get("calorias"),
                    "proteina": item.get("proteina"),
                    "gordura": item.get("gordura"),
                    "carboidrato": item.get("carboidrato")
                }
                if None in macros.values():
                    raise ValueError(f"Macronutrientes Obrigatórios para o alimento: {nome}")
                novo_alimento = {
                    "alimento": nome,
                    "calorias": macros["calorias"],
                    "proteina": macros["proteina"],
                    "gordura": macros["gordura"],
                    "carboidrato": macros["carboidrato"]
                }

                tabela_alimentos.insert(novo_alimento)
                alimento = novo_alimento
            quantidade = item.get("quantidade", 1)
            alimento_final = {
                "alimento": alimento["alimento"],
                "quantidade": quantidade,
                "calorias": alimento["calorias"] * quantidade,
                "proteina": alimento["proteina"] * quantidade,
                "gordura": alimento["gordura"] * quantidade,
                "carboidrato": alimento["carboidrato"] * quantidade
            }
            alimentos_final.append(alimento_final)

        calorias = sum(a["calorias"] for a in alimentos_final)
        macros = {
            "proteina": sum(a["proteina"] for a in alimentos_final),
            "gordura": sum(a["gordura"] for a in alimentos_final),
            "carboidrato": sum(a["carboidrato"] for a in alimentos_final)
        }
        registro = RegistroNutricional(usuario_email, data, alimentos_final, calorias, macros)
        return inserir_registro('nutricao', registro.to_dict())

    def listar_todos_alimentos(self):
        tabela_alimentos = db.table('alimentos')
        return [alimento.get("alimento") or alimento.get("nome") for alimento in tabela_alimentos.all() if alimento.get("alimento") or alimento.get("nome")]
        
    def listar_registros_usuario(self, usuario_email):
        return [
            RegistroNutricional.from_dict(dado)
            for dado in obter_registros('nutricao')
            if dado.get('usuario_email') == usuario_email
        ]

    def atualizar_registro(self, doc_id, novos_dados: dict):
        return atualizar_registro('nutricao', doc_id, novos_dados)

    def deletar_registro(self, doc_id):
        return deletar_registro('nutricao', doc_id)

    def buscar_alimento(self, nome_alimento):
        tabela_alimentos = db.table('alimentos')
        Alimento = Query()
        resultado = tabela_alimentos.search(Alimento.alimento == nome_alimento)
        if resultado:
            return resultado[0]
        else:
            return None

    def analisar_consumo(self, usuario_email):
        registros = self.listar_registros_usuario(usuario_email)
        total_calorias = sum(r.calorias for r in registros)
        total_proteina = sum(r.macros.get("proteina", 0) for r in registros)
        total_gordura = sum(r.macros.get("gordura", 0) for r in registros)
        total_carbo = sum(r.macros.get("carboidrato", 0) for r in registros)
        return {
            "calorias": total_calorias,
            "proteina": total_proteina,
            "gordura": total_gordura,
            "carboidrato": total_carbo
        }