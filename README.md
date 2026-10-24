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
```

> Observação: nesta versão as pastas `models/` e `utils/` ficam na raiz do projeto e o `main.py` fica em `src/`.

## Como executar
Na pasta raiz do projeto:
```text
python src/main.py
```
Não é necessário instalar pacotes extras (apenas a biblioteca padrão do Python).

## Funcionalidades
- **Cadastros:** Aluno (usuário gerado automaticamente: 1ª letra do nome + matrícula), Colaborador, Outros e Curso.
- **Consultas e Buscas:** alunos, funcionários, outros, todos (por nome) e cursos.
- **Relatórios:** totais e listagens em texto simples.
- **Importar:** alunos do arquivo CSV da Diretoria Acadêmica. Cursos inexistentes são criados automaticamente e matrículas repetidas são ignoradas.
- **Exportar:** listagens em CSV (separador `;`) na pasta `exportacoes/`.
- As datas seguem o formato `dd/mm/AAAA`. As datas de exemplo que estavam no banco em `AAAA-MM-DD` são convertidas ao iniciar o sistema.
