from fitness_app.core.auth import ServicoAutenticacao
from fitness_app.services.activity import ServicoAtividade
from fitness_app.services.nutrition import ServicoNutricional
from fitness_app.services.forum import ServicoForum
from fitness_app.services.feedback import ServicoFeedback
from fitness_app.services.wearable import ServicoWearable
from fitness_app.services.goal import ServicoMeta
from fitness_app.services.workout import ServicoTreino
from fitness_app.services.social import ServicoSocial
from fitness_app.services.video import ServicoVideo
from fitness_app.services.recommendation import ServicoRecomendacao
from datetime import datetime
from fitness_app.terminal.interface import (
    exibir_menu_atividades, exibir_menu_treinos, exibir_menu_nutricao,
    exibir_menu_metas, exibir_menu_forum, exibir_menu_feedback,
    exibir_menu_wearable, exibir_menu_social, exibir_menu_videos,
    exibir_menu_recomendacoes
)
from fitness_app.core.models import PlanoTreino
import os

# Instanciação de Objetos - cada serviço é uma instância de classe específica
servico_atividade = ServicoAtividade()
servico_nutricional = ServicoNutricional()
servico_forum = ServicoForum()
servico_feedback = ServicoFeedback()
servico_wearable = ServicoWearable()
servico_meta = ServicoMeta()
servico_treino = ServicoTreino()
servico_social = ServicoSocial()
servico_video = ServicoVideo()
servico_recomendacao = ServicoRecomendacao()

# Dicionário para tratar diferentes serviços de forma uniforme para mapeamento e identificação do objeto sem saber a classe
servicos_map = {
    'atividade': servico_atividade,
    'nutricao': servico_nutricional,
    'forum': servico_forum,
    'feedback': servico_feedback,
    'wearable': servico_wearable,
    'meta': servico_meta,
    'treino': servico_treino,
    'social': servico_social,
    'video': servico_video,
    'recomendacao': servico_recomendacao
}
# POLIMORFISMO EM AÇÃO - Função que executa operações em qualquer serviço
# Independente do tipo específico do objeto, todos respondem às mesmas mensagens
def executar_crud(servico_nome, operacao, *args, **kwargs):
    servico = servicos_map.get(servico_nome)
    if not servico:
        print(f"Serviço '{servico_nome}' inválido.")
        return None
    try:
        # POLIMORFISMO: getattr() permite chamar métodos dinamicamente
        # independente da classe específica do objeto
        metodo = getattr(servico, operacao)
        return metodo(*args, **kwargs)
    except Exception as e:
        print(f"Erro ao executar '{operacao}' em '{servico_nome}': {e}")
        return None


def autenticar_usuario(auth):
    email = input("E-mail: ")
    senha = input("Senha: ")
    usuario = auth.autenticar_usuario(email, senha)
    if usuario:
        print("Login realizado com sucesso!")
        return usuario 
    print("Usuário ou senha inválidos.")
    return None


def registrar_usuario(auth):
    nome = input("Nome: ")
    email = input("E-mail: ")
    senha = input("Senha: ")
    while True:
        genero = input("Gênero (Digite apenas M para Masculino ou F para Feminino): ").strip().upper()
        if genero in ("M", "F"):
            break
        print("Opção Inválida! Por favor digite apenas M ou F.")
    while True:
        try:
            idade = int(input("idade: "))
            if idade > 0:   
                break
            print("Idade inválida! Idade deve ser positiva.")
        except ValueError:
            print("Digite um numero inteiro para idade:")
    while True:
        try:
            peso = float(input("Peso (kg): "))
            if peso > 0:
                break
            print("Peso inválido! Peso deve ser positivo.")
        except ValueError:
            print("Digite um número válido para peso:")
    while True:
        try:
            altura = float(input("Altura (cm): "))
            if altura > 0:
                break
            print("Altura inválida! Altura deve ser positiva.")
        except ValueError:
            print("Digite um número válido para altura:")
    while True:
        print("Nível de Atividade:")
        print("1. Sedentário")
        print("2. Moderado")
        print("3. Ativo")
        nivel_atividade_op = input("Escolha uma opção (1-3): ")
        if nivel_atividade_op == "1":
            nivel_atividade = "Sedentário"
            break
        elif nivel_atividade_op == "2":
            nivel_atividade = "Moderado"
            break
        elif nivel_atividade_op == "3":
            nivel_atividade = "Ativo"
            break
        print("Opção inválida! Por favor, escolha entre 1 e 3.")

    while True:
        print("Objetivo:")
        print("1. Emagrecimento")
        print("2. Hipertrofia")
        print("3. Força")
        print("4. Resistência")
        print("5. Mobilidade")
        objetivo_op = input("Escolha uma opção (1-5): ")
        if objetivo_op == "1":
            objetivo = "Emagrecimento"
            break
        elif objetivo_op == "2":
            objetivo = "Hipertrofia"
            break
        elif objetivo_op == "3":
            objetivo = "Força"
            break
        elif objetivo_op == "4":
            objetivo = "Resistência"
            break
        elif objetivo_op == "5":
            objetivo = "Mobilidade"
            break
        print("Opção inválida! Por favor, escolha entre 1 e 5.")
    while True:
        print("Frequência de Treino:")
        print("1. 1x por semana")
        print("2. 2x por semana")
        print("3. 3x por semana")
        print("4. 4x por semana")
        print("5. 5x por semana")
        frequencia_op = input("Escolha uma opção (1-5): ")
        if frequencia_op == "1":
            frequencia_treino = "1x por semana"
            break
        elif frequencia_op == "2":
            frequencia_treino = "2x por semana"
            break
        elif frequencia_op == "3":
            frequencia_treino = "3x por semana"
            break
        elif frequencia_op == "4":
            frequencia_treino = "4x por semana"
            break
        elif frequencia_op == "5":
            frequencia_treino = "5x por semana"
            break
    while True:
        print("Restrições de Treino (você pode escolher mais de uma, separando por vírgula, ex: 2,3):")
        print("Restrições de Treino:")
        print("1. Nenhuma")
        print("2. Joelho")
        print("3. Ombro")
        print("4. Coluna")
        restricao_op = input("Escolha uma opção (1-4): ").split(",")
        restricao_dict = {
            "1": "nenhuma",
            "2": "joelho",
            "3": "ombro",
            "4": "coluna"
        } 
        restricoes_treino = []
        for op in restricao_op:
            op = op.strip()
            if op in restricao_dict and restricao_dict[op] != "nenhuma":
                restricoes_treino.append(restricao_dict[op])
        if not restricoes_treino and "1" in restricao_op:
            restricoes_treino = ["nenhuma"]
        if "nenhuma" in restricoes_treino and len(restricoes_treino) > 1:
            restricoes_treino = [r for r in restricoes_treino if r != "nenhuma"]
        if restricoes_treino:
            break
        print("Opção inválida! Por favor, escolha entre 1 e 4.")
    while True:
        print("Restrições Alimentares (você pode escolher mais de uma, separando por vírgula, ex: 2,3,4):")
        print("Restrições Alimentares:")
        print("1. Nenhuma")
        print("2. Lactose")
        print("3. Glúten")
        print("4. Diabetes")
        restricao_dieta_op = input("Escolha uma opção (1-4): ").split(",")
        restricao_dieta_dict = {
            "1": "nenhuma",
            "2": "lactose",
            "3": "glúten",
            "4": "diabetes"
        }
        restricoes_dieta = []
        for op in restricao_dieta_op:
            op = op.strip()
            if op in restricao_dieta_dict and restricao_dieta_dict[op] != "nenhuma":
                restricoes_dieta.append(restricao_dieta_dict[op])
        if not restricoes_dieta and "1" in restricao_dieta_op:
            restricoes_dieta = ["nenhuma"]
        if "nenhuma" in restricoes_dieta and len(restricoes_dieta) > 1:
            restricoes_dieta = [r for r in restricoes_dieta if r != "nenhuma"]
        if restricoes_dieta:
            break
        print("Opção inválida! Por favor, escolha entre 1 e 4.")
    dados_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "genero": genero,
        "idade": idade,
        "peso": peso,
        "altura": altura,
        "nivel_atividade": nivel_atividade,
        "objetivo": objetivo,
        "frequencia_treino": frequencia_treino,
        "restricoes_treino": restricoes_treino,
        "restricao_dieta": restricoes_dieta,
        "dados_wearable": None,
        "perfil_completo": True
    }
    try:
        auth.registrar_usuario(dados_usuario)
        print("Usuário registrado com sucesso!")
        print("Perfil completo!")
    except Exception as e:
        print(f"Erro ao registrar: {e}")
