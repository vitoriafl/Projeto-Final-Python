"""
Ponto de entrada principal da aplicação (Interface de Linha de Comando - CLI).

Este módulo executa a interface interativa do sistema no terminal, coordenando
a inicialização das configurações, a conexão com o banco de dados SQLite,
a importação/exportação de dados via arquivos CSV e a gestão dos modelos do sistema.

Fluxo de execução:
    1. Configura os caminhos absolutos do projeto (BASE_DIR, DB_PATH, CSV_PATH).
    2. Conecta ao banco e padroniza as datas para dd/mm/AAAA.
    3. Exibe o menu interativo (CLI) até o usuário escolher "0. Sair".

Funções:
    mostrar_lista: exibe uma listagem de objetos na tela.
    escolher_filtro: pergunta por qual campo buscar e qual valor.
    escolher_curso: pede o código e o nível de um curso existente.
    cadastrar_aluno, cadastrar_colaborador, cadastrar_outro, cadastrar_curso.
    menu_cadastros, menu_buscas, menu_relatorios, menu_importar, menu_exportar.
    main: função principal com o menu principal.

Uso:
    python src/main.py
"""

import sys
from pathlib import Path

# 1. Definição do diretório raiz do projeto (projeto_final/)
# .parent é 'src/', .parent.parent é 'projeto_final/'
BASE_DIR = Path(__file__).resolve().parent.parent

# Adiciona o diretório raiz ao sys.path para evitar problemas de importação
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Importação das funções do banco de dados e manipulação de arquivos
from database import *

# Importação dos modelos de classes orientados a objetos
from models import *

# Importação das funções utilitárias
from utils import *

# Configuração dinâmica dos caminhos de arquivos relativos à raiz
DB_PATH = BASE_DIR / "data" / "projeto_final.db"
CSV_IMPORT_PATH = BASE_DIR / "suporte" / "dados_alunos_importar.csv"
EXPORT_DIR = BASE_DIR / "exportacoes"


# --------------------------------------------------------------- Auxiliares

def mostrar_lista(titulo, itens):
    """Exibe na tela uma listagem de objetos (alunos, cursos etc.).

    Args:
        titulo (str): título da listagem.
        itens (list): objetos que possuem o método exibir().
    """
    print(f"\n===== {titulo} =====")
    if len(itens) == 0:
        print("Nenhum registro encontrado.")
        return
    for item in itens:
        print(item.exibir())
    print(f"Total: {len(itens)}")


def escolher_filtro(opcoes):
    """Mostra os campos de busca, lê a opção escolhida e o valor procurado.

    Args:
        opcoes (list): lista de tuplas (rótulo, coluna, tipo), onde tipo
            é 'texto', 'inteiro' ou 'data'.

    Returns:
        tuple: (coluna, valor) ou (None, None) se a opção for inválida.
    """
    for numero in range(len(opcoes)):
        print(f"{numero + 1}. {opcoes[numero][0]}")
    escolha = ler_inteiro("Buscar por: ")
    if escolha < 1 or escolha > len(opcoes):
        print("Opção inválida.")
        return None, None

    rotulo, coluna, tipo = opcoes[escolha - 1]
    if tipo == "inteiro":
        valor = ler_inteiro(f"{rotulo}: ")
    elif tipo == "data":
        valor = ler_data(f"{rotulo} (dd/mm/AAAA): ")
    else:
        valor = ler_texto(f"{rotulo} (pode ser parte do texto): ")
    return coluna, valor


def escolher_curso(conexao):
    """Mostra os cursos e pede o código e o nível de um curso existente.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.

    Returns:
        tuple: (codigo, codigo_nivel) de um curso cadastrado.
    """
    mostrar_lista("Cursos disponíveis", buscar_cursos(conexao))
    while True:
        codigo = ler_inteiro("Código do curso: ")
        nivel = ler_texto("Nível do curso (D, M, T, G ou P): ").upper()
        if curso_existe(conexao, codigo, nivel):
            return codigo, nivel
        print("Curso não encontrado. Confira o código e o nível.")


# ---------------------------------------------------------------- Cadastros

