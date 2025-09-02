"""
Serviço de Recomendação para Treinos e Alimentos
Este módulo fornece funcionalidades para recomendar treinos e alimentos com base nas preferências do usuário.
"""

import datetime
from tinydb import Query as Q
from fitness_app.core.abc import ServicoBase
from fitness_app.core.models import Recomendacao
from fitness_app.core.database import RepositorioTinyDB


class ServicoRecomendacao(ServicoBase):
    def __init__(self, repo=None, repo_perfis=None):
        super().__init__(repo or RepositorioTinyDB('treinos_prontos'))
        self.repo_perfis = repo_perfis or RepositorioTinyDB('perfis_usuario')
        # Aqui usei Composição: ServicoRecomendacao "possui" uma instância base de Recomendacao
        self.recomendacao_base = Recomendacao(
            tipo="",
            conteudo={},
            usuario_email="",
            data=""
        )

    def criar(self, perfil):
        email = getattr(perfil, 'email', perfil.get('email') if isinstance(perfil, dict) else None)
        if not email:
            raise ValueError("perfil deve conter atributo ou chave 'email'")

        return self.repo_perfis.inserir(perfil)
    
    def listar(self,usuario_email=None, model_cls=None):
        query = None
        if usuario_email:
            q = Q()
            query = q.email == usuario_email

        return self.repo_perfis.listar(query=query, model_cls=model_cls)

    def atualizar(self, id, dados: dict):
        q = Q()

        if isinstance(id, str) and "@" in id:
            registros = self.repo_perfis.listar(query=(q.email == id))
            if not registros:
                return False
            perfil_id = registros[0].get('id')
            if not perfil_id:
                return False
            return self.repo_perfis.atualizar(perfil_id, dados)

        return self.repo_perfis.atualizar(id, dados)

    def deletar(self, id):
        q = Q()
        if isinstance(id, str) and "@" in id:
            registros = self.repo_perfis.listar(query=(q.email == id))
            if not registros:
                return False
            perfil_id = registros[0].get('id')
            if not perfil_id:
                return False
            return self.repo_perfis.deletar(perfil_id)

        return self.repo_perfis.deletar(id)
    
    def map_preferencias_usuario(self, usuario):
        mapa_nivel = {
            "Sedentário": "iniciante",
            "Moderado":  "intermediario",
            "Ativo": "avancado"
        }

        mapa_objetivo = {
            "Força": "forca",
            "Resistência": "resistencia",
            "Emagrecimento": "emagrecimento",
            "Hipertrofia": "hipertrofia",
            "Mobilidade": "mobilidade"
        }

        nivel_atividade = getattr(usuario, 'nivel_atividade', None)
        nivel = mapa_nivel.get(nivel_atividade, 'iniciante')
        objetivo = getattr(usuario, 'objetivo',None)
        objetivo = mapa_objetivo.get(objetivo, (objetivo or "").lower())

        restricoes_dieta = getattr(usuario, 'restricao_dieta', []) or []
        if isinstance(restricoes_dieta, str):
            restricoes_dieta = [restricoes_dieta] if restricoes_dieta and restricoes_dieta.lower() != "nenhuma" else []

        restricoes_treino = getattr(usuario, 'restricoes_treino', []) or []
        if isinstance(restricoes_treino, str):
            restricoes_treino = [restricoes_treino] if restricoes_treino and restricoes_treino.lower() != "nenhuma" else []

        perfil = {
            "email": getattr(usuario, 'email', None),
            "nivel": nivel,
            "objetivo": objetivo,
            "frequencia_treino": getattr(usuario, 'frequencia_treino', None),
            "restricoes_dieta": [r for r in restricoes_dieta if r and r.lower() != "nenhuma"],
            "restricoes_treino": [r for r in restricoes_treino if r and r.lower() != "nenhuma"]
        }

        return perfil

    def recomendar_treinos_sugestoes(self, preferencia_usuario):
        treinos = self.repo.listar()
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nivel = preferencia_usuario.get('nivel', '')
        objetivo = preferencia_usuario.get('objetivo', '')
        
        recomendacoes = []
        for treino in treinos:
            if treino.get('nivel') == nivel and treino.get('objetivo') == objetivo:
                # Usa a classe da instância base para criar nova recomendação
                recomendacao = type(self.recomendacao_base)(
                    tipo='treino', 
                    conteudo=treino, 
                    usuario_email=usuario_email, 
                    data=data_atual
                )
                recomendacoes.append(recomendacao)

        return recomendacoes

    def recomendar_alimentos_sugestoes(self, preferencia_usuario):
        perfis_repo = RepositorioTinyDB('perfis_alimentares')
        perfis = perfis_repo.listar()
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        restricoes_usuario = set([r.lower() for r in preferencia_usuario.get('restricoes_dieta', [])])
        recomendacoes = []
        for perfil in perfis:
            restricoes_perfil = set([r.lower() for r in perfil.get('restricoes_dieta', [])])

            if (not restricoes_usuario and not restricoes_perfil) or (restricoes_usuario and restricoes_usuario.issubset(restricoes_perfil)):
                refeicoes = perfil.get('refeicoes', {})
                for nome_refeicao, opcoes in refeicoes.items():
                    for opcao in opcoes:
                        # Usa a classe da instância base para criar nova recomendação
                        recomendacao = type(self.recomendacao_base)(
                            tipo='refeicao',
                            conteudo={"nome_refeicao": nome_refeicao, "itens": opcao},
                            usuario_email=usuario_email,
                            data=data_atual
                        )
                        recomendacoes.append(recomendacao)
        return recomendacoes

    def recomendar_diretrizes_gerais(self, preferencia_usuario):
        diretrizes_repo = RepositorioTinyDB('diretrizes_gerais')
        diretrizes = diretrizes_repo.listar()
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nivel = preferencia_usuario.get('nivel', '').lower()
        objetivo = preferencia_usuario.get('objetivo', '').lower()
        recomendacoes = []
        for bloco in diretrizes:
            niveis = bloco.get('niveis', {})
            objetivos = bloco.get('objetivos', {})
            if nivel in niveis:
                info = niveis[nivel]
                descricao = (
                    f"Nível {nivel.title()}: Frequência: {info.get('frequencia', '-')}, "
                    f"Séries/músculo: {info.get('series_por_musculo', '-')}, Repetições: {info.get('repeticoes', '-')}, "
                    f"Descanso: {info.get('descanso', '-')}, Carga: {info.get('carga', '-')}, Progressão: {info.get('progressao', '-')}"
                )
                recomendacao = type(self.recomendacao_base)(
                    tipo='diretriz_geral',
                    conteudo={"descricao": descricao},
                    usuario_email=usuario_email,
                    data=data_atual
                )
                recomendacoes.append(recomendacao)
            if objetivo in objetivos:
                info = objetivos[objetivo]
                descricao = (
                    f"Objetivo {objetivo.title()}: {info.get('series', '-')} séries de {info.get('repeticoes', '-')} repetições, "
                    f"Descanso: {info.get('descanso', '-')}, Método: {info.get('metodo', '-')}"
                )
                recomendacao = type(self.recomendacao_base)(
                    tipo='diretriz_geral',
                    conteudo={"descricao": descricao},
                    usuario_email=usuario_email,
                    data=data_atual
                )
                recomendacoes.append(recomendacao)
        return recomendacoes

    def recomendar_grupos_musculares(self, preferencia_usuario):
        grupos_repo = RepositorioTinyDB('grupos_musculares')
        grupos_data = grupos_repo.listar()
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nivel_usuario = preferencia_usuario.get('nivel', '').lower()
        recomendacoes = []

        if not grupos_data:
            return []

        todos_os_grupos = grupos_data[0]

        grupos_musculares_validos = [
            'peitoral', 'costas', 'ombros', 'bracos', 'pernas', 'abdomen'
        ]

        for nome_grupo, detalhes_grupo in todos_os_grupos.items():
            if nome_grupo.lower() not in grupos_musculares_validos and not isinstance(detalhes_grupo, dict):
                continue
                
            if isinstance(detalhes_grupo, dict) and 'niveis' in detalhes_grupo:
                niveis_info = detalhes_grupo.get('niveis', {})

                if nivel_usuario in niveis_info:
                    info_nivel = niveis_info[nivel_usuario]

                    exercicios_normalizados = []
                    for ex in info_nivel.get('exercicios', []):
                        if isinstance(ex, dict):
                            exercicios_normalizados.append(ex)
                        elif isinstance(ex, str):
                            exercicios_normalizados.append({
                                "exercicio": ex,
                                "series": info_nivel.get('series', '-'),
                                "repeticoes": info_nivel.get('repeticoes', '-')
                            })

                    conteudo_recomendacao = {
                        "nome_grupo": nome_grupo.title(),
                        "exercicios": exercicios_normalizados,
                        "series": info_nivel.get('series', '-'),
                        "repeticoes": info_nivel.get('repeticoes', '-')
                    }

                    recomendacao = type(self.recomendacao_base)(
                        tipo='grupo_muscular',
                        conteudo=conteudo_recomendacao,
                        usuario_email=usuario_email,
                        data=data_atual
                    )
                    recomendacoes.append(recomendacao)
        return recomendacoes

    def recomendar_mobilidade(self, preferencia_usuario):
        mobilidade_repo = RepositorioTinyDB('mobilidade')
        mobilidade_data = mobilidade_repo.listar()
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nivel_usuario = preferencia_usuario.get('nivel', 'iniciante').lower()
        objetivo_usuario = preferencia_usuario.get('objetivo', '').lower()
        recomendacoes = []

        if not mobilidade_data:
            return []

        if objetivo_usuario == 'mobilidade':
            for bloco in mobilidade_data:
                protocolos = bloco.get('protocolos', {})
                exercicios_gerais = bloco.get('exercicios', {})

                desc = "Protocolos Sugeridos:\n"
                for proto_nome, proto_desc in protocolos.items():
                    desc += f"  - {proto_nome.replace('_', ' ').title()}: {proto_desc}\n"

                desc += "\nExercícios por Área:\n"
                for area, exercicios_niveis in exercicios_gerais.items():
                    exercicios_do_nivel = exercicios_niveis.get(nivel_usuario, [])
                    if exercicios_do_nivel:
                        desc += f"  - {area.title()}: {', '.join(exercicios_do_nivel)}\n"

                recomendacao = type(self.recomendacao_base)(
                    tipo='mobilidade',
                    conteudo={"descricao": desc.strip()},
                    usuario_email=usuario_email,
                    data=data_atual
                )
                recomendacoes.append(recomendacao)
            return recomendacoes

        restricoes = preferencia_usuario.get('restricoes_treino', [])
        if not restricoes or "Nenhuma" in restricoes:
            return []

        mapa_restricao_membro = {
            "Joelho": ["joelho"],
            "Ombro": ["ombros"],
            "Coluna": ["coluna"]
        }

        membros_afetados = set()
        for restricao in restricoes:
            for key, membros in mapa_restricao_membro.items():
                if key.lower() in restricao.lower():
                    membros_afetados.update(membros)

        exercicios_mobilidade = mobilidade_data[0].get('exercicios', {})
        for membro in membros_afetados:
            if membro in exercicios_mobilidade:
                exercicios_nivel = exercicios_mobilidade[membro].get(nivel_usuario, [])
                if exercicios_nivel:
                    descricao = f"Para sua restrição na área de '{membro.title()}', recomendamos os seguintes exercícios de mobilidade ({nivel_usuario.title()}): {', '.join(exercicios_nivel)}."
                    recomendacao = type(self.recomendacao_base)(
                        tipo='mobilidade',
                        conteudo={"descricao": descricao},
                        usuario_email=usuario_email,
                        data=data_atual
                    )
                    recomendacoes.append(recomendacao)

        return recomendacoes

    def recomendar_divisoes_semanais(self, preferencia_usuario):
        divisoes_repo = RepositorioTinyDB('divisoes_semanais')
        divisoes = divisoes_repo.listar()
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nivel = preferencia_usuario.get('nivel', '').lower()
        recomendacoes = []
        for bloco in divisoes:
            if nivel in bloco:
                info = bloco[nivel]
                exemplo = info.get('exemplo', '')
                if isinstance(exemplo, list):
                    exemplo_str = ', '.join(exemplo)
                elif isinstance(exemplo, dict):
                    exemplo_str = '; '.join([f"{k}: {v}" for k, v in exemplo.items()])
                else:
                    exemplo_str = str(exemplo)
                dias = info.get('dias', [])
                if isinstance(dias, list):
                    dias_str = ', '.join(dias)
                else:
                    dias_str = str(dias)
                descricao = (
                    f"Modelo: {info.get('modelo', '-')}, Dias: {dias_str}, Exemplo: {exemplo_str}"
                )
                recomendacao = type(self.recomendacao_base)(
                    tipo='divisao_semanal',
                    conteudo={"descricao": descricao},
                    usuario_email=usuario_email,
                    data=data_atual
                )
                recomendacoes.append(recomendacao)
        return recomendacoes

    def recomendar_progressao(self, preferencia_usuario):
        progressao_repo = RepositorioTinyDB('progressao')
        progressao = progressao_repo.listar()
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nivel = preferencia_usuario.get('nivel', '').lower()
        recomendacoes = []
        for bloco in progressao:
            if nivel in bloco:
                descricao = bloco.get(nivel, '')
                recomendacao = type(self.recomendacao_base)(
                    tipo='progressao',
                    conteudo={"descricao": descricao},
                    usuario_email=usuario_email,
                    data=data_atual
                )
                recomendacoes.append(recomendacao)
            if 'tecnicas_avancadas' in bloco:
                tecnicas = bloco.get('tecnicas_avancadas', [])
                if isinstance(tecnicas, list):
                    descricao = "Técnicas avançadas: " + ", ".join(tecnicas)
                else:
                    descricao = "Técnicas avançadas: " + str(tecnicas)
                recomendacao = type(self.recomendacao_base)(
                    tipo='progressao',
                    conteudo={"descricao": descricao},
                    usuario_email=usuario_email,
                    data=data_atual
                )
                recomendacoes.append(recomendacao)
        return recomendacoes

    def recomendar_consideracoes_finais(self, preferencia_usuario):
        consideracoes_repo = RepositorioTinyDB('consideracoes_finais')
        consideracoes = consideracoes_repo.listar()
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        recomendacoes = []
        for bloco in consideracoes:
            itens = bloco.get('itens', [])
            if itens:
                descricao = "; ".join(itens)
                recomendacao = type(self.recomendacao_base)(
                    tipo='consideracao_final',
                    conteudo={"descricao": descricao},
                    usuario_email=usuario_email,
                    data=data_atual
                )
                recomendacoes.append(recomendacao)
        return recomendacoes