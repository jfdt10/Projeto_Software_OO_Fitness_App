import uuid
class Usuario:
    def __init__(
        self,
        nome,
        email,
        senha,
        genero,
        idade,
        peso,
        altura,
        nivel_atividade,
        objetivo,
        frequencia_treino=None,
        restricoes_treino=None,
        restricao_dieta=None,
        dados_wearable=None,
        perfil_completo=False,
        criado_em=None,
        id=None
    ):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.genero = genero
        self.idade = idade
        self.peso = peso
        self.altura = altura
        self.nivel_atividade = nivel_atividade
        self.objetivo = objetivo
        self.frequencia_treino = frequencia_treino
        self.restricoes_treino = restricoes_treino if isinstance(restricoes_treino, list) else [restricoes_treino] if restricoes_treino else []
        self.restricao_dieta = restricao_dieta if isinstance(restricao_dieta,list) else [restricao_dieta] if restricao_dieta else []
        self.dados_wearable = dados_wearable
        self.perfil_completo = perfil_completo
        self.criado_em = criado_em
        self.id = id or str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        restricoes_treino = data.get("restricoes_treino")
        restricao_dieta = data.get("restricao_dieta")
        if restricoes_treino is None:
            restricoes_treino = []
        elif not isinstance(restricoes_treino, list):
            restricoes_treino = [restricoes_treino]

        if restricao_dieta is None:
            restricao_dieta = []
        elif not isinstance(restricao_dieta, list):
            restricao_dieta = [restricao_dieta]

        return Usuario(
            nome=data.get("nome"),
            email=data.get("email"),
            senha=data.get("senha"),
            genero=data.get("genero"),
            idade=data.get("idade"),
            peso=data.get("peso"),
            altura=data.get("altura"),
            nivel_atividade=data.get("nivel_atividade"),
            objetivo=data.get("objetivo"),
            frequencia_treino=data.get("frequencia_treino"),
            restricoes_treino=data.get("restricoes_treino"),
            restricao_dieta=data.get("restricao_dieta"),
            dados_wearable=data.get("dados_wearable"),
            perfil_completo=data.get("perfil_completo", False),
            criado_em=data.get("criado_em"),
            id=data.get("id")
        )

