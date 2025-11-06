class AVLNode:
    def __init__(self, key, data=None):
        self.key = key
        self.data = data          
        self.left = None          
        self.right = None         
        self.height = 1           
