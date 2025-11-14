// visualizacao interativa da arvore avl

class TreeVisualizer {
    constructor() {
        this.container = document.getElementById('treeContainer');
        this.treeData = null;
        this.expandedNodes = new Set();
        this.nodeElements = new Map();
        this.init();
    }
    
    async init() {
        this.loadTreeData();
        this.render();
    }
    
    loadTreeData() {
        // dados estaticos de exemplo
        this.treeData = {
            root: {
                key: "Eletronicos",
                height: 3,
                data: {
                    nome: "Eletronicos",
                    descricao: "dispositivos eletronicos",
                    produtos: [
                        {id: 1, nome: "Smartphone", preco: 1500, avaliacao: 4.5},
                        {id: 2, nome: "Notebook", preco: 3000, avaliacao: 4.8}
                    ]
                },
                leftChild: {
                    key: "Alimentos",
                    height: 2,
                    data: {
                        nome: "Alimentos",
                        descricao: "produtos alimenticios",
                        produtos: [
                            {id: 3, nome: "Cafe Premium", preco: 25, avaliacao: 4.7}
                        ]
                    },
                    leftChild: null,
                    rightChild: {
                        key: "Esportes",
                        height: 1,
                        data: {
                            nome: "Esportes",
                            descricao: "equipamentos esportivos",
                            produtos: [
                                {id: 4, nome: "Tenis Running", preco: 299, avaliacao: 4.6}
                            ]
                        },
                        leftChild: null,
                        rightChild: null
                    }
                },
                rightChild: {
                    key: "Roupas",
                    height: 2,
                    data: {
                        nome: "Roupas",
                        descricao: "vestuario e acessorios",
                        produtos: [
                            {id: 5, nome: "Camiseta", preco: 49.90, avaliacao: 4.2}
                        ]
                    },
                    leftChild: {
                        key: "Livros",
                        height: 1,
                        data: {
                            nome: "Livros",
                            descricao: "literatura e educacao",
                            produtos: [
                                {id: 6, nome: "Python Avancado", preco: 89.90, avaliacao: 4.9}
                            ]
                        },
                        leftChild: null,
                        rightChild: null
                    },
                    rightChild: null
                }
            }
        };
    }
    
    showEmptyState() {
        this.container.innerHTML = `
            <div class="empty-tree">
                <div class="empty-tree-icon">🌳</div>
                <div>nenhuma categoria cadastrada</div>
                <div style="margin-top: 10px; font-size: 14px; color: #BBB;">
                    use a pagina cadastrar para adicionar categorias
                </div>
            </div>
        `;
    }
    
    render() {
        if (!this.treeData || !this.treeData.root) {
            this.showEmptyState();
            return;
        }
        
        this.container.innerHTML = '';
        this.nodeElements.clear();
        
        // renderizar apenas a raiz inicialmente no centro
        this.renderNode(this.treeData.root, 0, 0, -150, 0);
    }
    
    renderNode(node, level, x, y, index) {
        if (!node) return;
        
        const nodeId = `node-${node.key}-${index}`;
        
        // criar elemento do no
        const nodeEl = document.createElement('div');
        nodeEl.className = `tree-node level-${level}`;
        nodeEl.style.left = `50%`;
        nodeEl.style.top = `50%`;
        nodeEl.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
        nodeEl.id = nodeId;
        
        const hasChildren = node.leftChild || node.rightChild;
        const isExpanded = this.expandedNodes.has(nodeId);
        
        // pegar informacoes do no
        const nodeName = node.key || node.name || 'Sem nome';
        const nodeHeight = node.height || 0;
        const nodeFB = node.balanceFactor || 0;
        const productCount = node.data?.produtos?.length || 0;
        
        nodeEl.innerHTML = `
            <div style="font-size: 0.7em; opacity: 0.8; margin-bottom: 5px;">altura</div>
            <div style="font-size: 1.3em; font-weight: 600; margin-bottom: 8px;">${nodeName}</div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8em;">
                <span>FB ${nodeFB}</span>
                <span>${productCount} produtos</span>
            </div>
        `;
        
        // evento de clique para expandir
        if (hasChildren) {
            nodeEl.style.cursor = 'pointer';
            nodeEl.addEventListener('click', (e) => {
                e.stopPropagation();
                console.log('Clicou no no:', nodeName, 'ID:', nodeId);
                this.toggleNode(nodeId, node, level, x, y);
            });
        } else {
            nodeEl.style.cursor = 'default';
        }
        
        this.container.appendChild(nodeEl);
        this.nodeElements.set(nodeId, {element: nodeEl, node: node, x: x, y: y, level: level});
        
        // animar entrada
        setTimeout(() => {
            nodeEl.classList.add('visible');
        }, 50 + level * 100);
        
        // renderizar filhos se expandido
        if (isExpanded) {
            this.renderChildren(nodeId, node, level, x, y);
        }
    }
    
