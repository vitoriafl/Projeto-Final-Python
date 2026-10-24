"""
Funções auxiliares do sistema de controle e cadastro acadêmico.

Este módulo reúne funções de uso geral, aproveitadas por várias partes do
sistema, para evitar repetição de código.

Funções:
    gerar_usuario: monta o nome de usuário (1ª letra do nome + matrícula).
    validar_data: verifica se uma data está no formato dd/mm/AAAA.
    data_hoje: devolve a data atual no formato dd/mm/AAAA.
    converter_data_iso: converte AAAA-MM-DD para dd/mm/AAAA.
    nome_do_nivel: devolve o nome de um nível de curso (ex.: G -> Graduação).
    ler_texto: lê um texto obrigatório digitado pelo usuário.
    ler_texto_opcional: lê um texto que pode ficar em branco.
    ler_inteiro: lê um número inteiro digitado pelo usuário.
    ler_data: lê uma data no formato dd/mm/AAAA.
"""

from datetime import datetime

NIVEIS = {
    "D": "Doutorado",
    "M": "Mestrado",
    "T": "Tecnologia",
    "G": "Graduação",
    "P": "Especial",
}

DIAS_POR_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def gerar_usuario(nome, matricula):
    """Gera o nome de usuário no padrão: primeira letra do nome + matrícula.

    Args:
        nome (str): nome completo da pessoa.
        matricula (int): número de matrícula.

    Returns:
        str: usuário gerado, em letras minúsculas (ex.: 'j2024001').
    """
    primeira_letra = nome.strip()[0].lower()
    return primeira_letra + str(matricula)


def ano_bissexto(ano):
    """Verifica se um ano é bissexto.

    Args:
        ano (int): ano a ser verificado.

    Returns:
        bool: True se o ano for bissexto.
    """
    return ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0)


def validar_data(data):
    """Verifica se a data informada está no formato dd/mm/AAAA e existe.

    Args:
        data (str): data a ser verificada.

    Returns:
        bool: True se a data for válida, False caso contrário.
    """
    partes = data.split("/")
    if len(partes) != 3:
        return False

    dia = partes[0]
    mes = partes[1]
    ano = partes[2]
    if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
        return False
    if len(dia) != 2 or len(mes) != 2 or len(ano) != 4:
        return False

    dia = int(dia)
    mes = int(mes)
    ano = int(ano)
    if mes < 1 or mes > 12:
        return False

    maximo_de_dias = DIAS_POR_MES[mes - 1]
    if mes == 2 and ano_bissexto(ano):
        maximo_de_dias = 29
    return dia >= 1 and dia <= maximo_de_dias


def converter_data_iso(data):
    """Converte uma data do formato AAAA-MM-DD para dd/mm/AAAA.

    Usada para padronizar as datas de exemplo que já estavam no banco.
    Se a data não estiver no formato AAAA-MM-DD, ela é devolvida sem mudança.

    Args:
        data (str): data no formato AAAA-MM-DD.

    Returns:
        str: data no formato dd/mm/AAAA.
    """
    partes = data.split("-")
    if len(partes) != 3:
        return data
    return partes[2] + "/" + partes[1] + "/" + partes[0]


def data_hoje():
    """Retorna a data atual no formato dd/mm/AAAA.

    Returns:
        str: data de hoje (ex.: '23/10/2026').
    """
    # str(datetime.now()) começa com a data no formato AAAA-MM-DD
    agora = str(datetime.now())
    return converter_data_iso(agora[:10])


def nome_do_nivel(letra):
    """Retorna o nome por extenso de um nível de curso.

    Args:
        letra (str): letra do nível (D, M, T, G ou P).

    Returns:
        str: nome do nível ou 'Desconhecido' se a letra não existir.
    """
    return NIVEIS.get(letra.upper(), "Desconhecido")


def ler_texto(mensagem):
    """Lê um texto obrigatório (não aceita resposta em branco).

    Args:
        mensagem (str): texto exibido para o usuário.

    Returns:
        str: texto digitado, sem espaços nas pontas.
    """
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Este campo é obrigatório.")


def ler_texto_opcional(mensagem):
    """Lê um texto que pode ficar em branco.

    Args:
        mensagem (str): texto exibido para o usuário.

    Returns:
        str: texto digitado ou None se ficou em branco.
    """
    texto = input(mensagem).strip()
    if texto == "":
        return None
    return texto


def ler_inteiro(mensagem):
    """Lê um número inteiro, repetindo a pergunta até ser válido.

    Args:
        mensagem (str): texto exibido para o usuário.

    Returns:
        int: número digitado.
    """
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit():
            return int(texto)
        print("Digite apenas números inteiros (0 a 9).")


def ler_data(mensagem):
    """Lê uma data no formato dd/mm/AAAA, repetindo até ser válida.

    Args:
        mensagem (str): texto exibido para o usuário.

    Returns:
        str: data digitada no formato dd/mm/AAAA.
    """
    while True:
        data = input(mensagem).strip()
        if validar_data(data):
            return data
        print("Data inválida. Use o formato dd/mm/AAAA.")
