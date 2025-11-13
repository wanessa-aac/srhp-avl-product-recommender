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

    # --- SRHP-08: Testes da Busca (Find) ---

def test_find_operation():
    """
    Testa a função 'find' (SRHP-08)
    """
    tree = AVLTree()
    # Usa uma sequência que força rotações (LR)
    tree.insert(30, "Categoria Eletrônicos")
    tree.insert(10, "Categoria Roupas")
    tree.insert(20, "Categoria Calçados")

    # Testa buscas por itens existentes (raiz, esquerda, direita)
    assert tree.find(20) == "Categoria Calçados"
    assert tree.find(10) == "Categoria Roupas"
    assert tree.find(30) == "Categoria Eletrônicos"

    # Testar busca por item não existente
    assert tree.find(99) is None

    # Testar busca em árvore vazia
    empty_tree = AVLTree()
    assert empty_tree.find(10) is None

# --- SRHP-09: Testes de Remoção (Delete) ---

def test_delete_leaf_node():
    """
    Testa a remoção de um nó folha (0 filhos).
    """
    tree = AVLTree()
    tree.insert(20, "data20")
    tree.insert(10, "data10")
    tree.insert(30, "data30")

    # Remove nó folha
    tree.delete(10)

    assert tree.find(10) is None
    assert tree.root.key == 20
    assert tree.root.leftChild is None
    assert tree.root.rightChild.key == 30

def test_delete_node_with_one_child():
    """
    Testa a remoção de um nó com um filho.
    """
    tree = AVLTree()
    tree.insert(20, "data20")
    tree.insert(10, "data10")
    tree.insert(30, "data30")
    tree.insert(5, "data5") # Adiciona um filho ao 10

    # Remove o nó 10 (que tem 1 filho: 5)
    tree.delete(10)

    assert tree.find(10) is None
    assert tree.root.key == 20
    assert tree.root.leftChild.key == 5 # O filho 5 deve "subir"
    assert tree.root.rightChild.key == 30

def test_delete_node_with_two_children():
    """
    Testa a remoção de um nó com 2 filhos (o 'root' neste caso)
    """
    tree = AVLTree()
    tree.insert(20, "data20") # Root
    tree.insert(10, "data10") # left
    tree.insert(30, "data30") # right

    # Remove o nó 20 (que tem 2 filhos)
    # O sucessor in-order (menor da direita) é 30.
    tree.delete(20)

    assert tree.find(20) is None
    # O Sucessor (30) deve se tornar a nova raiz
    # (neste caso simples, pois 30 não tinha filhos)
    assert tree.root.key == 30
    assert tree.root.leftChild.key == 10
    assert tree.root.rightChild is None

def test_delete_triggers_rebalance_BR():
    """
    Testa se a remoção de um nó força um relacionamento (Caso BR).
    """
    tree = AVLTree()
    # Inserir nós para formar uma árvore balanceada
    tree.insert(10, "data10")
    tree.insert(5, "data5")
    tree.insert(20, "data20")
    tree.insert(25, "data25") # Árvore: 10(L:5, R:20(R:25))

    # Agora, removemos o nó 5.
    # A árvore fica 10(L: None, R:20(R:25))
    # O nó 10 fica com FB = -2.
    # O seu filho direito (20) tem FB = -1.
    # Isso força uma Rotação Esquerda (RR).
    tree.delete(5)

    # A raiz deve ter mudado para 20
    assert tree.root.key == 20
    assert tree.root.leftChild.key == 10
    assert tree.root.rightChild.key == 25
    assert tree.find(5) is None