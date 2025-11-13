"""
modelos de dominio para o sistema de recomendaçao de produtos
"""

class Categoria:
    """representa uma categoria de produtos no marketplace"""
    
    def __init__(self, nome, descricao=""):
        self.nome = nome
        self.descricao = descricao
        self.produtos = []  # lista de produtos desta categoria
    
    def adicionar_produto(self, produto):
        """adiciona um produto a categoria"""
        self.produtos.append(produto)
    
    def remover_produto(self, produto_id):
        """remove um produto da categoria pelo ID"""
        self.produtos = [p for p in self.produtos if p.id != produto_id]
    
    def __repr__(self):
        return f"categoria(nome='{self.nome}', produtos={len(self.produtos)})"


class Produto:
    """representa um produto no marketplace"""
    
    def __init__(self, id, nome, preco, descricao="", avaliacao=0.0):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.avaliacao = avaliacao  # nota de 0 a 5
    
    def __repr__(self):
        return f"produto(id={self.id}, nome='{self.nome}', preco=R${self.preco:.2f})"