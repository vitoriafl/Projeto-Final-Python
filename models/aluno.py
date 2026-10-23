"""Módulo que define o modelo Aluno."""

class Aluno:
    # Atributos da classe
    data_cadastro = "" # dd/mm/aaaa
    matricula = 0
    cod_curso = 0 # Chave estrangeira da tabela curso
    nivel_curso = ""
    semestre_ingresso = 0
    ano_ingresso = 0
    semestre_maximo = 0
    ativo = 0 # 0 = desativado; 1 = ativado



