"""
aplicacao web para o sistema de recomendacao hierarquica de produtos
interface grafica usando fastapi
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from src.business_logic import SistemaRecomendacao

app = FastAPI(title="SRHP - Sistema de Recomendacao de Produtos")

# configurar arquivos estaticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# instanciar o sistema de recomendacao
sistema = SistemaRecomendacao()


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


# api endpoints

@app.get("/api/tree")
async def get_tree():
    """retorna a estrutura da arvore em json"""
    
    def node_to_dict(node):
        """converte um no da avl em dicionario"""
        if node is None:
            return None
        
        return {
            "key": node.key,
            "height": node.height,
            "data": {
                "nome": node.data.nome,
                "descricao": node.data.descricao,
                "produtos": [
                    {
                        "id": p.id,
                        "nome": p.nome,
                        "preco": p.preco,
                        "avaliacao": p.avaliacao
                    } for p in node.data.produtos
                ]
            },
            "leftChild": node_to_dict(node.leftChild),
            "rightChild": node_to_dict(node.rightChild)
        }
    
    tree_dict = {
        "root": node_to_dict(sistema.arvore_categorias.root)
    }
    
    return tree_dict


@app.post("/api/populate-sample")
async def populate_sample():
    """popula a arvore com dados de exemplo para demonstracao"""
    
    # limpar arvore atual
    sistema.arvore_categorias = SistemaRecomendacao().arvore_categorias
    
    # adicionar categorias de exemplo
    categorias_exemplo = [
        ("Eletronicos", "dispositivos eletronicos e gadgets"),
        ("Roupas", "vestuario e acessorios"),
        ("Alimentos", "produtos alimenticios"),
        ("Livros", "literatura e educacao"),
        ("Esportes", "equipamentos esportivos"),
    ]
    
    for nome, desc in categorias_exemplo:
        sistema.cadastrar_categoria(nome, desc)
    
    # adicionar alguns produtos
    produtos_exemplo = [
        ("Eletronicos", 1, "Smartphone XYZ", 1500.00, "ultimo modelo", 4.5),
        ("Eletronicos", 2, "Notebook ABC", 3000.00, "para trabalho", 4.8),
        ("Roupas", 3, "Camiseta Basica", 49.90, "100% algodao", 4.2),
        ("Alimentos", 4, "Cafe Premium", 25.00, "graos selecionados", 4.7),
        ("Livros", 5, "Python Avancado", 89.90, "aprenda python", 4.9),
    ]
    
    for cat, pid, nome, preco, desc, aval in produtos_exemplo:
        sistema.cadastrar_produto(cat, pid, nome, preco, desc, aval)
    
    return {"message": "arvore populada com dados de exemplo", "categorias": len(categorias_exemplo)}


if __name__ == "__main__":
    print("iniciando servidor fastapi")
    print("acesse http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
