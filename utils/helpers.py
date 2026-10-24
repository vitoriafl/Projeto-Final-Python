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

# Formato de data exigido pelo enunciado do projeto
FORMATO_DATA = "%d/%m/%Y"

# Níveis de curso (letra usada no banco/CSV -> nome por extenso)
NIVEIS = {
    "D": "Doutorado",
    "M": "Mestrado",
    "T": "Tecnologia",
    "G": "Graduação",
    "P": "Especial",
}


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


def validar_data(data):
    """Verifica se a data informada está no formato dd/mm/AAAA.

    Args:
        data (str): data a ser verificada.

    Returns:
        bool: True se a data for válida, False caso contrário.
    """
    try:
        datetime.strptime(data, FORMATO_DATA)
        return True
    except ValueError:
        return False


def data_hoje():
    """Retorna a data atual no formato dd/mm/AAAA.

    Returns:
        str: data de hoje (ex.: '23/10/2026').
    """
    return datetime.now().strftime(FORMATO_DATA)


def converter_data_iso(data):
    """Converte uma data do formato AAAA-MM-DD para dd/mm/AAAA.

    Usada para padronizar as datas de exemplo que já estavam no banco.
    Se a data não estiver no formato AAAA-MM-DD, ela é devolvida sem mudança.

    Args:
        data (str): data no formato AAAA-MM-DD.

    Returns:
        str: data no formato dd/mm/AAAA.
    """
    try:
        data_convertida = datetime.strptime(data, "%Y-%m-%d")
        return data_convertida.strftime(FORMATO_DATA)
    except (ValueError, TypeError):
        return data


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
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite apenas números inteiros.")


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