    renderChildren(parentId, parentNode, level, parentX, parentY) {
        const spacing = 350; // espacamento maior para nos maiores
        const childLevel = level + 1;
        const childY = parentY + 250; // mais espaco vertical
        
        if (parentNode.leftChild) {
            const leftX = parentX - spacing;
            this.renderNode(parentNode.leftChild, childLevel, leftX, childY, `${parentId}-left`);
            this.drawLine(parentX, parentY, leftX, childY);
        }
        
        if (parentNode.rightChild) {
            const rightX = parentX + spacing;
            this.renderNode(parentNode.rightChild, childLevel, rightX, childY, `${parentId}-right`);
            this.drawLine(parentX, parentY, rightX, childY);
        }
    }
    
    toggleNode(nodeId, node, level, x, y) {
        const nodeElement = document.getElementById(nodeId);
        
        if (this.expandedNodes.has(nodeId)) {
            // colapsar
            this.expandedNodes.delete(nodeId);
            if (nodeElement) {
                nodeElement.classList.remove('expanded');
            }
            this.removeChildren(nodeId);
        } else {
            // expandir
            this.expandedNodes.add(nodeId);
            if (nodeElement) {
                nodeElement.classList.add('expanded');
            }
            this.renderChildren(nodeId, node, level, x, y);
        }
    }
    
    removeChildren(parentId) {
        // remover todos os elementos filhos
        const toRemove = [];
        
        this.nodeElements.forEach((value, key) => {
            if (key.startsWith(`${parentId}-`)) {
                toRemove.push(key);
            }
        });
        
        toRemove.forEach(key => {
            const nodeData = this.nodeElements.get(key);
            if (nodeData && nodeData.element) {
                nodeData.element.remove();
            }
            this.nodeElements.delete(key);
        });
        
        // remover linhas conectoras
        const lines = this.container.querySelectorAll('.tree-line');
        lines.forEach(line => {
            const lineParent = line.dataset.parent;
            if (lineParent === parentId) {
                line.remove();
            }
        });
    }
    
    drawLine(x1, y1, x2, y2) {
        // desenhar linha conectora diagonal simples
        const line = document.createElement('div');
        line.className = 'tree-line';
        
        const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
        const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
        
        line.style.width = `${length}px`;
        line.style.height = '2px';
        line.style.left = '50%';
        line.style.top = '50%';
        line.style.transform = `translate(calc(-50% + ${x1}px), calc(-50% + ${y1 + 80}px)) rotate(${angle}deg)`;
        line.style.transformOrigin = '0 0';
        line.style.background = '#CCCCCC';
        
        this.container.appendChild(line);
        
        // animar entrada da linha
        setTimeout(() => {
            line.classList.add('visible');
        }, 200);
    }
}

// inicializar quando a pagina carregar
document.addEventListener('DOMContentLoaded', () => {
    const visualizer = new TreeVisualizer();
    
    // esconder o botao de popular dados pois ja tem dados estaticos
    const populateBtn = document.getElementById('populateBtn');
    if (populateBtn) {
        populateBtn.style.display = 'none';
    }
});
