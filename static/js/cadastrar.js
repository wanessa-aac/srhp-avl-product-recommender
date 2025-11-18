// pagina de cadastro

class CadastroPage {
    constructor() {
        this.formContainer = document.getElementById('formContainer');
        this.cadastradosContainer = document.getElementById('cadastradosContainer');
        this.categorias = [];
        this.produtos = [];
        
        this.init();
        this.carregarDados();
    }
    
    async carregarDados() {
        // carregar categorias e produtos do backend
        await this.carregarCategorias();
        await this.carregarProdutos();
    }
    
    async carregarCategorias() {
        try {
            const response = await fetch('/api/categorias');
            this.categorias = await response.json();
        } catch (error) {
            console.error('erro ao carregar categorias:', error);
            this.categorias = [];
        }
    }
    
    async carregarProdutos() {
        try {
            const response = await fetch('/api/produtos');
            this.produtos = await response.json();
        } catch (error) {
            console.error('erro ao carregar produtos:', error);
            this.produtos = [];
        }
    }
    
    init() {
        // eventos das abas
        this.categoriaBtn = document.querySelector('.tab-button.categoria');
        this.produtoBtn = document.querySelector('.tab-button.produto');
        this.tabsContainer = document.querySelector('.tabs-container');
        
        if (this.categoriaBtn && this.produtoBtn) {
            this.categoriaBtn.addEventListener('click', () => this.showCategoriaForm());
            this.produtoBtn.addEventListener('click', () => this.showProdutoForm());
        }
        
        // eventos do ver lista
        this.verListaBtn = document.getElementById('verListaBtn');
        this.listaOptions = document.getElementById('listaOptions');
        
        if (this.verListaBtn && this.listaOptions) {
            this.verListaBtn.addEventListener('click', () => this.toggleListaOptions());
            
            // eventos dos botoes de opcao
            const listaBtns = document.querySelectorAll('.lista-option-btn');
            listaBtns.forEach(btn => {
                btn.addEventListener('click', () => {
                    const listType = btn.getAttribute('data-list');
                    if (listType === 'categorias') {
                    this.mostrarCategorias();
                } else if (listType === 'produtos') {
                    this.mostrarProdutos();
                }
                // fechar o dropdown
                this.listaOptions.style.display = 'none';
                this.verListaBtn.classList.remove('active');
                });
            });
        }
    }
    
    toggleListaOptions() {
        if (this.listaOptions.style.display === 'none') {
            this.listaOptions.style.display = 'flex';
            this.verListaBtn.classList.add('active');
        } else {
            this.listaOptions.style.display = 'none';
            this.verListaBtn.classList.remove('active');
        }
    }
    
    showCategoriaForm() {
        // esconder as abas
        this.tabsContainer.classList.add('hidden');
        
        this.formContainer.innerHTML = `
            <div class="form-header">
                <span class="form-header-text">cadastro</span>
                <span class="form-header-text">categoria</span>
            </div>
            
            <div class="form-field">
                <label class="form-label">nome da categoria*</label>
                <input type="text" class="form-input" id="categoriaNome" placeholder="">
            </div>
            
            <div class="form-field">
                <label class="form-label">categoria pai (opcional)</label>
                <select class="form-select" id="categoriaPai">
                    <option value="">Selecione</option>
                    ${this.categorias.map(cat => `<option value="${cat.nome}">${cat.nome}</option>`).join('')}
                </select>
            </div>
            
            <button class="btn-submit" onclick="cadastroPage.cadastrarCategoria()">cadastrar</button>
        `;
        
        this.formContainer.style.display = 'block';
    }
    
    showProdutoForm() {
        // esconder as abas
        this.tabsContainer.classList.add('hidden');
        
        this.formContainer.innerHTML = `
            <div class="form-header">
                <span class="form-header-text">cadastro</span>
                <span class="form-header-text">produto</span>
            </div>
            
            <div class="form-field">
                <label class="form-label">nome da categoria*</label>
                <input type="text" class="form-input" id="produtoNome" placeholder="">
            </div>
            
            <div class="form-field">
                <label class="form-label">categoria*</label>
                <select class="form-select" id="produtoCategoria">
                    <option value="">Selecione</option>
                    ${this.categorias.map(cat => `<option value="${cat.nome}">${cat.nome}</option>`).join('')}
                </select>
            </div>
            
            <div class="form-field">
                <label class="form-label">preço (R$)*</label>
                <input type="number" step="0.01" min="0" class="form-input" id="produtoPreco" placeholder="">
            </div>
            
            <div class="form-field">
                <label class="form-label">descrição (opcional)</label>
                <textarea class="form-textarea" id="produtoDescricao" placeholder=""></textarea>
            </div>
            
            <button class="btn-submit produto" onclick="cadastroPage.cadastrarProduto()">cadastrar</button>
        `;
        
        this.formContainer.style.display = 'block';
    }
    
