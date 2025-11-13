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
    
    def cadastrar_categoria(self, nome_categoria, descricao=""):
        """
        cadastra uma nova categoria no sistema
        
        args
            nome_categoria (str) nome unico da categoria usado como chave na AVL
            descricao (str) descricao opcional da categoria
        
        returns
            bool true se cadastrou com sucesso false se a categoria ja existe
        
        complexidade Olog n devido a insercao na AVL
        """
        # verifica se a categoria ja existe
        if self.arvore_categorias.find(nome_categoria) is not None:
            print(f"categoria {nome_categoria} ja existe")
            return False
        
        # cria o objeto categoria
        nova_categoria = Categoria(nome_categoria, descricao)
        
        # insere na arvore AVL chave igual nome data igual objeto Categoria
        self.arvore_categorias.insert(nome_categoria, nova_categoria)
        
        print(f"categoria {nome_categoria} cadastrada com sucesso")
        return True
    
    def cadastrar_produto(self, nome_categoria, produto_id, nome_produto, 
                         preco, descricao="", avaliacao=0.0):
        """
        cadastra um produto em uma categoria existente
        
        args
            nome_categoria (str) nome da categoria onde o produto sera adicionado
            produto_id (int) id unico do produto
            nome_produto (str) nome do produto
            preco (float) preco do produto
            descricao (str) descricao opcional
            avaliacao (float) avaliacao de 0 a 5
        
        returns
            bool true se cadastrou com sucesso false se a categoria nao existe
        
        complexidade Olog n para buscar a categoria mais O1 para adicionar na lista
        """
        # busca a categoria na arvore Olog n
        categoria = self.arvore_categorias.find(nome_categoria)
        
        if categoria is None:
            print(f"categoria {nome_categoria} nao encontrada")
            print("dica cadastre a categoria primeiro")
            return False
        
        # cria o objeto produto
        novo_produto = Produto(produto_id, nome_produto, preco, descricao, avaliacao)
        
        # adiciona o produto a categoria O1
        categoria.adicionar_produto(novo_produto)
        
        print(f"produto {nome_produto} adicionado a categoria {nome_categoria}")
        return True
    
    def remover_categoria(self, nome_categoria):
        """
        remove uma categoria do sistema
        
        args
            nome_categoria (str) nome da categoria a ser removida
        
        returns
            bool true se removeu com sucesso false se nao encontrou
        
        complexidade Olog n
        """
        categoria = self.arvore_categorias.find(nome_categoria)
        
        if categoria is None:
            print(f"categoria {nome_categoria} nao encontrada")
            return False
        
        # aviso se a categoria tem produtos
        if len(categoria.produtos) > 0:
            print(f"atencao a categoria tem {len(categoria.produtos)} produtos")
        
        self.arvore_categorias.delete(nome_categoria)
        print(f"categoria {nome_categoria} removida com sucesso")
        return True
    
    def buscar_categoria(self, nome_categoria):
        """
        busca uma categoria pelo nome
        
        args
            nome_categoria (str) nome da categoria
        
        returns
            categoria objeto categoria se encontrado none caso contrario
        
        complexidade Olog n
        """
        return self.arvore_categorias.find(nome_categoria)
    
    def listar_produtos_categoria(self, nome_categoria):
        """
        lista todos os produtos de uma categoria especifica
        
        args
            nome_categoria (str) nome da categoria
        
        returns
            list lista de produtos da categoria
        """
        categoria = self.arvore_categorias.find(nome_categoria)
        
        if categoria is None:
            print(f"categoria {nome_categoria} nao encontrada")
            return []
        
        if len(categoria.produtos) == 0:
            print(f"a categoria {nome_categoria} nao tem produtos cadastrados")
            return []
        
        print(f"\nprodutos da categoria {nome_categoria}")
        print(f"descricao {categoria.descricao}")
        print(f"total de produtos {len(categoria.produtos)}\n")
        
        for produto in categoria.produtos:
            print(f"{produto.nome} id {produto.id}")
            print(f"preco r$ {produto.preco:.2f} avaliacao {int(produto.avaliacao)} estrelas")
            if produto.descricao:
                print(f"{produto.descricao}")
            print()
        
        return categoria.produtos
