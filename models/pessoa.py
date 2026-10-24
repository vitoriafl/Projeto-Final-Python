"""
Módulo que define a classe Pessoa.

A classe Pessoa é a classe base (mãe) das classes Aluno, Colaborador e Outro.
Ela guarda os dados que todas as pessoas do sistema têm em comum.
"""


class Pessoa:
    """Representa uma pessoa cadastrada no sistema.

    Attributes:
        usuario (str): nome de usuário (login).
        nome (str): nome completo (nome de registro).
        nome_social (str): nome social, se houver.
    """

    def __init__(self, usuario, nome, nome_social=None):
        """Cria uma pessoa.

        Args:
            usuario (str): nome de usuário.
            nome (str): nome completo.
            nome_social (str, optional): nome social. Padrão é None.
        """
        self.usuario = usuario
        self.nome = nome
        self.nome_social = nome_social

    def nome_exibicao(self):
        """Retorna o nome que deve aparecer no sistema.

        Se a pessoa tiver nome social, ele é usado; senão, usa o nome.

        Returns:
            str: nome a ser exibido.
        """
        if self.nome_social:
            return self.nome_social
        return self.nome

    def obter_matricula(self):
        """Retorna a matrícula da pessoa.

        Pessoas sem matrícula (ex.: Outro) devolvem texto vazio. As classes
        filhas que têm matrícula sobrescrevem este método (polimorfismo).

        Returns:
            str: texto vazio.
        """
        return ""

    def exibir(self):
        """Monta um texto com os dados básicos da pessoa.

        As classes filhas completam este texto com seus próprios dados.

        Returns:
            str: dados formatados para exibição.
        """
        return f"Usuário: {self.usuario} | Nome: {self.nome_exibicao()}"
