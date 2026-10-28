"""API para consultar portas e calcular rotas no predio."""

from pathlib import Path

from fastapi import FastAPI, HTTPException

from buscas import bfs, dfs, dijkstra, gulosa
from grafo import carregar_grafo


app = FastAPI(
    title="Rotas do Prédio com Grafos",
    description="Consulta de portas e rotas medidas em passos.",
)

ARQUIVO_ARESTAS = Path(__file__).with_name("arestas.txt")
grafo = carregar_grafo(ARQUIVO_ARESTAS)

ALGORITMOS = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}


def _validar_porta(porta):
    """Garante que uma porta pedida existe antes da busca."""
    if porta not in grafo:
        raise HTTPException(status_code=404, detail=f"Porta não encontrada: {porta}")


def _resultado_rota(algoritmo, origem, destino):
    """Executa um algoritmo e adapta sua tupla para o JSON da API."""
    caminho, custo, visitados = ALGORITMOS[algoritmo](grafo, origem, destino)
    return {
        "algoritmo": algoritmo,
        "caminho": caminho,
        "custo": custo,
        "unidade": "passos",
        "visitados": visitados,
    }


@app.get("/portas")
def listar_portas():
    """Lista todas as portas cadastradas em ordem alfabetica."""
    return {"portas": sorted(grafo)}


@app.get("/vizinhos/{porta}")
def listar_vizinhos(porta: str):
    """Mostra as portas conectadas diretamente e suas distancias."""
    _validar_porta(porta)

    # @unisenac O arquivo mantem a ordem das conexoes registrada na caminhada.
    vizinhos = [{"porta": vizinho, "peso": peso} for vizinho, peso in grafo[porta]]
    return {"porta": porta, "vizinhos": vizinhos, "unidade": "passos"}


@app.get("/rota")
def calcular_rota(origem: str, destino: str, algoritmo: str):
    """Calcula uma rota com um dos quatro algoritmos disponiveis."""
    _validar_porta(origem)
    _validar_porta(destino)

    if algoritmo not in ALGORITMOS:
        raise HTTPException(status_code=400, detail=f"Algoritmo inválido: {algoritmo}")

    # @unisenac A escolha aqui permite comparar o mesmo par de portas com cada busca.
    return _resultado_rota(algoritmo, origem, destino)


@app.get("/comparar")
def comparar_rotas(origem: str, destino: str):
    """Executa os quatro algoritmos para o mesmo par de portas."""
    _validar_porta(origem)
    _validar_porta(destino)

    return {
        "origem": origem,
        "destino": destino,
        "unidade": "passos",
        "resultados": {
            nome: _resultado_rota(nome, origem, destino) for nome in ALGORITMOS
        },
    }
