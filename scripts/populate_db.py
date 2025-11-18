"""
Script para popular o banco de dados com dados de teste
"""

from src.database import Database

def popular_banco():
    """Popula o banco de dados com dados de teste"""
    db = Database()
    
    # Limpar dados existentes
    print("  Limpando banco de dados existente...")
    db.limpar_tabelas()
    
    print("Populando banco de dados com dados de teste...")
    
    # Categorias principais (raiz)
    categorias_raiz = [
        ("Eletrônicos", "Dispositivos eletrônicos e gadgets"),
        ("Roupas", "Vestuário e acessórios"),
        ("Casa e Jardim", "Produtos para casa e jardim"),
        ("Esportes", "Equipamentos e acessórios esportivos"),
        ("Livros", "Livros físicos e digitais"),
    ]
    
    categoria_ids = {}
    
    # Inserir categorias raiz
    for nome, descricao in categorias_raiz:
        cat_id = db.inserir_categoria(nome, descricao)
        categoria_ids[nome] = cat_id
        print(f"  Categoria criada: {nome}")
    
    # Subcategorias de Eletrônicos
    subcat_eletronicos = [
        ("Smartphones", "Telefones celulares inteligentes", "Eletrônicos"),
        ("Notebooks", "Computadores portáteis", "Eletrônicos"),
        ("Tablets", "Tablets e dispositivos touch", "Eletrônicos"),
        ("Acessórios", "Acessórios para eletrônicos", "Eletrônicos"),
    ]
    
    for nome, descricao, pai in subcat_eletronicos:
        cat_id = db.inserir_categoria(nome, descricao, categoria_ids[pai])
        categoria_ids[nome] = cat_id
        print(f"  Subcategoria criada: {nome} (filho de {pai})")
    
    # Subcategorias de Roupas
    subcat_roupas = [
        ("Masculino", "Roupas masculinas", "Roupas"),
        ("Feminino", "Roupas femininas", "Roupas"),
        ("Infantil", "Roupas infantis", "Roupas"),
        ("Calçados", "Sapatos e tênis", "Roupas"),
    ]
    
    for nome, descricao, pai in subcat_roupas:
        cat_id = db.inserir_categoria(nome, descricao, categoria_ids[pai])
        categoria_ids[nome] = cat_id
        print(f"  Subcategoria criada: {nome} (filho de {pai})")
    
    # Subcategorias de Casa e Jardim
    subcat_casa = [
        ("Móveis", "Móveis para casa", "Casa e Jardim"),
        ("Decoração", "Itens de decoração", "Casa e Jardim"),
        ("Jardinagem", "Ferramentas e plantas", "Casa e Jardim"),
    ]
    
    for nome, descricao, pai in subcat_casa:
        cat_id = db.inserir_categoria(nome, descricao, categoria_ids[pai])
        categoria_ids[nome] = cat_id
        print(f"  Subcategoria criada: {nome} (filho de {pai})")
    
    # Subcategorias de Esportes
    subcat_esportes = [
        ("Fitness", "Equipamentos de academia", "Esportes"),
        ("Futebol", "Artigos de futebol", "Esportes"),
        ("Corrida", "Equipamentos para corrida", "Esportes"),
    ]
    
    for nome, descricao, pai in subcat_esportes:
        cat_id = db.inserir_categoria(nome, descricao, categoria_ids[pai])
        categoria_ids[nome] = cat_id
        print(f"  Subcategoria criada: {nome} (filho de {pai})")
    
    # Produtos - Smartphones
    produtos_smartphones = [
        ("iPhone 15 Pro", 8999.90, "iPhone 15 Pro 256GB, tela Super Retina XDR de 6.1 polegadas", 4.8),
        ("Samsung Galaxy S24 Ultra", 7499.00, "Galaxy S24 Ultra 256GB, câmera de 200MP", 4.7),
        ("Xiaomi 14 Pro", 4999.00, "Xiaomi 14 Pro 256GB, processador Snapdragon 8 Gen 3", 4.6),
        ("Google Pixel 8 Pro", 5999.00, "Pixel 8 Pro 128GB, câmera com IA", 4.5),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_smartphones:
        db.inserir_produto(nome, categoria_ids["Smartphones"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Notebooks
    produtos_notebooks = [
        ("MacBook Pro M3", 12999.00, "MacBook Pro 14 polegadas, chip M3, 512GB SSD", 4.9),
        ("Dell XPS 15", 8999.00, "Dell XPS 15, Intel i7, 16GB RAM, 512GB SSD", 4.7),
        ("Lenovo ThinkPad X1", 7999.00, "ThinkPad X1 Carbon, Intel i5, 16GB RAM", 4.6),
        ("ASUS ROG Strix", 6999.00, "ASUS ROG Strix G15, AMD Ryzen 7, RTX 3060", 4.5),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_notebooks:
        db.inserir_produto(nome, categoria_ids["Notebooks"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Tablets
    produtos_tablets = [
        ("iPad Pro 12.9", 8999.00, "iPad Pro 12.9 polegadas, chip M2, 256GB", 4.8),
        ("Samsung Galaxy Tab S9", 4999.00, "Galaxy Tab S9, 256GB, S Pen incluído", 4.6),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_tablets:
        db.inserir_produto(nome, categoria_ids["Tablets"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Acessórios
    produtos_acessorios = [
        ("AirPods Pro 2", 1999.00, "AirPods Pro 2ª geração, cancelamento de ruído ativo", 4.7),
        ("Mouse Logitech MX Master 3", 599.00, "Mouse sem fio Logitech MX Master 3", 4.6),
        ("Teclado Mecânico Keychron K8", 899.00, "Teclado mecânico sem fio, switches Gateron", 4.5),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_acessorios:
        db.inserir_produto(nome, categoria_ids["Acessórios"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Roupas Masculinas
    produtos_masculino = [
        ("Camiseta Básica Preta", 49.90, "Camiseta 100% algodão, cor preta", 4.3),
        ("Calça Jeans Slim", 199.90, "Calça jeans slim fit, lavagem escura", 4.4),
        ("Camisa Social Branca", 149.90, "Camisa social manga longa, 100% algodão", 4.5),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_masculino:
        db.inserir_produto(nome, categoria_ids["Masculino"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Roupas Femininas
    produtos_feminino = [
        ("Vestido Floral", 179.90, "Vestido midi com estampa floral", 4.6),
        ("Blusa Manga Longa", 89.90, "Blusa manga longa, tecido leve", 4.4),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_feminino:
        db.inserir_produto(nome, categoria_ids["Feminino"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Calçados
    produtos_calcados = [
        ("Tênis Nike Air Max", 699.90, "Tênis Nike Air Max 270, número 42", 4.7),
        ("Sapato Social Preto", 299.90, "Sapato social couro legítimo, preto", 4.5),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_calcados:
        db.inserir_produto(nome, categoria_ids["Calçados"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Móveis
    produtos_moveis = [
        ("Mesa de Jantar 6 Lugares", 2499.00, "Mesa de jantar em madeira maciça, 6 lugares", 4.5),
        ("Sofá Retrátil 3 Lugares", 2999.00, "Sofá retrátil cinza, 3 lugares", 4.6),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_moveis:
        db.inserir_produto(nome, categoria_ids["Móveis"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Fitness
    produtos_fitness = [
        ("Halteres Ajustáveis 20kg", 399.90, "Par de halteres ajustáveis, até 20kg cada", 4.4),
        ("Esteira Elétrica", 2999.00, "Esteira elétrica dobrável, 12 programas", 4.5),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_fitness:
        db.inserir_produto(nome, categoria_ids["Fitness"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Futebol
    produtos_futebol = [
        ("Bola de Futebol Oficial", 149.90, "Bola de futebol oficial, tamanho 5", 4.6),
        ("Chuteira Society", 299.90, "Chuteira society, número 42", 4.5),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_futebol:
        db.inserir_produto(nome, categoria_ids["Futebol"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    # Produtos - Livros
    produtos_livros = [
        ("Python Avançado", 89.90, "Livro sobre programação Python avançada", 4.7),
        ("Estruturas de Dados", 79.90, "Livro sobre estruturas de dados e algoritmos", 4.6),
        ("Clean Code", 99.90, "Código Limpo: Habilidades Práticas do Agile Software", 4.8),
    ]
    
    for nome, preco, descricao, avaliacao in produtos_livros:
        db.inserir_produto(nome, categoria_ids["Livros"], preco, descricao, avaliacao)
        print(f"  Produto criado: {nome}")
    
    print("\nBanco de dados populado com sucesso!")
    print(f"  - {len(categoria_ids)} categorias criadas")
    print(f"  - {sum([len(produtos_smartphones), len(produtos_notebooks), len(produtos_tablets), len(produtos_acessorios), len(produtos_masculino), len(produtos_feminino), len(produtos_calcados), len(produtos_moveis), len(produtos_fitness), len(produtos_futebol), len(produtos_livros)])} produtos criados")

if __name__ == "__main__":
    popular_banco()

