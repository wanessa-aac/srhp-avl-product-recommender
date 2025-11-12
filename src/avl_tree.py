class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data          
        self.leftChild = None          
        self.rightChild = None         
        self.height = 1   # altura da folha

class AVLTree:
    """
    Implementa a Árvore AVL regular.
    As operações não dependem de um tipo específico de negócio (lidam com 'key' e 'data').
    """
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        """
        Função pública de inserção na árvore AVL.
        Chama a função recursiva privada para inserir na raiz.
        """
        self.root = self._insert_recursive(self.root, key, data)

    def _insert_recursive(self, node, key, data):
        """
        SRHP-02: Inserção Recursiva
        Esta função realiza uma descida recursiva na árvore para localizar a posição de inserção,
        de forma semelhante a uma Árvore Binária de Busca (BST) convencional. 
        Em seguida, procede ao rebalanceamento da árvore durante o retorno (de baixo para cima, bottom-up).
        """

        # 1. Inserção BST Padrão (Recursiva)
        if not node:
            # Se encontrar um espaço vazio, crie um novo nó.
            return AVLNode( key, data)
        elif key < node.key:
            node.leftChild = self._insert_recursive(node.leftChild, key, data)
        else:
            # Aqui, estamos evitando chaves duplicadas. Se a chave for igual ou maior que a atual, insere à direita.
            node.rightChild = self._insert_recursive(node.rightChild, key, data)

        # 2. Atualização da Altura do Nó Atual (Ancestral)
        # (Depois de adicionar um novo nó abaixo dele)
        node.height = 1 + max(self._get_height(node.leftChild), self._get_height(node.rightChild))

        # 3. Calcular o Fator de Balanceamento (FB)
        balance = self._get_balance(node)

        # 4. Rebalancemento (SRHP-04 e SRHP-05)
        # Se o nó ficou desbalanceado, existem 4 casos:

        # ---- Caso 1: Rotação Simples Direta (LL) ----
        # Fator Balanceamento > 1 (árvore pesada à esquerda) e a chave foi inserida 
        # na sub-árvore esquerda (key < node.leftChild.key)
        if balance > 1 and key < node.leftChild.key:
            return self._right_rotate(node)

        # --- Caso 2: Rotação Simples Esquerda (RR) ----
        # Fator Balanceamento < -1 (árvore pesada à direita) e a chave foi inserida 
        # na sub-árvore direita (key > node.rightChild.key)
        if balance < -1 and key > node.rightChild.key:
            return self._left_rotate(node)

        # --- Caso 3: Rotação Dupla Esquerda-Direita (LR) ---
        # Fator Balanceamento > 1 (árvore pesada à esquerda) e a chave foi inserida
        # na sub-árvore direita (key > node.leftChild.key)
        if balance > 1 and key > node.leftChild.key:
            node.leftChild = self._left_rotate(node.leftChild) # Rotacão Esquerda no filho
            return self._right_rotate(node)                   # Rotação Direita no pai
        
        # --- Caso 4: Rotação Dupla Direita-Esquerda (RL) ---
        # Fator Balanceamento < -1 (árvore pesada à direita) e a chave foi inserida
        # na sub-árvore esquerda (key < node.rightChild.key)
        if balance < -1 and key < node.rightChild.key:
            node.rightChild = self._right_rotate(node.rightChild) # Rotação Direita no filho
            return self._left_rotate(node)                         # Rotação Esquerda no pai
        
        # Se não houver desbalanceamento, retorne o nó (atualizado)
        return node

    # ---- Funções Auxiliares (SRHP-03 e SRHP-04) ----

    def _get_height(self, node):
        """
        SRHP-03: Implementar Cálculo de Altura
        Essa função retorna a altura de um nó. Se o nó for Nulo (None), 
        ela retorna 0, o que simplifica bastante os cálculos.
        """
        if not node:
            return 0
        return node.height
    
    def _get_balance(self, node):
        """
        SRHP-03: Implementar Cálculo de Fator de Balanceamento (FB)
        FB = Altura(Direita) - Altura(Esquerda)
        Se FB > 1: lado esquerdo está mais pesado.
        Se FB < -1: lado direito está mais pesado.
        """
        if not node:
            return 0
        return self._get_height(node.leftChild) - self._get_height(node.rightChild)
    
    def _right_rotate(self, z):
        """
        SRHP-04: Implementar Rotação Simples Direita (LL)
        Executa uma rotação à direita no nó 'z' (o nó desbalanceado).
        
             z (FB=2)         y
            / \              / \
           y  T3    ->      x   z
          / \              / \ / \
         x  T2            T1 T2 T3
        / \
       T1 T4 (T4 não existe neste caso)
        """
        print("Executando rotação direita (LL)")
        y = z.leftChild
        T2 = y.rightChild

        # Executa a rotação
        y.rightChild = z
        z.leftChild = T2

        # Atualiza as alturas (OBS: Atualizar 'z' primeiro, já que ele agora é filho de 'y')
        z.height = 1 + max(self._get_height(z.leftChild),
                           self._get_height(z.rightChild))
        y.height = 1 + max(self._get_height(y.leftChild),
                           self._get_height(y.rightChild))
        # Retorna a nova raiz da sub-árvore
        return y
    
    def _left_rotate(self, z):
        """
        SRHP-04: Implementar Rotação Simples Esquerda (RR)
        Executa uma rotação à esquerda no nó 'z' (o nó desbalanceado).

           z (FB=-2)           y
          / \                 / \
         T1  y       ->      z   x
            / \             / \ / \
           T2  x           T1 T2 T3
              / \
             T3 T4 (T4 não existe neste caso)
        """
        print("Executando Rotação Esquerda (RR)")
        y = z.rightChild
        T2 = y.leftChild

        # Executa a rotação
        y.leftChild = z
        z.rightChild = T2

        # Atualiza as alturas (OBS: Atualizar 'z' primeiro)
        z.height = 1 + max(self._get_height(z.leftChild),
                           self._get_height(z.rightChild))
        y.height = 1 + max(self._get_height(y.leftChild),
                           self._get_height(z.rightChild))
        # Retorna a nova raiz da sub-árvore
        return y