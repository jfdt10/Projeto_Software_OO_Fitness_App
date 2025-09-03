import uuid
class Usuario:
    def __init__(
        self,
        nome,
        email,
        senha,
        genero=None,
        idade=None,
        peso=None,
        altura=None,
        nivel_atividade=None,
        objetivo=None,
        frequencia_treino=None,
        restricoes_treino=None,
        restricao_dieta=None,
        dados_wearable=None,
        perfil_completo=False,
        criado_em=None,
        id=None
    ):
        self.nome = nome
        self._email = email
        self._senha = None
        if senha is not None:
            self._senha = senha # Encapsulamento de atributos e uso de propertys para controle de acesso
        self.genero = genero
        self.idade = idade
        self.peso = peso
        self.altura = altura
        self.nivel_atividade = nivel_atividade
        self.objetivo = objetivo
        self.frequencia_treino = frequencia_treino
        self.restricoes_treino = restricoes_treino 
        self.restricao_dieta = restricao_dieta 
        self.dados_wearable = dados_wearable
        self.perfil_completo = perfil_completo
        self._criado_em = criado_em
        self._id = id or str(uuid.uuid4())


    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not self.validar_nome(valor):
            raise ValueError("Nome inválido. O nome deve conter pelo menos 2 caracteres e não pode conter caracteres numéricos.")
        self._nome = valor

    @staticmethod
    def validar_nome(nome):
        return len(nome.strip()) >= 2 and nome.replace(" ", "").isalpha()

    @property
    def id(self):
        return self._id
    
    @property
    def email(self):
        return self._email

    @property
    def peso(self):
        return self._peso
    
    @peso.setter # Setter para validação de dados
    def peso(self, v):
        if v is None:
            self._peso = None
            return 
        try:
            v = float(v)
        except (ValueError, TypeError):
            raise ValueError("Peso deve ser um número.")
        if v <= 0:
            raise ValueError("Peso deve ser um número positivo.")
        self._peso = v

    @property
    def altura(self):
        return self._altura
    
    @altura.setter
    def altura(self, v):
        if v is None:
            self._altura = None
            return
        try:
            v = float(v)
        except (ValueError, TypeError):
            raise ValueError("Altura deve ser um número.")
        if v <= 0:
            raise ValueError("Altura deve ser um número positivo.")
        self._altura = v

    def _normalize_restricao(self, r):
        if r is None:
            return None
        s = str(r).strip().lower()
        return s or None
    
    @property
    def restricoes_treino(self):
        return list(self._restricoes_treino)

    @restricoes_treino.setter
    def restricoes_treino(self, v):
        if v is None:
            self._restricoes_treino = []
            return
        if isinstance(v, str):
            v = [v]
        self._restricoes_treino = []
        for item in v:
            nr = self._normalize_restricao(item)
            if not nr:
                continue
            if nr == "nenhuma":
                self._restricoes_treino = ["nenhuma"]
                break
            if "nenhuma" in self._restricoes_treino:
                self._restricoes_treino.remove("nenhuma")
            if nr not in self._restricoes_treino:
                self._restricoes_treino.append(nr)

    def add_restricao_treino(self, r):
        r = self._normalize_restricao(r)
        if r is None:
            return
        if r == "nenhuma":
            self._restricoes_treino = ["nenhuma"]
            return
        if "nenhuma" in self._restricoes_treino:
            self._restricoes_treino.remove("nenhuma")
        if r not in self._restricoes_treino:
            self._restricoes_treino.append(r)

    def remove_restricao_treino(self, r):
        r = self._normalize_restricao(r)
        if r is None:
            return
        if r in self._restricoes_treino:
            self._restricoes_treino.remove(r)

    @property
    def restricao_dieta(self):
        return list(self._restricao_dieta)


    @restricao_dieta.setter
    def restricao_dieta(self, v):
        if v is None:
            self._restricao_dieta = []
            return
        if isinstance(v, str):
            v = [v]
        self._restricao_dieta = []
        for item in v:
            nr = self._normalize_restricao(item)
            if not nr:
                continue
            if nr == "nenhuma":
                self._restricao_dieta = ["nenhuma"]
                break
            if "nenhuma" in self._restricao_dieta:
                self._restricao_dieta.remove("nenhuma")
            if nr not in self._restricao_dieta:
                self._restricao_dieta.append(nr)

    def add_restricao_dieta(self, r):
        r = self._normalize_restricao(r)
        if r is None:
            return
        if r == "nenhuma":
            self._restricao_dieta = ["nenhuma"]
            return
        if "nenhuma" in self._restricao_dieta:
            self._restricao_dieta.remove("nenhuma")
        if r not in self._restricao_dieta:
            self._restricao_dieta.append(r)
    
    def remove_restricao_dieta(self, r):
        r = self._normalize_restricao(r)
        if r is None:
            return
        if r in self._restricao_dieta:
            self._restricao_dieta.remove(r)

    @property
    def criado_em(self):
        return self._criado_em 
    
    def senha(self, raw):
        self._senha = raw

    def check_senha(self, raw):
        return self._senha == raw

    # Método que é utilizado para todas as classes para conversão de objetos para dicionário
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self._senha,
            "genero": self.genero,
            "idade": self.idade,
            "peso": self.peso,
            "altura": self.altura,
            "nivel_atividade": self.nivel_atividade,
            "objetivo": self.objetivo,
            "frequencia_treino": self.frequencia_treino,
            "restricoes_treino": self.restricoes_treino,
            "restricao_dieta": self.restricao_dieta,
            "dados_wearable": self.dados_wearable,
            "perfil_completo": self.perfil_completo,
            "criado_em": self.criado_em
        }
    # Método que é utilizado para todas as classes para conversão de dicionários para objetos
    @classmethod
    def from_dict(cls, data):
        return cls(
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
        self._id = id or str(uuid.uuid4())
        self.usuario_email = usuario_email
        self.nome = nome
        self._exercicios = list(exercicios) if exercicios else []
        self.objetivo = objetivo
        self.nivel = nivel
        self._criado_em = criado_em
        self._tipo = self.__class__.__name__  # campo para filtrar e aplicar para uso e aplicação de polimorfismo em outras partes do sistema

    @property # ENCAPSULAMENTO
    def id(self):
        return self._id

    @property
    def criado_em(self):
        return self._criado_em
    
    @property
    def exercicios(self):
        return list(self._exercicios)
    

    def add_exercicio(self, ex):
        if ex:
            self._exercicios.append(ex)

    def remove_exercicio(self, ex):
        if ex in self._exercicios:
            self._exercicios.remove(ex)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_email": self.usuario_email,
            "nome": self.nome,
            "exercicios": self.exercicios,
            "objetivo": self.objetivo,
            "nivel": self.nivel,
            "criado_em": self._criado_em,
            "_tipo": self._tipo
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            usuario_email=data.get("usuario_email"),
            nome=data.get("nome"),
            exercicios=data.get("exercicios") or [],
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
        self._id = id or str(uuid.uuid4())

    @property
    def id(self):
        return self._id

    def to_dict(self):
        return {
            "usuario_email": self.usuario_email,
            "tipo": self.tipo,
            "data": self.data,
            "duracao": self.duracao,
            "calorias": self.calorias,
            "passos": self.passos,
            "ritmo": self.ritmo,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
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
        self._refeicoes = list(refeicoes) if refeicoes else []
        self.calorias = calorias
        self._macros = dict(macros) if isinstance(macros, dict) else (macros or {})
        self._id = id or str(uuid.uuid4())
        self._tipo = self.__class__.__name__  
    
    @property
    def id(self):
        return self._id
    
    @property
    def refeicoes(self):
        return list(self._refeicoes)

    @property
    def macros(self):
        return dict(self._macros) if isinstance(self._macros, dict) else self._macros

    def to_dict(self):
        return {
            "usuario_email": self.usuario_email,
            "data": self.data,
            "refeicoes": self.refeicoes,
            "calorias": self.calorias,
            "macros": self.macros,
            "id": self.id,
            "_tipo": self._tipo
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            usuario_email=data.get("usuario_email"),
            data=data.get("data"),
            refeicoes=data.get("refeicoes") or [],
            calorias=data.get("calorias"),
            macros=data.get("macros") or {},
            id=data.get("id")
        )

class Meta:
    def __init__(self, usuario_email, tipo, valor, data_inicio, data_fim, atingida=False, id=None):
        self.usuario_email = usuario_email
        self.tipo = tipo
        self.valor = valor
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.atingida = bool(atingida)
        self._id = id or str(uuid.uuid4())
    
    @property
    def id(self):
        return self._id

    def to_dict(self):
        return {
            "usuario_email": self.usuario_email,
            "tipo": self.tipo,
            "valor": self.valor,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "atingida": self.atingida,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
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
        self._id = id or str(uuid.uuid4())

    @property
    def id(self):
        return self._id

    def to_dict(self):
        return {
            "usuario_email": self.usuario_email,
            "data": self.data,
            "tipo": self.tipo,
            "valor": self.valor,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
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
        self._participantes = list(participantes) if participantes else []
        self._id = id or str(uuid.uuid4())
        self._tipo = self.__class__.__name__ 

    @property
    def id(self):
        return self._id

    @property
    def participantes(self):
        return list(self._participantes)
    
    def add_participante(self, email):
        if email not in self._participantes:
            self._participantes.append(email)
    
    def remove_participante(self, email):
        if email in self._participantes:
            self._participantes.remove(email)

    def to_dict(self):
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "participantes": self.participantes,
            "id": self.id,
            "_tipo": self._tipo
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data.get("nome"),
            descricao=data.get("descricao"),
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            participantes=data.get("participantes", []),
            id=data.get("id")
        )

class Video:
    def __init__(self, titulo, url, categoria=None, descricao=None, thumbnail=None, duracao=None, data_publicacao=None, usuario_email=None, id=None):
        self.titulo = titulo
        self.url = url
        self.categoria = categoria
        self.descricao = descricao
        self.thumbnail = thumbnail
        self.duracao = duracao
        self.data_publicacao = data_publicacao
        self.usuario_email = usuario_email
        self._id = id or str(uuid.uuid4())

    @property
    def id(self):
        return self._id
    
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "url": self.url,
            "categoria": self.categoria,
            "descricao": self.descricao,
            "thumbnail": self.thumbnail,
            "duracao": self.duracao,
            "data_publicacao": self.data_publicacao,
            "usuario_email": self.usuario_email,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            titulo=data.get("titulo"),
            url=data.get("url"),
            categoria=data.get("categoria"),
            descricao=data.get("descricao"),
            thumbnail=data.get("thumbnail"),
            duracao=data.get("duracao"),
            data_publicacao=data.get("data_publicacao"),
            usuario_email=data.get("usuario_email"),
            id=data.get("id")
        )

class Recomendacao:
    def __init__(self, usuario_email, tipo, conteudo, data, id=None):
        self.usuario_email = usuario_email
        self.tipo = tipo
        self.conteudo = conteudo
        self.data = data
        self._id = id or str(uuid.uuid4())

    @property
    def id(self):
        return self._id

    def to_dict(self):
        return {
            "usuario_email": self.usuario_email,
            "tipo": self.tipo,
            "conteudo": self.conteudo,
            "data": self.data,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
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
        self._nota = None  # Inicializa para usar o setter
        if nota is not None:
            self.nota = nota
        self.data = data
        self._id = id or str(uuid.uuid4()) 
        self._tipo = self.__class__.__name__

    @property
    def id(self):
        return self._id

    @property
    def nota(self):
        return self._nota
    
    @nota.setter
    def nota(self, v):
        try:
            v = int(v)
        except (TypeError, ValueError):
            raise ValueError("Nota deve ser um número inteiro.")
        if not (1 <= v <= 5):
            raise ValueError("Nota deve estar entre 1 e 5.")
        self._nota = v

    def to_dict(self):
        return {
            "usuario_email": self.usuario_email,
            "texto": self.texto,
            "nota": self.nota,
            "data": self.data,
            "id": self.id,
            "_tipo": self._tipo
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            usuario_email=data.get("usuario_email"),
            texto=data.get("texto"),
            nota=data.get("nota"),
            data=data.get("data"),
            id=data.get("id")
        )

# Classe Pai que define interface comum
class ConteudoForum:
    def __init__(self,usuario_email, mensagem,data,id=None):
        self.usuario_email = usuario_email
        self._mensagem = mensagem
        self.data = data
        self._id = id or str(uuid.uuid4())
        self._tipo = self.__class__.__name__  # Atributo para saber o tipo de conteúdo(Objeto de qual Classe?)


    @property
    def id(self):
        return self._id
    
    @property
    def mensagem(self):
        return self._mensagem
    

    def exibir(self):
        # Função Chamada na main para Polimorfismo: exibe qualquer conteúdo(sem saber o tipo)
        return f"Conteúdo de {self.usuario_email} em {self.data}: {self.mensagem}"

    def to_dict(self):
        return {
            "usuario_email": self.usuario_email,
            "mensagem": self.mensagem,
            "data": self.data,
            "id": self.id,
            "_tipo": self._tipo
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            usuario_email=data.get("usuario_email"),
            mensagem=data.get("mensagem"),
            data=data.get("data"),
            id=data.get("id")
        )
# Herança Classe Filha 1
class PostForum(ConteudoForum):
    def __init__(self, usuario_email, titulo, mensagem, data, id=None):
        super().__init__(usuario_email, mensagem, data, id)
        self._titulo = titulo

    @property
    def titulo(self):
        return self._titulo


    def exibir(self):
        # Função Chamada na main para Polimorfismo: exibe conteúdo específico de um post
        return f" POST - {self.titulo}\n   Autor: {self.usuario_email}\n   Data: {self.data}\n   Conteúdo: {self.mensagem}"

    def to_dict(self):
        base = super().to_dict()
        base["titulo"] = self.titulo
        return base

    @classmethod
    def from_dict(cls, data):
        return cls(
            usuario_email=data.get("usuario_email"),
            titulo=data.get("titulo"),
            mensagem=data.get("mensagem"),
            data=data.get("data"),
            id=data.get("id")
        )
# Herança Classe Filha 2
class ComentarioForum(ConteudoForum):
    def __init__(self, post_id, usuario_email, mensagem, data, id=None):
        super().__init__(usuario_email, mensagem, data, id)
        self.post_id = post_id

    def exibir(self):
        # Função Chamada na main para Polimorfismo: exibe conteúdo específico de um comentário
        return f" COMENTÁRIO\n   Autor: {self.usuario_email}\n   Data: {self.data}\n   Conteúdo: {self.mensagem}"

    def to_dict(self):
        base = super().to_dict()
        base["post_id"] = self.post_id
        return base

    @classmethod
    def from_dict(cls, data):
        return cls(
            post_id=data.get("post_id"),
            usuario_email=data.get("usuario_email"),
            mensagem=data.get("mensagem"),
            data=data.get("data"),
            id=data.get("id")
        )