def recuperar_senha_usuario(auth):
    print("\n--- Recuperação de Senha ---")
    email = input("Digite seu email: ").strip()
    
    if not email:
        print("Email não pode estar vazio.")
        return
    
    print("Por segurança, precisamos verificar algumas informações...")
    rec = auth.recuperar_senha(email)
    if rec:
        print("Recuperação concluída com sucesso.")
        print(" Importante!: Altere sua senha após o login pelo menu.")
    
def alterar_senha_usuario(auth, usuario_logado):
    print("\n--- Alterar Senha ---")
    senha_atual = input("Digite sua senha atual: ")
    nova_senha = input("Digite a nova senha: ").strip()
    if not nova_senha:
        print("A nova senha não pode estar vazia.")
        return
    try:
        
        resultado = auth.alterar_senha(usuario_logado.email, senha_atual, nova_senha)
        if resultado:
            print("Senha alterada com sucesso!")
        else:
            print("Erro ao alterar senha. Verifique sua senha atual.")
    except Exception as e:
        print(f"Erro ao alterar senha: {e}")

def gerenciar_treinos(usuario_logado):
    while True:
        subop = exibir_menu_treinos()
        if subop == "1":
            planos = executar_crud('treino', 'listar', usuario_email=usuario_logado.email)
            if not planos:
                print("Nenhum plano cadastrado.")
            else:
                for idx, p in enumerate(planos, 1):
                    print(f"\n{idx}. {p.nome} ({p.nivel}) - Objetivo: {getattr(p, 'objetivo', '-')}")
                    print("  Exercícios:")
                    if isinstance(p.exercicios, list):
                        for ex in p.exercicios:
                            if isinstance(ex, dict):
                                grupo = ex.get('grupo', '-')
                                exercicio = ex.get('exercicio', '-')
                                series = ex.get('series', '-')
                                repeticoes = ex.get('repeticoes', '-')
                                print(f"    - [{grupo}] {exercicio}: {series}x{repeticoes}")
                            else:
                                print(f"    - {ex}")
                    else:
                        print(f"    - {p.exercicios}")
                    if hasattr(p, 'videos') and p.videos:
                        print("  Vídeos associados:")
                        for v in p.videos:
                            print(f"    - {v.get('titulo', '-')}: {v.get('url', '-')}")
        elif subop == "2":
            print("\nComo deseja criar o plano?")
            print("1. Escolher plano pré-pronto")
            print("2. Criar plano personalizado")
            tipo_plano = input("Escolha uma opção: ")
            if tipo_plano == "1":
                preferencias = servico_recomendacao.map_preferencias_usuario(usuario_logado)
                recs = servico_recomendacao.recomendar_treinos_sugestoes(preferencia_usuario=preferencias)
                if not recs:
                    print("Nenhum plano pré-pronto encontrado para suas preferências.")
                    continue

                treinos_prontos = []
                for rec in recs:
                    dados = rec.conteudo
                    try:
                        plano = PlanoTreino.from_dict(dados)
                    except Exception:
                        plano = PlanoTreino(nome=dados.get('nome'), exercicios=dados.get('exercicios'), objetivo=dados.get('objetivo'), nivel=dados.get('nivel'))
                    treinos_prontos.append(plano)

                print("\n--- Planos Pré-Prontos Recomendados ---")
                for idx, t in enumerate(treinos_prontos, 1):
                    print(f"{idx}. {t.nome} ({t.nivel}, objetivo: {t.objetivo})")

                try:
                    idx_treino = int(input("Digite o número do plano para adicionar: ")) - 1
                    if 0 <= idx_treino < len(treinos_prontos):
                        plano = treinos_prontos[idx_treino]
                        executar_crud('treino', 'criar',
                            usuario_email=usuario_logado.email,
                            nome=plano.nome,
                            exercicios=plano.exercicios,
                            objetivo=plano.objetivo,
                            nivel=plano.nivel
                        )
                        print("Plano pré-pronto adicionado!")
                    else:
                        print("Índice inválido.")
                except ValueError:
                    print("Entrada inválida.")

            elif tipo_plano == "2":
                nome = input("Nome do plano: ")
                objetivo = input("Objetivo: ")
                nivel = input("Nível: ")
                exercicios = input("Exercícios (separados por vírgula): ").split(",")
                executar_crud('treino', 'criar',
                    usuario_email=usuario_logado.email,
                    nome=nome,
                    exercicios=exercicios,
                    objetivo=objetivo,
                    nivel=nivel
                )
                print("Plano personalizado criado!")
            else:
                print("Opção inválida.")
        elif subop == "3":
            planos = executar_crud('treino', 'listar', usuario_email=usuario_logado.email)
            for idx, p in enumerate(planos, 1):
                print(f"{idx}. {p.nome} ({p.nivel})")
            idx = int(input("Digite o número do plano para deletar: ")) - 1
            if 0 <= idx < len(planos):
                plano = planos[idx]
                executar_crud('treino', 'deletar', plano.id)
                print("Plano deletado!")
            else:
                print("Índice inválido.")
        elif subop == "4":
            planos = executar_crud('treino', 'listar', usuario_email=usuario_logado.email)
            if not planos:
                print("Nenhum plano cadastrado.")
                continue
            for idx, p in enumerate(planos, 1):
                print(f"{idx}. {p.nome} ({p.nivel})")
            idx_plano = input("Digite o número do plano para associar vídeo: ")
            try:
                idx_plano = int(idx_plano) - 1
                if 0 <= idx_plano < len(planos):
                    favoritos = executar_crud('video', 'listar', usuario_email=usuario_logado.email)
                    if not favoritos:
                        print("Nenhum vídeo favorito salvo.")
                        continue
                    for idx, v in enumerate(favoritos, 1):
                        print(f"{idx}. {v.titulo}")
                    idx_video = input("Digite o número do vídeo para associar: ")
                    idx_video = int(idx_video) - 1
                    if 0 <= idx_video < len(favoritos):
                        plano = planos[idx_plano]
                        video_info = {
                            'titulo': favoritos[idx_video].titulo,
                            'url': favoritos[idx_video].url,
                            'duracao': favoritos[idx_video].duracao,
                            'data_publicacao': favoritos[idx_video].data_publicacao,
                            'descricao': favoritos[idx_video].descricao,
                            'thumbnail': favoritos[idx_video].thumbnail
                        }
                       
                        if not hasattr(plano, 'videos') or not isinstance(plano.videos, list):
                            plano.videos = []
                        if video_info not in plano.videos:
                            plano.videos.append(video_info)
                            executar_crud('treino', 'atualizar', plano.id, {'videos': plano.videos})
                            print("Vídeo associado ao plano!")
                        else:
                            print("Este vídeo já está associado ao plano.")
                    else:
                        print("Índice de vídeo inválido.")
                else:
                    print("Índice de plano inválido.")
            except Exception:
                print("Entrada inválida.")
        elif subop == "5":
            planos = executar_crud('treino', 'listar', usuario_email=usuario_logado.email)
            if not planos:
                print("Nenhum plano cadastrado.")
                continue
            
            for idx, p in enumerate(planos, 1):
                print(f"{idx}. {p.nome} ({p.nivel})")
            
            try:
                idx_plano = int(input("Digite o número do plano: ")) - 1
                if 0 <= idx_plano < len(planos):
                    exercicio = input("Digite o nome do exercício para adicionar: ")
                    if servico_treino.add_exercicio(planos[idx_plano].id, exercicio):
                        print("Exercício adicionado com sucesso!")
                    else:
                        print("Erro ao adicionar exercício.")
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Entrada inválida.")

        elif subop == "6":
            planos = executar_crud('treino', 'listar', usuario_email=usuario_logado.email)
            if not planos:
                print("Nenhum plano cadastrado.")
                continue

            for idx, p in enumerate(planos, 1):
                print(f"{idx}. {p.nome} ({p.nivel})")

            try:
                idx_plano = int(input("Digite o número do plano: ")) - 1
                if 0 <= idx_plano < len(planos):
                    exercicio = input("Digite o nome do exercício para remover: ")
                    if servico_treino.remove_exercicio(planos[idx_plano].id, exercicio):
                        print("Exercício removido com sucesso!")
                    else:
                        print("Erro ao remover exercício.")
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Entrada inválida.")
        elif subop == "7":
            planos = executar_crud('treino', 'listar', usuario_email=usuario_logado.email)
            if not planos:
                print("Nenhum plano cadastrado para atualizar.")
                continue
            
            print("\n--- Seus Planos ---")
            for idx, p in enumerate(planos, 1):
                print(f"{idx}. {p.nome} ({p.nivel}) - Objetivo: {getattr(p, 'objetivo', '-')}")
            
            try:
                idx_plano = int(input("Digite o número do plano para atualizar: ")) - 1
                if 0 <= idx_plano < len(planos):
                    plano = planos[idx_plano]
                    
                    print("\n--- Atualizar Plano ---")
                    print("Deixe em branco para manter o valor atual.")
                    
                    novo_nome = input(f"Novo nome (atual: {plano.nome}): ") or plano.nome
                    
                    novo_objetivo = input(f"Novo objetivo (atual: {getattr(plano, 'objetivo', '-')}): ") or getattr(plano, 'objetivo', '')
                    
                    novo_nivel = input(f"Novo nível (atual: {plano.nivel}): ") or plano.nivel
                    
                    print(f"\nExercícios atuais:")
                    if isinstance(plano.exercicios, list):
                        for i, ex in enumerate(plano.exercicios, 1):
                            if isinstance(ex, dict):
                                print(f"  {i}. [{ex.get('grupo', '-')}] {ex.get('exercicio', '-')}: {ex.get('series', '-')}x{ex.get('repeticoes', '-')}")
                            else:
                                print(f"  {i}. {ex}")
                    
                    atualizar_exercicios = input("Deseja atualizar os exercícios? (s/n): ").lower()
                    novos_exercicios = plano.exercicios
                    
                    if atualizar_exercicios == 's':
                        print("Digite os novos exercícios (separados por vírgula) ou deixe em branco para manter:")
                        exercicios_input = input("Exercícios: ").strip()
                        if exercicios_input:
                            novos_exercicios = [ex.strip() for ex in exercicios_input.split(",")]
                    
                    dados_atualizados = {
                        "nome": novo_nome,
                        "objetivo": novo_objetivo,
                        "nivel": novo_nivel,
                        "exercicios": novos_exercicios
                    }
                    
                    if hasattr(plano, 'videos'):
                        dados_atualizados['videos'] = plano.videos
                    
                    resultado = executar_crud('treino', 'atualizar', plano.id, dados_atualizados)
                    
                    if resultado:
                        print("Plano atualizado com sucesso!")
                    else:
                        print("Erro ao atualizar plano.")
                        
                else:
                    print("Índice inválido.")
                    
            except ValueError:
                print("Entrada inválida. Digite um número.")
            except Exception as e:
                print(f"Erro inesperado: {e}")
        elif subop == "0":
            break
        else:
            print("Opção inválida.")


