"""
aplicacao web para o sistema de recomendacao hierarquica de produtos
interface grafica usando fastapi
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import uvicorn

from src.business_logic import SistemaRecomendacao
from src.database import Database

app = FastAPI(title="SRHP - Sistema de Recomendacao de Produtos")

# configurar arquivos estaticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# instanciar o sistema de recomendacao e banco de dados
sistema = SistemaRecomendacao()
db = Database()

def sincronizar_avl_com_banco():
    """
    carrega todos os dados do banco e popula a arvore AVL
    deve ser chamado na inicializacao do servidor
    complexidade: O(n log n) onde n e o numero de categorias
    """
    print("\n" + "="*60)
    print("SINCRONIZANDO AVL COM BANCO DE DADOS")
    print("="*60)
    
    # carregar categorias do banco
    categorias = db.listar_categorias()
    print(f"encontradas {len(categorias)} categorias no banco")
    
    # inserir categorias na AVL em ordem (pais primeiro)
    # primeira passagem: categorias raiz (sem pai)
    for cat in categorias:
        if not cat['categoria_pai_id']:
            sistema.cadastrar_categoria(cat['nome'], cat['descricao'])
    
    # segunda passagem: subcategorias
    for cat in categorias:
        if cat['categoria_pai_id']:
            sistema.cadastrar_categoria(cat['nome'], cat['descricao'])
    
    # carregar produtos e adicionar as categorias
    produtos = db.listar_produtos()
    print(f"encontrados {len(produtos)} produtos no banco")
    
    for prod in produtos:
        sistema.cadastrar_produto(
            prod['categoria_nome'],
            prod['id'],
            prod['nome'],
            prod['preco'],
            prod['descricao'],
            prod['avaliacao']
        )
    
    print("="*60)
    print("SINCRONIZACAO COMPLETA!")
    print("="*60 + "\n")
    
    # imprimir hierarquia para verificar
    sistema.imprimir_hierarquia()

# sincronizar na inicializacao
sincronizar_avl_com_banco()

# modelos pydantic para validacao

class CategoriaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = ""
    categoria_pai_id: Optional[int] = None

class CategoriaUpdate(BaseModel):
    nome: str
    descricao: Optional[str] = ""
    categoria_pai_id: Optional[int] = None

class ProdutoCreate(BaseModel):
    nome: str
    categoria_id: int
    preco: float
    descricao: Optional[str] = ""
    avaliacao: Optional[float] = 0.0

class ProdutoUpdate(BaseModel):
    nome: str
    categoria_id: int
    preco: float
    descricao: Optional[str] = ""
    avaliacao: Optional[float] = 0.0


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """pagina inicial"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/arvore", response_class=HTMLResponse)
async def arvore(request: Request):
    """pagina de visualizacao da arvore"""
    return templates.TemplateResponse("arvore.html", {"request": request})


@app.get("/buscar", response_class=HTMLResponse)
async def buscar(request: Request):
    """pagina de busca"""
    return templates.TemplateResponse("buscar.html", {"request": request})


@app.get("/cadastrar", response_class=HTMLResponse)
async def cadastrar(request: Request):
    """pagina de cadastro"""
    return templates.TemplateResponse("cadastrar.html", {"request": request})


# api endpoints para categorias

@app.get("/api/categorias")
async def listar_categorias():
    """lista todas as categorias"""
    categorias = db.listar_categorias()
    return JSONResponse(content=categorias)

@app.get("/api/categorias/{categoria_id}")
async def buscar_categoria(categoria_id: int):
    """busca uma categoria por id"""
    categoria = db.buscar_categoria_por_id(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="categoria nao encontrada")
    return JSONResponse(content=categoria)

