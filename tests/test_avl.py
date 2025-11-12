# Testes unitários para SRHP-06 e SRHP08

import pytest
import sys
import os

# Para importar o módulo ‘avl_tree’, precisamos adicionar o diretório ‘src’ ao path do Python. 
# Isso é essencial se o ‘srhp_project’ não estiver instalado como um pacote.  
# Execute o seguinte comando: sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ‘..’)))

from src.avl_tree import AVLTree

# --- SRHP-06: Testes de Rotação Específicos ---

def test_rotation_LL_right_simple():
    """
    Força uma Rotação Simples Direita (LL).
    Inserir 30, 20, 10 (em ordem decrescente).
    O nó 30 fica com FB=2.
    """
    tree = AVLTree()
    tree.insert(30, "data30")
    tree.insert(20, "data20")
    tree.insert(10, "data10")  # <--- Força a rotação LL no nó 30

    # A raiz deve ter mudado para 20
    assert tree.root.key == 20
    #Filhos devem estar corretos
    assert tree.root.leftChild.key == 10
    assert tree.root.rightChild.key == 30

def test_rotation_RR_left_simple():
    """"
    Força uma Rotação Simples Esquerda (RR).
    Inserir 10, 20, 30 (em ordem crescente).
    O nó 10 fica com FB=-2.
    """
    tree = AVLTree()
    tree.insert(10, "data10")
    tree.insert(20, "data20")
    tree.insert(30, "data30")  # <--- Força a rotação RR no nó 10

    # A raiz deve ter mudado para 20
    assert tree.root.key == 20
    # Filhos devem estar corretos
    assert tree.root.leftChild.key == 10
    assert tree.root.rightChild.key == 30

def test_rotation_LR_left_right():
    """
    Força uma Rotação Dupla Esquerda-Direita (LR).
    Inserir 30, 10, 20.
    O nó 30 fica com FB=2
    """
    tree = AVLTree()
    tree.insert(30, "data30")
    tree.insert(10, "data10")
    tree.insert(20, "data20")  # <--- Força a rotação LR no nó 30

    # A raiz deve ter mudado para 20
    assert tree.root.key == 20
    # Filhos devem estar corretos
    assert tree.root.leftChild.key == 10
    assert tree.root.rightChild.key == 30

def test_rotation_RL_right_left():
    """
    Força uma rotação Dupla Direita-Esquerda (RL).
    Inserir 10, 30, 20.
    O nó 10 fica com FB=-2.
    """
    tree = AVLTree()
    tree.insert(10, "data10")
    tree.insert(30, "data30")
    tree.insert(20, "data20")  # <--- Força a rotação RL no nó 10

    # A raiz deve ter mudado para 20
    assert tree.root.key == 20
    # Filhos devem estar corretos
    assert tree.root.leftChild.key == 10
    assert tree.root.rightChild.key == 30