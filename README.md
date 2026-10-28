# Rotas do Predio com Grafos

Trabalho da disciplina de Algoritmos e Estruturas de Dados II - UniSenac Pelotas.

## Integrantes

- Henrique Rodeghiero
- Matheus Rohrig

## Proposta

O projeto representa portas e pontos de referencia do predio como um grafo ponderado e nao direcionado. Cada peso corresponde a quantidade de **passos** medida entre duas portas. O ponto inicial de referencia e `LABTEC`.

O levantamento atual possui 37 portas e 38 conexoes. As medidas confirmadas ficam em `arestas.txt`; cada conexao aparece uma unica vez no arquivo e o programa a adiciona nos dois sentidos.

A foto do desenho original usado no levantamento esta no arquivo `0.pdf`.

## Estrutura

- `arestas.txt`: conexoes e pesos em passos.
- `grafo.py`: carrega o grafo e verifica se todas as portas sao alcancaveis a partir de `LABTEC`.
- `buscas.py`: implementa BFS, DFS, busca gulosa e Dijkstra.
- `api.py`: disponibiliza consultas e rotas com FastAPI.
- `tests/`: verificacoes automatizadas dos algoritmos e da camada da API.

## Instalacao e execucao

No PowerShell, dentro da pasta do projeto:

```powershell
py -m pip install fastapi uvicorn
py -m uvicorn api:app --reload
```

Com o servidor em execucao, abra a documentacao interativa em:

```text
http://127.0.0.1:8000/docs
```

Para conferir o carregamento e a conectividade do grafo:

```powershell
py grafo.py
```

Para executar os testes:

```powershell
py -m unittest discover -s tests -v
```

## Endpoints

| Metodo | Endpoint | Descricao |
| --- | --- | --- |
| GET | `/portas` | Lista as portas cadastradas em ordem alfabetica. |
| GET | `/vizinhos/{porta}` | Mostra as conexoes diretas e os pesos de uma porta. |
| GET | `/rota?origem=&destino=&algoritmo=` | Calcula uma rota com `bfs`, `dfs`, `gulosa` ou `dijkstra`. |
| GET | `/comparar?origem=&destino=` | Executa os quatro algoritmos para o mesmo par de portas. |

Portas inexistentes retornam HTTP 404. Um nome de algoritmo diferente dos quatro disponiveis retorna HTTP 400.

Exemplo:

```text
GET /rota?origem=LABTEC&destino=LAB202&algoritmo=dijkstra
```

Resposta:

```json
{
  "algoritmo": "dijkstra",
  "caminho": ["LABTEC", "LAB201", "LAB202"],
  "custo": 8,
  "unidade": "passos",
  "visitados": 3
}
```

## Algoritmos

### BFS (busca em largura)

Usa uma fila e explora primeiro as portas mais proximas em quantidade de arestas. Por isso, encontra uma rota com o menor numero de conexoes, mas nao necessariamente com o menor numero de passos.

### DFS (busca em profundidade)

Usa uma pilha e percorre um ramo ate o maximo antes de voltar. O resultado depende da ordem das conexoes no arquivo `arestas.txt`.

### Busca gulosa

Em cada porta, escolhe o vizinho ainda nao visitado ligado pela aresta de menor peso imediato. Ela nao volta atras nem soma os pesos anteriores ao escolher; por isso pode nao encontrar uma rota mesmo em um grafo conectado e pode encontrar uma rota mais cara do que Dijkstra.

### Dijkstra

Usa uma fila de prioridade (`heapq`) ordenada pelo custo acumulado desde a origem. Assim, encontra a rota com a menor soma de passos quando todos os pesos sao positivos.

## Exemplo real: BFS e Dijkstra escolhem caminhos diferentes

Executando os algoritmos no grafo deste projeto, de `LABTEC` ate `SECRETARIA_B`:

| Algoritmo | Caminho | Custo | Portas examinadas |
| --- | --- | ---: | ---: |
| BFS | `LABTEC -> LAB201 -> LAB202 -> LAB203 -> PATIO2 -> BANHEIRO_FEM -> BANHEIRO_MASC -> SECRETARIA_A -> SECRETARIA_B` | 51 passos | 28 |
| Dijkstra | `LABTEC -> LAB201 -> LAB202 -> LAB203 -> PATIO2 -> BIBLIOTECA -> SALA_PROF -> DIRECAO -> LIDERANCA_ADM -> COORD_PEDAGOGICA -> SECRETARIA_B` | 48 passos | 19 |

A BFS escolhe uma rota com menos arestas: sao 8 conexoes, contra 10 conexoes na rota de Dijkstra. Dijkstra aceita mais conexoes porque a soma das distancias e menor: 48 passos em vez de 51.

## Pontos para a demonstracao

1. O arquivo `arestas.txt` guarda cada medida uma unica vez; `grafo.py` cria o caminho de volta automaticamente.
2. O valor `visitados` informa quantas portas cada algoritmo retirou para exame antes de terminar.
3. Em `/comparar`, os quatro algoritmos recebem a mesma origem e o mesmo destino, permitindo observar suas estrategias.
4. O menor numero de arestas (BFS) nao significa necessariamente o menor numero de passos (Dijkstra).
