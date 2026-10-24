"""
Módulo que define o modelo Curso.

Um curso é identificado pelo par (código, nível), pois o mesmo código pode
existir em níveis diferentes (ex.: 99-G e 99-P).
"""

from utils.helpers import nome_do_nivel


class Curso:
    """Representa um curso oferecido pela faculdade."""

    CAMPOS = ["codigo", "codigo_nivel", "nivel", "nome", "sigla", "periodo"]

    def __init__(self, codigo, codigo_nivel, nome, sigla, periodo):
        """Cria um curso.

        Args:
            codigo (int): código do curso.
            codigo_nivel (str): letra do nível (D, M, T, G ou P).
            nome (str): nome do curso.
            sigla (str): sigla do curso.
            periodo (str): período (Noturno, Integral etc.).
        """
        self.codigo = codigo
        self.codigo_nivel = codigo_nivel.upper()
        self.nivel = nome_do_nivel(codigo_nivel)
        self.nome = nome
        self.sigla = sigla
        self.periodo = periodo

    def exibir(self):
        """Monta um texto com os dados do curso.

        Returns:
            str: dados formatados para exibição.
        """
        return (f"Código: {self.codigo}-{self.codigo_nivel} | {self.nome}"
                f" | Sigla: {self.sigla} | Nível: {self.nivel}"
                f" | Período: {self.periodo}")

    def para_lista(self):
        """Retorna os dados do curso em uma lista (ordem de CAMPOS).

        Returns:
            list: valores dos atributos do curso.
        """
        return [self.codigo, self.codigo_nivel, self.nivel,
                self.nome, self.sigla, self.periodo]