class PlanoTreino:
    def __init__(self, usuario_email, nome, exercicios, objetivo, nivel, criado_em=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.usuario_email = usuario_email
        self.nome = nome
        self.exercicios = exercicios
        self.objetivo = objetivo
        self.nivel = nivel
        self.criado_em = criado_em

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return PlanoTreino(
            usuario_email=data.get("usuario_email"),
            nome=data.get("nome"),
            exercicios=data.get("exercicios"),
            objetivo=data.get("objetivo"),
            nivel=data.get("nivel"),
            criado_em=data.get("criado_em"),
            id=data.get("id")
        )

class Atividade:
    def __init__(self, usuario_email, tipo, data, duracao, calorias, passos=None, ritmo=None, id=None):
        self.usuario_email = usuario_email
        self.tipo = tipo
        self.data = data
        self.duracao = duracao
        self.calorias = calorias
        self.passos = passos
        self.ritmo = ritmo
        self.id = id or str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Atividade(
            usuario_email=data.get("usuario_email"),
            tipo=data.get("tipo"),
            data=data.get("data"),
            duracao=data.get("duracao"),
            calorias=data.get("calorias"),
            passos=data.get("passos"),
            ritmo=data.get("ritmo"),
            id=data.get("id")
        )

class RegistroNutricional:
    def __init__(self, usuario_email, data, refeicoes, calorias, macros, id=None):
        self.usuario_email = usuario_email
        self.data = data
        self.refeicoes = refeicoes
        self.calorias = calorias
        self.macros = macros
        self.id = id or str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return RegistroNutricional(
            usuario_email=data.get("usuario_email"),
            data=data.get("data"),
            refeicoes=data.get("refeicoes"),
            calorias=data.get("calorias"),
            macros=data.get("macros"),
            id=data.get("id")
        )

class Meta:
    def __init__(self, usuario_email, tipo, valor, data_inicio, data_fim, atingida=False, id=None):
        self.usuario_email = usuario_email
        self.tipo = tipo
        self.valor = valor
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.atingida = atingida
        self.id = id or str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Meta(
            usuario_email=data.get("usuario_email"),
            tipo=data.get("tipo"),
            valor=data.get("valor"),
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            atingida=data.get("atingida", False),
            id=data.get("id")
        )

class DadoWearable:
    def __init__(self, usuario_email, data, tipo, valor, id=None):
        self.usuario_email = usuario_email
        self.data = data
        self.tipo = tipo
        self.valor = valor
        self.id = id or str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return DadoWearable(
            usuario_email=data.get("usuario_email"),
            data=data.get("data"),
            tipo=data.get("tipo"),
            valor=data.get("valor"),
            id=data.get("id")
        )

class Desafio:
    def __init__(self, nome, descricao, data_inicio, data_fim, participantes=None, id=None):
        self.nome = nome
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.participantes = participantes or []
        self.id = id or str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Desafio(
            nome=data.get("nome"),
            descricao=data.get("descricao"),
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            participantes=data.get("participantes", []),
            id=data.get("id")
        )

class Video:
    def __init__(self, titulo, url, categoria=None, descricao=None, thumbnail=None, duracao=None, data_publicacao=None, id=None):
        self.titulo = titulo
        self.url = url
        self.categoria = categoria
        self.descricao = descricao
        self.thumbnail = thumbnail
        self.duracao = duracao
        self.data_publicacao = data_publicacao
        self.id = id or str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Video(
            titulo=data.get("titulo"),
            url=data.get("url"),
            categoria=data.get("categoria"),
            descricao=data.get("descricao"),
            thumbnail=data.get("thumbnail"),
            duracao=data.get("duracao"),
            data_publicacao=data.get("data_publicacao"),
            id=data.get("id")
        )

class Recomendacao:
    def __init__(self, usuario_email, tipo, conteudo, data, id=None):
        self.usuario_email = usuario_email
        self.tipo = tipo
        self.conteudo = conteudo
        self.data = data
        self.id = id or str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Recomendacao(
            usuario_email=data.get("usuario_email"),
            tipo=data.get("tipo"),
            conteudo=data.get("conteudo"),
            data=data.get("data"),
            id=data.get("id")
        )

class Feedback:
    def __init__(self, usuario_email, texto, nota, data, id=None):
        self.usuario_email = usuario_email
        self.texto = texto
        self.nota = nota
        self.data = data
        self.id = id or str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Feedback(
            usuario_email=data.get("usuario_email"),
            texto=data.get("texto"),
            nota=data.get("nota"),
            data=data.get("data"),
            id=data.get("id")
        )



class ConteudoForum:
    def __init__(self,usuario_email, mensagem,data,id=None):
        self.usuario_email = usuario_email
        self.mensagem = mensagem
        self.data = data
        self.id = id or str(uuid.uuid4())
    def to_dict(self):
        return self.__dict__


class PostForum(ConteudoForum):
    def __init__(self, usuario_email, titulo, mensagem, data, id=None):
        super().__init__(usuario_email, mensagem, data, id)
        self.titulo = titulo

    @staticmethod # decorator para não modificar os atributos da instância constructor
    def from_dict(data):
        return PostForum(
            usuario_email=data.get("usuario_email"),
            titulo=data.get("titulo"),
            mensagem=data.get("mensagem"),
            data=data.get("data"),
            id=data.get("id")
        )

class ComentarioForum(ConteudoForum):
    def __init__(self, post_id, usuario_email, mensagem, data, id=None):
        super().__init__(usuario_email, mensagem, data, id)
        self.post_id = post_id

    @staticmethod 
    def from_dict(data):
        return ComentarioForum(
            post_id=data.get("post_id"),
            usuario_email=data.get("usuario_email"),
            mensagem=data.get("mensagem"),
            data=data.get("data"),
            id=data.get("id")
        )