"""
Módulo de utilitários e funções de suporte do sistema.

Este pacote centraliza ferramentas auxiliares e funções utilitárias
utilizadas ao longo da aplicação, como tratamento de datas, geração
de nomes de usuário e leitura de dados digitados no terminal.

Funções exportadas:
    - gerar_usuario, validar_data, data_hoje, converter_data_iso, nome_do_nivel
    - ler_texto, ler_texto_opcional, ler_inteiro, ler_data
"""

from .helpers import *

# Define a API pública do módulo: especifica quais funções serão exportadas ao usar "from utils import *"
__all__ = [
    "gerar_usuario",
    "validar_data",
    "data_hoje",
    "converter_data_iso",
    "nome_do_nivel",
    "ler_texto",
    "ler_texto_opcional",
    "ler_inteiro",
    "ler_data",
]
