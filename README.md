# Projeto Software Fitness App - Orientado a Objetos

Sistema completo de gerenciamento fitness desenvolvido com foco em **Programação Orientada a Objetos**, demonstrando os Cinco pilares fundamentais: **Herança**, **Polimorfismo**, **Encapsulamento**, **Abstração** e **Composição**.

## Conceitos de POO Implementados

### Encapsulamento
- **Atributos privados** protegidos com underscore (_atributo)
- **Properties e Setters** com validação automática (peso, altura, notas)
- **Métodos privados** para lógica interna
- **Validações automáticas** que protegem integridade dos dados

### Herança
- **Classes abstratas** como RepositorioBase e ServicoBase
- **Herança de implementação** com RepositorioTinyDB
- **Hierarquia de classes** ConteudoForum → PostForum / ComentarioForum
- **Reutilização de código** através de super()

### Polimorfismo
- **Métodos abstratos** implementados diferentemente em cada classe
- **Interface uniforme** para diferentes tipos de objetos
- **Método exibir()** com comportamento específico por classe e e chamando de funções sem refencia ao tipo de classe
- **Duck typing** para objetos com to_dict()

### Abstração
- **Classes abstratas** definindo contratos obrigatórios
- **Interfaces padronizadas** (to_dict, from_dict) para todos os modelos
- **Camada de serviços** abstraindo lógica de negócio

### Composição
- **Uso nos Serviços** por meio de uso de instância base para criação de novos objetos
- **Sistema composto por múltiplos serviços** - main.py orquestra diferentes componentes
- **Usuario composto por listas complexas** - restrições de treino e dieta como componentes

## Funcionalidades e Classes Implementadas

### Gerenciamento de Usuários
**Classe Usuario**
- Encapsula dados pessoais com validação automática
- Properties para peso e altura com validação
- Gestão de restrições de treino e dieta
- Métodos de conversão to_dict() e from_dict()

**Classe ServicoAutenticacao**
- Herda de ServicoBase (abstração)
- Gerencia cadastro, login e recuperação de senha
- Validação de dados de entrada
- Controle de sessão do usuário

### Sistema de Treinos
**Classe PlanoTreino**
- Encapsula exercícios em lista protegida
- Métodos para adicionar/remover exercícios
- Validação de dados de entrada
- Identificação única por ID

**Classe ServicoTreino**
- Herda de ServicoBase
- Implementa CRUD completo para treinos
- Lógica de negócio para criação de planos
- Integração com recomendações

### Registro de Atividades
**Classe Atividade**
- Modelo simples para diferentes tipos de atividade
- Encapsulamento de dados como calorias, passos, duração
- Suporte a ritmo personalizado
- Conversão polimórfica de/para dicionário

**Classe ServicoAtividade**
- Herda de ServicoBase
- Lógica para diferentes tipos de atividade
- Cálculos automáticos de calorias
- Histórico completo de atividades

### Sistema Nutricional
**Classe RegistroNutricional**
- Encapsula refeições em estrutura protegida
- Gestão automática de macronutrientes
- Validação de dados nutricionais
- Cálculos automáticos de totais

**Classe ServicoNutricional**
- Base de dados de alimentos pré-cadastrados
- Análise nutricional personalizada
- Busca inteligente de alimentos
- Relatórios de consumo

### Gestão de Metas
**Classe Meta**
- Encapsulamento de objetivos com validação
- Controle de datas e status
- Diferentes tipos de meta
- Acompanhamento de progresso

**Classe ServicoMeta**
- Lógica de definição e acompanhamento
- Validação de metas alcançáveis
- Relatórios de progresso
- Sistema de conquistas

### Integração Wearable
**Classe DadoWearable**
- Modelo para diferentes tipos de dados
- Suporte a passos, sono, batimentos cardíacos
- Validação de valores
- Timestamp automático

**Classe ServicoWearable**
- Simulação de dados de dispositivos
- Import/Export de arquivos CSV
- Integração com atividades
- Geração de relatórios

### Recursos Sociais
**Classe Desafio**
- Gestão de desafios entre usuários
- Lista protegida de participantes
- Métodos para adicionar/remover participantes
- Controle de datas e status

**Classe ServicoSocial**
- Criação e gestão de desafios
- Sistema de participação
- Rankings e leaderboards
- Compartilhamento de progresso

### Sistema de Forum
**Classe ConteudoForum (Classe Base)**
- Classe abstrata para conteúdo do fórum
- Atributos comuns: usuário, mensagem, data
- Método abstrato exibir() para polimorfismo em chamadas em menus.py
- Base para herança de PostForum e ComentarioForum

**Classe PostForum (Herda de ConteudoForum)**
- Adiciona atributo título específico
- Implementa exibir() com formatação de post
- Herda funcionalidades da classe pai
- Especialização para posts principais

**Classe ComentarioForum (Herda de ConteudoForum)**
- Adiciona referência ao post (post_id)
- Implementa exibir() com formatação de comentário
- Herda funcionalidades da classe pai
- Especialização para respostas

**Classe ServicoForum**
- Gerenciamento polimórfico de posts e comentários
- Criação, listagem e exclusão de conteúdo
- Demonstração prática de polimorfismo
- Interface uniforme para diferentes tipos de conteúdo

