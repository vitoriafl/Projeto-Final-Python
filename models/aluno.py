"""
Módulo que define o modelo Aluno.

A classe Aluno herda de Pessoa e acrescenta os dados acadêmicos do aluno
(matrícula, curso, período de ingresso, prazo máximo e situação).
"""

from models.pessoa import Pessoa
from utils.helpers import gerar_usuario


class Aluno(Pessoa):
    """Representa um aluno (Graduação, Pós-Graduação ou Especial).

    O usuário é gerado automaticamente: primeira letra do nome + matrícula.
    """

    CAMPOS = [
        "usuario", "nome", "nome_social", "data_cadastro", "matricula",
        "codigo_curso", "nivel_curso", "semestre_ingresso", "ano_ingresso",
        "semestre_maximo", "ano_maximo", "ativo",
    ]

    def __init__(self, nome, nome_social, data_cadastro, matricula,
                 codigo_curso, nivel_curso, semestre_ingresso, ano_ingresso,
                 semestre_maximo, ano_maximo, ativo=1):
        """Cria um aluno e gera o seu usuário.

        Args:
            nome (str): nome completo.
            nome_social (str): nome social (ou None).
            data_cadastro (str): data do cadastro (dd/mm/AAAA).
            matricula (int): número de matrícula (RA).
            codigo_curso (int): código do curso.
            nivel_curso (str): letra do nível do curso (D, M, T, G ou P).
            semestre_ingresso (int): semestre de ingresso.
            ano_ingresso (int): ano de ingresso.
            semestre_maximo (int): semestre limite para conclusão.
            ano_maximo (int): ano limite para conclusão.
            ativo (int, optional): 1 = ativado, 0 = desativado. Padrão é 1.
        """
        usuario = gerar_usuario(nome, matricula)
        super().__init__(usuario, nome, nome_social)
        self.data_cadastro = data_cadastro
        self.matricula = matricula
        self.codigo_curso = codigo_curso
        self.nivel_curso = nivel_curso
        self.semestre_ingresso = semestre_ingresso
        self.ano_ingresso = ano_ingresso
        self.semestre_maximo = semestre_maximo
        self.ano_maximo = ano_maximo
        self.ativo = ativo

    def obter_matricula(self):
        """Retorna a matrícula (RA) do aluno.

        Returns:
            int: número de matrícula.
        """
        return self.matricula

    def situacao(self):
        """Retorna a situação do aluno por extenso.

        Returns:
            str: 'Ativo' ou 'Inativo'.
        """
        if self.ativo == 1:
            return "Ativo"
        return "Inativo"

    def exibir(self):
        """Monta um texto com todos os dados do aluno.

        Returns:
            str: dados formatados para exibição.
        """
        texto = super().exibir()
        texto += f" | Matrícula: {self.matricula}"
        texto += f" | Curso: {self.codigo_curso}-{self.nivel_curso}"
        texto += f" | Ingresso: {self.semestre_ingresso}/{self.ano_ingresso}"
        texto += f" | Máximo: {self.semestre_maximo}/{self.ano_maximo}"
        texto += f" | Cadastro: {self.data_cadastro}"
        texto += f" | {self.situacao()}"
        return texto

    def para_lista(self):
        """Retorna os dados do aluno em uma lista (ordem de CAMPOS).

        Returns:
            list: valores dos atributos do aluno.
        """
        return [
            self.usuario, self.nome, self.nome_social, self.data_cadastro,
            self.matricula, self.codigo_curso, self.nivel_curso,
            self.semestre_ingresso, self.ano_ingresso, self.semestre_maximo,
            self.ano_maximo, self.ativo,
        ]
