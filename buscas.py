"""Algoritmos de busca usados nas rotas do predio."""

from collections import deque
import heapq


def _reconstruir_caminho(predecessores, destino):
    """Monta o caminho indo do destino ate a origem pelos predecessores."""
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    return list(reversed(caminho))


def _custo_do_caminho(grafo, caminho):
    """Soma os pesos das arestas que compoem um caminho encontrado."""
    custo = 0

    for origem, destino in zip(caminho, caminho[1:]):
        for vizinho, peso in grafo[origem]:
            if vizinho == destino:
                custo += peso
                break

    return custo


def bfs(grafo, origem, destino):
    """Encontra uma rota com a menor quantidade de arestas."""
    fila = deque([origem])
    descobertos = {origem}
    predecessores = {origem: None}
    visitados = 0

    while fila:
        atual = fila.popleft()
        visitados += 1

        if atual == destino:
            caminho = _reconstruir_caminho(predecessores, destino)
            return caminho, _custo_do_caminho(grafo, caminho), visitados

        for vizinho, _ in grafo[atual]:
            if vizinho not in descobertos:
                # @unisenac A fila faz a BFS explorar primeiro as portas mais proximas.
                descobertos.add(vizinho)
                predecessores[vizinho] = atual
                fila.append(vizinho)

    return [], 0, visitados


def dfs(grafo, origem, destino):
    """Explora uma rota em profundidade, respeitando a ordem dos vizinhos."""
    pilha = [origem]
    descobertos = {origem}
    predecessores = {origem: None}
    visitados = 0

    while pilha:
        atual = pilha.pop()
        visitados += 1

        if atual == destino:
            caminho = _reconstruir_caminho(predecessores, destino)
            return caminho, _custo_do_caminho(grafo, caminho), visitados

        # @unisenac Inverter mantem o primeiro vizinho do arquivo como o primeiro explorado.
        for vizinho, _ in reversed(grafo[atual]):
            if vizinho not in descobertos:
                descobertos.add(vizinho)
                predecessores[vizinho] = atual
                pilha.append(vizinho)

    return [], 0, visitados


def gulosa(grafo, origem, destino):
    """Segue sempre para o vizinho nao visitado de menor peso imediato."""
    atual = origem
    caminho = [origem]
    ja_visitados = {origem}
    custo = 0
    visitados = 0

    while True:
        visitados += 1

        if atual == destino:
            return caminho, custo, visitados

        opcoes = [
            (peso, vizinho)
            for vizinho, peso in grafo[atual]
            if vizinho not in ja_visitados
        ]
        if not opcoes:
            return [], 0, visitados

        # @unisenac A gulosa compara apenas as saidas da porta atual e nao volta atras.
        peso, proxima_porta = min(opcoes, key=lambda opcao: (opcao[0], opcao[1]))
        custo += peso
        atual = proxima_porta
        caminho.append(atual)
        ja_visitados.add(atual)


def dijkstra(grafo, origem, destino):
    """Encontra a rota com a menor soma de pesos usando uma fila de prioridade."""
    fila_prioridade = [(0, origem)]
    custos = {origem: 0}
    predecessores = {origem: None}
    finalizados = set()
    visitados = 0

    while fila_prioridade:
        custo_atual, atual = heapq.heappop(fila_prioridade)

        if atual in finalizados:
            continue

        # @unisenac Um no finalizado ja possui seu menor custo possivel a partir da origem.
        finalizados.add(atual)
        visitados += 1

        if atual == destino:
            caminho = _reconstruir_caminho(predecessores, destino)
            return caminho, custo_atual, visitados

        for vizinho, peso in grafo[atual]:
            novo_custo = custo_atual + peso
            if novo_custo < custos.get(vizinho, float("inf")):
                custos[vizinho] = novo_custo
                predecessores[vizinho] = atual
                heapq.heappush(fila_prioridade, (novo_custo, vizinho))

    return [], 0, visitados