def cadastrar_aluno(conexao):
    """Lê os dados de um aluno e grava no banco.

    O usuário é gerado automaticamente ao final do cadastro.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    print("\n--- Cadastro de Aluno ---")
    nome = ler_texto("Nome: ")
    nome_social = ler_texto_opcional("Nome social (Enter para deixar em branco): ")
    matricula = ler_inteiro("Matrícula: ")
    codigo_curso, nivel_curso = escolher_curso(conexao)
    semestre_ingresso = ler_inteiro("Semestre de ingresso: ")
    ano_ingresso = ler_inteiro("Ano de ingresso: ")
    semestre_maximo = ler_inteiro("Semestre máximo: ")
    ano_maximo = ler_inteiro("Ano máximo: ")
    while ano_maximo < ano_ingresso:
        print("O ano máximo não pode ser menor que o ano de ingresso.")
        ano_maximo = ler_inteiro("Ano máximo: ")

    aluno = Aluno(nome, nome_social, data_hoje(), matricula, codigo_curso,
                  nivel_curso, semestre_ingresso, ano_ingresso,
                  semestre_maximo, ano_maximo)
    if inserir_aluno(conexao, aluno):
        print(f"Aluno cadastrado! Usuário gerado: {aluno.usuario}")
    else:
        print("Erro: já existe um aluno com essa matrícula.")


def cadastrar_colaborador(conexao):
    """Lê os dados de um colaborador e grava no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    print("\n--- Cadastro de Colaborador ---")
    nome = ler_texto("Nome: ")
    nome_social = ler_texto_opcional("Nome social (Enter para deixar em branco): ")
    matricula = ler_inteiro("Matrícula: ")
    funcao = ler_texto("Função: ")
    email = ler_texto("E-mail: ")
    secao = ler_texto("Seção: ")
    expiracao = ler_data("Expiração (dd/mm/AAAA): ")

    usuario = gerar_usuario(nome, matricula)
    colaborador = Colaborador(usuario, nome, nome_social, matricula, funcao,
                              email, secao, expiracao)
    if inserir_colaborador(conexao, colaborador):
        print(f"Colaborador cadastrado! Usuário gerado: {usuario}")
    else:
        print("Erro: já existe um colaborador com essa matrícula ou usuário.")


def cadastrar_outro(conexao):
    """Lê os dados de um usuário externo (Outro) e grava no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    print("\n--- Cadastro de Outros (externos) ---")
    usuario = ler_texto("Usuário: ")
    nome = ler_texto("Nome: ")
    nome_social = ler_texto_opcional("Nome social (Enter para deixar em branco): ")
    documento = ler_texto("Documento: ")
    motivo = ler_texto("Motivo: ")
    expiracao = ler_data("Expiração (dd/mm/AAAA): ")

    outro = Outro(usuario, nome, nome_social, documento, motivo, expiracao)
    if inserir_outro(conexao, outro):
        print("Cadastro realizado com sucesso!")
    else:
        print("Erro: esse usuário já existe.")


def cadastrar_curso(conexao):
    """Lê os dados de um curso e grava no banco.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    print("\n--- Cadastro de Curso ---")
    codigo = ler_inteiro("Código: ")
    nivel = ler_texto("Nível (D-Doutorado, M-Mestrado, T-Tecnologia, "
                      "G-Graduação, P-Especial): ").upper()
    while nome_do_nivel(nivel) == "Desconhecido":
        print("Nível inválido.")
        nivel = ler_texto("Nível (D, M, T, G ou P): ").upper()
    nome = ler_texto("Nome: ")
    sigla = ler_texto("Sigla: ")
    periodo = ler_texto("Período (ex.: Noturno, Integral): ")

    curso = Curso(codigo, nivel, nome, sigla, periodo)
    if inserir_curso(conexao, curso):
        print("Curso cadastrado com sucesso!")
    else:
        print("Erro: já existe um curso com esse código e nível.")