@app.post("/api/categorias")
async def criar_categoria(categoria: CategoriaCreate):
    """cria uma nova categoria"""
    try:
        # 1. inserir na AVL (O(log n) - estrutura principal)
        sucesso_avl = sistema.cadastrar_categoria(categoria.nome, categoria.descricao)
        
        if not sucesso_avl:
            raise HTTPException(status_code=400, detail="categoria ja existe na AVL")
        
        # 2. persistir no banco (backup/persistencia)
        categoria_id = db.inserir_categoria(
            nome=categoria.nome,
            descricao=categoria.descricao,
            categoria_pai_id=categoria.categoria_pai_id
        )
        
        return JSONResponse(content={
            "id": categoria_id, 
            "message": "categoria criada com sucesso na AVL e banco"
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/categorias/{categoria_id}")
async def atualizar_categoria(categoria_id: int, categoria: CategoriaUpdate):
    """atualiza uma categoria existente"""
    sucesso = db.atualizar_categoria(
        categoria_id=categoria_id,
        nome=categoria.nome,
        descricao=categoria.descricao,
        categoria_pai_id=categoria.categoria_pai_id
    )
    if not sucesso:
        raise HTTPException(status_code=404, detail="categoria nao encontrada")
    return JSONResponse(content={"message": "categoria atualizada com sucesso"})

@app.delete("/api/categorias/{categoria_id}")
async def deletar_categoria(categoria_id: int):
    """deleta uma categoria"""
    # 1. buscar nome da categoria no banco
    categoria = db.buscar_categoria_por_id(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="categoria nao encontrada")
    
    # 2. remover da AVL (O(log n))
    sistema.remover_categoria(categoria['nome'])
    
    # 3. remover do banco (persistencia)
    sucesso = db.deletar_categoria(categoria_id)
    
    return JSONResponse(content={
        "message": "categoria deletada com sucesso da AVL e banco"
    })

# api endpoints para produtos

@app.get("/api/produtos")
async def listar_produtos():
    """lista todos os produtos"""
    produtos = db.listar_produtos()
    return JSONResponse(content=produtos)

@app.get("/api/produtos/categoria/{categoria_id}")
async def listar_produtos_por_categoria(categoria_id: int):
    """
    lista produtos de uma categoria usando busca na AVL
    complexidade: O(log n) para encontrar a categoria
    """
    # buscar categoria no banco para obter o nome
    categoria_db = db.buscar_categoria_por_id(categoria_id)
    if not categoria_db:
        raise HTTPException(status_code=404, detail="categoria nao encontrada")
    
    # buscar na AVL (O(log n))
    categoria_avl = sistema.buscar_categoria(categoria_db['nome'])
    if not categoria_avl:
        raise HTTPException(status_code=404, detail="categoria nao encontrada na AVL")
    
    # converter produtos da AVL para formato JSON
    produtos = [{
        'id': p.id,
        'nome': p.nome,
        'preco': p.preco,
        'descricao': p.descricao,
        'avaliacao': p.avaliacao,
        'categoria_id': categoria_id,
        'categoria_nome': categoria_db['nome']
    } for p in categoria_avl.produtos]
    
    return JSONResponse(content=produtos)

@app.get("/api/produtos/{produto_id}")
async def buscar_produto(produto_id: int):
    """busca um produto por id"""
    produto = db.buscar_produto_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="produto nao encontrado")
    return JSONResponse(content=produto)

@app.post("/api/produtos")
async def criar_produto(produto: ProdutoCreate):
    """cria um novo produto"""
    try:
        # 1. buscar nome da categoria
        categoria = db.buscar_categoria_por_id(produto.categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="categoria nao encontrada")
        
        # 2. persistir no banco primeiro para obter o ID
        produto_id = db.inserir_produto(
            nome=produto.nome,
            categoria_id=produto.categoria_id,
            preco=produto.preco,
            descricao=produto.descricao,
            avaliacao=produto.avaliacao
        )
        
        # 3. adicionar na AVL (O(log n) para encontrar categoria + O(1) para adicionar)
        sucesso_avl = sistema.cadastrar_produto(
            categoria['nome'],
            produto_id,
            produto.nome,
            produto.preco,
            produto.descricao,
            produto.avaliacao
        )
        
        if not sucesso_avl:
            # se falhar na AVL, remover do banco
            db.deletar_produto(produto_id)
            raise HTTPException(status_code=400, detail="erro ao adicionar produto na AVL")
        
        return JSONResponse(content={
            "id": produto_id, 
            "message": "produto criado com sucesso na AVL e banco"
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/produtos/{produto_id}")
async def atualizar_produto(produto_id: int, produto: ProdutoUpdate):
    """atualiza um produto existente"""
    sucesso = db.atualizar_produto(
        produto_id=produto_id,
        nome=produto.nome,
        categoria_id=produto.categoria_id,
        preco=produto.preco,
        descricao=produto.descricao,
        avaliacao=produto.avaliacao
    )
    if not sucesso:
        raise HTTPException(status_code=404, detail="produto nao encontrado")
    return JSONResponse(content={"message": "produto atualizado com sucesso"})

@app.delete("/api/produtos/{produto_id}")
async def deletar_produto(produto_id: int):
    """deleta um produto"""
    # 1. buscar produto no banco
    produto = db.buscar_produto_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="produto nao encontrado")
    
    # 2. buscar categoria na AVL (O(log n))
    categoria = sistema.buscar_categoria(produto['categoria_nome'])
    if categoria:
        # remover produto da categoria na AVL
        categoria.produtos = [p for p in categoria.produtos if p.id != produto_id]
    
    # 3. remover do banco (persistencia)
    sucesso = db.deletar_produto(produto_id)
    
    return JSONResponse(content={
        "message": "produto deletado com sucesso da AVL e banco"
    })

# api para arvore avl

@app.get("/api/tree")
async def get_tree():
    """
    retorna a estrutura da arvore AVL em json
    usa travessia in-ordem para converter a AVL em estrutura hierarquica
    complexidade: O(n) onde n e o numero de categorias
    """
    
    def node_to_dict(node):
        """
        converte um no da AVL em dicionario recursivamente
        travessia pre-ordem (raiz, esquerda, direita)
        """
        if node is None:
            return None
        
        categoria = node.data
        
        # converter produtos para formato json
        produtos = [{
            'id': p.id,
            'nome': p.nome,
            'preco': p.preco,
            'descricao': p.descricao,
            'avaliacao': p.avaliacao
        } for p in categoria.produtos]
        
        node_dict = {
            'id': f"avl-{node.key}",  # identificador unico baseado na chave
            'nome': categoria.nome,
            'descricao': categoria.descricao,
            'altura': node.height,
            'produtos': produtos,
            'num_produtos': len(produtos),
            'children': []
        }
        
        # adicionar filhos (esquerda e direita da AVL)
        if node.leftChild:
            left_dict = node_to_dict(node.leftChild)
            if left_dict:
                node_dict['children'].append(left_dict)
        
        if node.rightChild:
            right_dict = node_to_dict(node.rightChild)
            if right_dict:
                node_dict['children'].append(right_dict)
        
        return node_dict
    
    # converter a arvore AVL inteira
    if sistema.arvore_categorias.root is None:
        return JSONResponse(content=[])
    
    tree = node_to_dict(sistema.arvore_categorias.root)
    
    return JSONResponse(content=[tree] if tree else [])


# endpoints avancados usando funcionalidades da AVL

@app.get("/api/buscar/{nome_categoria}")
async def buscar_categoria_avl(nome_categoria: str):
    """
    busca uma categoria na AVL pelo nome
    complexidade: O(log n)
    """
    categoria = sistema.buscar_categoria(nome_categoria)
    
    if not categoria:
        raise HTTPException(status_code=404, detail="categoria nao encontrada na AVL")
    
    produtos = [{
        'id': p.id,
        'nome': p.nome,
        'preco': p.preco,
        'descricao': p.descricao,
        'avaliacao': p.avaliacao
    } for p in categoria.produtos]
    
    return JSONResponse(content={
        'nome': categoria.nome,
        'descricao': categoria.descricao,
        'produtos': produtos,
        'num_produtos': len(produtos)
    })

@app.get("/api/recomendar/{nome_categoria}")
async def recomendar_produtos_avl(nome_categoria: str, 
                                   ordenar_por: str = "avaliacao", 
                                   limite: Optional[int] = None):
    """
    recomenda produtos usando o sistema de recomendacao hierarquica
    inclui produtos de subcategorias usando travessia da AVL
    complexidade: O(log n) para encontrar + O(m) para percorrer subarvore
    """
    # usar o sistema de recomendacao
    recomendacoes = sistema.recomendar_produtos(nome_categoria, ordenar_por, limite)
    
    if not recomendacoes:
        raise HTTPException(status_code=404, 
                          detail="categoria nao encontrada ou sem produtos")
    
    # converter para formato JSON
    resultado = [{
        'produto': {
            'id': item['produto'].id,
            'nome': item['produto'].nome,
            'preco': item['produto'].preco,
            'descricao': item['produto'].descricao,
            'avaliacao': item['produto'].avaliacao
        },
        'categoria': item['categoria']
    } for item in recomendacoes]
    
    return JSONResponse(content=resultado)

@app.get("/api/hierarquia")
async def obter_hierarquia():
    """
    retorna estatisticas da hierarquia da AVL
    complexidade: O(1)
    """
    if sistema.arvore_categorias.root is None:
        return JSONResponse(content={
            'total_categorias': 0,
            'altura_arvore': 0,
            'balanceada': True
        })
    
    def contar_nos(node):
        if node is None:
            return 0
        return 1 + contar_nos(node.leftChild) + contar_nos(node.rightChild)
    
    def calcular_altura(node):
        if node is None:
            return -1
        return node.height
    
    total = contar_nos(sistema.arvore_categorias.root)
    altura = calcular_altura(sistema.arvore_categorias.root)
    
    return JSONResponse(content={
        'total_categorias': total,
        'altura_arvore': altura,
        'balanceada': True,  # AVL sempre balanceada
        'altura_teorica_minima': int(total.bit_length() - 1) if total > 0 else 0
    })


if __name__ == "__main__":
    print("iniciando servidor fastapi")
    print("acesse http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