    async cadastrarCategoria() {
        const nome = document.getElementById('categoriaNome').value.trim();
        const categoriaPaiId = document.getElementById('categoriaPai').value;
        
        if (!nome) {
            alert('por favor, preencha o nome da categoria');
            return;
        }
        
        try {
            const response = await fetch('/api/categorias', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nome: nome,
                    descricao: '',
                    categoria_pai_id: categoriaPaiId ? parseInt(categoriaPaiId) : null
                })
            });
            
            if (response.ok) {
                alert('categoria cadastrada com sucesso!');
                // recarregar categorias
                await this.carregarCategorias();
                // limpar formulario
                document.getElementById('categoriaNome').value = '';
                document.getElementById('categoriaPai').value = '';
            } else {
                const error = await response.json();
                alert('erro ao cadastrar categoria: ' + error.detail);
            }
        } catch (error) {
            console.error('erro:', error);
            alert('erro ao cadastrar categoria');
        }
    }
    
    async cadastrarProduto() {
        const nome = document.getElementById('produtoNome').value.trim();
        const categoriaId = document.getElementById('produtoCategoria').value;
        const preco = document.getElementById('produtoPreco').value.trim();
        const descricao = document.getElementById('produtoDescricao').value.trim();
        
        if (!nome || !categoriaId || !preco) {
            alert('por favor, preencha todos os campos obrigatorios');
            return;
        }
        
        try {
            const response = await fetch('/api/produtos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nome: nome,
                    categoria_id: parseInt(categoriaId),
                    preco: parseFloat(preco),
                    descricao: descricao,
                    avaliacao: 0.0
                })
            });
            
            if (response.ok) {
                alert('produto cadastrado com sucesso!');
                // recarregar produtos
                await this.carregarProdutos();
                // limpar formulario
                document.getElementById('produtoNome').value = '';
                document.getElementById('produtoCategoria').value = '';
                document.getElementById('produtoPreco').value = '';
                document.getElementById('produtoDescricao').value = '';
            } else {
                const error = await response.json();
                alert('erro ao cadastrar produto: ' + error.detail);
            }
        } catch (error) {
            console.error('erro:', error);
            alert('erro ao cadastrar produto');
        }
    }
    
    showCategoriaForm() {
        // esconder as abas
        this.tabsContainer.classList.add('hidden');
        
        this.formContainer.innerHTML = `
            <div class="form-header">
                <span class="form-header-text">cadastro</span>
                <span class="form-header-text">categoria</span>
            </div>
            
            <div class="form-field">
                <label class="form-label">nome da categoria*</label>
                <input type="text" class="form-input" id="categoriaNome" placeholder="">
            </div>
            
            <div class="form-field">
                <label class="form-label">categoria pai (opcional)</label>
                <select class="form-select" id="categoriaPai">
                    <option value="">Selecione</option>
                    ${this.categorias.map(cat => `<option value="${cat.nome}">${cat.nome}</option>`).join('')}
                </select>
            </div>
            
            <button class="btn-submit" onclick="cadastroPage.cadastrarCategoria()">cadastrar</button>
        `;
        
        this.formContainer.style.display = 'block';
    }
    
    showProdutoForm() {
        // esconder as abas
        this.tabsContainer.classList.add('hidden');
        
        this.formContainer.innerHTML = `
            <div class="form-header">
                <span class="form-header-text">cadastro</span>
                <span class="form-header-text">produto</span>
            </div>
            
            <div class="form-field">
                <label class="form-label">nome da categoria*</label>
                <input type="text" class="form-input" id="produtoNome" placeholder="">
            </div>
            
            <div class="form-field">
                <label class="form-label">categoria*</label>
                <select class="form-select" id="produtoCategoria">
                    <option value="">Selecione</option>
                    ${this.categorias.map(cat => `<option value="${cat.nome}">${cat.nome}</option>`).join('')}
                </select>
            </div>
            
            <div class="form-field">
                <label class="form-label">preço (R$)*</label>
                <input type="number" step="0.01" min="0" class="form-input" id="produtoPreco" placeholder="">
            </div>
            
            <div class="form-field">
                <label class="form-label">descrição (opcional)</label>
                <textarea class="form-textarea" id="produtoDescricao" placeholder=""></textarea>
            </div>
            
            <button class="btn-submit produto" onclick="cadastroPage.cadastrarProduto()">cadastrar</button>
        `;
        
        this.formContainer.style.display = 'block';
    }
    
    mostrarCategorias() {
        this.tabsContainer.classList.add('hidden');
        this.formContainer.style.display = 'none';
        
        this.cadastradosContainer.innerHTML = `
            <div class="cadastrados-header">categorias</div>
            <ul class="cadastrados-list">
                ${this.categorias.map((cat, index) => {
                    // construir a hierarquia
                    let hierarchyInfo = '';
                    if (cat.categoria_pai_nome) {
                        hierarchyInfo = `<div class="cadastrado-info">categoria pai: ${cat.categoria_pai_nome}</div>`;
                    }
                    
                    return `
                        <li class="cadastrado-item" data-id="${cat.id}" data-type="categoria">
                            <div class="cadastrado-header">
                                <div class="cadastrado-label">${cat.nome}</div>
                                <div class="menu-dots-wrapper">
                                    <button class="menu-dots-btn" onclick="cadastroPage.toggleMenu(event, ${cat.id}, 'categoria')">
                                        <div class="dot"></div>
                                        <div class="dot"></div>
                                        <div class="dot"></div>
                                    </button>
                                    <div class="menu-actions" id="menu-${cat.id}">
                                        <button class="menu-action-btn editar" onclick="cadastroPage.editarItem(${cat.id}, 'categoria')">editar</button>
                                        <button class="menu-action-btn apagar" onclick="cadastroPage.apagarItem(${cat.id}, 'categoria')">apagar</button>
                                    </div>
                                </div>
                            </div>
                            ${hierarchyInfo}
                        </li>
                    `;
                }).join('')}
            </ul>
        `;
        
        this.cadastradosContainer.style.display = 'block';
    }
    
    mostrarProdutos() {
        this.tabsContainer.classList.add('hidden');
        this.formContainer.style.display = 'none';
        
        this.cadastradosContainer.innerHTML = `
            <div class="cadastrados-header">produtos</div>
            <ul class="cadastrados-list">
                ${this.produtos.map((prod, index) => `
                    <li class="cadastrado-item" data-id="${prod.id}" data-type="produto">
                        <div class="cadastrado-header">
                            <div class="cadastrado-label">${prod.nome}</div>
                            <div class="menu-dots-wrapper">
                                <button class="menu-dots-btn" onclick="cadastroPage.toggleMenu(event, ${prod.id}, 'produto')">
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                </button>
                                <div class="menu-actions" id="menu-prod-${prod.id}">
                                    <button class="menu-action-btn editar" onclick="cadastroPage.editarItem(${prod.id}, 'produto')">editar</button>
                                    <button class="menu-action-btn apagar" onclick="cadastroPage.apagarItem(${prod.id}, 'produto')">apagar</button>
                                </div>
                            </div>
                        </div>
                        <div class="cadastrado-info">categoria: ${prod.categoria_nome}</div>
                        <div class="cadastrado-info">${prod.descricao}</div>
                        <div class="cadastrado-info" style="font-weight: 600;">R$ ${prod.preco.toFixed(2).replace('.', ',')}</div>
                    </li>
                `).join('')}
            </ul>
        `;
        
        this.cadastradosContainer.style.display = 'block';
    }
    
    toggleMenu(event, id, type) {
        event.stopPropagation();
        
        // fechar todos os menus abertos
        document.querySelectorAll('.menu-actions').forEach(menu => {
            menu.classList.remove('show');
        });
        
        // abrir o menu clicado
        const menuId = type === 'categoria' ? `menu-${id}` : `menu-prod-${id}`;
        const menu = document.getElementById(menuId);
        if (menu) {
            menu.classList.add('show');
        }
        
        // fechar o menu ao clicar fora
        const closeMenus = (e) => {
            if (!e.target.closest('.menu-dots-wrapper')) {
                document.querySelectorAll('.menu-actions').forEach(m => {
                    m.classList.remove('show');
                });
                document.removeEventListener('click', closeMenus);
            }
        };
        setTimeout(() => {
            document.addEventListener('click', closeMenus);
        }, 0);
    }
    
    editarItem(id, type) {
        console.log(`editar ${type} id: ${id}`);
        // fechar o menu
        document.querySelectorAll('.menu-actions').forEach(menu => {
            menu.classList.remove('show');
        });
        
        // implementar edicao futuramente
        alert(`funcionalidade de edicao sera implementada em breve para ${type} #${id}`);
    }
    
    async apagarItem(id, type) {
        console.log(`apagar ${type} id: ${id}`);
        
        // fechar o menu
        document.querySelectorAll('.menu-actions').forEach(menu => {
            menu.classList.remove('show');
        });
        
        if (!confirm(`tem certeza que deseja apagar este ${type}?`)) {
            return;
        }
        
        try {
            const endpoint = type === 'categoria' ? `/api/categorias/${id}` : `/api/produtos/${id}`;
            const response = await fetch(endpoint, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                alert(`${type} apagado com sucesso!`);
                // recarregar dados
                if (type === 'categoria') {
                    await this.carregarCategorias();
                    this.mostrarCategorias();
                } else {
                    await this.carregarProdutos();
                    this.mostrarProdutos();
                }
            } else {
                const error = await response.json();
                alert('erro ao apagar: ' + error.detail);
            }
        } catch (error) {
            console.error('erro:', error);
            alert('erro ao apagar ' + type);
        }
    }
}

// inicializar
let cadastroPage;
document.addEventListener('DOMContentLoaded', () => {
    cadastroPage = new CadastroPage();
});
