"""
Serviço de Recomendação para Treinos e Alimentos
Este módulo fornece funcionalidades para recomendar treinos e alimentos com base nas preferências do usuário.
"""

import datetime
from fitness_app.core.models import Recomendacao
from fitness_app.core.database import obter_registros

class ServicoRecomendacao:
    def __init__(self):
        pass

    def recomendar_treinos_sugestoes(self, preferencia_usuario):
        treinos = obter_registros('treinos_prontos')
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nivel = preferencia_usuario.get('nivel', '')
        objetivo = preferencia_usuario.get('objetivo', '')
        
        recomendacoes = []
        for treino in treinos:
            if treino.get('nivel') == nivel and treino.get('objetivo') == objetivo:
                recomendacoes.append(Recomendacao(tipo='treino', conteudo=treino, usuario_email=usuario_email, data=data_atual))
        
        return recomendacoes

    def recomendar_alimentos_sugestoes(self, preferencia_usuario):
        perfis = obter_registros('perfis_alimentares')
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        restricoes_usuario = set([r.lower() for r in preferencia_usuario.get('restricoes_dieta', [])])
        recomendacoes = []
        for perfil in perfis:
            restricoes_perfil = set([r.lower() for r in perfil.get('restricoes_dieta', [])])
        
            if (not restricoes_usuario and not restricoes_perfil) or (restricoes_usuario and  restricoes_usuario.issubset(restricoes_perfil)):
                refeicoes = perfil.get('refeicoes', {})
                for nome_refeicao, opcoes in refeicoes.items():
                    for opcao in opcoes:
                        recomendacoes.append(Recomendacao(
                            tipo='refeicao',
                            conteudo={"nome_refeicao": nome_refeicao, "itens": opcao},
                            usuario_email=usuario_email,
                            data=data_atual
                        ))
        return recomendacoes

    def recomendar_diretrizes_gerais(self, preferencia_usuario):
        diretrizes = obter_registros('diretrizes_gerais')
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
                    f"Nível {nivel.title()}: Frequência: {info['frequencia']}, "
                    f"Séries/músculo: {info['series_por_musculo']}, Repetições: {info['repeticoes']}, "
                    f"Descanso: {info['descanso']}, Carga: {info['carga']}, Progressão: {info['progressao']}"
                )
                recomendacoes.append(Recomendacao(tipo='diretriz_geral', conteudo={"descricao": descricao}, usuario_email=usuario_email, data=data_atual))
            if objetivo in objetivos:
                info = objetivos[objetivo]
                descricao = (
                    f"Objetivo {objetivo.title()}: {info['series']} séries de {info['repeticoes']} repetições, "
                    f"Descanso: {info['descanso']}, Método: {info['metodo']}"
                )
                recomendacoes.append(Recomendacao(tipo='diretriz_geral', conteudo={"descricao": descricao}, usuario_email=usuario_email, data=data_atual))
        return recomendacoes

    def recomendar_grupos_musculares(self, preferencia_usuario):
        grupos_data = obter_registros('grupos_musculares')
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nivel_usuario = preferencia_usuario.get('nivel', '').lower()
        recomendacoes = []

        if not grupos_data:
            return []

        todos_os_grupos = grupos_data[0] 

        for nome_grupo, detalhes_grupo in todos_os_grupos.items():
            if isinstance(detalhes_grupo, dict) and 'niveis' in detalhes_grupo:
                niveis_info = detalhes_grupo.get('niveis', {})
                
                if nivel_usuario in niveis_info:
                    info_nivel = niveis_info[nivel_usuario]
    
                    conteudo_recomendacao = {
                        "nome_grupo": nome_grupo.title(),
                        "exercicios": info_nivel.get('exercicios', []),
                        "series": info_nivel.get('series', '-'),
                        "repeticoes": info_nivel.get('repeticoes', '-')
                    }
                    
                    recomendacoes.append(Recomendacao(
                        tipo='grupo_muscular',
                        conteudo=conteudo_recomendacao,
                        usuario_email=usuario_email,
                        data=data_atual
                    ))
        return recomendacoes

    def recomendar_mobilidade(self, preferencia_usuario):
        mobilidade_data = obter_registros('mobilidade')
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

                recomendacoes.append(Recomendacao(
                    tipo='mobilidade',
                    conteudo={"descricao": desc.strip()},
                    usuario_email=usuario_email,
                    data=data_atual
                ))
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

        if not membros_afetados:
            return []

        exercicios_mobilidade = mobilidade_data[0].get('exercicios', {})
        for membro in membros_afetados:
            if membro in exercicios_mobilidade:
                exercicios_nivel = exercicios_mobilidade[membro].get(nivel_usuario, [])
                if exercicios_nivel:
                    descricao = f"Para sua restrição na área de '{membro.title()}', recomendamos os seguintes exercícios de mobilidade ({nivel_usuario.title()}): {', '.join(exercicios_nivel)}."
                    recomendacoes.append(Recomendacao(
                        tipo='mobilidade',
                        conteudo={"descricao": descricao},
                        usuario_email=usuario_email,
                        data=data_atual
                    ))
                    
        return recomendacoes

    def recomendar_divisoes_semanais(self, preferencia_usuario):
        divisoes = obter_registros('divisoes_semanais')
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
                descricao = (
                    f"Modelo: {info['modelo']}, Dias: {', '.join(info['dias'])}, Exemplo: {exemplo_str}"
                )
                recomendacoes.append(Recomendacao(tipo='divisao_semanal', conteudo={"descricao": descricao}, usuario_email=usuario_email, data=data_atual))
        return recomendacoes

    def recomendar_progressao(self, preferencia_usuario):
        progressao = obter_registros('progressao')
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        nivel = preferencia_usuario.get('nivel', '').lower()
        recomendacoes = []
        for bloco in progressao:
            if nivel in bloco:
                descricao = bloco[nivel]
                recomendacoes.append(Recomendacao(tipo='progressao', conteudo={"descricao": descricao}, usuario_email=usuario_email, data=data_atual))
            if 'tecnicas_avancadas' in bloco:
                descricao = "Técnicas avançadas: " + ", ".join(bloco['tecnicas_avancadas'])
                recomendacoes.append(Recomendacao(tipo='progressao', conteudo={"descricao": descricao}, usuario_email=usuario_email, data=data_atual))
        return recomendacoes

    def recomendar_consideracoes_finais(self, preferencia_usuario):
        consideracoes = obter_registros('consideracoes_finais')
        usuario_email = preferencia_usuario.get('email', '')
        data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        recomendacoes = []
        for bloco in consideracoes:
            itens = bloco.get('itens', [])
            if itens:
                descricao = "; ".join(itens)
                recomendacoes.append(Recomendacao(tipo='consideracao_final', conteudo={"descricao": descricao}, usuario_email=usuario_email, data=data_atual))
        return recomendacoes