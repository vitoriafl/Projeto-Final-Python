"""
Módulo que define o modelo Colaborador.

A classe Colaborador herda de Pessoa e representa os servidores da
instituição (professores e funcionários).
"""

from models.pessoa import Pessoa


class Colaborador(Pessoa):
    """Representa um colaborador (professor ou funcionário)."""

    # Nomes das colunas, na mesma ordem de para_lista() (usado na exportação CSV)
    CAMPOS = [
        "usuario", "nome", "nome_social", "matricula", "funcao",
        "email", "secao", "expiracao",
    ]

    def __init__(self, usuario, nome, nome_social, matricula, funcao,
                 email, secao, expiracao):
        """Cria um colaborador.

        Args:
            usuario (str): nome de usuário.
            nome (str): nome completo.
            nome_social (str): nome social (ou None).
            matricula (int): número de matrícula.
            funcao (str): função/cargo.
            email (str): e-mail institucional.
            secao (str): seção/setor onde trabalha.
            expiracao (str): data de expiração do cadastro (dd/mm/AAAA).
        """
        super().__init__(usuario, nome, nome_social)
        self.matricula = matricula
        self.funcao = funcao
        self.email = email
        self.secao = secao
        self.expiracao = expiracao

    def exibir(self):
        """Monta um texto com todos os dados do colaborador.

        Returns:
            str: dados formatados para exibição.
        """
        texto = super().exibir()
        texto += f" | Matrícula: {self.matricula}"
        texto += f" | Função: {self.funcao}"
        texto += f" | E-mail: {self.email}"
        texto += f" | Seção: {self.secao}"
        texto += f" | Expiração: {self.expiracao}"
        return texto

    def para_lista(self):
        """Retorna os dados do colaborador em uma lista (ordem de CAMPOS).

        Returns:
            list: valores dos atributos do colaborador.
        """
        return [
            self.usuario, self.nome, self.nome_social, self.matricula,
            self.funcao, self.email, self.secao, self.expiracao,
        ]
