"""
Módulo de modelos do sistema.

Este pacote centraliza a exportação das classes de domínio da aplicação,
permitindo a importação direta a partir do pacote 'models'.

Classes exportadas:
    - Pessoa: Classe base com os atributos gerais de uma pessoa.
    - Aluno: Representação dos dados e comportamentos de alunos.
    - Colaborador: Representação dos colaboradores do sistema.
    - Outro: Representação de demais cadastros/vínculos.
    - Curso: Modelo de dados para os cursos oferecidos.
"""

from .pessoa import Pessoa
from .aluno import Aluno
from .colaborador import Colaborador
from .outro import Outro
from .curso import Curso

# Define a API pública do módulo: especifica quais classes serão exportadas ao usar "from models import *"
__all__ = ["Pessoa", "Aluno", "Colaborador", "Outro", "Curso"]
