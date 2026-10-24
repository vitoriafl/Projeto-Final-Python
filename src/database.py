"""
Módulo de gerenciamento e persistência de dados em SQLite.

Este módulo centraliza as operações de acesso ao banco de dados da aplicação,
incluindo o estabelecimento de conexões, a execução de consultas e a
importação e exportação de dados via arquivos CSV.

Funções principais:
    conectar: abre a conexão com o banco de dados.
    padronizar_datas: converte datas antigas (AAAA-MM-DD) para dd/mm/AAAA.
    inserir_curso, inserir_aluno, inserir_colaborador, inserir_outro: cadastros.
    curso_existe: verifica se um curso (código + nível) está cadastrado.
    contar_registros: conta os registros de uma tabela.
    buscar_cursos, buscar_alunos, buscar_colaboradores, buscar_outros:
        listam os registros, com filtro opcional.
    importar_alunos_csv: importa os alunos enviados pela Diretoria Acadêmica.
    exportar_csv: grava uma listagem em arquivo CSV.

Observação sobre o SQL: os valores digitados pelo usuário são enviados
separados do comando, no lugar dos '?'. Assim, um nome com aspas (ex.: D'Ávila)
não quebra o comando nem permite alterar o SQL (SQL injection).
"""

import sqlite3

from models import Aluno, Colaborador, Outro, Curso
from utils import converter_data_iso, data_hoje, nome_do_nivel

SQL_CURSO = "SELECT codigo, codigo_nivel, nome, sigla, periodo FROM curso"
SQL_ALUNO = (
    "SELECT nome, nome_social, data_cadastro, matricula, codigo_curso, "
    "nivel_curso, semestre_ingresso, ano_ingresso, semestre_maximo, "
    "ano_maximo, ativo FROM aluno"
)
SQL_COLABORADOR = (
    "SELECT usuario, nome, nome_social, matricula, funcao, email, secao, "
    "expiracao FROM colaborador"
)
SQL_OUTRO = (
    "SELECT usuario, nome, nome_social, documento, motivo, expiracao "
    "FROM outro"
)

# Colunas do CSV da Diretoria Acadêmica (posições 0 a 10):
# nome, nome_social, ra, curso, nivel, pingr, tpering, ingresso, perult, tperult, aperult
TOTAL_COLUNAS_CSV = 11
COLUNAS_NUMERICAS_CSV = [2, 3, 5, 7, 8, 10]


def conectar(caminho_banco):
    """Abre a conexão com o banco de dados SQLite.

    Args:
        caminho_banco (Path): caminho do arquivo .db.

    Returns:
        sqlite3.Connection: conexão aberta com o banco.
    """
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    return conexao


def executar(conexao, sql, parametros=(), confirmar=True):
    """Executa um comando de alteração (INSERT, UPDATE ou DELETE).

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        sql (str): comando SQL com '?' no lugar dos valores.
        parametros (tuple, optional): valores do comando.
        confirmar (bool, optional): se True, grava (commit) na hora.
    """
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    if confirmar:
        conexao.commit()


def consultar(conexao, sql, parametros=()):
    """Executa uma consulta (SELECT) e devolve todas as linhas.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        sql (str): consulta SQL com '?' no lugar dos valores.
        parametros (tuple, optional): valores da consulta.

    Returns:
        list: lista de tuplas com o resultado.
    """
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    return cursor.fetchall()


def existe(conexao, sql, parametros):
    """Verifica se uma consulta encontra pelo menos um registro.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        sql (str): consulta SQL com '?' no lugar dos valores.
        parametros (tuple): valores da consulta.

    Returns:
        bool: True se encontrou algum registro.
    """
    return len(consultar(conexao, sql, parametros)) > 0


