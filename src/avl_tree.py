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
                           self._get_height(y.rightChild))
        # Retorna a nova raiz da sub-árvore
        return y
    
    def delete(self, key):
        """
        Função pública de remoção.
        Chama a função recursiva privada para remover da raiz.
        """
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        """
        SRHP-07: Implementar Remoção Balanceada (Recursiva)
        """

        # --- Fase 1:  Remoção BST Padrão (Recursiva) ---

        # Caso base: Nó não encontrado ou árvore vazia
        if not node:
            return node
        
        # Busca recursiva
        if key < node.key:
            node.leftChild = self._delete_recursive(node.leftChild, key)
        elif key > node.key:
            node.rightChild = self._delete_recursive(node.rightChild, key)
        else:
            # Nó encontrado! Agora tratamos os 3 casos de remoção:

            # Caso 1: Nó com 0 ou 1 filho (esquerda ou direita)
            if node.leftChild is None:
                temp = node.rightChild
                node = None # Libera o nó
                return temp # Retorna o filho (ou None se for 0 filhos)
            elif node.rightChild is None:
                temp = node.leftChild
                node = None # Libera o nó
                return temp # Retorna o filho
            
            # caso 2: Nó com 2 filhos
            # Pega o sucessor in-ordem (o menor nó da sub-árvore direita)
            temp = self._get_min_value_node(node.rightChild)

            # Copia os dados do sucessor para este nó
            node.key = temp.key
            node.data = temp.data

            # Remove o sucessor (que agora é uma duplicata)
            # da sub-árvore direita. Essa remoção cairá no caso 1
            # (pois o sucessor tem no máximo 1 filho à direita).
            node.rightChild = self._delete_recursive(node.rightChild, temp.key)

        # Se a árvore ficou vazia após a remoção (só tinha 1 nó)
        if not node:
            return node
            
        # --- Fase 2: Rebalancemento (Bottom-Up) ---
        # Este código é executado "no caminho de volta" da recursão.

        # 1. Atualizar a Altura do nó atual
        node.height = 1 + max(self._get_height(node.leftChild),
                            self._get_height(node.rightChild))
        
        # 2. Calcular o Fator de Balanceamento (FB)
        balance = self._get_balance(node)

        # 3. Rebalancemento (4 Casos)

        # ---- Caso 1: Rotação Simples Direita (LL) ----
        #FB > 1 (pesado à esquerda) e FBdo filho esquerdo >= 0
        if balance > 1 and self._get_balance(node.leftChild) >= 0:
            return self._right_rotate(node)
        
        # --- Caso 2: Rotação Simples Esquerda (RR) ----
        # FB < -1 (pesado à direita) e FB do filho direito <= 0
        if balance < -1 and self._get_balance(node.rightChild) <= 0:
            return self._left_rotate(node)
        
        # --- Caso 3: Rotação Dupla Esquerda-Direita (LR) ---
        # FB > 1 (pesado à esquerda) e FB do filho esquerdo < 0
        if balance > 1 and self._get_balance(node.leftChild) < 0:
            node.leftChild = self._left_rotate(node.leftChild)
            return self._right_rotate(node)
        
        # --- Caso 4: Rotação Dupla Direita-Esquerda (RL) ---
        # FB < -1 (pesado à direita) e FB do filho direito > 0 
        if balance < -1 and self._get_balance(node.rightChild) > 0:
            node.rightChild = self._right_rotate(node.rightChild)
            return self._left_rotate(node)

        # Retorna o nó (potencialmente nova raiz da sub-árvore)
        return node

    def _get_min_value_node(self, node):
        """
        Função auxiliar para encontrar o nó com menor valor (sucessor in-order)
        numa sub-árvore. Vai sempre o mais à esquerda possível.
        """
        current = node
        while current.leftChild is not None:
            current = current.leftChild
        return current
        
    def find(self, key):
        """
        Função pública de busca.
        Chama a função recursiva privada para buscar na raiz.
        """
        return self._find_recursive(self.root, key)

    def _find_recursive(self, node, key):
        """
        SRHP-08: Implementar Busca (O(log n))
        Busca recursivamente pela chave.
        Retorna o 'data' (objeto Categoria) se encontar, ou None.
        """
        # Caso base 1: Não encontrou (chegou a uma folha nula)
        if not node:
            return None
        
        # Caso base 2: Encontrou
        if key == node.key:
            return node.data  # Retorna o dado (ex: objeto Categoria)
        
        # Passos recursivos
        if key < node.key:
            # Se a chave for menor, busca na sub-árvore esquerda
            return self._find_recursive(node.leftChild, key)
        else:
            # Se a chave for maior, busca na sub-árvore direita
            return self._find_recursive(node.rightChild, key)
        

    def _find_node(self, node, key):
        """
        Retorna o objeto `AVLNode` cujo `key` corresponde ao solicitado,
        ou `None` se não existir. Implementado como método interno para
        permitir operações que precisam do nó (por exemplo, varredura de subárvore).
        """
        if not node:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._find_node(node.leftChild, key)
        return self._find_node(node.rightChild, key)

    def recommend(self, key):
        """
        Retorna uma lista de produtos recomendados para a categoria `key`.

        Comportamento esperado (seguindo os testes SRHP-10):
        - Se a `key` não existir na árvore, retorna lista vazia.
        - Se existir, retorna os produtos da categoria e de todas as
          subcategorias descendentes (varredura DFS a partir do nó).

        A função assume que os `data` armazenados nos nós são dicionários
        contendo a chave 'produtos' (lista). Se o formato for diferente,
        apenas ignora e não adiciona elementos.
        """
        root_node = self._find_node(self.root, key)
        if root_node is None:
            return []

        resultados = []

        def dfs(n):
            if not n:
                return
            data = n.data
            # aceitar estruturas onde 'produtos' é uma lista
            if isinstance(data, dict) and 'produtos' in data and data['produtos']:
                resultados.extend(data['produtos'])
            dfs(n.leftChild)
            dfs(n.rightChild)

        dfs(root_node)
        return resultados
    