def menu_cadastros(conexao):
    """Submenu de cadastros.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    while True:
        print("\n--- CADASTROS ---")
        print("1. Aluno")
        print("2. Colaborador")
        print("3. Outros")
        print("4. Curso")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            cadastrar_aluno(conexao)
        elif opcao == "2":
            cadastrar_colaborador(conexao)
        elif opcao == "3":
            cadastrar_outro(conexao)
        elif opcao == "4":
            cadastrar_curso(conexao)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------- Buscas

def menu_buscas(conexao):
    """Submenu de consultas e buscas.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    while True:
        print("\n--- CONSULTAS E BUSCAS ---")
        print("1. Alunos")
        print("2. Funcionários (colaboradores)")
        print("3. Outros")
        print("4. Todos (por nome)")
        print("5. Cursos")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            coluna, valor = escolher_filtro([
                ("Nome", "nome", "texto"),
                ("Matrícula", "matricula", "inteiro"),
                ("Ano de entrada", "ano_ingresso", "inteiro"),
                ("Ano máximo", "ano_maximo", "inteiro"),
                ("Data de cadastro", "data_cadastro", "data"),
            ])
            if coluna is not None:
                mostrar_lista("Alunos encontrados",
                              buscar_alunos(conexao, coluna, valor))
        elif opcao == "2":
            # A tabela colaborador não possui data de cadastro; usa-se a expiração
            coluna, valor = escolher_filtro([
                ("Nome", "nome", "texto"),
                ("Matrícula", "CAST(matricula AS TEXT)", "texto"),
                ("Setor (seção)", "secao", "texto"),
                ("Função", "funcao", "texto"),
                ("Data de expiração", "expiracao", "data"),
            ])
            if coluna is not None:
                mostrar_lista("Funcionários encontrados",
                              buscar_colaboradores(conexao, coluna, valor))
        elif opcao == "3":
            coluna, valor = escolher_filtro([
                ("Nome", "nome", "texto"),
                ("Nome social", "nome_social", "texto"),
                ("Documento", "documento", "texto"),
                ("Expiração", "expiracao", "data"),
            ])
            if coluna is not None:
                mostrar_lista("Outros encontrados",
                              buscar_outros(conexao, coluna, valor))
        elif opcao == "4":
            nome = ler_texto("Nome (pode ser parte do nome): ")
            mostrar_lista("Alunos", buscar_alunos(conexao, "nome", nome))
            mostrar_lista("Funcionários", buscar_colaboradores(conexao, "nome", nome))
            mostrar_lista("Outros", buscar_outros(conexao, "nome", nome))
        elif opcao == "5":
            coluna, valor = escolher_filtro([
                ("Nome", "nome", "texto"),
                ("Nível (D, M, T, G ou P)", "codigo_nivel", "texto"),
            ])
            if coluna is not None:
                mostrar_lista("Cursos encontrados",
                              buscar_cursos(conexao, coluna, valor))
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------- Relatórios

def menu_relatorios(conexao):
    """Submenu de relatórios em texto simples.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    while True:
        print("\n--- RELATÓRIOS ---")
        print("1. Total - Alunos/Colaboradores/Outros")
        print("2. Todos os Alunos")
        print("3. Todos os Funcionários")
        print("4. Todos os Outros")
        print("5. Todos")
        print("6. Todos os Cursos")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            total_alunos = contar_registros(conexao, "aluno")
            total_colaboradores = contar_registros(conexao, "colaborador")
            total_outros = contar_registros(conexao, "outro")
            print("\n===== Totais =====")
            print(f"Alunos:        {total_alunos}")
            print(f"Colaboradores: {total_colaboradores}")
            print(f"Outros:        {total_outros}")
            print(f"Total geral:   {total_alunos + total_colaboradores + total_outros}")
        elif opcao == "2":
            mostrar_lista("Todos os Alunos", buscar_alunos(conexao))
        elif opcao == "3":
            mostrar_lista("Todos os Funcionários", buscar_colaboradores(conexao))
        elif opcao == "4":
            mostrar_lista("Todos os Outros", buscar_outros(conexao))
        elif opcao == "5":
            mostrar_lista("Alunos", buscar_alunos(conexao))
            mostrar_lista("Funcionários", buscar_colaboradores(conexao))
            mostrar_lista("Outros", buscar_outros(conexao))
        elif opcao == "6":
            mostrar_lista("Todos os Cursos", buscar_cursos(conexao))
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ------------------------------------------------- Importação e exportação

def menu_importar(conexao):
    """Importa alunos de um arquivo CSV.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    print("\n--- IMPORTAR DADOS ---")
    print(f"Arquivo padrão: {CSV_IMPORT_PATH}")
    caminho = ler_texto_opcional("Caminho do CSV (Enter para usar o padrão): ")
    if caminho is None:
        caminho = CSV_IMPORT_PATH
    else:
        caminho = Path(caminho)

    if not caminho.exists():
        print("Arquivo não encontrado.")
        return

    print("Importando, aguarde...")
    importados, repetidos, invalidos, cursos_criados = importar_alunos_csv(conexao, caminho)
    print(f"Alunos importados:            {importados}")
    print(f"Já cadastrados (ignorados):   {repetidos}")
    print(f"Linhas inválidas (ignoradas): {invalidos}")
    print(f"Cursos criados automaticamente: {cursos_criados}")


def linhas_resumo(tipo, pessoas):
    """Monta linhas resumidas (tipo, usuário, nome, nome social, matrícula).

    Usada nas exportações que juntam pessoas de tipos diferentes.

    Args:
        tipo (str): tipo da pessoa (Aluno, Colaborador ou Outro).
        pessoas (list): objetos que herdam de Pessoa.

    Returns:
        list: lista de linhas para o CSV.
    """
    linhas = []
    for pessoa in pessoas:
        # Outros não têm matrícula; nesse caso a coluna fica vazia
        if isinstance(pessoa, Outro):
            matricula = ""
        else:
            matricula = pessoa.matricula
        linhas.append([tipo, pessoa.usuario, pessoa.nome, pessoa.nome_social, matricula])
    return linhas


