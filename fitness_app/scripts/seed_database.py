import json
import os
import sys
from fitness_app.core.database import RepositorioTinyDB

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)



def popular_alimentos():
    print("Populando tabela de alimentos...")
    repo_alimentos = RepositorioTinyDB('alimentos')
    repo_alimentos.truncate()

    try:
        with open('fitness_app/data/food_database.json', 'r', encoding='utf-8') as f:
            perfis = json.load(f)

        alimentos_unicos = {}
        for perfil in perfis:
            refeicoes = perfil.get('refeicoes', {})
            for lista_refeicoes in refeicoes.values():
                for grupo in lista_refeicoes:
                    for alimento in grupo:
                        nome = alimento.get('alimento')
                        if nome and nome not in alimentos_unicos:
                            alimento_plano = {
                                'alimento': nome,
                                'calorias': alimento.get('calorias', 0),
                                'proteina': alimento.get('proteina', 0),
                                'gordura': alimento.get('gordura', 0),
                                'carboidrato': alimento.get('carboidrato', 0)
                            }
                            alimentos_unicos[nome] = alimento_plano

        if alimentos_unicos:
            repo_alimentos.insert_multiple(list(alimentos_unicos.values()))
            print(f" {len(alimentos_unicos)} alimentos inseridos com sucesso!")
        else:
            print(" Nenhum alimento encontrado no JSON.")
    except FileNotFoundError:
        print(" ERRO: Arquivo 'food_database.json' não encontrado.")
    except json.JSONDecodeError:
        print(" ERRO: Arquivo 'food_database.json' não é um JSON válido.")


def popular_treinos():
    print("\nPopulando tabela de treinos prontos...")
    repo_treinos = RepositorioTinyDB('treinos_prontos')
    repo_treinos.truncate()
    repo_diretrizes = RepositorioTinyDB('diretrizes_gerais')
    repo_diretrizes.truncate()
    repo_grupos = RepositorioTinyDB('grupos_musculares')
    repo_grupos.truncate()
    repo_mobilidade = RepositorioTinyDB('mobilidade')
    repo_mobilidade.truncate()
    repo_divisoes = RepositorioTinyDB('divisoes_semanais')
    repo_divisoes.truncate()
    repo_progressao = RepositorioTinyDB('progressao')
    repo_progressao.truncate()
    repo_consideracoes = RepositorioTinyDB('consideracoes_finais')
    repo_consideracoes.truncate()

    try:
        with open('fitness_app/data/workouts.json', 'r', encoding='utf-8') as f:
            workouts_data = json.load(f)

        treinos_para_inserir = [item for item in workouts_data if 'nome' in item and 'nivel' in item]
        bloco_geral = next((item for item in workouts_data if 'treino_musculacao' in item), None)

        if treinos_para_inserir:
            repo_treinos.insert_multiple(treinos_para_inserir)
            print(f" {len(treinos_para_inserir)} treinos inseridos com sucesso!")
        else:
            print(" Nenhum treino pronto encontrado no JSON.")

        if bloco_geral:
            treino_musculacao = bloco_geral['treino_musculacao']
            if 'diretrizes_gerais' in treino_musculacao:
                repo_diretrizes.inserir(treino_musculacao['diretrizes_gerais'])
            if 'grupos_musculares' in treino_musculacao:
                repo_grupos.inserir(treino_musculacao['grupos_musculares'])
            if 'mobilidade' in treino_musculacao:
                repo_mobilidade.inserir(treino_musculacao['mobilidade'])
            if 'divisoes_semanais' in treino_musculacao:
                repo_divisoes.inserir(treino_musculacao['divisoes_semanais'])
            if 'progressao' in treino_musculacao:
                repo_progressao.inserir(treino_musculacao['progressao'])
            if 'consideracoes_finais' in treino_musculacao:
                repo_consideracoes.inserir({'itens': treino_musculacao['consideracoes_finais']})
            print(" Bloco de diretrizes gerais e informações extras inserido!")
        else:
            print(" Nenhum bloco de diretrizes gerais encontrado no JSON.")
    except FileNotFoundError:
        print(" ERRO: Arquivo 'workouts.json' não encontrado.")
    except json.JSONDecodeError:
        print(" ERRO: Arquivo 'workouts.json' não é um JSON válido.")

def popular_perfis_alimentares():
    print("Populando tabela de perfis alimentares...")
    repo_perfis = RepositorioTinyDB('perfis_alimentares')
    repo_perfis.truncate()
    try:
        with open('fitness_app/data/food_database.json', 'r', encoding='utf-8') as f:
            perfis = json.load(f)
        if perfis:
            repo_perfis.insert_multiple(perfis)
            print(f" {len(perfis)} perfis alimentares inseridos com sucesso!")
        else:
            print(" Nenhum perfil alimentar encontrado no JSON.")
    except FileNotFoundError:
        print(" ERRO: Arquivo 'food_database.json' não encontrado.")
    except json.JSONDecodeError:
        print(" ERRO: Arquivo 'food_database.json' não é um JSON válido.")


if __name__ == '__main__':
    print("--- Iniciando a configuração do banco de dados ---")
    popular_alimentos()
    popular_treinos()
    popular_perfis_alimentares()
    print("\n--- Configuração do banco de dados finalizada! ---")
    