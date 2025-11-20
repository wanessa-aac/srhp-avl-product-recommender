"""
Script de visualização para os testes de recomendação (SRHP-10).
Mostra a estrutura da árvore AVL, os produtos de cada categoria,
e o resultado da recomendação de forma visual e interativa.
"""

import sys
import os

# Para importar o módulo 'avl_tree', adicionamos o diretório 'src' ao path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.avl_tree import AVLTree


def print_tree(node, prefix="", is_left=None):
    """
    Imprime a árvore AVL de forma visual com indentação e ramificações.
    """
    if node is None:
        return

    if is_left is None:
        # Raiz
        print(f"🌳 {node.key}")
    else:
        # Nó não-raiz
        connector = "├── " if is_left else "└── "
        print(f"{prefix}{connector}{node.key}")

    if node.leftChild is not None or node.rightChild is not None:
        if node.leftChild is not None:
            new_prefix = prefix + ("│   " if is_left else "    ")
            print_tree(node.leftChild, new_prefix, True)
        if node.rightChild is not None:
            new_prefix = prefix + ("│   " if is_left else "    ")
            print_tree(node.rightChild, new_prefix, False)


def print_category_details(tree, keys):
    """
    Mostra detalhes de cada categoria (nome e produtos).
    """
    print("\n📋 Detalhes das Categorias:")
    print("-" * 60)
    for key in keys:
        data = tree.find(key)
        if data:
            nome = data.get("nome", "Sem nome")
            produtos = data.get("produtos", [])
            produtos_str = ", ".join(produtos) if produtos else "(nenhum)"
            print(f"  Categoria {key}: {nome}")
            print(f"    └─ Produtos: {produtos_str}")
    print()


def visualize_test_1():
    """
    Teste 1: Recomendação com descendentes.
    """
    print("\n" + "=" * 60)
    print("TESTE 1: Recomendação com Descendentes")
    print("=" * 60)

    tree = AVLTree()

    # Inserção de categorias
    tree.insert(50, {"nome": "Eletrônicos", "produtos": ["P1"]})
    tree.insert(30, {"nome": "Celulares", "produtos": ["P2", "P3"]})
    tree.insert(70, {"nome": "TVs", "produtos": []})
    tree.insert(20, {"nome": "Smartphones", "produtos": ["P4"]})
    tree.insert(40, {"nome": "Feature Phones", "produtos": ["P5"]})

    print("\n🌲 Estrutura da Árvore:")
    print_tree(tree.root)

    print_category_details(tree, [50, 30, 70, 20, 40])

    # Teste a recomendação
    print("🔍 Recomendação para Categoria 30 (Celulares):")
    recomendados = tree.recommend(30)
    esperado = {"P2", "P3", "P4", "P5"}
    resultado = "✅ PASSOU" if set(recomendados) == esperado else "❌ FALHOU"

    print(f"  Resultado: {recomendados}")
    print(f"  Esperado:  {list(esperado)}")
    print(f"  Status: {resultado}")


def visualize_test_2():
    """
    Teste 2: Categoria sem filhos.
    """
    print("\n" + "=" * 60)
    print("TESTE 2: Categoria sem Subcategorias")
    print("=" * 60)

    tree = AVLTree()
    tree.insert(10, {"nome": "Periféricos", "produtos": ["Mouse", "Teclado"]})

    print("\n🌲 Estrutura da Árvore:")
    print_tree(tree.root)

    print_category_details(tree, [10])

    print("🔍 Recomendação para Categoria 10 (Periféricos):")
    recomendados = tree.recommend(10)
    esperado = {"Mouse", "Teclado"}
    resultado = "✅ PASSOU" if set(recomendados) == esperado else "❌ FALHOU"

    print(f"  Resultado: {recomendados}")
    print(f"  Esperado:  {list(esperado)}")
    print(f"  Status: {resultado}")


def visualize_test_3():
    """
    Teste 3: Categoria inválida.
    """
    print("\n" + "=" * 60)
    print("TESTE 3: Categoria Inexistente")
    print("=" * 60)

    tree = AVLTree()
    tree.insert(10, {"nome": "Livros", "produtos": ["Livro1"]})

    print("\n🌲 Estrutura da Árvore:")
    print_tree(tree.root)

    print_category_details(tree, [10])

    print("🔍 Recomendação para Categoria 999 (inexistente):")
    recomendados = tree.recommend(999)
    esperado = []
    resultado = "✅ PASSOU" if recomendados == esperado else "❌ FALHOU"

    print(f"  Resultado: {recomendados}")
    print(f"  Esperado:  {esperado}")
    print(f"  Status: {resultado}")


def visualize_test_4():
    """
    Teste 4: Árvore vazia.
    """
    print("\n" + "=" * 60)
    print("TESTE 4: Árvore Vazia")
    print("=" * 60)

    tree = AVLTree()

    print("\n🌲 Estrutura da Árvore:")
    if tree.root is None:
        print("  (Árvore vazia)")

    print("\n🔍 Recomendação para Categoria 10 (em árvore vazia):")
    recomendados = tree.recommend(10)
    esperado = []
    resultado = "✅ PASSOU" if recomendados == esperado else "❌ FALHOU"

    print(f"  Resultado: {recomendados}")
    print(f"  Esperado:  {esperado}")
    print(f"  Status: {resultado}")


def main():
    """
    Executa todos os testes de visualização.
    """
    print("\n" + "=" * 60)
    print("VISUALIZAÇÃO DOS TESTES DE RECOMENDAÇÃO (SRHP-10)")
    print("=" * 60)

    visualize_test_1()
    visualize_test_2()
    visualize_test_3()
    visualize_test_4()

    print("\n" + "=" * 60)
    print("✨ Visualização Completa!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
