# Projeto de Software Fitness App Orientado a Objetos:


# Funcionalidades Principais :

 - **Criação e gerenciamento de planos de treino personalizados**
   - **Classes:**
      - Plano_Treino(Classe responsável por definir todos os atributos necessário para o plano de treino com atributos como usuario, email, nome, identificador(id), objetivo, nivel, data da criação do plano).
      - Servico_Treino(Classe responsável por definir métodos e receber atributos vindos da classe Plano Treino a fim de executar funcinalidades como criar treino, deletar treino, listar planos treino e atualizar treinos).
    
 - **Registro e acompanhamento de atividades físicas**
   - **Classes:**
      - Atividade(Classe responsável por definir atributos para a gestão de atividades físicas como usuario, email, calorias, passos, tipo de exercicio,data, duração).
      - Serivco_Atividade( Classe Responsável por definir métodos e receber atributos vindos da Classe Atividade a fim de executar funcionalidades como criar atividades, deletar atividades, atualizar atividades, listar atividades.
 - **Registro de alimentos e análise nutricional do usuário de forma personalizada**
   - **Classes:**
      - Plano_Nutricional(Classe responsável por definir todos os atributos necessários para o gerenciamento da nutrição como usuario, data, alimentos ou refeições, macros e calorias).
      - Servico_Nutricao(Classe Responsável por receber atributos vindos da classe Plano Nutricional a fim de executar funcionalidades como registrar alimento, deletar registro alimento, listar alimentos do usuario, listar alimentos pré cadastrados,atualizar registro e analisar alimentação).
 - **Definição de metas**
   - **Classes:**
      - Meta(Classe cuja atribuição é definir atributos para o gerenciamento dos objetivos como objetivo,usuario,tipo de meta(emagrecimento,hipertrofia,força...),data de início,data esperada de finalização e conclusão de metas).
      - Servico_Meta(Classe recebe atributos vindos de Meta e gerencia os métodos como criar metas, atualizar metas, listar metas, deletar metas
 - **Integração com Wearable Devices**
   - **Classes:**
      - Wearable(Classe que define atributos para uso de dispostivos wearable como data, tipo(passos, calorias, sono, frequência cardíaca..) e valor(quantidade de cada tipo)).
      - Servico_Wearable( Classe que define os métodos e recebe atributos da classe Wearable sendo responsável por gerar_dados_aleatorios(simulação de uso de wearable devices),registro manual,listar dados wearable do usuário, exportar e importar arquivos do tipo .csv para simulação de importação de dispositivos wearable).
 - **Compartilhamento de desafios e Progresso**
   - **Classes:**
      - Desafio(Classe que define atributos para desafios entre usuário e compartilhamento de progresso guardando dados como nome, descrição, data início, data fim, numero de participantes).
      - Servico_Desafio(Classe que implementa métodos de criação de desafios,exclusão de desafios, listar desafios e participar de desafios)
    
- **Videos e Conteúdos instrutivos**
   - **Classes:**
      -Video(Classe que define atributos do video como título,url e categoria).
      -Servico_Video(Classe que implementa os métodos de registrar videos, pesquisar videos, listar videos do usuário, deletar videos, buscar tutorias de exercícios).
  
- **Recomendações Personalizadas**
   - **Classes:**:
      - Recomendacao( Classe que define atributos como usuario, email, tipo, conteudo, data).
      - Servico_Recomendacao( Classe que coloca métodos para lógica de recomendação e sugestão de treinos e alimentação pré cadastrados de acordo com o perfil do usuário,além de recomendação de diretrizes gerais, treino de mobilidade,divisões semanais, considerações finais(orientações gerais) e função verificar preferência do usuário).
- **Feedback do Usuário e Votação para treinos e programas**
   - **Classes:**
      - Feedback( Classe que define atributos como usuario,email, texto, nota, data).
      - Servico_Feedback( Classe que faz a lógica e definição de métodos para adicionar feedback, deletar feedback, atualizar feedback, e listar feedback).
- **Forum e Comunidade**
   - **Classes:**
     - Conteudo_Forum( Classe geral que define atributos para forum conteúdo usuario,email,mensagem e data).
     - Post_Forum( Classe que herda atributos de Conteudo Forum apenas acrescentando o atributo título do post).
     - Conteudo_Forum( Classe que herda atributos de Conteudo Forum apenas acrescentando o atributo identificador id_post_forum).

## Estrutura do Projeto

```
fitness_app/
│
├── main.py                # Entrada do app no terminal (CLI)
├── app.py                 # Entrada para futura interface Streamlit
├── requirements.txt
├
│
├── core/
│   ├── __init__.py
│   ├── database.py        # Setup TinyDB, funções CRUD, backup/import
│   ├── auth.py            # Cadastro/login de usuários
│   ├── models.py          # Classes principais (Usuário, PlanoTreino, etc.)
│   └── utils.py           # Funções auxiliares
|
|
|── scripts/
|   ├── __init_.py
|   ├── gerar_dados.py # Gerar Dados Simulados para Wearable
|   ├── seed_database.py # Popular Banco de Dados tinyDB 
|
|  
|
├── services/
│   ├── workout.py         # Serviço de planos de treino
│   ├── activity.py        # Serviço de atividades físicas
│   ├── nutrition.py       # Serviço de nutrição
│   ├── goal.py            # Serviço de metas e progresso
│   ├── wearable.py        # Serviço de integração com wearables
│   ├── social.py          # Serviço de desafios e social
│   ├── video.py           # Serviço de vídeos
│   ├── recommendation.py  # Serviço de recomendações
│   ├── feedback.py        # Serviço de feedback
│   └── forum.py           # Serviço de fórum
│
├── data/
│   ├── workouts.json         # Treinos Prontos
│   ├── food_database.json    # Alimentações Pré-cadastradas
│   ├── wearable.csv
|   ├── fitness.json # Banco Principal do Sistema
```

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/jfdt10/Projeto_Software_OO_Fitness_App.git
   cd 
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## Como Usar

- **Terminal (CLI):**
  ```bash
  python -m fitness_app.main
  ```
- **Interface Web (em breve):**
  ```bash
  python -m fitness_app.app
  ```

## Licença

Este projeto está sob a licença MIT.

     
