"""
Script de inicialização do banco de dados
Cria o banco se não existir e popula com dados de teste
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database
from scripts.populate_db import popular_banco

def init_database():
    """Inicializa o banco de dados"""
    db_path = "srhp.db"
    
    # Verificar se o banco já existe e tem dados
    db_exists = os.path.exists(db_path)
    
    if db_exists:
        # Verificar se o banco tem dados
        db = Database()
        categorias = db.listar_categorias()
        produtos = db.listar_produtos()
        
        if len(categorias) == 0 and len(produtos) == 0:
            print("Banco de dados existe mas está vazio. Populando...")
            popular_banco()
        else:
            print(f"Banco de dados já existe com {len(categorias)} categorias e {len(produtos)} produtos.")
    else:
        # Criar banco novo e popular
        print("Criando novo banco de dados...")
        db = Database()  # Isso cria as tabelas
        print("Banco de dados criado. Populando com dados de teste...")
        popular_banco()

if __name__ == "__main__":
    init_database()

