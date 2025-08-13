from fitness_app.core.models import Usuario
from fitness_app.core.database import atualizar_usuario, usuarios, inserir_registro, obter_registros, usuario_existe



class ServicoAutenticacao:
    def registrar_usuario(self, usuario: Usuario):
        if usuario_existe(nome=usuario.nome, email=usuario.email):
            raise ValueError("Usuário já existe com este nome ou e-mail.")
        dados = usuario.to_dict()
        inserir_registro('usuarios', dados)
        return True

    def autenticar_usuario(self, email, senha):
        for dado in obter_registros('usuarios'):
            if dado.get('email') == email and dado.get('senha') == senha:
                return Usuario.from_dict(dado)
        return None

    def buscar_usuario_por_email(self, email):
        for dado in obter_registros('usuarios'):
            if dado.get('email') == email:
                return Usuario.from_dict(dado)
        return None
    
    def atualizar_usuario(self, email, usuario: Usuario):
        return atualizar_usuario(email, usuario.to_dict())