def salvar_exportacao(nome_arquivo, cabecalho, linhas):
    """Grava a listagem na pasta de exportações e avisa o usuário.

    Args:
        nome_arquivo (str): nome do arquivo CSV.
        cabecalho (list): nomes das colunas.
        linhas (list): lista de listas com os valores.
    """
    if len(linhas) == 0:
        print("Nenhum registro encontrado. Nada foi exportado.")
        return
    caminho = EXPORT_DIR / nome_arquivo
    exportar_csv(caminho, cabecalho, linhas)
    print(f"{len(linhas)} registro(s) exportado(s) para: {caminho}")


def para_linhas(objetos):
    """Converte uma lista de objetos em linhas para o CSV.

    Args:
        objetos (list): objetos que possuem o método para_lista().

    Returns:
        list: lista de listas com os valores.
    """
    linhas = []
    for objeto in objetos:
        linhas.append(objeto.para_lista())
    return linhas


def menu_exportar(conexao):
    """Submenu de exportação de listagens em CSV.

    Os arquivos são gravados na pasta 'exportacoes' do projeto.

    Args:
        conexao (sqlite3.Connection): conexão com o banco.
    """
    cabecalho_resumo = ["tipo", "usuario", "nome", "nome_social", "matricula"]
    while True:
        print("\n--- EXPORTAR DADOS (CSV) ---")
        print("1. Alunos")
        print("2. Funcionários")
        print("3. Outros")
        print("4. Todos")
        print("5. Por Curso")
        print("6. Por Matrícula (ou parte dela)")
        print("7. Por Seção")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            salvar_exportacao("alunos.csv", Aluno.CAMPOS,
                              para_linhas(buscar_alunos(conexao)))
        elif opcao == "2":
            salvar_exportacao("funcionarios.csv", Colaborador.CAMPOS,
                              para_linhas(buscar_colaboradores(conexao)))
        elif opcao == "3":
            salvar_exportacao("outros.csv", Outro.CAMPOS,
                              para_linhas(buscar_outros(conexao)))
        elif opcao == "4":
            linhas = linhas_resumo("Aluno", buscar_alunos(conexao))
            linhas += linhas_resumo("Colaborador", buscar_colaboradores(conexao))
            linhas += linhas_resumo("Outro", buscar_outros(conexao))
            salvar_exportacao("todos.csv", cabecalho_resumo, linhas)
        elif opcao == "5":
            codigo = ler_inteiro("Código do curso: ")
            alunos = buscar_alunos(conexao, "codigo_curso", codigo)
            salvar_exportacao(f"alunos_curso_{codigo}.csv", Aluno.CAMPOS,
                              para_linhas(alunos))
        elif opcao == "6":
            parte = str(ler_inteiro("Matrícula (ou parte dela): "))
            coluna = "CAST(matricula AS TEXT)"
            linhas = linhas_resumo("Aluno", buscar_alunos(conexao, coluna, parte))
            linhas += linhas_resumo("Colaborador",
                                    buscar_colaboradores(conexao, coluna, parte))
            salvar_exportacao(f"matricula_{parte}.csv", cabecalho_resumo, linhas)
        elif opcao == "7":
            secao = ler_texto("Seção (pode ser parte do nome): ")
            colaboradores = buscar_colaboradores(conexao, "secao", secao)
            salvar_exportacao("funcionarios_secao.csv", Colaborador.CAMPOS,
                              para_linhas(colaboradores))
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


# ---------------------------------------------------------------- Principal

def main():
    """Função principal: conecta ao banco e exibe o menu principal."""
    conexao = conectar(DB_PATH)
    padronizar_datas(conexao)

    while True:
        print("\n========== SISTEMA DE CADASTRO ACADÊMICO ==========")
        print("1. Cadastros")
        print("2. Consultas e Buscas")
        print("3. Relatórios")
        print("4. Importar Dados")
        print("5. Exportar Dados")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_cadastros(conexao)
        elif opcao == "2":
            menu_buscas(conexao)
        elif opcao == "3":
            menu_relatorios(conexao)
        elif opcao == "4":
            menu_importar(conexao)
        elif opcao == "5":
            menu_exportar(conexao)
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida.")

    conexao.close()


if __name__ == "__main__":
    main()