def gerenciar_atividades(usuario_logado):
    while True:
        subop = exibir_menu_atividades()
        if subop == "1":
            atividades = executar_crud('atividade', 'listar', usuario_email=usuario_logado.email)
            if not atividades:
                print("Nenhuma atividade registrada.")
            else:
                for idx, a in enumerate(atividades, 1):
                    print(f"{idx}. {a.tipo} em {a.data} ({a.calorias} kcal)")
        elif subop == "2":
            tipo = input("Tipo de atividade: ")
            data = input("Data (DD-MM-YYYY): ")
            duracao_str = input("Duração (min): ")
            calorias_str = input("Calorias gastas (deixe vazio para calcular automaticamente): ")
            passos_str = input("Passos (opcional): ")
            try:
                duracao = float(duracao_str) if duracao_str.strip() else 0
                calorias = float(calorias_str) if calorias_str.strip() else None
                passos = int(passos_str) if passos_str.strip() else None
            except ValueError as e:
                print(f"Erro: valores numéricos inválidos - {e}")
                continue
            
            ritmo = None
            if tipo.lower() in ["caminhada", "corrida", "ciclismo"]:
                print("Ritmo:")
                print("1. Lento")
                print("2. Medio")
                print("3. Rapido")
                ritmo = input("Escolha uma opção de ritmo: ")
                ritmos = {
                    "1": "Lento",
                    "2": "Medio",
                    "3": "Rapido"
                }
                ritmo = ritmos.get(ritmo, "Medio")
                resultado = executar_crud('atividade', 'criar', 
                usuario_email=usuario_logado.email, 
                tipo=tipo, 
                data=data, 
                duracao=duracao,
                calorias=calorias,
                passos=passos,
                ritmo=ritmo,
                usuario=usuario_logado)
            
            if resultado:
                print("Atividade registrada com sucesso!")
            else:
                print("Erro ao registrar atividade.")
        elif subop == "3":
            atividades = executar_crud('atividade', 'listar', usuario_email=usuario_logado.email)
            for idx, a in enumerate(atividades, 1):
                print(f"{idx}. {a.tipo} em {a.data} ({a.calorias} kcal)")
            idx = int(input("Digite o número da atividade para deletar: ")) - 1
            if 0 <= idx < len(atividades):
                atividade_obj = atividades[idx]
                executar_crud('atividade', 'deletar', id=atividade_obj.id)
                print("Atividade deletada!")
            else:
                print("Índice inválido.")
        elif subop == "4":
            atividades = executar_crud('atividade', 'listar', usuario_email=usuario_logado.email)
            if not atividades:
                print("Nenhuma atividade registrada.")
            else:
                for idx, a in enumerate(atividades, 1):
                    print(f"{idx}. {a.tipo} em {a.data} ({a.calorias} kcal)")
            try:
                idx = int(input("Digite o número da atividade para atualizar: ")) - 1
                if 0 <= idx < len(atividades):
                    atividade_obj = atividades[idx]
                    print("Deixe em Branco para manter o valor atual")
                    novo_tipo = input(f"Novo tipo de atividade (atual: {atividade_obj.tipo}): ") or atividade_obj.tipo
                    nova_data = input(f"Nova data (atual: {atividade_obj.data}): ") or atividade_obj.data
                    nova_duracao = input(f"Nova duração (min) (atual: {atividade_obj.duracao}): ") or atividade_obj.duracao
                    novas_calorias_str = input(f"Novas calorias gastas (atual: {atividade_obj.calorias}): ")
                    if not novas_calorias_str:
                        peso_usuario = usuario_logado.peso
                        try:
                            novas_calorias = float(servico_atividade.calcular_calorias(
                                novo_tipo,
                                float(peso_usuario),
                                float(nova_duracao)
                            ))
                        except Exception:
                            novas_calorias = atividade_obj.calorias
                    else:
                       try:
                            novas_calorias = float(novas_calorias_str)
                       except ValueError:
                            novas_calorias = atividade_obj.calorias
                    passos_atual = atividade_obj.passos if atividade_obj.passos is not None else "Nenhum"
                    novos_passos_str = input(f"Novos passos (atual: {passos_atual}): ")

                    if novos_passos_str.strip():
                        try:
                            novos_passos = int(novos_passos_str)
                        except ValueError:
                            novos_passos = atividade_obj.passos
                    else:
                        novos_passos = atividade_obj.passos
                    novos_dados = {
                        "tipo": novo_tipo,
                        "data": nova_data,
                        "duracao": nova_duracao,
                        "calorias": novas_calorias,
                        "passos": novos_passos
                    }
                    resultado = executar_crud('atividade', 'atualizar', id=atividade_obj.id, dados=novos_dados)
                    if resultado:
                        print("Atividade atualizada com sucesso!")
                    else:
                        print("Erro ao atualizar atividade.")
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
            except Exception as e:
                print(f"Erro inesperado: {e}")
        elif subop == "0":
            break
        else:
            print("Opção inválida.")