### Conteúdo Educativo
**Classe Video**
- Encapsulamento de dados de vídeo
- Integração com URLs externas
- Categorização de conteúdo
- Metadados como duração e thumbnail

**Classe ServicoVideo**
- Integração com API Youtube
- Busca por categoria e exercício
- Sistema de favoritos
- Curadoria de conteúdo

### Recomendações Inteligentes
**Classe Recomendacao**
- Armazenamento de sugestões personalizadas
- Diferentes tipos de recomendação
- Associação com usuário específico
- Timestamp para controle

**Classe ServicoRecomendacao**
- Sistema de recomendação baseados no perfil
- Sugestões de treinos e nutrição
- Análise de preferências do usuário

### Sistema de Feedback
**Classe Feedback**
- Encapsulamento com validação de notas (1-5)
- Property para nota com validação automática
- Associação com usuário e data
- Texto livre para comentários

**Classe ServicoFeedback**
- Coleta e análise de feedback
- Relatórios de satisfação
- Sistema de avaliações
- Métricas de qualidade

### Camada de Abstração
**Classe RepositorioBase (Abstract Base Class)**
- Define contrato obrigatório para repositórios
- Métodos abstratos: inserir, listar, obter, atualizar, deletar
- Base para implementações específicas de banco
- Garantia de interface padronizada

**Classe ServicoBase (Abstract Base Class)**
- Define contrato para todos os serviços
- Métodos abstratos: listar, criar, deletar, atualizar
- Injeção de Dependências do repositório
- Base para lógica de negócio

**Classe RepositorioTinyDB (Herda de RepositorioBase)**
- Implementação específica para TinyDB
- Polimorfismo com diferentes tipos de objeto
- Conversão automática via to_dict/from_dict
- Encapsulamento da complexidade do banco

## Estrutura do Projeto

```
fitness_app/
├── main.py                     # Ponto de entrada CLI
├── requirements.txt            # Dependências do projeto
│
├── core/                       # Núcleo do sistema
│   ├── models.py              # Todos os modelos com OOP
│   ├── database.py            # Repository Pattern + TinyDB
│   ├── auth.py                # Sistema de autenticação
│   ├── abc.py                 # Classes abstratas
│   └── utils.py               # Utilitários
│
├── services/                   # Camada de negócios
│   ├── workout.py             # Serviço de treinos
│   ├── activity.py            # Serviço de atividades
│   ├── nutrition.py           # Serviço nutricional
│   ├── goal.py                # Serviço de metas
│   ├── wearable.py            # Serviço wearable
│   ├── social.py              # Serviço social
│   ├── video.py               # Serviço de vídeos
│   ├── recommendation.py      # Serviço de recomendações
│   ├── feedback.py            # Serviço de feedback
│   └── forum.py               # Serviço de fórum
│
├── terminal/                   # Interface de usuário
│   ├── interface.py           # Menus e navegação
│   └── menus.py               # Lógica dos menus
│
├── data/                       # Dados e banco
│   ├── fitness.json           # Banco principal TinyDB
│   ├── workouts.json          # Treinos pré-cadastrados
│   ├── food_database.json     # Base de alimentos
│   └── wearable_data.csv      # Dados simulados
│
└── scripts/                    # Scripts auxiliares
    ├── gerar_dados.py         # Gerador de dados simulados
    └── seed_database.py       # Populador do banco
```

## Instalação e Configuração

### Requisitos
- Python 3.8 ou superior
- Dependências listadas em requirements.txt

### Passos de instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/jfdt10/Projeto_Software_OO_Fitness_App.git
   cd Projeto_Software_OO_Fitness_App
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**
   ```bash
   # Popular com dados iniciais
   python -m fitness_app.scripts.seed_database
   
   # Gerar dados simulados (opcional)
   python -m fitness_app.scripts.gerar_dados
   ```

## Como Usar

### Interface de Terminal
```bash
python -m fitness_app.main
```
## Funcionalidades Principais

- **Cadastro e autenticação** de usuários com validação
- **Criação de planos de treino** personalizados e pré-prontos
- **Registro de atividades físicas** com múltiplos tipos
- **Análise nutricional** com base de alimentos pré-cadastrada
- **Sistema de metas** com acompanhamento de progresso
- **Integração com wearables** através de simulação e CSV
- **Recursos sociais** incluindo desafios entre usuários
- **Fórum da comunidade** com posts e comentários
- **Sistema de feedback** e avaliações
- **Conteúdo educativo** com integração de vídeos
- **Recomendações personalizadas** baseadas no perfil

## Backup e Utilitários

### Backup do banco
```python
from fitness_app.core.database import backup_banco
backup_banco("meu_backup.json")
```

### Importar dados
```python
from fitness_app.core.database import importar_banco
importar_banco("meu_backup.json")
```

## Licença

Este projeto está sob a licença MIT. Veja LICENSE para mais detalhes.

## Contato
Desenvolvido como projeto acadêmico para Disciplina de Projeto de Software com aplicação de conceitos de Programação Orientada a Objetos para construção de um sistema.
