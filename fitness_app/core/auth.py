from fitness_app.core.models import Usuario
from fitness_app.core.database import RepositorioTinyDB
from tinydb import Query as Q


class ServicoAutenticacao:
    def __init__(self):
        self.repo = RepositorioTinyDB('usuarios')

    def registrar_usuario(self, dados_usuario: dict):
        if self.repo.usuario_existe('nome', dados_usuario.get('nome')) or self.repo.usuario_existe('email', dados_usuario.get('email')):
            raise ValueError("Usuário já existe com este nome ou e-mail.")

        usuario = Usuario(
            nome=dados_usuario.get('nome'),
            email=dados_usuario.get('email'),
            senha=dados_usuario.get('senha'),
            genero=dados_usuario.get('genero'),
            idade=dados_usuario.get('idade'),
            peso=dados_usuario.get('peso'),
            altura=dados_usuario.get('altura'),
            nivel_atividade=dados_usuario.get('nivel_atividade'),
            objetivo=dados_usuario.get('objetivo'),
            frequencia_treino=dados_usuario.get('frequencia_treino'),
            restricoes_treino=dados_usuario.get('restricoes_treino'),
            restricao_dieta=dados_usuario.get('restricao_dieta'),
            dados_wearable=dados_usuario.get('dados_wearable'),
            perfil_completo=dados_usuario.get('perfil_completo', False)
        )
        rt = dados_usuario.get('restricoes_treino')
        usuario.restricoes_treino = [] 
        if rt is not None:
            if isinstance(rt, str):
                rt = [rt]
            for r in rt:
                usuario.add_restricao_treino(r)

        rd = dados_usuario.get('restricao_dieta')
        usuario.restricao_dieta = []
        if rd is not None:
            if isinstance(rd, str):
                rd = [rd]
            for r in rd:
                usuario.add_restricao_dieta(r)
        
        dados = usuario.to_dict()
        return self.repo.inserir(dados)

    def autenticar_usuario(self, email, senha):
        q = Q()
        resultados = self.repo._table.search((q.email == email) & (q.senha == senha))
        if resultados:
            return Usuario.from_dict(resultados[0])
        return None

    def buscar_usuario_por_email(self, email):
        q = Q()
        resultados = self.repo._table.search(q.email == email)
        if resultados:
            return Usuario.from_dict(resultados[0])
        return None


    def atualizar_usuario(self, email, dados_usuario: dict):
        usuario_atual = self.buscar_usuario_por_email(email)
        if not usuario_atual:
            return False

        q = Q()
        resultados = self.repo._table.search(q.email == email)
        if not resultados:
            return False
        user_id = resultados[0].get('id')

        simples = ("nome", "genero", "idade", "nivel_atividade", "objetivo", "frequencia_treino", "dados_wearable", "perfil_completo")
        for campo in simples:
            if campo in dados_usuario:
                setattr(usuario_atual, campo, dados_usuario[campo])

        if "peso" in dados_usuario:
            usuario_atual.peso = dados_usuario["peso"]
        if "altura" in dados_usuario:
            usuario_atual.altura = dados_usuario["altura"]

        if "senha" in dados_usuario:
            usuario_atual.senha(dados_usuario["senha"])

        if "restricoes_treino" in dados_usuario:
            rt = dados_usuario.get("restricoes_treino")
            usuario_atual.restricoes_treino = []
            if isinstance(rt, str):
                rt = [rt]
            for r in (rt or []):
                usuario_atual.add_restricao_treino(r)

        if "restricao_dieta" in dados_usuario:
            rd = dados_usuario.get("restricao_dieta")
            usuario_atual.restricao_dieta = []
            if isinstance(rd, str):
                rd = [rd]
            for r in (rd or []):
                usuario_atual.add_restricao_dieta(r)

        return self.repo.atualizar(user_id, usuario_atual.to_dict())   
    
    def recuperar_senha(self, email):

        usuarios = self.repo.listar(model_cls=Usuario)
        
        for usuario in usuarios:
            if usuario.email == email:
                print(f"\nUsuário encontrado: {usuario.nome}")
                idade_informada = input(f"Qual sua idade? ")
            try:
                if int(idade_informada) != usuario.idade:
                    print("Informação incorreta. Recuperação negada.")
                    return False
            except ValueError:
                print("Idade inválida. Recuperação negada.")
                return False

            print(f"Sua senha é: {usuario._senha}")
            return True

        print("Usuário não encontrado no sistema.")
        return False
    
    def alterar_senha(self, email, senha_atual, nova_senha):
        if not nova_senha or len(nova_senha) < 3:
            raise ValueError("Nova senha deve ter pelo menos 3 caracteres.")
        usuario = self.buscar_usuario_por_email(email)
        if not usuario:
            print("Usuário não encontrado.")
            return False
        
        if not usuario.check_senha(senha_atual):
            print("Senha atual incorreta.")
            return False
        
        usuario.senha(nova_senha)
        
        dados_atualizados = usuario.to_dict()
        q = Q()
        resultados = self.repo._table.search(q.email == email)
        if resultados:
            user_id = resultados[0].get('id')
            self.repo.atualizar(user_id, dados_atualizados)
            return True
        
        print("Erro ao atualizar senha no banco de dados.")
        return False