def gerenciar_nutricao(usuario_logado):
    while True:
        subop = exibir_menu_nutricao()
        if subop == "1":
            registros = executar_crud('nutricao', 'listar', usuario_email=usuario_logado.email)
            if not registros:
                print("Nenhum registro encontrado.")
            else:
                for idx, r in enumerate(registros, 1):
                    print(f"\n{idx}. Data: {r.data}")
                    print(f"   Calorias Totais: {r.calorias} kcal")
                    print("   Refeições:")
                    for refeicao in r.refeicoes:
                        print(f"    - {refeicao['alimento']} ({refeicao['quantidade']}x): {refeicao['calorias']} kcal")

        elif subop == "2":
            data = input("Data (DD-MM-YYYY, deixe em branco para hoje): ") or datetime.now().strftime('%d-%m-%Y')
            nomes_alimentos = servico_nutricional.listar_todos_alimentos()
            
            alimentos_refeicao = []
            while True:
                if nomes_alimentos:
                    print("\nAlimentos disponíveis no banco de dados:")
                    for idx, nome in enumerate(nomes_alimentos, 1):
                        print(f"{idx}. {nome}")
                else:
                    print("Nenhum alimento cadastrado ainda.")

                nome_input = input("Digite o nome ou índice do alimento (ou 'fim' para terminar): ").strip()
                if nome_input.lower() == 'fim':
                    break

                alimento_selecionado = None
                if nome_input.isdigit():
                    try:
                        idx = int(nome_input) - 1
                        if 0 <= idx < len(nomes_alimentos):
                            alimento_selecionado = servico_nutricional.buscar_alimento(nome_alimento=nomes_alimentos[idx])
                        else:
                            print("Índice inválido.")
                            continue
                    except (ValueError, IndexError):
                        print("Entrada inválida.")
                        continue
                else:
                    alimento_selecionado = servico_nutricional.buscar_alimento(nome_alimento=nome_input)

                if not alimento_selecionado:
                    print(f"Alimento '{nome_input}' não encontrado. Vamos cadastrá-lo.")
                    try:
                        calorias = float(input(f"Calorias de '{nome_input}': "))
                        proteina = float(input(f"Proteína (g) de '{nome_input}': "))
                        gordura = float(input(f"Gordura (g) de '{nome_input}': "))
                        carboidrato = float(input(f"Carboidrato (g) de '{nome_input}': "))
                        alimento_selecionado = {
                            "alimento": nome_input, "calorias": calorias, "proteina": proteina,
                            "gordura": gordura, "carboidrato": carboidrato
                        }
                    except ValueError:
                        print("Valores nutricionais inválidos. Tente novamente.")
                        continue
                
                try:
                    quantidade = float(input(f"Quantidade de '{alimento_selecionado['alimento']}' (unidades/porção): "))
                except ValueError:
                    print("Quantidade inválida.")
                    continue

                alimento_para_registrar = alimento_selecionado.copy()
                alimento_para_registrar['quantidade'] = quantidade
                alimentos_refeicao.append(alimento_para_registrar)
                print(f"'{alimento_selecionado['alimento']}' adicionado.")

            if alimentos_refeicao:
                executar_crud('nutricao', 'criar', usuario_email=usuario_logado.email, data=data, alimentos=alimentos_refeicao)
                print("Refeição registrada com sucesso!")
            else:
                print("Nenhum alimento adicionado. Registro cancelado.")

        elif subop == "3":
            registros = executar_crud('nutricao', 'listar', usuario_email=usuario_logado.email)
            if not registros:
                print("Nenhum registro para deletar.")
                continue
            for idx, r in enumerate(registros, 1):
                print(f"{idx}. {r.data} - {r.calorias} kcal")
            try:
                idx_del = int(input("Digite o número do registro para deletar: ")) - 1
                if 0 <= idx_del < len(registros):
                    executar_crud('nutricao', 'deletar', id=registros[idx_del].id)
                    print("Registro deletado!")
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Entrada inválida.")

        elif subop == "4":
            registros = executar_crud('nutricao', 'listar', usuario_email=usuario_logado.email)
            if not registros:
                print("Nenhum registro para atualizar.")
                continue
            for idx, r in enumerate(registros, 1):
                print(f"{idx}. {r.data} - {r.calorias} kcal")
            try:
                idx_up = int(input("Digite o número do registro para atualizar: ")) - 1
                if 0 <= idx_up < len(registros):
                    registro = registros[idx_up]
                    print("Deixe em branco para manter o valor atual.")
                    nova_data = input(f"Nova data (DD-MM-YYYY) (atual: {registro.data}): ") or registro.data
                    
                    alimentos_refeicao = []
                    nomes_alimentos = servico_nutricional.listar_todos_alimentos()
                    
                    print("\nAlimentos atuais:")
                    for refeicao in registro.refeicoes:
                        print(f"- {refeicao['alimento']} ({refeicao['quantidade']}x)")
                    
                    print("\nAdicione novos alimentos (ou deixe vazio para manter atuais):")
                    while True:
                        if nomes_alimentos:
                            print("\nAlimentos disponíveis no banco de dados:")
                            for idx, nome in enumerate(nomes_alimentos, 1):
                                print(f"{idx}. {nome}")
                        else:
                            print("Nenhum alimento cadastrado ainda.")

                        nome_input = input("Digite o nome ou índice do alimento (ou 'fim' para terminar): ").strip()
                        if nome_input.lower() == 'fim':
                            break

                        alimento_selecionado = None
                        if nome_input.isdigit():
                            try:
                                idx = int(nome_input) - 1
                                if 0 <= idx < len(nomes_alimentos):
                                    alimento_selecionado = servico_nutricional.buscar_alimento(nome_alimento=nomes_alimentos[idx])
                                else:
                                    print("Índice inválido.")
                                    continue
                            except (ValueError, IndexError):
                                print("Entrada inválida.")
                                continue
                        else:
                            alimento_selecionado = servico_nutricional.buscar_alimento(nome_alimento=nome_input)

                        if not alimento_selecionado:
                            print(f"Alimento '{nome_input}' não encontrado. Vamos cadastrá-lo.")
                            try:
                                calorias = float(input(f"Calorias de '{nome_input}': "))
                                proteina = float(input(f"Proteína (g) de '{nome_input}': "))
                                gordura = float(input(f"Gordura (g) de '{nome_input}': "))
                                carboidrato = float(input(f"Carboidrato (g) de '{nome_input}': "))
                                alimento_selecionado = {
                                    "alimento": nome_input, "calorias": calorias, "proteina": proteina,
                                    "gordura": gordura, "carboidrato": carboidrato
                                }
                            except ValueError:
                                print("Valores nutricionais inválidos. Tente novamente.")
                                continue
                        
                        try:
                            quantidade = float(input(f"Quantidade de '{alimento_selecionado['alimento']}' (unidades/porção): "))
                        except ValueError:
                            print("Quantidade inválida.")
                            continue

                        alimento_para_registrar = alimento_selecionado.copy()
                        alimento_para_registrar['quantidade'] = quantidade
                        alimentos_refeicao.append(alimento_para_registrar)
                        print(f"'{alimento_selecionado['alimento']}' adicionado.")

                    if alimentos_refeicao:
                        dados_atualizar = {"data": nova_data, "alimentos": alimentos_refeicao}
                        executar_crud('nutricao', 'atualizar', id=registro.id, dados=dados_atualizar)
                        print("Registro atualizado com sucesso!")
                    else:
                        if nova_data != registro.data:
                            dados_atualizar = {"data": nova_data}
                            executar_crud('nutricao', 'atualizar', id=registro.id, dados=dados_atualizar)
                            print("Data do registro atualizada!")
                        else:
                            print("Nenhuma alteração feita.")
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Entrada inválida.")

        elif subop == "5":
            resumo = servico_nutricional.analisar_consumo(usuario_email=usuario_logado.email)
            if not resumo or resumo.get('calorias', 0) == 0:
                print("Nenhum dado de consumo para analisar.")
                continue
            print("\n--- Análise de Consumo do Dia ---")
            print(f"Total de calorias: {resumo['calorias']:.2f} kcal")
            print(f"Total de proteínas: {resumo['proteina']:.2f} g")
            print(f"Total de gorduras: {resumo['gordura']:.2f} g")
            print(f"Total de carboidratos: {resumo['carboidrato']:.2f} g")
            print("\nAnálise concluída!")
        elif subop == "0":
            break
        else:
            print("Opção inválida.")
