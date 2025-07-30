from fitness_app.core.auth import ServicoAutenticacao
from fitness_app.services.workout import ServicoTreino
from fitness_app.services.activity import ServicoAtividade
from fitness_app.services.nutrition import ServicoNutricional
from fitness_app.services.goal import ServicoMeta
from fitness_app.services.wearable import ServicoWearable
from fitness_app.services.social import ServicoSocial
from fitness_app.core.database import db
from fitness_app.core.models import Usuario, Atividade, RegistroNutricional, Meta
from tinydb import Query
from fitness_app.services.recommendation import ServicoRecomendacao
from fitness_app.services.video import ServicoVideo
from fitness_app.services.feedback import ServicoFeedback
from fitness_app.services.forum import ServicoForum
from datetime import datetime
from difflib import get_close_matches


def menu_principal():
    print("=== Fitness App ===")
    print("1. Login")
    print("2. Registrar Usuário")
    print("0. Sair")
    return input("Escolha uma opção: ")

def menu_usuario():
    print("\n--- Menu do Usuário ---")
    print("1. Planos de Treino")
    print("2. Atividades")
    print("3. Nutrição")
    print("4. Metas")
    print("5. Wearable")
    print("6. Social/Desafios")
    print("7. Vídeos")
    print("8. Recomendações")
    print("9. Feedback")
    print("10. Fórum")
    print("0. Logout")
    return input("Escolha uma opção: ")



