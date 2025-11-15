"""
modulo de banco de dados sqlite para o sistema de recomendacao
"""

import sqlite3
from typing import List, Optional, Dict, Any
from contextlib import contextmanager


class Database:
    """classe para gerenciar o banco de dados sqlite"""
    
    def __init__(self, db_path: str = "srhp.db"):
        """inicializa a conexao com o banco de dados"""
        self.db_path = db_path
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        """context manager para conexoes do banco"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_db(self):
        """cria as tabelas do banco de dados"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # tabela de categorias
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
                    descricao TEXT,
                    categoria_pai_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (categoria_pai_id) REFERENCES categorias(id)
                )
            """)
            
            # tabela de produtos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    categoria_id INTEGER NOT NULL,
                    preco REAL NOT NULL,
                    descricao TEXT,
                    avaliacao REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
                )
            """)
            
            # indices para melhor performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_produtos_categoria 
                ON produtos(categoria_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_categorias_pai 
                ON categorias(categoria_pai_id)
            """)
    
    # metodos para categorias
    
    def inserir_categoria(self, nome: str, descricao: str = "", categoria_pai_id: Optional[int] = None) -> int:
        """insere uma nova categoria"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categorias (nome, descricao, categoria_pai_id) VALUES (?, ?, ?)",
                (nome, descricao, categoria_pai_id)
            )
            return cursor.lastrowid
    
    def listar_categorias(self) -> List[Dict[str, Any]]:
        """lista todas as categorias"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.nome, c.descricao, c.categoria_pai_id,
                       p.nome as categoria_pai_nome
                FROM categorias c
                LEFT JOIN categorias p ON c.categoria_pai_id = p.id
                ORDER BY c.nome
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def buscar_categoria_por_id(self, categoria_id: int) -> Optional[Dict[str, Any]]:
        """busca uma categoria por id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.nome, c.descricao, c.categoria_pai_id,
                       p.nome as categoria_pai_nome
                FROM categorias c
                LEFT JOIN categorias p ON c.categoria_pai_id = p.id
                WHERE c.id = ?
            """, (categoria_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def buscar_categoria_por_nome(self, nome: str) -> Optional[Dict[str, Any]]:
        """busca uma categoria por nome"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.nome, c.descricao, c.categoria_pai_id,
                       p.nome as categoria_pai_nome
                FROM categorias c
                LEFT JOIN categorias p ON c.categoria_pai_id = p.id
                WHERE c.nome = ?
            """, (nome,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def atualizar_categoria(self, categoria_id: int, nome: str, descricao: str = "", 
                           categoria_pai_id: Optional[int] = None) -> bool:
        """atualiza uma categoria existente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE categorias 
                SET nome = ?, descricao = ?, categoria_pai_id = ?
                WHERE id = ?
            """, (nome, descricao, categoria_pai_id, categoria_id))
            return cursor.rowcount > 0
    
    def deletar_categoria(self, categoria_id: int) -> bool:
        """deleta uma categoria"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
            return cursor.rowcount > 0
    
    # metodos para produtos
    
    def inserir_produto(self, nome: str, categoria_id: int, preco: float, 
                       descricao: str = "", avaliacao: float = 0.0) -> int:
        """insere um novo produto"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO produtos (nome, categoria_id, preco, descricao, avaliacao)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, categoria_id, preco, descricao, avaliacao))
            return cursor.lastrowid
    
    def listar_produtos(self) -> List[Dict[str, Any]]:
        """lista todos os produtos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.nome, p.preco, p.descricao, p.avaliacao,
                       p.categoria_id, c.nome as categoria_nome
                FROM produtos p
                JOIN categorias c ON p.categoria_id = c.id
                ORDER BY p.nome
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def listar_produtos_por_categoria(self, categoria_id: int) -> List[Dict[str, Any]]:
        """lista produtos de uma categoria especifica"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.nome, p.preco, p.descricao, p.avaliacao,
                       p.categoria_id, c.nome as categoria_nome
                FROM produtos p
                JOIN categorias c ON p.categoria_id = c.id
                WHERE p.categoria_id = ?
                ORDER BY p.nome
            """, (categoria_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def buscar_produto_por_id(self, produto_id: int) -> Optional[Dict[str, Any]]:
        """busca um produto por id"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.nome, p.preco, p.descricao, p.avaliacao,
                       p.categoria_id, c.nome as categoria_nome
                FROM produtos p
                JOIN categorias c ON p.categoria_id = c.id
                WHERE p.id = ?
            """, (produto_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def atualizar_produto(self, produto_id: int, nome: str, categoria_id: int, 
                         preco: float, descricao: str = "", avaliacao: float = 0.0) -> bool:
        """atualiza um produto existente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE produtos 
                SET nome = ?, categoria_id = ?, preco = ?, descricao = ?, avaliacao = ?
                WHERE id = ?
            """, (nome, categoria_id, preco, descricao, avaliacao, produto_id))
            return cursor.rowcount > 0
    
    def deletar_produto(self, produto_id: int) -> bool:
        """deleta um produto"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            return cursor.rowcount > 0
    
    def limpar_tabelas(self):
        """limpa todas as tabelas (cuidado!)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos")
            cursor.execute("DELETE FROM categorias")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('produtos', 'categorias')")
