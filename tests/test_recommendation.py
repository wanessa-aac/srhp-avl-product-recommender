# Testes unitários para SRHP-10: Recomendação por Categoria + Subcategorias

import pytest
import sys
import os

# Para importar o módulo 'avl_tree', adicionamos o diretório 'src' ao path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.avl_tree import AVLTree


# --- SRHP-10: Testes de Recomendação de Produtos ---


def test_recommendation_descendant_categories():
    """
    Valida que a recomendação retorna produtos da categoria
    e de todas as subcategorias descendentes.

    Estrutura de categorias (AVL balanceada):

                50 (Eletrônicos)
               /               \
         30 (Celulares)       70 (TVs)
           /      \
    20 (Smartphones) 40 (Feature Phones)

    Produtos:
        Eletrônicos(50): P1
        Celulares(30): P2, P3
        Smartphones(20): P4
        Feature Phones(40): P5

    Recomendação para categoria 30 -> {P2, P3, P4, P5}
    """

    tree = AVLTree()

    # Inserção de categorias (value contém dict com nome e produtos)
    tree.insert(50, {"nome": "Eletrônicos", "produtos": ["P1"]})
    tree.insert(30, {"nome": "Celulares", "produtos": ["P2", "P3"]})
    tree.insert(70, {"nome": "TVs", "produtos": []})
    tree.insert(20, {"nome": "Smartphones", "produtos": ["P4"]})
    tree.insert(40, {"nome": "Feature Phones", "produtos": ["P5"]})

    recomendados = tree.recommend(30)

    esperado = set(["P2", "P3", "P4", "P5"])

    assert set(recomendados) == esperado


def test_recommendation_single_category_no_children():
    """
    Categoria sem subcategorias deve retornar apenas seus próprios produtos.
    """

    tree = AVLTree()

    tree.insert(10, {"nome": "Periféricos", "produtos": ["Mouse", "Teclado"]})

    recomendados = tree.recommend(10)

    assert set(recomendados) == {"Mouse", "Teclado"}


def test_recommendation_invalid_category():
    """
    Categoria inexistente deve retornar lista vazia.
    """

    tree = AVLTree()

    tree.insert(10, {"nome": "Livros", "produtos": ["Livro1"]})

    recomendados = tree.recommend(999)

    assert recomendados == []


def test_recommendation_empty_tree():
    """
    Recomendação em árvore vazia deve retornar lista vazia.
    """

    tree = AVLTree()

    assert tree.recommend(10) == []
