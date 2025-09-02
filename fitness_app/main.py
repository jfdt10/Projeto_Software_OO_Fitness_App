from fitness_app.core.auth import ServicoAutenticacao
from fitness_app.terminal.interface import exibir_menu_principal, exibir_menu_usuario
from fitness_app.terminal.menus import (
    registrar_usuario, gerenciar_treinos, gerenciar_atividades,
    gerenciar_nutricao, gerenciar_metas, gerenciar_wearable,
    gerenciar_social, gerenciar_videos, gerenciar_recomendacoes,
    gerenciar_feedback, gerenciar_forum, alterar_senha_usuario, recuperar_senha_usuario
)

def main():
    auth = ServicoAutenticacao()
    usuario_logado = None

    while True:
        if not usuario_logado:
            op = exibir_menu_principal()
            if op == "1":
                email = input("E-mail: ")
                senha = input("Senha: ")
                usuario_logado = auth.autenticar_usuario(email, senha)
                if usuario_logado:
                    print("Login realizado com sucesso!")
                    print(f"Bem-vindo, {usuario_logado.nome}!")
                else:
                    print("Usuário ou senha inválidos.")
            elif op == "2":
                registrar_usuario(auth)
            elif op == "3":
                recuperar_senha_usuario(auth)
            elif op == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")
        else:
            op = exibir_menu_usuario()
            if op == "1":
                gerenciar_treinos(usuario_logado)
            elif op == "2":
                gerenciar_atividades(usuario_logado)
            elif op == "3":
                gerenciar_nutricao(usuario_logado)
            elif op == "4":
                gerenciar_metas(usuario_logado)
            elif op == "5":
                gerenciar_wearable(usuario_logado)
            elif op == "6":
                gerenciar_social(usuario_logado)
            elif op == "7":
                gerenciar_videos(usuario_logado)
            elif op == "8":
                gerenciar_recomendacoes(usuario_logado, auth)
            elif op == "9":
                gerenciar_feedback(usuario_logado)
            elif op == "10":
                gerenciar_forum(usuario_logado)
            elif op == "11":
                alterar_senha_usuario(auth, usuario_logado)
            elif op == "0":
                usuario_logado = None
                print("Logout realizado.")
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    main()