def padronizar_datas(conexao):
    """Converte para dd/mm/AAAA as datas gravadas no formato AAAA-MM-DD.

    Os dados de exemplo do banco vieram no formato AAAA-MM-DD, mas o
    enunciado exige dd/mm/AAAA. A função só altera as datas no formato antigo.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    colunas_de_data = [
        ("aluno", "data_cadastro"),
        ("colaborador", "expiracao"),
        ("outro", "expiracao"),
    ]
    for tabela_coluna in colunas_de_data:
        tabela = tabela_coluna[0]
        coluna = tabela_coluna[1]
        # Nomes de tabela/coluna vêm da lista acima (fixa), nunca do usuário
        sql = f"SELECT usuario, {coluna} FROM {tabela} WHERE {coluna} LIKE '____-__-__'"
        for linha in consultar(conexao, sql):
            usuario = linha[0]
            data = linha[1]
            executar(conexao,
                     f"UPDATE {tabela} SET {coluna} = ? WHERE usuario = ?",
                     (converter_data_iso(data), usuario),
                     confirmar=False)
    conexao.commit()


def inserir_curso(conexao, curso, confirmar=True):
    """Grava um curso no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        curso (Curso): curso a ser gravado.
        confirmar (bool, optional): se True, grava (commit) na hora.

    Returns:
        bool: True se gravou, False se o curso já existia.
    """
    if curso_existe(conexao, curso.codigo, curso.codigo_nivel):
        return False
    sql = ("INSERT INTO curso (codigo, codigo_nivel, nivel, nome, sigla, periodo) "
           "VALUES (?, ?, ?, ?, ?, ?)")
    executar(conexao, sql, tuple(curso.para_lista()), confirmar)
    return True


def inserir_aluno(conexao, aluno, confirmar=True):
    """Grava um aluno no banco.

    O curso do aluno precisa estar cadastrado antes (chave estrangeira).

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        aluno (Aluno): aluno a ser gravado.
        confirmar (bool, optional): se True, grava (commit) na hora.

    Returns:
        bool: True se gravou, False se a matrícula/usuário já existia.
    """
    if existe(conexao,
              "SELECT usuario FROM aluno WHERE usuario = ? OR matricula = ?",
              (aluno.usuario, aluno.matricula)):
        return False
    sql = ("INSERT INTO aluno (usuario, nome, nome_social, data_cadastro, "
           "matricula, codigo_curso, nivel_curso, semestre_ingresso, "
           "ano_ingresso, semestre_maximo, ano_maximo, ativo) "
           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    executar(conexao, sql, tuple(aluno.para_lista()), confirmar)
    return True


def inserir_colaborador(conexao, colaborador):
    """Grava um colaborador no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        colaborador (Colaborador): colaborador a ser gravado.

    Returns:
        bool: True se gravou, False se o usuário/matrícula já existia.
    """
    if existe(conexao,
              "SELECT usuario FROM colaborador WHERE usuario = ? OR matricula = ?",
              (colaborador.usuario, colaborador.matricula)):
        return False
    sql = ("INSERT INTO colaborador (usuario, nome, nome_social, matricula, "
           "funcao, email, secao, expiracao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
    executar(conexao, sql, tuple(colaborador.para_lista()))
    return True


def inserir_outro(conexao, outro):
    """Grava um usuário externo (Outro) no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        outro (Outro): usuário externo a ser gravado.

    Returns:
        bool: True se gravou, False se o usuário já existia.
    """
    if existe(conexao, "SELECT usuario FROM outro WHERE usuario = ?",
              (outro.usuario,)):
        return False
    sql = ("INSERT INTO outro (usuario, nome, nome_social, documento, motivo, "
           "expiracao) VALUES (?, ?, ?, ?, ?, ?)")
    executar(conexao, sql, tuple(outro.para_lista()))
    return True


def curso_existe(conexao, codigo, codigo_nivel):
    """Verifica se um curso está cadastrado.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        codigo (int): código do curso.
        codigo_nivel (str): letra do nível do curso.

    Returns:
        bool: True se o curso existe.
    """
    return existe(conexao,
                  "SELECT codigo FROM curso WHERE codigo = ? AND codigo_nivel = ?",
                  (codigo, codigo_nivel.upper()))


def contar_registros(conexao, tabela):
    """Conta quantos registros existem em uma tabela.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        tabela (str): nome da tabela (aluno, colaborador, outro ou curso).

    Returns:
        int: quantidade de registros.
    """
    linhas = consultar(conexao, f"SELECT COUNT(*) FROM {tabela}")
    return linhas[0][0]


def montar_filtro(coluna, valor, tipo):
    """Monta o trecho WHERE de uma busca.

    Texto é buscado por parte (LIKE '%valor%', sem diferenciar maiúsculas);
    número e data são buscados pelo valor exato.

    Args:
        coluna (str): coluna (ou expressão SQL) a ser filtrada.
        valor (str | int): valor procurado.
        tipo (str): 'texto', 'inteiro' ou 'data'.

    Returns:
        tuple: (trecho_sql, parametros).
    """
    if coluna is None:
        return "", ()
    if tipo == "texto":
        return f" WHERE {coluna} LIKE ?", ("%" + valor + "%",)
    return f" WHERE {coluna} = ?", (valor,)


def buscar_cursos(conexao, coluna=None, valor=None, tipo="texto"):
    """Lista os cursos, com filtro opcional.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        coluna (str, optional): coluna a filtrar (ex.: 'nome').
        valor (str | int, optional): valor procurado.
        tipo (str, optional): 'texto', 'inteiro' ou 'data'. Padrão é 'texto'.

    Returns:
        list: lista de objetos Curso.
    """
    filtro, parametros = montar_filtro(coluna, valor, tipo)
    linhas = consultar(conexao, SQL_CURSO + filtro + " ORDER BY nome", parametros)
    cursos = []
    for linha in linhas:
        cursos.append(Curso(linha[0], linha[1], linha[2], linha[3], linha[4]))
    return cursos


def buscar_alunos(conexao, coluna=None, valor=None, tipo="texto"):
    """Lista os alunos, com filtro opcional.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        coluna (str, optional): coluna a filtrar (ex.: 'nome', 'matricula').
        valor (str | int, optional): valor procurado.
        tipo (str, optional): 'texto', 'inteiro' ou 'data'. Padrão é 'texto'.

    Returns:
        list: lista de objetos Aluno.
    """
    filtro, parametros = montar_filtro(coluna, valor, tipo)
    linhas = consultar(conexao, SQL_ALUNO + filtro + " ORDER BY nome", parametros)
    alunos = []
    for linha in linhas:
        alunos.append(Aluno(linha[0], linha[1], linha[2], linha[3], linha[4],
                            linha[5], linha[6], linha[7], linha[8], linha[9],
                            linha[10]))
    return alunos


def buscar_colaboradores(conexao, coluna=None, valor=None, tipo="texto"):
    """Lista os colaboradores, com filtro opcional.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        coluna (str, optional): coluna a filtrar (ex.: 'secao').
        valor (str | int, optional): valor procurado.
        tipo (str, optional): 'texto', 'inteiro' ou 'data'. Padrão é 'texto'.

    Returns:
        list: lista de objetos Colaborador.
    """
    filtro, parametros = montar_filtro(coluna, valor, tipo)
    linhas = consultar(conexao, SQL_COLABORADOR + filtro + " ORDER BY nome",
                       parametros)
    colaboradores = []
    for linha in linhas:
        colaboradores.append(Colaborador(linha[0], linha[1], linha[2], linha[3],
                                         linha[4], linha[5], linha[6], linha[7]))
    return colaboradores


def buscar_outros(conexao, coluna=None, valor=None, tipo="texto"):
    """Lista os usuários externos (Outros), com filtro opcional.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        coluna (str, optional): coluna a filtrar (ex.: 'documento').
        valor (str | int, optional): valor procurado.
        tipo (str, optional): 'texto', 'inteiro' ou 'data'. Padrão é 'texto'.

    Returns:
        list: lista de objetos Outro.
    """
    filtro, parametros = montar_filtro(coluna, valor, tipo)
    linhas = consultar(conexao, SQL_OUTRO + filtro + " ORDER BY nome", parametros)
    outros = []
    for linha in linhas:
        outros.append(Outro(linha[0], linha[1], linha[2], linha[3],
                            linha[4], linha[5]))
    return outros


def linha_csv_valida(campos):
    """Verifica se uma linha do CSV de alunos pode ser importada.

    Args:
        campos (list): valores da linha, já separados pela vírgula.

    Returns:
        bool: True se a linha tem todas as colunas, nome, nível e números válidos.
    """
    if len(campos) != TOTAL_COLUNAS_CSV:
        return False
    if campos[0].strip() == "" or campos[4].strip() == "":
        return False
    for posicao in COLUNAS_NUMERICAS_CSV:
        if not campos[posicao].strip().isdigit():
            return False
    return True


def importar_alunos_csv(conexao, caminho_csv):
    """Importa os alunos do arquivo CSV enviado pela Diretoria Acadêmica.

    Tratamentos feitos em cada linha:
        - linhas com números inválidos ou sem nome são descartadas;
        - nome social em branco é gravado como vazio (None);
        - se o curso (código + nível) não existir, ele é criado
          automaticamente com um nome provisório;
        - o aluno fica ativo se o ano limite ainda não passou;
        - matrículas já cadastradas não são importadas de novo.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        caminho_csv (str): caminho do arquivo CSV.

    Returns:
        tuple: (importados, repetidos, invalidos, cursos_criados).
    """
    importados = 0
    repetidos = 0
    invalidos = 0
    cursos_criados = 0
    data_cadastro = data_hoje()
    ano_atual = int(data_cadastro[6:])

    # utf-8-sig: sem isso o Windows lê os acentos do CSV errado
    with open(caminho_csv, "r", encoding="utf-8-sig") as arquivo:
        primeira_linha = True
        for linha in arquivo:
            if primeira_linha:
                primeira_linha = False
            else:
                campos = linha.strip().split(",")
                if not linha_csv_valida(campos):
                    invalidos += 1
                else:
                    resultado = importar_aluno(conexao, campos, data_cadastro, ano_atual)
                    if resultado == "repetido":
                        repetidos += 1
                    else:
                        importados += 1
                        if resultado == "importado_com_curso":
                            cursos_criados += 1

    conexao.commit()
    return importados, repetidos, invalidos, cursos_criados


def importar_aluno(conexao, campos, data_cadastro, ano_atual):
    """Grava no banco (sem commit) um aluno vindo de uma linha válida do CSV.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        campos (list): valores da linha do CSV.
        data_cadastro (str): data do cadastro (dd/mm/AAAA).
        ano_atual (int): ano atual, para definir se o aluno está ativo.

    Returns:
        str: 'importado', 'repetido' ou 'importado_com_curso' (quando o curso
        também precisou ser criado).
    """
    nome = campos[0].strip()
    nome_social = campos[1].strip()
    if nome_social == "":
        nome_social = None
    matricula = int(campos[2])
    codigo_curso = int(campos[3])
    nivel = campos[4].strip().upper()
    semestre_ingresso = int(campos[5])
    ano_ingresso = int(campos[7])
    semestre_maximo = int(campos[8])
    ano_maximo = int(campos[10])

    ativo = 0
    if ano_maximo >= ano_atual:
        ativo = 1

    aluno = Aluno(nome, nome_social, data_cadastro, matricula,
                  codigo_curso, nivel, semestre_ingresso, ano_ingresso,
                  semestre_maximo, ano_maximo, ativo)
    if existe(conexao,
              "SELECT usuario FROM aluno WHERE usuario = ? OR matricula = ?",
              (aluno.usuario, aluno.matricula)):
        return "repetido"

    # O curso precisa existir antes do aluno (chave estrangeira)
    curso_criado = False
    if not curso_existe(conexao, codigo_curso, nivel):
        nome_curso = f"Curso {codigo_curso} - {nome_do_nivel(nivel)} (importado)"
        inserir_curso(conexao, Curso(codigo_curso, nivel, nome_curso, "", ""),
                      confirmar=False)
        curso_criado = True

    inserir_aluno(conexao, aluno, confirmar=False)
    if curso_criado:
        return "importado_com_curso"
    return "importado"


def exportar_csv(caminho_arquivo, cabecalho, linhas):
    """Grava uma listagem em arquivo CSV (separado por ';', abre no Excel).

    Args:
        caminho_arquivo (str): caminho do arquivo a ser criado.
        cabecalho (list): nomes das colunas.
        linhas (list): lista de listas com os valores.
    """
    # utf-8-sig: faz o Excel reconhecer os acentos
    with open(caminho_arquivo, "w", encoding="utf-8-sig") as arquivo:
        arquivo.write(";".join(cabecalho) + "\n")
        for linha in linhas:
            valores = []
            for valor in linha:
                if valor is None:
                    valores.append("")
                else:
                    valores.append(str(valor).replace(";", ","))
            arquivo.write(";".join(valores) + "\n")
