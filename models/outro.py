"""
Módulo que define o modelo Outro.

A classe Outro herda de Pessoa e representa alunos externos de projetos
e pessoas externas (visitantes, prestadores de serviço etc.).
"""

from models.pessoa import Pessoa


class Outro(Pessoa):
    """Representa um usuário externo (visitante, prestador, aluno de projeto)."""

    # Nomes das colunas, na mesma ordem de para_lista() (usado na exportação CSV)
    CAMPOS = ["usuario", "nome", "nome_social", "documento", "motivo", "expiracao"]

    def __init__(self, usuario, nome, nome_social, documento, motivo, expiracao):
        """Cria um usuário externo.

        Args:
            usuario (str): nome de usuário.
            nome (str): nome completo.
            nome_social (str): nome social (ou None).
            documento (str): documento de identificação (CPF, RG etc.).
            motivo (str): motivo do acesso à instituição.
            expiracao (str): data de expiração do cadastro (dd/mm/AAAA).
        """
        super().__init__(usuario, nome, nome_social)
        self.documento = documento
        self.motivo = motivo
        self.expiracao = expiracao

    def exibir(self):
        """Monta um texto com todos os dados do usuário externo.

        Returns:
            str: dados formatados para exibição.
        """
        texto = super().exibir()
        texto += f" | Documento: {self.documento}"
        texto += f" | Motivo: {self.motivo}"
        texto += f" | Expiração: {self.expiracao}"
        return texto

    def para_lista(self):
        """Retorna os dados em uma lista (ordem de CAMPOS).

        Returns:
            list: valores dos atributos.
        """
        return [
            self.usuario, self.nome, self.nome_social,
            self.documento, self.motivo, self.expiracao,
        ]
