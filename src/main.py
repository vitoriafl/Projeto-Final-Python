"""
Ponto de entrada principal da aplicação (Interface de Linha de Comando - CLI).

Este módulo executa a interface interativa do sistema no terminal, coordenando 
a inicialização das configurações, a conexão com o banco de dados SQLite, 
a importação/exportação de dados via arquivos CSV e a gestão dos modelos do sistema.

Fluxo de execução:
    1. Configura os caminhos absolutos do projeto (BASE_DIR, DB_PATH, CSV_PATH).
    2. Exibe o menu interativo (CLI) para navegação do usuário.

Funções:
    
"""

import sys
from pathlib import Path

# 1. Definição do diretório raiz do projeto (projeto_final/)
# .parent é 'src/', .parent.parent é 'projeto_final/'
BASE_DIR = Path(__file__).resolve().parent.parent

# Adiciona o diretório raiz ao sys.path para evitar problemas de importação
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Importação das funções do banco de dados e manipulação de arquivos
from database import *

# Importação dos modelos de classes orientados a objetos
from models import *

# Importação das funções utilitárias
from utils import *

# Configuração dinâmica dos caminhos de arquivos relativos à raiz
DB_PATH = BASE_DIR / "data" / "projeto_final.db"
CSV_IMPORT_PATH = BASE_DIR / "suporte" / "dados_alunos_importar.csv"
