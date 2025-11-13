"""
modulo de logica de negocio para o sistema de recomendacao hierarquica de produtos
conecta as operacoes de negocio categorias e produtos com a estrutura avl
"""

from src.avl_tree import AVLTree
from src.models import Categoria, Produto


class SistemaRecomendacao:
    """
    gerencia o sistema de recomendacao de produtos usando avl tree
    
    a arvore avl armazena as categorias chave igual nome da categoria
    cada no da arvore contem um objeto categoria com sua lista de produtos
    """
    
    def __init__(self):
        """inicializa o sistema com uma arvore avl vazia"""
        self.arvore_categorias = AVLTree()
        print("sistema de recomendacao inicializado com sucesso")