def main():
    auth = ServicoAutenticacao()
    treino = ServicoTreino()
    atividade = ServicoAtividade()
    nutricional = ServicoNutricional()
    meta = ServicoMeta()
    wearable = ServicoWearable()
    social = ServicoSocial()
    video = ServicoVideo()
    recomendacao = ServicoRecomendacao()
    feedback = ServicoFeedback()
    forum = ServicoForum()


    usuario_logado = None

    while True:
        if not usuario_logado:
            op = menu_principal()
            if op == "1":
                email = input("E-mail: ")
                senha = input("Senha: ")
                usuario_logado = auth.autenticar_usuario(email, senha)
                if usuario_logado:
                    print("Login realizado com sucesso!")
                    print(f"Bem-vindo, {usuario_logado.nome}!")
                    mapa_nivel = {
                        "Sedentário": "Iniciante",
                        "Moderado": "Intermediário",
                        "Ativo": "Avançado"
                    }
                    preferencias_usuario = {
                        "nivel": mapa_nivel[usuario_logado.nivel_atividade],
                        "objetivo": usuario_logado.objetivo,
                        "frequencia_treino": usuario_logado.frequencia_treino,
                        "restricao_dieta": usuario_logado.restricao_dieta,
                        "restricoes_treino": usuario_logado.restricoes_treino
                    }
                else:
                    print("Usuário ou senha inválidos.")
            elif op == "2":
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
                    print("Restrições de Treino:")
                    print("1. Nenhuma")
                    print("2. Joelho")
                    print("3. Ombro")
                    print("4. Coluna")
                    restricao_op = input("Escolha uma opção (1-4): ")
                    restricao_dict = {
                        "1": "Nenhuma",
                        "2": "Joelho",
                        "3": "Coluna",
                        "4": "Ombro",
                        "5": "Outras"
                 }
                    if restricao_op in restricao_dict:
                        restricoes_treino = restricao_dict[restricao_op]
                        break
                    print("Opção inválida! Por favor, escolha entre 1 e 4.")
                while True:
                    print("Restrições Alimentares:")
                    print("1. Nenhuma")
                    print("2. Lactose")
                    print("3. Glúten")
                    print("4. Diabetes")
                    restricao_dieta_op = input("Escolha uma opção (1-4): ")
                    restricao_dieta_dict = {
                        "1": "Nenhuma",
                        "2": "Lactose",
                        "3": "Glúten",
                        "4": "Diabetes",
                        "5": "Outras"
                    }
                    if restricao_dieta_op in restricao_dieta_dict:
                        restricao_dieta = restricao_dieta_dict[restricao_dieta_op]
                        break
                    print("Opção inválida! Por favor, escolha entre 1 e 4.")
                usuario = Usuario(
                nome, email, senha, genero, idade, peso, altura,
                nivel_atividade, objetivo,
                frequencia_treino, restricoes_treino, restricao_dieta, dados_wearable=None,
                perfil_completo=False,
                )
                try:
                    auth.registrar_usuario(usuario)
                    print("Usuário registrado com sucesso!")
                except Exception as e:
                    print(f"Erro ao registrar: {e}")
            elif op == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")
        else:
            op = menu_usuario()
            if op == "1":
                while True:
                    print("\n--- Planos de Treino ---")
                    print("1. Listar planos")
                    print("2. Criar plano")
                    print("3. Deletar plano")
                    print("4. Associar vídeo favorito a um plano")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")
                    if subop == "1":
                        planos = treino.listar_planos_usuario(usuario_logado.email)
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
                            tabela = db.table('treinos_prontos')
                            treinos_prontos = tabela.all()
                            print("\n--- Planos Pré-Prontos Disponíveis ---")
                            for idx, t in enumerate(treinos_prontos, 1):
                                print(f"{idx}. {t['nome']} ({t['nivel']}, objetivo: {t['objetivo']})")
                            idx_treino = int(input("Digite o número do plano para adicionar: ")) - 1
                            if 0 <= idx_treino < len(treinos_prontos):
                                plano = treinos_prontos[idx_treino]
                                treino.criar_plano_personalizado(
                                    usuario_email=usuario_logado.email,
                                    nome=plano['nome'],
                                    exercicios=plano['exercicios'],
                                    objetivo=plano['objetivo'],
                                    nivel=plano['nivel']
                                )
                                print("Plano pré-pronto adicionado!")
                            else:
                                print("Índice inválido.")
                        elif tipo_plano == "2":
                            nome = input("Nome do plano: ")
                            objetivo = input("Objetivo: ")
                            nivel = input("Nível: ")
                            exercicios = input("Exercícios (separados por vírgula): ").split(",")
                            treino.criar_plano_personalizado(
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
                        planos = treino.listar_planos_usuario(usuario_logado.email)
                        for idx, p in enumerate(planos, 1):
                            print(f"{idx}. {p.nome} ({p.nivel})")
                        idx = int(input("Digite o número do plano para deletar: ")) - 1
                        if 0 <= idx < len(planos):
                            tabela = db.table('planos_treino')
                            plano = planos[idx]
                            Plano = Query()
                            result = tabela.search(
                                (Plano.nome == plano.nome) &
                                (Plano.nivel == plano.nivel) &
                                (Plano.usuario_email == usuario_logado.email)
                            )
                            if result:
                                doc_id = result[0].doc_id
                                treino.deletar_plano(doc_id)
                                print("Plano deletado!")
                            else:
                                print("Não foi possível encontrar o plano no banco de dados.")
                        else:
                            print("Índice inválido.")
                    elif subop == "4":
                        planos = treino.listar_planos_usuario(usuario_logado.email)
                        if not planos:
                            print("Nenhum plano cadastrado.")
                            continue
                        for idx, p in enumerate(planos, 1):
                            print(f"{idx}. {p.nome} ({p.nivel})")
                        idx_plano = input("Digite o número do plano para associar vídeo: ")
                        try:
                            idx_plano = int(idx_plano) - 1
                            if 0 <= idx_plano < len(planos):
                                favoritos = video.listar_videos(usuario_logado.email)
                                if not favoritos:
                                    print("Nenhum vídeo favorito salvo.")
                                    continue
                                for idx, v in enumerate(favoritos, 1):
                                    print(f"{idx}. {v.titulo}")
                                idx_video = input("Digite o número do vídeo para associar: ")
                                idx_video = int(idx_video) - 1
                                if 0 <= idx_video < len(favoritos):
                                    tabela = db.table('planos_treino')
                                    plano = planos[idx_plano]
                                    Plano = Query()
                                    result = tabela.search(
                                        (Plano.nome == plano.nome) &
                                        (Plano.nivel == plano.nivel) &
                                        (Plano.usuario_email == usuario_logado.email)
                                    )
                                    if result:
                                        doc_id = result[0].doc_id
                                        plano_dict = result[0].copy()
                                        if 'videos' not in plano_dict or not isinstance(plano_dict['videos'], list):
                                            plano_dict['videos'] = []

                                        video_info = {
                                            'titulo': favoritos[idx_video].titulo,
                                            'url': favoritos[idx_video].url,
                                            'duracao': favoritos[idx_video].duracao,
                                            'data_publicacao': favoritos[idx_video].data_publicacao,
                                            'descricao': favoritos[idx_video].descricao,
                                            'thumbnail': favoritos[idx_video].thumbnail
                                        }
                                        if video_info not in plano_dict['videos']:
                                            plano_dict['videos'].append(video_info)
                                            tabela.update({'videos': plano_dict['videos']}, doc_ids=[doc_id])
                                            print("Vídeo associado ao plano!")
                                        else:
                                            print("Este vídeo já está associado ao plano.")
                                    else:
                                        print("Não foi possível encontrar o plano no banco de dados.")
                                else:
                                    print("Índice de vídeo inválido.")
                            else:
                                print("Índice de plano inválido.")
                        except Exception:
                            print("Entrada inválida.")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")
            elif op == "2":
                while True:
                    print("\n--- Atividades ---")
                    print("1. Listar atividades")
                    print("2. Registrar atividade")
                    print("3. Deletar atividade")
                    print("4. Atualizar atividade")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")
                    if subop == "1":
                        atividades = atividade.listar_atividades_usuario(usuario_logado.email)
                        if not atividades:
                            print("Nenhuma atividade registrada.")
                        else:
                            for idx, a in enumerate(atividades, 1):
                                print(f"{idx}. {a.tipo} em {a.data} ({a.calorias} kcal)")
                    elif subop == "2":
                        tipo = input("Tipo de atividade: ")
                        data = input("Data (DD-MM-YYYY): ")
                        duracao = input("Duração (min): ")
                        calorias = input("Calorias gastas (deixe vazio para calcular automaticamente): ")
                        passos = input("Passos (opcional): ")
                        calorias_val = calorias if calorias else None
                        nova = Atividade(
                            usuario_email=usuario_logado.email,
                            tipo=tipo,
                            data=data,
                            duracao=duracao,
                            calorias=calorias_val,
                            passos=passos if passos else None
                        )
                        atividade.registrar_atividade(nova, usuario=usuario_logado)
                        print("Atividade registrada!")
                    elif subop == "3":
                        atividades = atividade.listar_atividades_usuario(usuario_logado.email)
                        for idx, a in enumerate(atividades, 1):
                            print(f"{idx}. {a.tipo} em {a.data} ({a.calorias} kcal)")
                        idx = int(input("Digite o número da atividade para deletar: ")) - 1
                        if 0 <= idx < len(atividades):
                            tabela = db.table('atividades')
                            atividade_obj = atividades[idx]
                            Ativ = Query()
                            result = tabela.search(
                                (Ativ.usuario_email == atividade_obj.usuario_email) &
                                (Ativ.tipo == atividade_obj.tipo) &
                                (Ativ.data == atividade_obj.data) &
                                (Ativ.duracao == atividade_obj.duracao)
                            )
                            if result:
                                doc_id = result[0].doc_id
                                atividade.deletar_atividade(doc_id)
                                print("Atividade deletada!")
                            else:
                                print("Não foi possível encontrar a atividade no banco de dados.")
                        else:
                            print("Índice inválido.")
                    elif subop == "4":
                        atividades = atividade.listar_atividades_usuario(usuario_logado.email)
                        if not atividades:
                            print("Nenhuma atividade registrada.")
                        else:
                            for idx, a in enumerate(atividades, 1):
                                print(f"{idx}. {a.tipo} em {a.data} ({a.calorias} kcal)")
                            idx = int(input("Digite o número da atividade para atualizar: ")) - 1
                            if 0 <= idx < len(atividades):
                                tabela = db.table('atividades')
                                atividade_obj = atividades[idx]
                                Ativ = Query()
                                result = tabela.search(
                                    (Ativ.usuario_email == atividade_obj.usuario_email) &
                                    (Ativ.tipo == atividade_obj.tipo) &
                                    (Ativ.data == atividade_obj.data) &
                                    (Ativ.duracao == atividade_obj.duracao)
                                )
                                if result:
                                    doc_id = result[0].doc_id
                                    print("Deixe em branco para manter o valor atual.")
                                    novo_tipo = input(f"Novo tipo de atividade (atual: {atividade_obj.tipo}): ") or atividade_obj.tipo
                                    nova_data = input(f"Nova data (atual: {atividade_obj.data}): ") or atividade_obj.data
                                    nova_duracao = input(f"Nova duração (min) (atual: {atividade_obj.duracao}): ") or atividade_obj.duracao
                                    novas_calorias = input(f"Novas calorias gastas (atual: {atividade_obj.calorias}): ") or atividade_obj.calorias
                                    novos_passos = input(f"Novos passos (atual: {atividade_obj.passos}): ") or atividade_obj.passos
                                    novos_dados = {
                                        "tipo": novo_tipo,
                                        "data": nova_data,
                                        "duracao": nova_duracao,
                                        "calorias": novas_calorias,
                                        "passos": novos_passos
                                    }
                                    atividade.atualizar_atividade(doc_id, novos_dados)
                                    print("Atividade atualizada!")
                                else:
                                    print("Não foi possível encontrar a atividade no banco de dados.")
                            else:
                                print("Índice inválido.")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")
            elif op == "3":
                while True:
                    print("\n--- Nutrição ---")
                    print("1. Listar registros")
                    print("2. Registrar refeição")
                    print("3. Deletar registro")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")
                    if subop == "1":
                        registros = nutricional.listar_registros_usuario(usuario_logado.email)
                        if not registros:
                            print("Nenhum registro encontrado.")
                        else:
                            for idx, r in enumerate(registros, 1):
                                if not isinstance(r, RegistroNutricional):
                                    r = RegistroNutricional(
                                        usuario_email=r.get('usuario_email', usuario_logado.email),
                                        data=r.get('data', '-'),
                                        alimentos=r.get('alimentos', []),
                                        calorias=r.get('calorias', 0),
                                        id=r.get('id', None)
                                    )
                                print(f"{idx}. {r.data}: {r.calorias} kcal")
                    elif subop == "2":
                        data = input("Data (DD-MM-YYYY): ")
                        nomes_alimentos = nutricional.listar_todos_alimentos()
                        if nomes_alimentos:
                            print("\nAlimentos disponíveis no banco de dados:")
                            for idx, nome in enumerate(nomes_alimentos, 1):
                                print(f"{idx}. {nome}")
                        else:
                            print("Nenhum alimento cadastrado ainda.")

                        alimentos = []
                        while True:
                            nome_input = input("Digite o nome do alimento que deseja adicionar (ou 'fim' para terminar): ").strip()
                            if nome_input.lower() == 'fim':
                                break

                            alimento = nutricional.buscar_alimento(nome_input)
                            
                            if not alimento:
                                similares = get_close_matches(nome_input, nomes_alimentos, n=3, cutoff=0.6)
                                print(f"Alimento '{nome_input}' não encontrado.")
                                
                                if similares:
                                    print("Você quis dizer algum destes?")
                                    for i, s in enumerate(similares, 1):
                                        print(f"{i}. {s}")
                                    print(f"{len(similares) + 1}. Nenhum destes, cadastrar novo alimento")
                                    
                                    try:
                                        escolha = int(input(f"Escolha uma opção (1-{len(similares) + 1}): "))
                                        if 1 <= escolha <= len(similares):
                                            nome_escolhido = similares[escolha - 1]
                                            alimento = nutricional.buscar_alimento(nome_escolhido)
                                        elif escolha == len(similares) + 1:
                                            alimento = None 
                                        else:
                                            print("Opção inválida.")
                                            continue
                                    except (ValueError, IndexError):
                                        print("Opção inválida.")
                                        continue
                                
                                if not alimento: 
                                    print(f"Vamos cadastrar '{nome_input}'...")
                                    try:
                                        calorias = float(input(f"Calorias de '{nome_input}': "))
                                        proteina = float(input(f"Proteína (g) de '{nome_input}': "))
                                        gordura = float(input(f"Gordura (g) de '{nome_input}': "))
                                        carboidrato = float(input(f"Carboidrato (g) de '{nome_input}': "))
                                        
                                        nutricional.cadastrar_alimento(nome_input, calorias, proteina, gordura, carboidrato)
                                        print(f"Alimento '{nome_input}' cadastrado com sucesso!")
                                        alimento = nutricional.buscar_alimento(nome_input)
                                    except ValueError:
                                        print("Valores nutricionais inválidos. Tente novamente.")
                                        continue

                            # Se encontrou o alimento (seja direto ou após cadastro)
                            if alimento:
                                while True:
                                    try:
                                        quantidade = float(input(f"Quantidade de '{alimento['nome']}' (ex: 1 para unidade, 0.5 para meia): ") or 1)
                                        break
                                    except ValueError:
                                        print("Quantidade inválida. Digite um número.")
                                
                                alimentos.append({
                                    "alimento": alimento["nome"],
                                    "calorias": alimento["calorias"],
                                    "proteina": alimento["proteina"],
                                    "gordura": alimento["gordura"],
                                    "carboidrato": alimento["carboidrato"],
                                    "quantidade": quantidade
                                })
                                print(f"'{alimento['nome']}' adicionado à refeição.")

                        if not alimentos:
                            print("Nenhum alimento adicionado. Registro cancelado.")
                            continue

                        total_calorias = sum(a["calorias"] * a["quantidade"] for a in alimentos)
                        registro = RegistroNutricional(
                            usuario_email=usuario_logado.email,
                            data=data,
                            alimentos=alimentos,
                            calorias=total_calorias
                        )
                        try:
                            nutricional.registrar_refeicao(usuario_logado.email, data, alimentos, registro=registro)
                        except TypeError:
                            nutricional.registrar_refeicao(usuario_logado.email, data, alimentos)
                        print("Refeição registrada!")
                    elif subop == "3":
                        registros = nutricional.listar_registros_usuario(usuario_logado.email)
                        for idx, r in enumerate(registros, 1):
                            print(f"{idx}. {r.data}")
                        idx = int(input("Digite o número do registro para deletar: ")) - 1
                        if 0 <= idx < len(registros):
                            nutricional.deletar_registro(registros[idx].id)
                            print("Registro deletado!")
                        else:
                            print("Índice inválido.")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")
            elif op == "4":
                while True:
                    print("\n--- Metas ---")
                    print("1. Listar metas")
                    print("2. Criar meta")
                    print("3. Deletar meta")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")
                    if subop == "1":
                        metas = meta.listar_metas_usuario(usuario_logado.email)
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
                        nova = Meta(
                            usuario_email=usuario_logado.email,
                            tipo=tipo,
                            valor=valor,
                            data_inicio=data_inicio,
                            data_fim=data_fim
                        )
                        meta.criar_meta(
                            usuario_email=usuario_logado.email,
                            tipo=tipo,
                            valor=valor,
                            data_inicio=data_inicio,
                            data_fim=data_fim
                        )
                        print("Meta criada!")
                    elif subop == "3":
                        metas = meta.listar_metas_usuario(usuario_logado.email)
                        if not metas:
                            print("Nenhuma meta cadastrada.")
                        else:
                            for idx, m in enumerate(metas, 1):
                                print(f"{idx}. {m.tipo}: {m.valor}")
                            idx = int(input("Digite o número da meta para deletar: ")) - 1
                            if 0 <= idx < len(metas):
                                meta.deletar_meta(metas[idx].id)
                                print("Meta deletada!")
                            else:
                                print("Índice inválido.")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")
            elif op == "5":
                while True:
                    print("\n--- Wearable ---")
                    print("1. Listar dados")
                    print("2. Registrar dado manual")
                    print("3. Gerar dado aleatório")
                    print("4. Deletar dado")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")
                    if subop == "1":
                        dados = wearable.listar_dados_usuario(usuario_logado.email)
                        if not dados:
                            print("Nenhum dado registrado.")
                        else:
                            for idx, d in enumerate(dados, 1):
                                print(f"{idx}. {d.tipo} em {d.data}: {d.valor}")
                    elif subop == "2":
                        tipo = input("Tipo de dado (passos, batimentos, sono): ")
                        valor = input("Valor: ")
                        wearable.registrar_dado_manual(usuario_logado.email, tipo, valor)
                        print("Dado registrado!")
                    elif subop == "3":
                        tipo = input("Tipo de dado (passos, batimentos, sono): ")
                        wearable.gerar_dado_aleatorio(usuario_logado.email, tipo)
                        print("Dado aleatório gerado!")
                    elif subop == "4":
                        dados = wearable.listar_dados_usuario(usuario_logado.email)
                        for idx, d in enumerate(dados, 1):
                            print(f"{idx}. {d.tipo} em {d.data}")
                        idx = int(input("Digite o número do dado para deletar: ")) - 1
                        if 0 <= idx < len(dados):
                            wearable.deletar_dado(dados[idx].id)
                            print("Dado deletado!")
                        else:
                            print("Índice inválido.")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")
            elif op == "6":
                while True:
                    print("\n--- Social/Desafios ---")
                    print("1. Listar desafios")
                    print("2. Criar desafio")
                    print("3. Participar de desafio")
                    print("4. Deletar desafio")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")
                    if subop == "1":
                        desafios = social.listar_desafios()
                        if not desafios:
                            print("Nenhum desafio cadastrado.")
                        else:
                            for idx, d in enumerate(desafios, 1):
                                print(f"{idx}. {d.nome}: {d.descricao}")
                    elif subop == "2":
                        nome = input("Nome do desafio: ")
                        descricao = input("Descrição: ")
                        data_inicio = input("Data início (DD-MM-YYYY): ")
                        data_fim = input("Data fim (DD-MM-YYYY): ")
                        social.criar_desafio(nome, descricao, data_inicio, data_fim)
                        print("Desafio criado!")
                    elif subop == "3":
                        desafios = social.listar_desafios()
                        for idx, d in enumerate(desafios, 1):
                            print(f"{idx}. {d.nome}")
                        idx = int(input("Digite o número do desafio para participar: ")) - 1
                        if 0 <= idx < len(desafios):
                            social.participar_desafio(desafios[idx].id, usuario_logado.email)
                            print("Participação registrada!")
                        else:
                            print("Índice inválido.")
                    elif subop == "4":
                        desafios = social.listar_desafios()
                        for idx, d in enumerate(desafios, 1):
                            print(f"{idx}. {d.nome}")
                        idx = int(input("Digite o número do desafio para deletar: ")) - 1
                        if 0 <= idx < len(desafios):
                            social.deletar_desafio(desafios[idx].id)
                            print("Desafio deletado!")
                        else:
                            print("Índice inválido.")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")
            elif op == "7":
                while True:
                    print("\n--- Vídeos ---")
                    print("1. Pesquisar vídeos no YouTube")
                    print("2. Listar vídeos favoritos")
                    print("3. Salvar vídeo pesquisado como favorito")
                    print("4. Deletar vídeo favorito")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")
                    if subop == "1":
                        termo = input("Digite o termo de busca: ")
                        resultados = video.pesquisar_videos(termo, max_results=10)
                        if not resultados:
                            print("Nenhum vídeo encontrado.")
                        else:
                            print("\n--- Resultados da Busca ---")
                            for idx, v in enumerate(resultados, 1):
                                print(f"{idx}. {v.titulo}")
                                print(f"   URL: {v.url}")
                                print(f"   Duração: {v.duracao}")
                                print(f"   Publicado: {v.data_publicacao}")
                                print(f"   Descrição: {v.descricao}")
                                print(f"   Thumbnail: {v.thumbnail}")
                        # Armazena resultados na sessão para possível favoritar
                        video._ultimos_resultados = resultados
                    elif subop == "2":
                        favoritos = video.listar_videos(usuario_logado.email)
                        if not favoritos:
                            print("Nenhum vídeo favorito salvo.")
                        else:
                            print("\n--- Vídeos Favoritos ---")
                            for idx, v in enumerate(favoritos, 1):
                                print(f"{idx}. {v.titulo}")
                                print(f"   URL: {v.url}")
                                print(f"   Duração: {v.duracao}")
                                print(f"   Publicado: {v.data_publicacao}")
                                print(f"   Descrição: {v.descricao}")
                                print(f"   Thumbnail: {v.thumbnail}")
                    elif subop == "3":
                        # Favoritar vídeo pesquisado
                        ultimos = getattr(video, '_ultimos_resultados', None)
                        if not ultimos:
                            print("Faça uma busca primeiro!")
                            continue
                        for idx, v in enumerate(ultimos, 1):
                            print(f"{idx}. {v.titulo}")
                        idx = input("Digite o número do vídeo para favoritar: ")
                        try:
                            idx = int(idx) - 1
                            if 0 <= idx < len(ultimos):
                                video.registrar_video(ultimos[idx], usuario_logado.email)
                                print("Vídeo favoritado!")
                            else:
                                print("Índice inválido.")
                        except Exception:
                            print("Entrada inválida.")
                    elif subop == "4":
                        favoritos = video.listar_videos(usuario_logado.email)
                        if not favoritos:
                            print("Nenhum vídeo favorito salvo.")
                            continue
                        for idx, v in enumerate(favoritos, 1):
                            print(f"{idx}. {v.titulo}")
                        idx = input("Digite o número do vídeo para deletar: ")
                        try:
                            idx = int(idx) - 1
                            if 0 <= idx < len(favoritos):
                                doc_id = getattr(favoritos[idx], 'id', None) or getattr(favoritos[idx], 'doc_id', None)
                                if doc_id:
                                    video.deletar_video(doc_id)
                                    print("Vídeo deletado!")
                                else:
                                    print("Não foi possível encontrar o vídeo no banco de dados.")
                            else:
                                print("Índice inválido.")
                        except Exception:
                            print("Entrada inválida.")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")

            elif op == "8":
                while True:
                    print("\n--- Recomendações ---")
                    print("1. Recomendações de treino")
                    print("2. Recomendações de nutrição")
                    print("3. Diretrizes gerais")
                    print("4. Grupos musculares")
                    print("5. Mobilidade")
                    print("6. Divisões semanais")
                    print("7. Progressão")
                    print("8. Considerações finais")
                    print("9. Atualizar minhas preferências")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")

                    if subop == "1":
                        treinos = recomendacao.recomendar_treinos_sugestoes(preferencias_usuario)
                        if not treinos:
                            print("Nenhuma recomendação de treino encontrada para suas preferências.")
                        else:
                            print("\n--- Recomendações de Treino ---")
                            for idx, rec in enumerate(treinos, 1):
                                dados = rec.dados
                                print(f"{idx}. {dados.get('nome', '-')}")
                                print(f"   Nível: {dados.get('nivel', '-')}")
                                print(f"   Objetivo: {dados.get('objetivo', '-')}")
                                print("   Exercícios:")
                                for ex in dados.get('exercicios', []):
                                    if isinstance(ex, dict):
                                        grupo = ex.get('grupo', '-')
                                        exercicio = ex.get('exercicio', '-')
                                        series = ex.get('series', '-')
                                        repeticoes = ex.get('repeticoes', '-')
                                        print(f"      - [{grupo}] {exercicio}: {series}x{repeticoes}")
                                    else:
                                        print(f"      - {ex}")
                    elif subop == "2":
                        alimentos = recomendacao.recomendar_alimentos_sugestoes(preferencias_usuario)
                        if not alimentos:
                            print("Nenhuma recomendação de alimento encontrada para suas preferências.")
                        else:
                            print("\n--- Recomendações de Nutrição ---")
                            for idx, rec in enumerate(alimentos, 1):
                                dados = rec.dados
                                print(f"{idx}. {dados.get('nome', '-')}")
                                print(f"   Grupo: {dados.get('grupo', '-')}")
                                print(f"   Calorias: {dados.get('calorias', '-')} kcal")
                                print(f"   Macronutrientes: {dados.get('macros', '-')}")
                    elif subop == "3":
                        diretrizes = recomendacao.recomendar_diretrizes_gerais(preferencias_usuario)
                        if not diretrizes:
                            print("Nenhuma diretriz geral encontrada para suas preferências.")
                        else:
                            print("\n--- Diretrizes Gerais ---")
                            for idx, rec in enumerate(diretrizes, 1):
                                dados = rec.dados
                                print(f"{idx}. {dados.get('descricao', dados)}")
                    elif subop == "4":
                        grupos = recomendacao.recomendar_grupos_musculares(preferencias_usuario)
                        if not grupos:
                            print("Nenhum grupo muscular encontrado para suas preferências.")
                        else:
                            print("\n--- Grupos Musculares ---")
                            for idx, rec in enumerate(grupos, 1):
                                dados = rec.dados
                                print(f"{idx}. {dados.get('nome', dados)}")
                    elif subop == "5":
                        mobilidade = recomendacao.recomendar_mobilidade(preferencias_usuario)
                        if not mobilidade:
                            print("Nenhuma recomendação de mobilidade encontrada para suas preferências.")
                        else:
                            print("\n--- Recomendações de Mobilidade ---")
                            for idx, rec in enumerate(mobilidade, 1):
                                dados = rec.dados
                                print(f"{idx}. {dados.get('descricao', dados)}")
                    elif subop == "6":
                        divisoes = recomendacao.recomendar_divisoes_semanais(preferencias_usuario)
                        if not divisoes:
                            print("Nenhuma divisão semanal encontrada para suas preferências.")
                        else:
                            print("\n--- Divisões Semanais ---")
                            for idx, rec in enumerate(divisoes, 1):
                                dados = rec.dados
                                print(f"{idx}. {dados.get('descricao', dados)}")
                    elif subop == "7":
                        progressao = recomendacao.recomendar_progressao(preferencias_usuario)
                        if not progressao:
                            print("Nenhuma recomendação de progressão encontrada para suas preferências.")
                        else:
                            print("\n--- Recomendações de Progressão ---")
                            for idx, rec in enumerate(progressao, 1):
                                dados = rec.dados
                                print(f"{idx}. {dados.get('descricao', dados)}")
                    elif subop == "8":
                        consideracoes = recomendacao.recomendar_consideracoes_finais(preferencias_usuario)
                        if not consideracoes:
                            print("Nenhuma consideração final encontrada para suas preferências.")
                        else:
                            print("\n--- Considerações Finais ---")
                            for idx, rec in enumerate(consideracoes, 1):
                                dados = rec.dados
                                print(f"{idx}. {dados.get('descricao', dados)}")
                    elif subop == "9":
                        print("\n--- Atualizar Preferências ---")
                        print(f"Nível atual: {preferencias_usuario['nivel']}")
                        print(f"Objetivo atual: {preferencias_usuario['objetivo']}")
                        print(f"Frequência de treino atual: {preferencias_usuario['frequencia_treino']}")
                        print(f"Restrição dieta atual: {preferencias_usuario['restricao_dieta']}")
                        print(f"Restrições treino atual: {preferencias_usuario['restricoes_treino']}")
                        
                        novo_nivel = input(f"Novo nível (pressione Enter para manter): ").strip()
                        if novo_nivel: preferencias_usuario['nivel'] = novo_nivel

                        novo_objetivo = input(f"Novo objetivo (pressione Enter para manter): ").strip()
                        if novo_objetivo: preferencias_usuario['objetivo'] = novo_objetivo
                        
                        nova_freq = input(f"Nova frequência (pressione Enter para manter): ").strip()
                        if nova_freq: preferencias_usuario['frequencia_treino'] = nova_freq

                        nova_restricao_dieta = input(f"Nova restrição de dieta (pressione Enter para manter): ").strip()
                        if nova_restricao_dieta: preferencias_usuario['restricao_dieta'] = nova_restricao_dieta

                        novas_restricoes_treino = input(f"Novas restrições de treino (pressione Enter para manter): ").strip()
                        if novas_restricoes_treino: preferencias_usuario['restricoes_treino'] = novas_restricoes_treino
                        
                        print("Preferências atualizadas!")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")
            elif op == "9":
                while True:
                    print("\n--- Feedback ---")
                    print("1. Enviar feedback")
                    print("2. Listar feedbacks")
                    print("3. Deletar feedback")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")
                    if subop == "1":
                        texto = input("Digite seu feedback: ")
                        while True:
                            try:
                                nota = int(input("Dê uma nota de 1 a 5: "))
                                if 1 <= nota <= 5:
                                    break
                                else:
                                    print("Nota inválida. Deve ser entre 1 e 5.")
                            except ValueError:
                                print("Entrada inválida. Digite um número entre 1 e 5.")
                        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        feedback.criar_feedback(usuario_logado.email, texto, nota, data_atual)
                        print("Feedback enviado! Agradecemos pelo seu feedback!")
                    elif subop == "2":
                        feedbacks = feedback.listar_feedbacks()
                        if not feedbacks:
                            print("Nenhum feedback encontrado.")
                        else:
                            for idx, f in enumerate(feedbacks, 1):
                                print(f"{idx}. {f.usuario_email}: (Nota: {f.nota}) (Data: {f.data})")
                                print(f" Texto: {f.texto}")
                    elif subop == "3":
                        meus_feedback = feedback.listar_feedbacks_usuario(usuario_logado.email)
                        if not meus_feedback:
                            print("Nenhum feedback encontrado.")
                        else:
                            for idx, f in enumerate(meus_feedback, 1):
                                print(f"{idx}. (Nota: {f.nota}) (Data: {f.data})")
                                print(f" Texto: {f.texto}")

                        idx_delete = int(input("Digite o número do feedback para deletar: (0 para cancelar) "))
                        if idx_delete == 0:
                            continue
                        if 1 <= idx_delete <= len(meus_feedback):
                            feedback_id = meus_feedback[idx_delete - 1]
                            feedback.deletar_feedback(feedback_id.id)
                            print("Feedback deletado!")
                        else:
                            print("Índice inválido.")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")
            elif op == "10":
                while True:
                    print("\n--- Fórum ---")
                    print("1. Criar Post")
                    print("2. Listar Posts")
                    print("3. Comentar Post")
                    print("4. Listar Comentários dos Posts")
                    print("5. Listar todos os Conteúdos do Fórum")
                    print("6. Exibir todos os Conteúdos do Usuário no Fórum")
                    print("7. Deletar Post")
                    print("0. Voltar")
                    subop = input("Escolha uma opção: ")
                    if subop == "1":
                        titulo = input("Digite o Título do Post:")
                        mensagem = input("Digite o Conteúdo do Post:")
                        data_post = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        criarpost = forum.criar_post(usuario_logado.email, titulo, mensagem, data_post)
                        if criarpost:
                            print("Post criado com sucesso!")
                        else:
                            print("Erro ao criar post.")
                    elif subop == "2":
                        posts = forum.listar_posts()
                        if not posts:
                            print("Nenhum post encontrado.")
                        else:
                            for idx, p in enumerate(posts, 1):
                                print(f"{idx}. {p.titulo} (Autor: {p.usuario_email}) (Data: {p.data})")
                                print(f" Conteúdo: {p.mensagem}")
                    elif subop == "3":
                        comentario = input("Digite o conteúdo do comentário: ")
                        post_id = input("Digite o ID do post para comentar: ")
                        data_comentario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if forum.comentar_post(post_id, usuario_logado.email, comentario, data_comentario):
                            print("Comentário adicionado com sucesso!")
                        else:
                            print("Erro ao adicionar comentário. Verifique o ID do post.")
                    elif subop == "4":
                        post_id = input("Digite o ID do post para listar comentários: ")
                        comentarios = forum.listar_comentarios(post_id)
                        if not comentarios:
                            print("Nenhum comentário encontrado para este post.")
                        else:
                            for idx, c in enumerate(comentarios, 1):
                                print(f"{idx}. {c.usuario_email}: {c.mensagem} (Data: {c.data})")
                    elif subop == "5":
                        posts = forum.listar_posts()
                        comentarios = []
                        for post in posts:
                            comentarios.extend(forum.listar_comentarios(post.id))
                        conteudos = posts + comentarios
                        if not conteudos:
                            print("Nenhum conteúdo encontrado no fórum.")
                        else:
                            forum.exibir_todos_conteudos(conteudos)
                    elif subop == "6":
                        forum.exibir_conteudo_usuario(usuario_logado.email)
                    elif subop == "7":
                        post_id = input("Digite o ID do post para deletar: ")
                        if forum.deletar_post(post_id):
                            print("Post deletado com sucesso!")
                        else:
                            print("Erro ao deletar post. Verifique o ID do post.")
                    elif subop == "0":
                        break
                    else:
                        print("Opção inválida.")

            elif op == "0":
                usuario_logado = None
                print("Logout realizado.")
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    main()