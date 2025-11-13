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
    
    def imprimir_hierarquia(self):
        """
        imprime a arvore de categorias de forma hierarquica usando travessia preordem
        
        travessia preordem raiz esquerda direita
        isso mostra a hierarquia de forma natural pai antes dos filhos
        
        complexidade On visita todos os nos uma vez
        """
        print("\n" + "="*60)
        print("HIERARQUIA DE CATEGORIAS")
        print("="*60 + "\n")
        
        if self.arvore_categorias.root is None:
            print("sistema vazio nenhuma categoria cadastrada")
            return
        
        # chama a funcao recursiva de travessia
        self._imprimir_pre_ordem(self.arvore_categorias.root, nivel=0, prefixo="")
        
        print("\n" + "="*60)
    
    def _imprimir_pre_ordem(self, node, nivel=0, prefixo=""):
        """
        funcao recursiva auxiliar para travessia preordem com formatacao hierarquica
        
        args
            node no atual da arvore
            nivel nivel de profundidade para indentacao
            prefixo prefixo visual para mostrar a estrutura da arvore
        
        recursividade esta funcao chama a si mesma para percorrer a arvore
        """
        if node is None:
            return
        
        # determina o simbolo de conexao
        if nivel == 0:
            conector = ">"
        else:
            conector = "├──" if prefixo else "└──"
        
        # imprime o no atual preordem visita a raiz primeiro
        indentacao = "   " * nivel
        categoria = node.data
        
        print(f"{indentacao}{conector} {categoria.nome}")
        print(f"{indentacao}    {len(categoria.produtos)} produtos | Altura: {node.height}")
        
        if categoria.descricao:
            print(f"{indentacao}    {categoria.descricao}")
        
        # recursao visita subarvore esquerda
        if node.leftChild:
            self._imprimir_pre_ordem(node.leftChild, nivel + 1, "├──")
        
        # recursao visita subarvore direita
        if node.rightChild:
            self._imprimir_pre_ordem(node.rightChild, nivel + 1, "└──")
