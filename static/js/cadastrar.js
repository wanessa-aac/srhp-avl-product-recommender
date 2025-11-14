// pagina de cadastro

class CadastroPage {
    constructor() {
        this.formContainer = document.getElementById('formContainer');
        this.cadastradosContainer = document.getElementById('cadastradosContainer');
        this.categorias = [
            { id: 1, nome: 'Eletronicos', pai: null },
            { id: 2, nome: 'Alimentos', pai: null },
            { id: 3, nome: 'Roupas', pai: null },
            { id: 4, nome: 'Livros', pai: null },
            { id: 5, nome: 'Esportes', pai: null },
            { id: 6, nome: 'Celulares', pai: 'Eletronicos' },
            { id: 7, nome: 'Computadores', pai: 'Eletronicos' },
            { id: 8, nome: 'Graos', pai: 'Alimentos' }
        ];
        
        this.produtos = [
            { id: 1, nome: 'Smartphone Galaxy', categoria: 'Eletronicos', preco: 2499.00, descricao: 'Celular top de linha com camera de 108MP' },
            { id: 2, nome: 'Notebook Dell', categoria: 'Eletronicos', preco: 3999.00, descricao: 'Notebook potente para trabalho e jogos' },
            { id: 3, nome: 'Arroz Integral 1kg', categoria: 'Alimentos', preco: 12.90, descricao: 'Arroz integral organico' },
            { id: 4, nome: 'Camiseta Basica', categoria: 'Roupas', preco: 49.90, descricao: 'Camiseta 100% algodao' },
            { id: 5, nome: 'Python Avancado', categoria: 'Livros', preco: 89.90, descricao: 'Livro completo sobre Python' },
            { id: 6, nome: 'iPhone 15 Pro', categoria: 'Eletronicos', preco: 7999.00, descricao: 'Ultimo lancamento da Apple' },
            { id: 7, nome: 'Mouse Gamer', categoria: 'Eletronicos', preco: 299.00, descricao: 'Mouse com RGB e 16000 DPI' },
            { id: 8, nome: 'Teclado Mecanico', categoria: 'Eletronicos', preco: 599.00, descricao: 'Teclado mecanico switches azuis' }
        ];
        
        this.init();
    }
    
    init() {
        // eventos das abas
        this.categoriaBtn = document.querySelector('.tab-button.categoria');
        this.produtoBtn = document.querySelector('.tab-button.produto');
        this.tabsContainer = document.querySelector('.tabs-container');
        
        this.categoriaBtn.addEventListener('click', () => this.showCategoriaForm());
        this.produtoBtn.addEventListener('click', () => this.showProdutoForm());
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
    
    cadastrarCategoria() {
        const nome = document.getElementById('categoriaNome').value.trim();
        const categoriaPai = document.getElementById('categoriaPai').value;
        
        if (!nome) {
            alert('Por favor, preencha o nome da categoria');
            return;
        }
        
        console.log('cadastrando categoria:', { nome, categoriaPai });
        
        // adicionar na lista
        const novaCategoria = {
            id: this.categorias.length + 1,
            nome: nome,
            pai: categoriaPai || null
        };
        this.categorias.push(novaCategoria);
        
        alert('Categoria cadastrada com sucesso!');
        
        // limpar formulario
        document.getElementById('categoriaNome').value = '';
        document.getElementById('categoriaPai').value = '';
    }
    
    cadastrarProduto() {
        const nome = document.getElementById('produtoNome').value.trim();
        const categoria = document.getElementById('produtoCategoria').value;
        const preco = document.getElementById('produtoPreco').value.trim();
        const descricao = document.getElementById('produtoDescricao').value.trim();
        
        if (!nome || !categoria || !preco) {
            alert('Por favor, preencha todos os campos obrigatórios');
            return;
        }
        
        console.log('cadastrando produto:', { nome, categoria, preco, descricao });
        
        // adicionar na lista
        const novoProduto = {
            id: this.produtos.length + 1,
            nome: nome,
            categoria: categoria,
            preco: parseFloat(preco),
            descricao: descricao || ''
        };
        this.produtos.push(novoProduto);
        
        alert('Produto cadastrado com sucesso!');
        
        // limpar formulario
        document.getElementById('produtoNome').value = '';
        document.getElementById('produtoCategoria').value = '';
        document.getElementById('produtoPreco').value = '';
        document.getElementById('produtoDescricao').value = '';
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
        
        this.cadastradosContainer.innerHTML = `
            <div class="cadastrados-header">Categorias</div>
            <ul class="cadastrados-list">
                ${this.categorias.map(cat => `
                    <li class="cadastrado-item">
                        <div class="cadastrado-header">
                            <span class="cadastrado-nome">${cat.nome}</span>
                        </div>
                        <div class="cadastrado-info">
                            ${cat.pai ? `Categoria pai: ${cat.pai}` : 'Categoria raiz'}
                        </div>
                    </li>
                `).join('')}
            </ul>
        `;
        
        this.cadastradosContainer.style.display = 'block';
    }
    
    mostrarProdutos() {
        this.tabsContainer.classList.add('hidden');
        
        this.cadastradosContainer.innerHTML = `
            <div class="cadastrados-header">Produtos</div>
            <ul class="cadastrados-list">
                ${this.produtos.map(prod => `
                    <li class="cadastrado-item">
                        <div class="cadastrado-header">
                            <span class="cadastrado-nome">${prod.nome}</span>
                            <span class="cadastrado-nome">R$ ${prod.preco.toFixed(2).replace('.', ',')}</span>
                        </div>
                        <div class="cadastrado-info">
                            Categoria: ${prod.categoria}
                        </div>
                        ${prod.descricao ? `<div class="cadastrado-info">${prod.descricao}</div>` : ''}
                    </li>
                `).join('')}
            </ul>
        `;
        
        this.cadastradosContainer.style.display = 'block';
    }
}

// inicializar
let cadastroPage;
document.addEventListener('DOMContentLoaded', () => {
    cadastroPage = new CadastroPage();
});
