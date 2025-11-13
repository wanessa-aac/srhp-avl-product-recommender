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
    
    def _buscar_node(self, node, chave):
        """
        busca recursiva que retorna o NO nao apenas o data da AVL
        necessario para iniciar a travessia da subarvore
        
        args
            node no atual
            chave chave a ser buscada
        
        returns
            AVLNode no encontrado ou None
        """
        if node is None:
            return None
        
        if chave == node.key:
            return node
        elif chave < node.key:
            return self._buscar_node(node.leftChild, chave)
        else:
            return self._buscar_node(node.rightChild, chave)
    
    def _coletar_produtos_recursivo(self, node, lista_produtos, lista_categorias):
        """
        recursao principal coleta produtos de um no e todos os seus descendentes
        
        usa travessia inordem esquerda raiz direita para coletar produtos
        de forma organizada
        
        args
            node no atual da AVL
            lista_produtos lista acumuladora de produtos passada por referencia
            lista_categorias lista de nomes de categorias visitadas
        
        recursividade esta funcao explora TODA a subarvore a partir do no dado
        complexidade Om onde m e o numero de nos na subarvore
        """
        if node is None:
            return
        
        # recursao processa subarvore esquerda primeiro
        self._coletar_produtos_recursivo(node.leftChild, lista_produtos, lista_categorias)
        
        # processa o no atual coleta produtos desta categoria
        categoria = node.data
        lista_categorias.append(categoria.nome)
        
        # adiciona todos os produtos desta categoria a lista de recomendacoes
        for produto in categoria.produtos:
            lista_produtos.append({
                'produto': produto,
                'categoria': categoria.nome
            })
        
        # recursao processa subarvore direita
        self._coletar_produtos_recursivo(node.rightChild, lista_produtos, lista_categorias)
    
    def recomendar_produtos(self, nome_categoria, ordenar_por="avaliacao", limite=None):
        """
        recomenda produtos de uma categoria e todas as suas subcategorias
        
        esta e a funcionalidade CORE do sistema de recomendacao
        usa travessia recursiva para coletar produtos de toda a subarvore
        
        args
            nome_categoria (str) nome da categoria raiz
            ordenar_por (str) avaliacao preco_asc preco_desc nome
            limite (int) numero maximo de produtos a retornar None para todos
        
        returns
            list lista de produtos recomendados
        
        complexidade Olog n para buscar mais Om para percorrer m nos da subarvore
        """
        # busca a categoria na arvore Olog n
        node = self._buscar_node(self.arvore_categorias.root, nome_categoria)
        
        if node is None:
            print(f"categoria {nome_categoria} nao encontrada")
            return []
        
        print(f"\nRECOMENDACOES baseadas em {nome_categoria}")
        print(f"incluindo produtos de subcategorias\n")
        
        # coleta produtos recursivamente de toda a subarvore
        produtos_recomendados = []
        categorias_visitadas = []
        
        self._coletar_produtos_recursivo(node, produtos_recomendados, categorias_visitadas)
        
        # mostra estatisticas
        print(f"Estatisticas da busca")
        print(f"categorias visitadas {len(categorias_visitadas)}")
        print(f"produtos encontrados {len(produtos_recomendados)}")
        print(f"categorias {', '.join(categorias_visitadas)}\n")
        
        if len(produtos_recomendados) == 0:
            print("nenhum produto encontrado nesta categoria ou subcategorias")
            return []
        
        # ordena os produtos
        produtos_ordenados = self._ordenar_produtos(produtos_recomendados, ordenar_por)
        
        # aplica limite se especificado
        if limite:
            produtos_ordenados = produtos_ordenados[:limite]
        
        # exibe os produtos
        self._exibir_recomendacoes(produtos_ordenados, ordenar_por)
        
        return produtos_ordenados
    
    def _ordenar_produtos(self, produtos_com_categoria, criterio):
        """
        ordena a lista de produtos conforme o criterio especificado
        
        args
            produtos_com_categoria lista de dicts produto Produto categoria str
            criterio avaliacao preco_asc preco_desc nome
        
        returns
            list lista ordenada
        """
        if criterio == "avaliacao":
            return sorted(produtos_com_categoria, 
                         key=lambda x: x['produto'].avaliacao, 
                         reverse=True)
        elif criterio == "preco_asc":
            return sorted(produtos_com_categoria, 
                         key=lambda x: x['produto'].preco)
        elif criterio == "preco_desc":
            return sorted(produtos_com_categoria, 
                         key=lambda x: x['produto'].preco, 
                         reverse=True)
        elif criterio == "nome":
            return sorted(produtos_com_categoria, 
                         key=lambda x: x['produto'].nome)
        else:
            return produtos_com_categoria
    
    def _exibir_recomendacoes(self, produtos_ordenados, criterio):
        """exibe os produtos recomendados de forma formatada"""
        print(f"TOP RECOMENDACOES ordenado por {criterio}")
        print("-" * 70)
        
        for i, item in enumerate(produtos_ordenados, 1):
            produto = item['produto']
            categoria = item['categoria']
            
            print(f"{i}. {produto.nome} ID {produto.id}")
            print(f"   Categoria {categoria}")
            print(f"   Preco R$ {produto.preco:.2f} | Avaliacao {int(produto.avaliacao)} estrelas ({produto.avaliacao:.1f}/5.0)")
            
            if produto.descricao:
                print(f"   {produto.descricao}")
            
            print()
