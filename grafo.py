from collections import deque
from pathlib import Path


def carregar_grafo(caminho):
    """Carrega um grafo não direcionado a partir do arquivo de arestas."""
    grafo = {}

    with open(caminho, encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue

            partes = linha.split()
            if len(partes) != 3:
                raise ValueError(f"Linha {numero_linha}: use ORIGEM DESTINO PESO")

            origem, destino, peso_texto = partes
            peso = int(peso_texto)
            if peso <= 0:
                raise ValueError(f"Linha {numero_linha}: o peso deve ser positivo")

            # @unisenac Cada aresta é registrada nos dois sentidos.
            grafo.setdefault(origem, []).append((destino, peso))
            grafo.setdefault(destino, []).append((origem, peso))

    return grafo


def portas_alcancaveis(grafo, origem):
    """Usa BFS para encontrar todas as portas alcançáveis da origem."""
    if origem not in grafo:
        raise ValueError(f"Porta de origem não encontrada: {origem}")

    visitados = {origem}
    fila = deque([origem])

    while fila:
        atual = fila.popleft()
        for vizinho, _ in grafo[atual]:
            if vizinho not in visitados:
                # @unisenac A fila garante que a BFS explore por camadas.
                visitados.add(vizinho)
                fila.append(vizinho)

    return visitados


if __name__ == "__main__":
    arquivo_arestas = Path(__file__).with_name("arestas.txt")
    grafo = carregar_grafo(arquivo_arestas)
    quantidade_arestas = sum(len(vizinhos) for vizinhos in grafo.values()) // 2
    alcancaveis = portas_alcancaveis(grafo, "LABTEC")

    print(f"Portas: {len(grafo)}")
    print(f"Arestas: {quantidade_arestas}")
    print(f"Portas alcançáveis a partir do LABTEC: {len(alcancaveis)}/{len(grafo)}")
    faltando = sorted(set(grafo) - alcancaveis)
    if faltando:
        print("Portas não alcançadas:", ", ".join(faltando))
    else:
        print("Todas as portas cadastradas são alcançáveis!")
