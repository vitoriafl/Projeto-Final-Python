import sqlite3

script_sql = """
PRAGMA foreign_keys = ON;

-- 1. Criação das Tabelas (convenção: snake_case, sem acentos, tabelas no singular)
CREATE TABLE IF NOT EXISTS curso (
    codigo INTEGER NOT NULL,
    codigo_nivel TEXT NOT NULL,
    nivel TEXT NOT NULL,
    nome TEXT NOT NULL,
    sigla TEXT,
    periodo TEXT,
    PRIMARY KEY (codigo, codigo_nivel)
);

CREATE TABLE IF NOT EXISTS aluno (
    usuario TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    nome_social TEXT,
    data_cadastro TEXT DEFAULT (DATE('now')),
    matricula INTEGER UNIQUE NOT NULL,
    codigo_curso INTEGER NOT NULL,
    nivel_curso TEXT NOT NULL,
    semestre_ingresso INTEGER NOT NULL,
    ano_ingresso INTEGER NOT NULL,
    semestre_maximo INTEGER,
    ano_maximo INTEGER,
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    FOREIGN KEY (codigo_curso, nivel_curso) REFERENCES curso (codigo, codigo_nivel)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS colaborador (
    usuario TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    nome_social TEXT,
    matricula INTEGER UNIQUE,
    funcao TEXT,
    email TEXT,
    secao TEXT,
    expiracao TEXT
);

CREATE TABLE IF NOT EXISTS outro (
    usuario TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    nome_social TEXT,
    documento TEXT,
    motivo TEXT,
    expiracao TEXT
);

-- 2. Inserção dos Cursos
INSERT INTO curso (codigo, codigo_nivel, nivel, nome, sigla, periodo) VALUES
(36,  'T', 'Tecnologia', 'Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas', 'TADS',      'Noturno'),
(89,  'G', 'Graduação',  'Engenharia Ambiental','EA','Noturno'),
(94,  'G', 'Graduação',  'Sistemas de Informação','SI','Integral'),
(87,  'T', 'Tecnologia', 'Curso Superior de Tecnologia em Saneamento Ambiental', 'TSA', 'Noturno'),
(111, 'G', 'Graduação',  'Engenharia de Transportes','Eng Trans', 'Noturno'),
(88,  'G', 'Graduação',  'Engenharia de Telecomunicações','Eng Tel','Integral'),
(82,  'M', 'Mestrado',   'Mestrado em Tecnologia', 'MT','Integral'),
(35,  'D', 'Doutorado',  'Doutorado em Tecnologia','DT','Integral'),
(99,  'G', 'Graduação', 'Aluno Especial de Graduação', 'EspGrad', ''),
(99,  'P', 'Pós-Graduação', 'Aluno Especial de Pós-graduação', 'EspPos', '');

-- 3. Inserção de Exemplo: Alunos (usuario = 1ª letra do Nome + Matricula)
INSERT INTO aluno (usuario, nome, nome_social, data_cadastro, matricula, codigo_curso, nivel_curso, semestre_ingresso, ano_ingresso, semestre_maximo, ano_maximo, ativo) VALUES
('j2024001', 'João Carlos da Silva',    NULL,           '2024-02-10', '2024001', 36,  'T', 1, 2024, 2, 2027, 1),
('m2023050', 'Maria Eduarda Oliveira',  'Duda Oliveira','2023-08-01', '2023050', 94,  'G', 2, 2023, 2, 2028, 1),
('l2022102', 'Lucas Gabriel Santos',    NULL,           '2022-02-15', '2022102', 89,  'G', 1, 2022, 2, 2027, 1),
('a2024200', 'Ana Beatris Souza',       NULL,           '2024-03-01', '2024200', 82,  'M', 1, 2024, 2, 2026, 1);

-- 4. Inserção de Exemplo: Colaboradores
INSERT INTO colaborador (usuario, nome, nome_social, matricula, funcao, email, secao) VALUES
('carlos.admin',   'Carlos Alberto Pereira',  NULL, 'COL1001', 'Analista de TI',       'carlos.admin@instituicao.edu.br',  'Secretaria Acadêmica'),
('patricia.prof',  'Patrícia Mendes Rocha',   NULL, 'COL1002', 'Professora Assistente', 'patricia.prof@instituicao.edu.br', 'Departamento de Tecnologia');

-- 5. Inserção de Exemplo: Outros
INSERT INTO outro (usuario, nome, nome_social, documento, motivo, expiracao) VALUES
('visitante.roberto', 'Roberto de Almeida', NULL, '123.456.789-00', 'Pesquisador Visitante', '2025-12-31'),
('prestador.marcos',  'Marcos Vinicius Lima', NULL, '987.654.321-11', 'Manutenção de Redes',    '2024-06-30');
"""

conn = sqlite3.connect('../data/projeto_final.db')
cursor = conn.cursor()
cursor.executescript(script_sql)
conn.commit()
conn.close()

print("Banco de dados SQLite criado e populado com sucesso!")

