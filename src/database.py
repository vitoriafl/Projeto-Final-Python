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
"""

import csv
import sqlite3
from datetime import datetime

from models import Aluno, Colaborador, Outro, Curso
from utils import converter_data_iso, data_hoje, nome_do_nivel

# Consultas base de cada tabela (as colunas seguem a ordem dos construtores)
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


def conectar(caminho_banco):
    """Abre a conexão com o banco de dados SQLite.

    Args:
        caminho_banco (Path): caminho do arquivo .db.

    Returns:
        sqlite3.Connection: conexão aberta com o banco.
    """
    conexao = sqlite3.connect(caminho_banco)
    # Liga a verificação das chaves estrangeiras (aluno -> curso)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def executar(conexao, sql, parametros=(), confirmar=True):
    """Executa um comando de alteração (INSERT, UPDATE ou DELETE).

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        sql (str): comando SQL com '?' no lugar dos valores.
        parametros (tuple, optional): valores do comando.
        confirmar (bool, optional): se True, grava (commit) na hora.

    Returns:
        bool: True se deu certo, False se violou alguma regra do banco
        (registro repetido, curso inexistente etc.).
    """
    try:
        conexao.execute(sql, parametros)
        if confirmar:
            conexao.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def consultar(conexao, sql, parametros=()):
    """Executa uma consulta (SELECT) e devolve todas as linhas.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        sql (str): consulta SQL com '?' no lugar dos valores.
        parametros (tuple, optional): valores da consulta.

    Returns:
        list: lista de tuplas com o resultado.
    """
    cursor = conexao.execute(sql, parametros)
    return cursor.fetchall()


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
    for tabela, coluna in colunas_de_data:
        # Nomes de tabela/coluna vêm da lista acima (fixa), nunca do usuário
        sql = f"SELECT usuario, {coluna} FROM {tabela} WHERE {coluna} LIKE '____-__-__'"
        for usuario, data in consultar(conexao, sql):
            executar(conexao,
                     f"UPDATE {tabela} SET {coluna} = ? WHERE usuario = ?",
                     (converter_data_iso(data), usuario),
                     confirmar=False)
    conexao.commit()


# ---------------------------------------------------------------- Cadastros

def inserir_curso(conexao, curso, confirmar=True):
    """Grava um curso no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        curso (Curso): curso a ser gravado.
        confirmar (bool, optional): se True, grava (commit) na hora.

    Returns:
        bool: True se gravou, False se o curso já existia.
    """
    sql = ("INSERT INTO curso (codigo, codigo_nivel, nivel, nome, sigla, periodo) "
           "VALUES (?, ?, ?, ?, ?, ?)")
    return executar(conexao, sql, tuple(curso.para_lista()), confirmar)


def inserir_aluno(conexao, aluno, confirmar=True):
    """Grava um aluno no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        aluno (Aluno): aluno a ser gravado.
        confirmar (bool, optional): se True, grava (commit) na hora.

    Returns:
        bool: True se gravou, False se a matrícula/usuário já existia
        ou se o curso não está cadastrado.
    """
    sql = ("INSERT INTO aluno (usuario, nome, nome_social, data_cadastro, "
           "matricula, codigo_curso, nivel_curso, semestre_ingresso, "
           "ano_ingresso, semestre_maximo, ano_maximo, ativo) "
           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    return executar(conexao, sql, tuple(aluno.para_lista()), confirmar)


def inserir_colaborador(conexao, colaborador):
    """Grava um colaborador no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        colaborador (Colaborador): colaborador a ser gravado.

    Returns:
        bool: True se gravou, False se o usuário/matrícula já existia.
    """
    sql = ("INSERT INTO colaborador (usuario, nome, nome_social, matricula, "
           "funcao, email, secao, expiracao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
    return executar(conexao, sql, tuple(colaborador.para_lista()))


def inserir_outro(conexao, outro):
    """Grava um usuário externo (Outro) no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        outro (Outro): usuário externo a ser gravado.

    Returns:
        bool: True se gravou, False se o usuário já existia.
    """
    sql = ("INSERT INTO outro (usuario, nome, nome_social, documento, motivo, "
           "expiracao) VALUES (?, ?, ?, ?, ?, ?)")
    return executar(conexao, sql, tuple(outro.para_lista()))


def curso_existe(conexao, codigo, codigo_nivel):
    """Verifica se um curso está cadastrado.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        codigo (int): código do curso.
        codigo_nivel (str): letra do nível do curso.

    Returns:
        bool: True se o curso existe.
    """
    linhas = consultar(conexao,
                       "SELECT codigo FROM curso WHERE codigo = ? AND codigo_nivel = ?",
                       (codigo, codigo_nivel.upper()))
    return len(linhas) > 0


# ------------------------------------------------------- Consultas e buscas

def contar_registros(conexao, tabela):
    """Conta quantos registros existem em uma tabela.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        tabela (str): nome da tabela (aluno, colaborador, outro ou curso).

    Returns:
        int: quantidade de registros.
    """
    # O nome da tabela vem do próprio programa, nunca do usuário
    linhas = consultar(conexao, f"SELECT COUNT(*) FROM {tabela}")
    return linhas[0][0]


def montar_filtro(coluna, valor):
    """Monta o trecho WHERE de uma busca.

    Texto é buscado por parte (LIKE '%valor%', sem diferenciar maiúsculas);
    número é buscado pelo valor exato.

    Args:
        coluna (str): coluna (ou expressão SQL) a ser filtrada.
        valor (str | int): valor procurado.

    Returns:
        tuple: (trecho_sql, parametros).
    """
    if coluna is None:
        return "", ()
    if isinstance(valor, str):
        return f" WHERE {coluna} LIKE ?", ("%" + valor + "%",)
    return f" WHERE {coluna} = ?", (valor,)


def buscar_cursos(conexao, coluna=None, valor=None):
    """Lista os cursos, com filtro opcional.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        coluna (str, optional): coluna a filtrar (ex.: 'nome').
        valor (str | int, optional): valor procurado.

    Returns:
        list: lista de objetos Curso.
    """
    filtro, parametros = montar_filtro(coluna, valor)
    linhas = consultar(conexao, SQL_CURSO + filtro + " ORDER BY nome", parametros)
    cursos = []
    for linha in linhas:
        cursos.append(Curso(linha[0], linha[1], linha[2], linha[3], linha[4]))
    return cursos


def buscar_alunos(conexao, coluna=None, valor=None):
    """Lista os alunos, com filtro opcional.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        coluna (str, optional): coluna a filtrar (ex.: 'nome', 'matricula').
        valor (str | int, optional): valor procurado.

    Returns:
        list: lista de objetos Aluno.
    """
    filtro, parametros = montar_filtro(coluna, valor)
    linhas = consultar(conexao, SQL_ALUNO + filtro + " ORDER BY nome", parametros)
    alunos = []
    for linha in linhas:
        alunos.append(Aluno(linha[0], linha[1], linha[2], linha[3], linha[4],
                            linha[5], linha[6], linha[7], linha[8], linha[9],
                            linha[10]))
    return alunos


def buscar_colaboradores(conexao, coluna=None, valor=None):
    """Lista os colaboradores, com filtro opcional.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        coluna (str, optional): coluna a filtrar (ex.: 'secao').
        valor (str | int, optional): valor procurado.

    Returns:
        list: lista de objetos Colaborador.
    """
    filtro, parametros = montar_filtro(coluna, valor)
    linhas = consultar(conexao, SQL_COLABORADOR + filtro + " ORDER BY nome",
                       parametros)
    colaboradores = []
    for linha in linhas:
        colaboradores.append(Colaborador(linha[0], linha[1], linha[2], linha[3],
                                         linha[4], linha[5], linha[6], linha[7]))
    return colaboradores


def buscar_outros(conexao, coluna=None, valor=None):
    """Lista os usuários externos (Outros), com filtro opcional.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
        coluna (str, optional): coluna a filtrar (ex.: 'documento').
        valor (str | int, optional): valor procurado.

    Returns:
        list: lista de objetos Outro.
    """
    filtro, parametros = montar_filtro(coluna, valor)
    linhas = consultar(conexao, SQL_OUTRO + filtro + " ORDER BY nome", parametros)
    outros = []
    for linha in linhas:
        outros.append(Outro(linha[0], linha[1], linha[2], linha[3],
                            linha[4], linha[5]))
    return outros


# ------------------------------------------------- Importação e exportação

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
        caminho_csv (Path): caminho do arquivo CSV.

    Returns:
        tuple: (importados, repetidos, invalidos, cursos_criados).
    """
    importados = 0
    repetidos = 0
    invalidos = 0
    cursos_criados = 0
    ano_atual = datetime.now().year
    data_cadastro = data_hoje()

    # utf-8-sig ignora o caractere especial (BOM) do início do arquivo
    with open(caminho_csv, "r", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            nome = linha["nome"].strip()
            nivel = linha["nivel"].strip().upper()
            try:
                matricula = int(linha["ra"])
                codigo_curso = int(linha["curso"])
                semestre_ingresso = int(linha["pingr"])
                ano_ingresso = int(linha["ingresso"])
                semestre_maximo = int(linha["perult"])
                ano_maximo = int(linha["aperult"])
            except ValueError:
                invalidos += 1
                continue
            if nome == "" or nivel == "":
                invalidos += 1
                continue

            nome_social = linha["nome_social"].strip()
            if nome_social == "":
                nome_social = None

            # Cria o curso que ainda não existe, para não quebrar a chave estrangeira
            if not curso_existe(conexao, codigo_curso, nivel):
                nome_curso = f"Curso {codigo_curso} - {nome_do_nivel(nivel)} (importado)"
                inserir_curso(conexao, Curso(codigo_curso, nivel, nome_curso, "", ""),
                              confirmar=False)
                cursos_criados += 1

            ativo = 0
            if ano_maximo >= ano_atual:
                ativo = 1

            aluno = Aluno(nome, nome_social, data_cadastro, matricula,
                          codigo_curso, nivel, semestre_ingresso, ano_ingresso,
                          semestre_maximo, ano_maximo, ativo)
            # Grava tudo de uma vez no final (commit único), o que é bem mais rápido
            if inserir_aluno(conexao, aluno, confirmar=False):
                importados += 1
            else:
                repetidos += 1

    conexao.commit()
    return importados, repetidos, invalidos, cursos_criados


def exportar_csv(caminho_arquivo, cabecalho, linhas):
    """Grava uma listagem em arquivo CSV (separado por ';', abre no Excel).

    Args:
        caminho_arquivo (Path): caminho do arquivo a ser criado.
        cabecalho (list): nomes das colunas.
        linhas (list): lista de listas com os valores.
    """
    # Cria a pasta de destino se ela ainda não existir
    caminho_arquivo.parent.mkdir(exist_ok=True)
    with open(caminho_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(cabecalho)
        escritor.writerows(linhas)


# Define a API pública do módulo: o que é importado com "from database import *"
__all__ = [
    "conectar", "padronizar_datas",
    "inserir_curso", "inserir_aluno", "inserir_colaborador", "inserir_outro",
    "curso_existe", "contar_registros",
    "buscar_cursos", "buscar_alunos", "buscar_colaboradores", "buscar_outros",
    "importar_alunos_csv", "exportar_csv",
]
