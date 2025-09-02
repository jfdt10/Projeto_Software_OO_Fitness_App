"""
Serviço de Nutrição para o aplicativo de fitness.
Este Módulo fornece funcionalidades para registrar atividades, listar atividades do usuário, atualizar e deletar atividades.
"""
from fitness_app.core.abc import ServicoBase
from fitness_app.core.models import RegistroNutricional
from fitness_app.core.database import RepositorioTinyDB
from tinydb import Query as Q


class ServicoNutricional(ServicoBase):
    def __init__(self, repo=None):
        super().__init__(repo or RepositorioTinyDB('nutricao'))
        # Aqui usei Composição: ServicoNutricional "possui" uma instância base de RegistroNutricional
        self.registro_nutricional_base = RegistroNutricional(
            usuario_email="",
            data="",
            refeicoes=[],
            calorias=0,
            macros={}
        )
        self.repo_alimentos = RepositorioTinyDB('alimentos')

    def _tabela_alimentos(self):
        if hasattr(self.repo_alimentos, "_db"):
            return self.repo_alimentos._db.table('alimentos')
        raise RuntimeError("Tabela 'alimentos' não encontrada.")

    def buscar_alimento(self, nome_alimento):
        tabela_alimentos = self._tabela_alimentos()
        q = Q()
        resultado = tabela_alimentos.search(q.alimento == nome_alimento)
        if resultado:
            return resultado[0]
        else:
            return None

    def criar(self, usuario_email, data, alimentos):
        tabela_alimentos = self._tabela_alimentos()
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
        
        # Usa a classe da instância base para criar novo registro
        registro = type(self.registro_nutricional_base)(
            usuario_email, 
            data, 
            alimentos_final, 
            calorias, 
            macros
        )
        return self.repo.inserir(registro)

    def listar_todos_alimentos(self):
        tabela_alimentos = self._tabela_alimentos()
        return [alimento.get("alimento") or alimento.get("nome") for alimento in tabela_alimentos.all() if alimento.get("alimento") or alimento.get("nome")]
        
    def listar(self, usuario_email=None):
        # Usa a classe da instância base para o model_cls
        registros = self.repo.listar(model_cls=type(self.registro_nutricional_base))
        if usuario_email:
            registros = [r for r in registros if getattr(r, "usuario_email", None) == usuario_email]
        return registros

    def atualizar(self, id, dados: dict):
        if "alimentos" in dados:
            alimentos = dados["alimentos"]
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
                    tabela_alimentos = self._tabela_alimentos()
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
            dados["refeicoes"] = alimentos_final
            dados["calorias"] = calorias
            dados["macros"] = macros
        return self.repo.atualizar(id, dados)

    def deletar(self, id):
        return self.repo.deletar(id)

    def analisar_consumo(self, usuario_email):
        registros = self.listar(usuario_email)
        total_calorias = 0
        total_proteina = 0
        total_gordura = 0
        total_carbo = 0
        for r in registros:
            if isinstance(r, dict):
                calorias = r.get("calorias", 0)
                macros = r.get("macros", {})
            else:
                calorias = getattr(r, "calorias", 0)
                macros = getattr(r, "macros", {})
            if calorias is None:
                calorias = 0
            if not isinstance(macros, dict):
                macros = {}
            proteina = macros.get("proteina", 0)
            gordura = macros.get("gordura", 0)
            carbo = macros.get("carboidrato", 0)
            if proteina is None:
                proteina = 0
            if gordura is None:
                gordura = 0
            if carbo is None:
                carbo = 0
            total_calorias += calorias
            total_proteina += proteina
            total_gordura += gordura
            total_carbo += carbo
        return {
            "calorias": total_calorias,
            "proteina": total_proteina,
            "gordura": total_gordura,
            "carboidrato": total_carbo
        }