def gerenciar_metas(usuario_logado):
    while True:
        subop = exibir_menu_metas()
        if subop == "1":
            metas = executar_crud('meta', 'listar', usuario_email=usuario_logado.email)
            if not metas:
                print("Nenhuma meta cadastrada.")
            else:
                for idx, m in enumerate(metas, 1):
                    status = "Atingida" if m.atingida else "Pendente"
                    print(f"{idx}. {m.tipo}: {m.valor} ({status})")
        elif subop == "2":
            tipo = input("Tipo de meta: ")
            valor = input("Valor/meta: ")
            data_inicio = input("Data início (DD-MM-YYYY): ")
            data_fim = input("Data fim (DD-MM-YYYY): ")
            executar_crud('meta', 'criar',
                usuario_email=usuario_logado.email,
                tipo=tipo,
                valor=valor,
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            print("Meta criada!")
        elif subop == "3":
            metas = executar_crud('meta', 'listar', usuario_email=usuario_logado.email)
            if not metas:
                print("Nenhuma meta cadastrada.")
            else:
                for idx, m in enumerate(metas, 1):
                    print(f"{idx}. {m.tipo}: {m.valor}")
                idx = int(input("Digite o número da meta para deletar: ")) - 1
                if 0 <= idx < len(metas):
                   executar_crud('meta', 'deletar', id=metas[idx].id)
                   print("Meta deletada!")
                else:
                    print("Índice inválido.")

        elif subop == "4":
            metas = executar_crud('meta', 'listar', usuario_email=usuario_logado.email)
            if not metas:
                print("Nenhuma meta cadastrada.")
            else:
                for idx, m in enumerate(metas, 1):
                    print(f"{idx}. {m.tipo}: {m.valor}")
                idx = int(input("Digite o número da meta para atualizar: ")) - 1
                if 0 <= idx < len(metas):
                    tipo = input("Novo tipo de meta: ")
                    valor = input("Novo valor/meta: ")
                    data_inicio = input("Nova data início (DD-MM-YYYY): ")
                    data_fim = input("Nova data fim (DD-MM-YYYY): ")
                    executar_crud('meta', 'atualizar',
                        id=metas[idx].id,
                        dados={
                            "tipo": tipo,
                            "valor": valor,
                            "data_inicio": data_inicio,
                            "data_fim": data_fim
                        }
                    )
                    print("Meta atualizada!")
        elif subop == "5":
             progresso = servico_meta.verificar_progresso(usuario_email=usuario_logado.email)
             print("Metas atingidas:")
             for m in progresso["atingidas"]:
                print(f"- {m.tipo}: {m.valor}")
             print("Metas pendentes:")
             for m in progresso["pendentes"]:
                 print(f"- {m.tipo}: {m.valor}")
        elif subop == "6":
            metas = executar_crud('meta', 'listar', usuario_email=usuario_logado.email)
            if not metas:
                print("Nenhuma meta cadastrada.")
            else:
                for idx, m in enumerate(metas, 1):
                    status = "Atingida" if m.atingida else "Pendente"
                    print(f"{idx}. {m.tipo}: {m.valor} ({status})")
                idx = int(input("Digite o número da meta para concluir: ")) - 1
                if 0 <= idx < len(metas):
                    servico_meta.concluir_meta(id=metas[idx].id)
                    print("Meta concluída!")
        elif subop == "0":
            break
        else:
            print("Opção inválida.")


def gerenciar_wearable(usuario_logado):
    while True:
        subop = exibir_menu_wearable()
        if subop == "1":
            dados = executar_crud('wearable', 'listar', usuario_email=usuario_logado.email)
            if not dados:
                print("Nenhum dado de wearable registrado.")
            else:
                for idx, d in enumerate(dados, 1):
                    print(f"{idx}. {d.data} - {d.tipo}: {d.valor}")
        elif subop == "2":
            tipo = input("Tipo de dado (ex: passos, batimentos): ")
            valor = input("Valor: ")
            executar_crud('wearable', 'criar',
                usuario_email=usuario_logado.email,
                tipo=tipo,
                valor=valor
            )
            print("Dado registrado com sucesso!")
        elif subop == "3":
            dados = executar_crud('wearable', 'listar', usuario_email=usuario_logado.email)
            if not dados:
                print("Nenhum dado para deletar.")
            else:
                for idx, d in enumerate(dados, 1):
                    print(f"{idx}. {d.data} - {d.tipo}: {d.valor}")
                
                print("\nOpções de exclusão:")
                print("1. Deletar um dado específico")
                print("2. Deletar múltiplos dados")
                print("3. Deletar todos os dados")
                print("0. Cancelar")
                
                opcao_delete = input("Escolha uma opção: ")
                
                if opcao_delete == "1":
                    try:
                        idx_del = int(input("Digite o número do dado para deletar: ")) - 1
                        if 0 <= idx_del < len(dados):
                            executar_crud('wearable', 'deletar', id=dados[idx_del].id)
                            print("Dado deletado com sucesso!")
                        else:
                            print("Índice inválido.")
                    except ValueError:
                        print("Entrada inválida.")
                
                elif opcao_delete == "2":
                    indices_str = input("Digite os números dos dados para deletar (separados por vírgula, ex: 1,3,5): ")
                    try:
                        indices = [int(i.strip()) - 1 for i in indices_str.split(",") if i.strip()]
                        indices_validos = [i for i in indices if 0 <= i < len(dados)]
                        
                        if not indices_validos:
                            print("Nenhum índice válido fornecido.")
                            continue
                        
                        print(f"\nVocê irá deletar {len(indices_validos)} dados:")
                        for i in indices_validos:
                            print(f"- {dados[i].data} - {dados[i].tipo}: {dados[i].valor}")
                        
                        confirmacao = input("Confirma a exclusão? (s/n): ").lower()
                        if confirmacao == 's':
                            deletados = 0
                            for i in sorted(indices_validos, reverse=True):
                                if executar_crud('wearable', 'deletar', id=dados[i].id):
                                    deletados += 1
                            print(f"{deletados} dados deletados com sucesso!")
                        else:
                            print("Exclusão cancelada.")
                    except ValueError:
                        print("Formato inválido. Use números separados por vírgula.")
                
                elif opcao_delete == "3":
                    print(f"\nVocê irá deletar TODOS os {len(dados)} dados:")
                    for d in dados:
                        print(f"- {d.data} - {d.tipo}: {d.valor}")
                    
                    confirmacao = input("\nTem certeza que deseja deletar TODOS os dados? (digite 'CONFIRMAR' para prosseguir): ")
                    if confirmacao == "CONFIRMAR":
                        deletados = 0
                        for d in dados:
                            if executar_crud('wearable', 'deletar', id=d.id):
                                deletados += 1
                        print(f"Todos os {deletados} dados foram deletados!")
                    else:
                        print("Exclusão cancelada.")
                
                elif opcao_delete == "0":
                    print("Operação cancelada.")
                else:
                    print("Opção inválida.")
        elif subop == "4":
            tipo = input("Tipo de dado para simular (passos, batimentos, sono): ")
            if tipo in ["passos", "batimentos", "sono"]:
                dado_gerado = servico_wearable.gerar_dado_aleatorio(usuario_email=usuario_logado.email, tipo=tipo)
                print(f"Dado simulado gerado: {dado_gerado.tipo}: {dado_gerado.valor}")
            else:
                print("Tipo de simulação inválido.")
        elif subop == "5":
            nome_arquivo = input("Digite o nome do arquivo CSV (ex: meus_dados_wearable.csv): ").strip()
            if not nome_arquivo:
                print("Nome de arquivo inválido.")
                continue
            if not nome_arquivo.lower().endswith('.csv'):
                nome_arquivo += '.csv'
            pasta_fitness_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Seta a Pasta no diretório relativo a menus.py duas vezes selecionando /fitness_app
            pasta_data = os.path.join(pasta_fitness_app, 'data')
            os.makedirs(pasta_data, exist_ok=True)
            caminho_completo = os.path.join(pasta_data, nome_arquivo)
            try:
                servico_wearable.exportar_dados_csv(usuario_email=usuario_logado.email, caminho_csv=caminho_completo)
                print(f"Dados exportados para: fitness_app/data/{nome_arquivo}")
            except Exception as e:
                print(f"Erro ao exportar: {e}")
        elif subop == "6":
            nome_arquivo = input("Digite o nome do arquivo CSV para importar (ex: wearable.csv): ").strip()
            if not nome_arquivo:
                print("Nome de arquivo inválido.")
                continue
            if not nome_arquivo.lower().endswith('.csv'):
                nome_arquivo += '.csv'
            pasta_fitness_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pasta_data = os.path.join(pasta_fitness_app, 'data')
            caminho_completo = os.path.join(pasta_data, nome_arquivo)
            if not os.path.exists(caminho_completo):
                print(f"Arquivo não encontrado: fitness_app/data/{nome_arquivo}")
                print("Coloque o arquivo dentro da pasta fitness_app/data e tente novamente.")
                continue
            try:
                servico_wearable.importar_dados_csv(caminho_csv=caminho_completo, usuario_email=usuario_logado.email)
                print(f"Dados importados com sucesso de: fitness_app/data/{nome_arquivo}")
            except FileNotFoundError:
                print(f"Arquivo não encontrado: fitness_app/data/{nome_arquivo}")
            except Exception as e:
                print(f"Erro ao importar: {e}")
        elif subop == "0":
            break
        else:
            print("Opção inválida.")

def gerenciar_social(usuario_logado):
    while True:
        subop = exibir_menu_social()
        if subop == "1":
            desafios = executar_crud('social', 'listar')
            if not desafios:
                print("Nenhum desafio disponível.")
            else:
                for idx, d in enumerate(desafios, 1):
                    print(f"{idx}. {d.nome} ({d.data_inicio} - {d.data_fim})\n   {d.descricao}\n")
        elif subop == "2":
            nome = input("Nome do desafio: ")
            descricao = input("Descrição: ")
            data_inicio = input("Data de início (DD-MM-YYYY): ")
            data_fim = input("Data de fim (DD-MM-YYYY): ")
            executar_crud('social', 'criar',
                nome=nome,
                descricao=descricao,
                data_inicio=data_inicio,
                data_fim=data_fim
            )
            print("Desafio criado!")
        elif subop == "3":
            desafios = executar_crud('social', 'listar')
            if not desafios:
                print("Nenhum desafio para participar.")
            else:
                for idx, d in enumerate(desafios, 1):
                    print(f"{idx}. {d.nome}")
                idx = int(input("Digite o número do desafio para entrar: ")) - 1
                if 0 <= idx < len(desafios):
                    servico_social.participar_desafio(desafio_id=desafios[idx].id, usuario_email=usuario_logado.email)
                    print("Você entrou no desafio!")
                else:
                    print("Índice inválido.")
        elif subop == "4":
            desafios = executar_crud('social', 'listar')
            if not desafios:
                print("Nenhum desafio para ver participantes.")
            else:
                for idx, d in enumerate(desafios, 1):
                    print(f"{idx}. {d.nome}")
                idx = int(input("Digite o número do desafio: ")) - 1
                if 0 <= idx < len(desafios):
                    participantes = getattr(desafios[idx], 'participantes', [])
                    print(f"Participantes do desafio '{desafios[idx].nome}':")
                    print(f"<{len(participantes)} participantes>")
                    if participantes:
                        for p_email in participantes:
                            print(f"- {p_email}")
                    else:
                        print("Nenhum participante ainda.")
                else:
                    print("Índice inválido.")
        elif subop == "5":
            desafios = executar_crud('social', 'listar')
            if not desafios:
                print("Nenhum desafio disponível para sair.")
            else:
                for idx, d in enumerate(desafios, 1):
                    print(f"{idx}. {d.nome}")
                idx = int(input("Digite o número do desafio para sair: ")) - 1
                if 0 <= idx < len(desafios):
                    servico_social.sair_desafio(desafio_id=desafios[idx].id, usuario_email=usuario_logado.email)
                    print("Você saiu do desafio!")
                else:
                    print("Índice inválido.")
        elif subop == "6":
            desafios = executar_crud('social', 'listar')
            if not desafios:
                print("Nenhum desafio para atualizar.")
            else:
                for idx, d in enumerate(desafios, 1):
                    print(f"{idx}. {d.nome} ({d.data_inicio} - {d.data_fim})")
                idx = int(input("Digite o número do desafio para atualizar: ")) - 1
                if 0 <= idx < len(desafios):
                    desafio = desafios[idx]
                    print("Deixe em branco para manter o valor atual.")
                    novo_nome = input(f"Novo nome (atual: {desafio.nome}): ") or desafio.nome
                    nova_descricao = input(f"Nova descrição (atual: {desafio.descricao}): ") or desafio.descricao
                    nova_data_inicio = input(f"Nova data início (DD-MM-YYYY) (atual: {desafio.data_inicio}): ") or desafio.data_inicio
                    nova_data_fim = input(f"Nova data fim (DD-MM-YYYY) (atual: {desafio.data_fim}): ") or desafio.data_fim
                    executar_crud('social', 'atualizar', id=desafio.id, dados={
                        "nome": novo_nome,
                        "descricao": nova_descricao,
                        "data_inicio": nova_data_inicio,
                        "data_fim": nova_data_fim
                    })
                    print("Desafio atualizado!")
                else:
                    print("Índice inválido.")
        elif subop == "7":
            desafios = executar_crud('social', 'listar')
            if not desafios:
                print("Nenhum desafio para deletar.")
            else:
                for idx, d in enumerate(desafios, 1):
                    print(f"{idx}. {d.nome}")
                idx = int(input("Digite o número do desafio para deletar: ")) - 1
                if 0 <= idx < len(desafios):
                    executar_crud('social', 'deletar', id=desafios[idx].id)
                    print("Desafio deletado!")
                else:
                    print("Índice inválido.")
        elif subop == "0":
            break
        else:
            print("Opção inválida.")


def gerenciar_videos(usuario_logado):
    while True:
        subop = exibir_menu_videos()
        if subop == "1":
            termo = input("Digite o termo de busca: ")
            resultados = servico_video.pesquisar_videos(query=termo, max_results=10)
            if not resultados:
                print("Nenhum vídeo encontrado.")
            else:
                print("\n--- Resultados da Busca ---")
                for idx, v in enumerate(resultados, 1):
                    print(f"{idx}. {v.titulo}")
                    print(f"   URL: {v.url}")
                servico_video._ultimos_resultados = resultados
        elif subop == "2":
            favoritos = executar_crud('video', 'listar', usuario_email=usuario_logado.email)
            if not favoritos:
                print("Nenhum vídeo favorito salvo.")
            else:
                print("\n--- Vídeos Favoritos ---")
                for idx, v in enumerate(favoritos, 1):
                    print(f"{idx}. {v.titulo}")
                    print(f"   URL: {v.url}")
        elif subop == "3":
            ultimos = getattr(servico_video, '_ultimos_resultados', None)
            if not ultimos:
                print("Faça uma busca primeiro!")
                continue
            for idx, v in enumerate(ultimos, 1):
                print(f"{idx}. {v.titulo}")
            idx = input("Digite o número do vídeo para favoritar: ")
            try:
                idx = int(idx) - 1
                if 0 <= idx < len(ultimos):
                    executar_crud('video', 'criar', video_data=ultimos[idx], usuario_email=usuario_logado.email)
                    print("Vídeo favoritado!")
                else:
                    print("Índice inválido.")
            except Exception as e:
                print(f"Entrada inválida: {e}")
        elif subop == "4":
            favoritos = executar_crud('video', 'listar', usuario_email=usuario_logado.email)
            if not favoritos:
                print("Nenhum vídeo favorito salvo.")
                continue
            for idx, v in enumerate(favoritos, 1):
                print(f"{idx}. {v.titulo}")
            idx = input("Digite o número do vídeo para deletar: ")
            try:
                idx = int(idx) - 1
                if 0 <= idx < len(favoritos):
                    executar_crud('video', 'deletar', id=favoritos[idx].id)
                    print("Vídeo deletado!")
                else:
                    print("Índice inválido.")
            except Exception as e:
                print(f"Entrada inválida: {e}")
        elif subop == "0":
            break
        else:
            print("Opção inválida.")


def gerenciar_recomendacoes(usuario_logado, auth: ServicoAutenticacao):
    preferencias_usuario = servico_recomendacao.map_preferencias_usuario(usuario_logado)
    
    while True:
        subop = exibir_menu_recomendacoes()
        
        if subop == "1":
            treinos = servico_recomendacao.recomendar_treinos_sugestoes(preferencia_usuario=preferencias_usuario)
            if not treinos:
                print("Nenhuma recomendação de treino encontrada para suas preferências.")
            else:
                print("\n--- Recomendações de Treino ---")
                for idx, rec in enumerate(treinos, 1):
                    dados = rec.conteudo
                    print(f"\n{idx}. {dados.get('nome', '-')}")
                    print(f"   Nível: {dados.get('nivel', '-')}")
                    print(f"   Objetivo: {dados.get('objetivo', '-')}")
                    print("   Exercícios:")
                    for ex in dados.get('exercicios', []):
                        if isinstance(ex, dict):
                            print(f"      - [{ex.get('grupo', '-')}] {ex.get('exercicio', '-')}: {ex.get('series', '-')}x{ex.get('repeticoes', '-')}")
                        else:
                            print(f"      - {ex}")

        elif subop == "2":
            alimentos = servico_recomendacao.recomendar_alimentos_sugestoes(preferencia_usuario=preferencias_usuario)
            if not alimentos:
                print("Nenhuma recomendação de alimento encontrada para suas preferências.")
            else:
                print("\n--- Recomendações de Nutrição ---")
                for idx, rec in enumerate(alimentos, 1):
                    dados = rec.conteudo
                    print(f"\n{idx}. {dados.get('nome_refeicao', '-')}:")
                    for item in dados.get("itens", []):
                        print(f"   - {item.get('alimento', '-')}: {item.get('calorias', '-')} kcal | Prot: {item.get('proteina', '-')}g | Gord: {item.get('gordura', '-')}g | Carb: {item.get('carboidrato', '-')}g")

        elif subop == "3":
            diretrizes = servico_recomendacao.recomendar_diretrizes_gerais(preferencia_usuario=preferencias_usuario)
            if not diretrizes:
                print("Nenhuma diretriz geral encontrada.")
            else:
                print("\n--- Diretrizes Gerais ---")
                for idx, rec in enumerate(diretrizes, 1):
                    print(f"{idx}. {rec.conteudo.get('descricao', '-')}")

        elif subop == "4":
            grupos = servico_recomendacao.recomendar_grupos_musculares(preferencia_usuario=preferencias_usuario)
            if not grupos:
                print("Nenhuma recomendação de grupo muscular encontrada.")
            else:
                print("\n--- Recomendações de Grupos Musculares ---")
                for idx, rec in enumerate(grupos, 1):
                    dados = rec.conteudo
                    print(f"\n{idx}. Grupo: {dados.get('nome_grupo', '-')}")
                    for ex in dados.get('exercicios', []):
                        print(f"   - {ex.get('exercicio', '-')}: {ex.get('series', '-')}x{ex.get('repeticoes', '-')}")

        elif subop == "5":
            mobilidade = servico_recomendacao.recomendar_mobilidade(preferencia_usuario=preferencias_usuario)
            if not mobilidade:
                print("Nenhuma recomendação de mobilidade encontrada.")
            else:
                print("\n--- Recomendações de Mobilidade ---")
                for idx, rec in enumerate(mobilidade, 1):
                    print(f"{idx}. {rec.conteudo.get('descricao', '-')}")

        elif subop == "6":
            divisoes = servico_recomendacao.recomendar_divisoes_semanais(preferencia_usuario=preferencias_usuario)
            if not divisoes:
                print("Nenhuma recomendação de divisão semanal encontrada.")
            else:
                print("\n--- Divisões Semanais Sugeridas ---")
                for idx, rec in enumerate(divisoes, 1):
                    print(f"{idx}. {rec.conteudo.get('descricao', '-')}")

        elif subop == "7":
            progressao = servico_recomendacao.recomendar_progressao(preferencia_usuario=preferencias_usuario)
            if not progressao:
                print("Nenhuma recomendação de progressão encontrada.")
            else:
                print("\n--- Recomendações de Progressão de Carga ---")
                for idx, rec in enumerate(progressao, 1):
                    print(f"{idx}. {rec.conteudo.get('descricao', '-')}")

        elif subop == "8":
            consideracoes = servico_recomendacao.recomendar_consideracoes_finais(preferencia_usuario=preferencias_usuario)
            if not consideracoes:
                print("Nenhuma consideração final encontrada.")
            else:
                print("\n--- Considerações Finais ---")
                for idx, rec in enumerate(consideracoes, 1):
                    print(f"{idx}. {rec.conteudo.get('descricao', '-')}")

        elif subop == "9":
            print("\n--- Atualizar Preferências ---")
            print("Deixe o campo em branco para manter o valor atual.")

            try:
                novo_peso_str = input(f"Novo Peso (kg) (atual: {usuario_logado.peso}): ")
                if novo_peso_str:
                    usuario_logado.peso = float(novo_peso_str)

                nova_altura_str = input(f"Nova Altura (cm) (atual: {usuario_logado.altura}): ")
                if nova_altura_str:
                    usuario_logado.altura = float(nova_altura_str)
            except ValueError:
                print("Peso e altura devem ser números positivos. Tente novamente.")
                return

            print(f"\nNível de Atividade atual: {usuario_logado.nivel_atividade}")
            print("1. Sedentário, 2. Moderado, 3. Ativo")
            nivel_op = input("Escolha uma nova opção (ou deixe em branco): ")
            if nivel_op == "1": usuario_logado.nivel_atividade = "Sedentário"
            elif nivel_op == "2": usuario_logado.nivel_atividade = "Moderado"
            elif nivel_op == "3": usuario_logado.nivel_atividade = "Ativo"

            print(f"\nObjetivo atual: {usuario_logado.objetivo}")
            print("1. Emagrecimento, 2. Hipertrofia, 3. Força, 4. Resistência, 5. Mobilidade")
            objetivo_op = input("Escolha uma nova opção (ou deixe em branco): ")
            if objetivo_op == "1": usuario_logado.objetivo = "Emagrecimento"
            elif objetivo_op == "2": usuario_logado.objetivo = "Hipertrofia"
            elif objetivo_op == "3": usuario_logado.objetivo = "Força"
            elif objetivo_op == "4": usuario_logado.objetivo = "Resistência"
            elif objetivo_op == "5": usuario_logado.objetivo = "Mobilidade"

            print(f"\nFrequência de Treino atual: {usuario_logado.frequencia_treino}")
            print("1. 1x, 2. 2x, 3. 3x, 4. 4x, 5. 5x por semana")
            frequencia_op = input("Escolha uma nova opção (ou deixe em branco): ")
            if frequencia_op == "1": usuario_logado.frequencia_treino = "1x por semana"
            elif frequencia_op == "2": usuario_logado.frequencia_treino = "2x por semana"
            elif frequencia_op == "3": usuario_logado.frequencia_treino = "3x por semana"
            elif frequencia_op == "4": usuario_logado.frequencia_treino = "4x por semana"
            elif frequencia_op == "5": usuario_logado.frequencia_treino = "5x por semana"

            print(f"\nRestrições de Treino atuais: {', '.join(usuario_logado.restricoes_treino)}")
            print("1. Nenhuma, 2. Joelho, 3. Ombro, 4. Coluna")
            restricao_op = input("Escolha novas opções (separadas por vírgula, ou deixe em branco): ")
            if restricao_op:
                restricao_dict = {"1": "nenhuma", "2": "joelho", "3": "ombro", "4": "coluna"}
                restricoes_treino = [restricao_dict[op.strip()] for op in restricao_op.split(',') if op.strip() in restricao_dict]
                if "nenhuma" in restricoes_treino:
                    usuario_logado.restricoes_treino = ["nenhuma"]
                else:
                    usuario_logado.restricoes_treino = [r for r in restricoes_treino if r != "nenhuma"]

            print(f"\nRestrições Alimentares atuais: {', '.join(usuario_logado.restricao_dieta)}")
            print("1. Nenhuma, 2. Lactose, 3. Glúten, 4. Diabetes")
            restricao_dieta_op = input("Escolha novas opções (separadas por vírgula, ou deixe em branco): ")
            if restricao_dieta_op:
                restricao_dieta_dict = {"1": "nenhuma", "2": "lactose", "3": "glúten", "4": "diabetes"}
                restricoes_dieta = [restricao_dieta_dict[op.strip()] for op in restricao_dieta_op.split(',') if op.strip() in restricao_dieta_dict]
                if "nenhuma" in restricoes_dieta:
                    usuario_logado.restricao_dieta = ["nenhuma"]
                else:
                    usuario_logado.restricao_dieta = [r for r in restricoes_dieta if r != "nenhuma"]

            auth.atualizar_usuario(usuario_logado.email, usuario_logado.to_dict())
            preferencias_usuario = servico_recomendacao.map_preferencias_usuario(usuario_logado)
            print("\nPreferências atualizadas com sucesso!")

        elif subop == "0":
            break                
        else:
            print("Opção inválida.")


def gerenciar_feedback(usuario_logado):
    while True:
        subop = exibir_menu_feedback()
        if subop == "1":
            texto = input("Digite seu feedback: ")
            while True:
                try:
                    nota = int(input("Dê uma nota de 1 a 5: "))
                    if 1 <= nota <= 5:
                        break
                    else:
                        print("Nota inválida. Deve ser número inteiro entre 1 e 5.")
                except ValueError:
                    print("Entrada inválida. Digite um número inteiro entre 1 e 5.")
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                executar_crud('feedback', 'criar', usuario_email=usuario_logado.email, texto=texto, nota=nota, data=data_atual)
                print("Feedback enviado! Agradecemos pelo seu feedback!")
            except ValueError:
                print("Erro ao enviar feedback.")
        elif subop == "2":
            feedbacks = executar_crud('feedback', 'listar', usuario_email=usuario_logado.email) 
            if not feedbacks:
                print("Nenhum feedback encontrado.")
            else:
                for idx, f in enumerate(feedbacks, 1):
                    print(f"{idx}. (Nota: {f.nota}) (Data: {f.data})")
                    print(f" Texto: {f.texto}")
        elif subop == "3":
            meus_feedbacks = executar_crud('feedback', 'listar', usuario_email=usuario_logado.email)
            if not meus_feedbacks:
                print("Você não enviou nenhum feedback ainda.")
            else:
                print("\n--- Seus Feedbacks ---")
                for idx, f in enumerate(meus_feedbacks, 1):
                    print(f"{idx}. (Nota: {f.nota}) (Data: {f.data})")
                    print(f" Texto: {f.texto}")

                try:
                    idx_delete = int(input("Digite o número do feedback para deletar: (0 para cancelar) "))
                    if idx_delete == 0:
                        continue
                    if 1 <= idx_delete <= len(meus_feedbacks):
                        executar_crud('feedback', 'deletar', id=meus_feedbacks[idx_delete - 1].id)
                        print("Feedback deletado!")
                    else:
                        print("Índice inválido.")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número.")

        elif subop == "4":
            meus_feedbacks = executar_crud('feedback', 'listar', usuario_email=usuario_logado.email)
            if not meus_feedbacks:
                print("Você não enviou nenhum feedback ainda.")
            else:
                print("\n--- Seus Feedbacks ---")
                for idx, f in enumerate(meus_feedbacks, 1):
                    print(f"{idx}. (Nota: {f.nota}) (Data: {f.data})")
                    print(f" Texto: {f.texto}")

                try:
                    idx_update = int(input("Digite o número do feedback para atualizar: (0 para cancelar) "))
                    if idx_update == 0:
                        continue
                    if 1 <= idx_update <= len(meus_feedbacks):
                        feedback_selecionado = meus_feedbacks[idx_update - 1]
                        novo_texto = input(f"Novo texto (deixe em branco para manter): ")
                        novo_nota_str = input(f"Nova nota (1-5) (deixe em branco para manter): ")
                        novo_nota = feedback_selecionado.nota
                        if novo_nota_str:
                            try:
                                novo_nota = int(novo_nota_str)
                                if not (1 <= novo_nota <= 5):
                                    print("Nota inválida. Deve ser um número inteiro entre 1 e 5.")
                                    continue
                            except ValueError:
                                print("Entrada inválida. Digite um número inteiro entre 1 e 5.")
                                continue
                        dados_atualizados = {
                            "texto": novo_texto if novo_texto else feedback_selecionado.texto,
                            "nota": novo_nota
                        }
                        try:
                            resultado = executar_crud('feedback', 'atualizar', id=feedback_selecionado.id, dados=dados_atualizados)
                            if resultado is None:
                                print("Erro ao atualizar feedback. Verifique os dados e tente novamente.")
                            elif resultado is False:
                                print("Atualização não realizada.")
                            else:
                                print("Feedback atualizado!")
                        except ValueError as e:
                            print(f"Erro ao atualizar feedback: {e}")
                    else:
                        print("Índice inválido.")
                except Exception as e:
                    print(f"Erro inesperado ao atualizar feedback: {e}")
        elif subop == "0":
            break
        else:
            print("Opção inválida.")


def gerenciar_forum(usuario_logado):
    while True:
        subop = exibir_menu_forum()
        if subop == "1":
            titulo = input("Digite o Título do Post:")
            mensagem = input("Digite o Conteúdo do Post:")
            data_post = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            executar_crud('forum', 'criar', usuario_email=usuario_logado.email, titulo=titulo, mensagem=mensagem, data=data_post)
            print("Post criado com sucesso!")
        elif subop == "2":
            posts = servico_forum.listar_posts()
            if not posts:
                print("Nenhum post encontrado.")
            else:
                for idx, p in enumerate(posts, 1):
                    print(f"{idx}. {p.titulo} (Autor: {p.usuario_email})")
        elif subop == "3":
            posts = servico_forum.listar_posts()
            if not posts:
                print("Nenhum post para comentar.")
            else:
                for idx, p in enumerate(posts, 1):
                    print(f"{idx}. {p.titulo}")
                idx_post = int(input("Escolha o post para comentar: ")) - 1
                if 0 <= idx_post < len(posts):
                    mensagem = input("Digite seu comentário: ")
                    data_comentario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    servico_forum.comentar_post(post_id=posts[idx_post].id, usuario_email=usuario_logado.email, mensagem=mensagem, data=data_comentario)
                    print("Comentário adicionado!")
                else:
                    print("Índice inválido.")
        elif subop == "4":
            posts = servico_forum.listar_posts()
            if not posts:
                print("Nenhum post para ver comentários.")
            else:
                for idx, p in enumerate(posts, 1):
                    print(f"{idx}. {p.titulo}")
                idx_post = int(input("Escolha o post para ver os comentários: ")) - 1
                if 0 <= idx_post < len(posts):
                    comentarios = servico_forum.listar_comentarios(post_id=posts[idx_post].id)
                    if not comentarios:
                        print("Nenhum comentário neste post.")
                    else:
                        for c in comentarios:
                            print(c.exibir())
                else:
                    print("Índice inválido.")
        elif subop == "5":
            conteudos = executar_crud('forum', 'listar')
            if not conteudos:
                print("Nenhum conteúdo no fórum.")
            else:
                for c in conteudos:
                    print(c.exibir())
        elif subop == "6":
            conteudos = executar_crud('forum', 'listar', usuario_email=usuario_logado.email)
            if not conteudos:
                print("Você não tem nenhum conteúdo no fórum.")
            else:
                for c in conteudos:
                    print(c.exibir())
        elif subop == "7":
            posts = servico_forum.listar_posts(usuario_email=usuario_logado.email)
            if not posts:
                print("Você não tem posts para deletar.")
            else:
                for idx, p in enumerate(posts, 1):
                    print(f"{idx}. {p.titulo}")
                idx_del = int(input("Escolha o post para deletar: ")) - 1
                if 0 <= idx_del < len(posts):
                    executar_crud('forum', 'deletar', id=posts[idx_del].id)
                    print("Post deletado.")
                else:
                    print("Índice inválido.")

        elif subop == "8":
            comentarios = servico_forum.listar_comentarios(usuario_email=usuario_logado.email)
            if not comentarios:
                print("Você não tem comentários para deletar.")
            else:
                for idx, c in enumerate(comentarios, 1):
                    print(f"{idx}. {c.mensagem}")
                idx_del = int(input("Escolha o comentario para deletar: ")) - 1
                if 0 <= idx_del < len(comentarios):
                    executar_crud('forum', 'deletar', id=comentarios[idx_del].id)
                    print("Comentario deletado.")
                else:
                    print("Índice inválido.")

        elif subop == "9":
            posts = servico_forum.listar_posts(usuario_email=usuario_logado.email)
            if not posts:
                print("Você não tem posts para atualizar.")
            else:
                for idx, p in enumerate(posts, 1):
                    print(f"{idx}. {p.titulo}")
                try:
                    idx_atualizar = int(input("Escolha o post para atualizar: ")) - 1
                    if 0 <= idx_atualizar < len(posts):
                        post_selecionado = posts[idx_atualizar]
                        
                        print("Deixe em branco para manter o valor atual.")
                        novo_titulo = input(f"Novo título (atual: {post_selecionado.titulo}): ")
                        nova_mensagem = input(f"Nova mensagem (atual: {post_selecionado.mensagem}): ")
                        
                        dados_atualizados = {}
                        if novo_titulo:
                            dados_atualizados["titulo"] = novo_titulo
                        if nova_mensagem:
                            dados_atualizados["mensagem"] = nova_mensagem
                            
                        if dados_atualizados:
                            resultado = executar_crud('forum', 'atualizar', 
                                id=post_selecionado.id, 
                                dados=dados_atualizados
                            )
                            if resultado:
                                print("Post atualizado com sucesso!")
                            else:
                                print("Erro ao atualizar post.")
                        else:
                            print("Nenhuma alteração feita.")
                    else:
                        print("Índice inválido.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")
                except Exception as e:
                    print(f"Erro inesperado: {e}")

        elif subop == "10":
           comentarios = servico_forum.listar_comentarios(usuario_email=usuario_logado.email)
           if not comentarios:
               print("Você não tem comentários para atualizar.")
           else:
               for idx, c in enumerate(comentarios, 1):
                   print(f"{idx}. {c.mensagem}")
               try:
                   idx_atualizar = int(input("Escolha o comentário para atualizar: ")) - 1
                   if 0 <= idx_atualizar < len(comentarios):
                       comentario_selecionado = comentarios[idx_atualizar]
                       nova_mensagem = input(f"Nova mensagem (atual: {comentario_selecionado.mensagem}): ")
                       
                       if nova_mensagem:
                           dados_atualizados = {"mensagem": nova_mensagem}
                           resultado = executar_crud('forum', 'atualizar', 
                               id=comentario_selecionado.id, 
                               dados=dados_atualizados
                           )
                           if resultado:
                               print("Comentário atualizado com sucesso!")
                           else:
                               print("Erro ao atualizar comentário.")
                       else:
                           print("Nenhuma alteração feita.")
                   else:
                       print("Índice inválido.")
               except ValueError:
                   print("Entrada inválida. Digite um número.")
               except Exception as e:
                   print(f"Erro inesperado: {e}")
        elif subop == "0":
            break
        else:
            print("Opção inválida.")