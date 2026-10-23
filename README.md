# Sistema de Controle e Cadastro Acadêmico (Projeto Final)

Sistema desenvolvido em Python para controle e cadastro de usuários (Alunos, Colaboradores e Outros/Visitantes) e Cursos de uma faculdade.

## Estrutura do Projeto
```text
projeto_final/
├── data/
│   └── projeto_final.db      # Banco de dados SQLite
├── suporte/
│   ├── dados_alunos_importar.csv #Arquivo com os dados dos alunos a serem importados
│   └── cria_bd_projeto #Arquivo que faz a criação do banco de dados do projeto	
├── src/
│   ├── __init__.py
│   ├── database.py           # Conexão, tabelas, consultas e importação/exportação CSV
│   ├── models/               # Modelos Orientados a Objetos (com herança)
│   │   ├── __init__.py
│   │   ├── pessoa.py         # Classe Pessoa
│   │   ├── aluno.py          # Classe Aluno
│   │   ├── curso.py          # Classe Curso
│   │   ├── colaborador.py    # Classe Colaborador
│   │   └── outro.py          # Classe Outro
│   └── utils/
│       ├── __init__.py
│       └── helpers.py        # Utilitários (geração de usuário e conversão de datas)
├── main.py                   # Ponto de entrada com menu interativo (CLI)
├── README.md
└── requirements.txt
