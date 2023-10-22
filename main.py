import random
from collections import deque
from viewer import MazeViewer
from math import inf, sqrt
import heapq
import time
from metricas import calcular_media, exibir_graficos


def gera_labirinto(n_linhas, n_colunas, inicio, goal):
    # cria labirinto vazio
    labirinto = [[0] * n_colunas for _ in range(n_linhas)]

    # adiciona celulas ocupadas em locais aleatorios de
    # forma que 50% do labirinto esteja ocupado
    numero_de_obstaculos = int(0.40 * n_linhas * n_colunas)
    for _ in range(numero_de_obstaculos):
        linha = random.randint(0, n_linhas-1)
        coluna = random.randint(0, n_colunas-1)
        labirinto[linha][coluna] = 1

    # remove eventuais obstaculos adicionados na posicao
    # inicial e no goal
    labirinto[inicio.y][inicio.x] = 0
    labirinto[goal.y][goal.x] = 0

    return labirinto


class Celula:
    def __init__(self, y, x, anterior):
        self.y = y
        self.x = x
        self.anterior = anterior

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y



def distancia(celula_1, celula_2):
    dx = celula_1.x - celula_2.x
    dy = celula_1.y - celula_2.y
    return sqrt(dx ** 2 + dy ** 2)


def esta_contido(lista, celula):
    for elemento in lista:
        if (elemento.y == celula.y) and (elemento.x == celula.x):
            return True
    return False


def custo_caminho(caminho):
    if len(caminho) == 0:
        return inf

    custo_total = 0
    for i in range(1, len(caminho)):
        custo_total += distancia(caminho[i].anterior, caminho[i])

    return custo_total


def obtem_caminho(goal):
    caminho = []

    celula_atual = goal
    while celula_atual is not None:
        caminho.append(celula_atual)
        celula_atual = celula_atual.anterior

    # o caminho foi gerado do final para o
    # comeco, entao precisamos inverter.
    caminho.reverse()

    return caminho


def celulas_vizinhas_livres(celula_atual, labirinto):
    # generate neighbors of the current state
    vizinhos = [
        Celula(y=celula_atual.y-1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x-1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+0, anterior=celula_atual),
        Celula(y=celula_atual.y+1, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y+0, x=celula_atual.x+1, anterior=celula_atual),
        Celula(y=celula_atual.y-1, x=celula_atual.x+1, anterior=celula_atual),
    ]

    # seleciona as celulas livres
    vizinhos_livres = []
    for v in vizinhos:
        # verifica se a celula esta dentro dos limites do labirinto
        if (v.y < 0) or (v.x < 0) or (v.y >= len(labirinto)) or (v.x >= len(labirinto[0])):
            continue
        # verifica se a celula esta livre de obstaculos.
        if labirinto[v.y][v.x] == 0:
            vizinhos_livres.append(v)

    return vizinhos_livres


def breadth_first_search(labirinto, inicio, goal, viewer):
    tempo_inicial = time.time()

    # Nós gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # Nós já expandidos (amarelos)
    expandidos = set()

    # Adiciona o nó inicial na fronteira
    fronteira.append(inicio)

    # Variável para armazenar o goal quando ele for encontrado
    goal_encontrado = None

    # Repete enquanto nós não encontramos o goal e ainda existem nós para serem expandidos na fronteira.
    while (len(fronteira) > 0) and (goal_encontrado is None):
        # Seleciona o nó mais recente para ser expandido
        no_atual = fronteira.popleft()

        # Busca os vizinhos do nó
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # Para cada vizinho, verifica se é o goal e adiciona na fronteira se ainda não foi expandido e não está na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # Encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)

        expandidos.add(no_atual)
        # viewer.update(generated=fronteira,
        #               expanded=expandidos)        


    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)

    # print(
    #     f"DFS:"
    #     f"\tCusto total do caminho: {custo}.\n"
    #     f"\tNúmero de passos: {len(caminho) - 1}.\n"
    #     f"\tNúmero total de nós expandidos: {len(expandidos)}.\n\n"
    # )

    # viewer.update(path=caminho)
    # viewer.pause()

    tempo_final = time.time()
    tempo_total = tempo_final - tempo_inicial

    return caminho, custo, expandidos, tempo_total


def depth_first_search(labirinto, inicio, goal, viewer):
    tempo_inicial = time.time()

    # Nós gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # Nós já expandidos (amarelos)
    expandidos = set()

    # Adiciona o nó inicial na fronteira
    fronteira.append(inicio)

    # Variável para armazenar o goal quando ele for encontrado
    goal_encontrado = None

    # Repete enquanto nós não encontramos o goal e ainda existem nós para serem expandidos na fronteira.
    while (len(fronteira) > 0) and (goal_encontrado is None):
        # Seleciona o nó mais recente para ser expandido
        no_atual = fronteira.pop()

        # Busca os vizinhos do nó
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # Para cada vizinho, verifica se é o goal e adiciona na fronteira se ainda não foi expandido e não está na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # Encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)

        #viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)

    # viewer.update(path=caminho)
    # viewer.pause()

    tempo_final = time.time()
    tempo_total = tempo_final - tempo_inicial

    return caminho, custo, expandidos, tempo_total


def a_star_search(labirinto, inicio, goal, viewer):
    tempo_inicial = time.time()
    fronteira = []
    expandidos = set()

    fronteira.append((inicio, 0, distancia(inicio, goal)))

    goal_encontrado = None

    while (len(fronteira) > 0) and (goal_encontrado is None):
        fronteira.sort(key=lambda x: x[1] + x[2])

        no_atual, custo_atual, _ = fronteira.pop(0)

        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                break
            else:
                custo_vizinho = custo_atual + 1 
                heuristica = distancia(v, goal)
                custo_total = custo_vizinho + heuristica

                if (not esta_contido(expandidos, v)) and (not any(x[0] == v for x in fronteira)):
                    fronteira.append((v, custo_vizinho, heuristica))
        expandidos.add(no_atual)

        # viewer.update(generated=[x[0] for x in fronteira],
        #               expanded=expandidos)
        

    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)

    tempo_final = time.time()
    tempo_total = tempo_final - tempo_inicial


    return caminho, custo, expandidos, tempo_total


def uniform_cost_search(labirinto, inicio, goal, viewer):
    tempo_inicial = time.time()

    fronteira = []
    expandidos = set()

    fronteira.append((inicio, 0))

    goal_encontrado = None

    while fronteira and goal_encontrado is None:

        fronteira.sort(key=lambda x: x[1])

        no_atual, custo_atual = fronteira.pop(0)

        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                break
            else:
                # Calcula custo e adiciona à fronteira se apropriado
                custo_vizinho = custo_atual + 1 

                if (not esta_contido(expandidos, v)) and (not any(x[0] == v for x in fronteira)):
                    fronteira.append((v, custo_vizinho))
                    expandidos.add(v)

        # Atualiza a visualização

        # viewer.update(generated=[x[0] for x in fronteira], expanded=expandidos)

    caminho = obtem_caminho(goal_encontrado)
    custo = custo_caminho(caminho)
    tempo_final = time.time()

    tempo = tempo_final - tempo_inicial
    return caminho, custo, expandidos, tempo


#-------------------------------


def main():

    #dados_bsf = {}
    dados_dfs = {}
    dados_a_star = {}
    dados_custo_uniforme = {}



    for _ in range(10):
        SEED = 43  # coloque None no lugar do 42 para deixar aleatorio
        random.seed(0)

        N_LINHAS  = 100
        N_COLUNAS = 100
        INICIO = Celula(y=0, x=0, anterior=None)
        GOAL   = Celula(y=N_LINHAS-1, x=N_COLUNAS-1, anterior=None)


        """
        O labirinto sera representado por uma matriz (lista de listas)
        em que uma posicao tem 0 se ela eh livre e 1 se ela esta ocupada.
        """
        labirinto = gera_labirinto(N_LINHAS, N_COLUNAS, INICIO, GOAL)

        viewer = MazeViewer(labirinto, INICIO, GOAL,
                            step_time_miliseconds=1, zoom=5)

        #----------------------------------------
        # BFS Search
        #----------------------------------------
        # viewer._figname = "BFS"
        # caminho, custo_total, expandidos, tempo = \
        #         breadth_first_search(labirinto, INICIO, GOAL, viewer)

        # if len(caminho) == 0:
        #     print("Goal é inalcançavel neste labirinto.")

        # print(
        #     f"BFS:"
        #     f"\tCusto total do caminho: {custo_total}.\n"
        #     f"\tNumero de passos: {len(caminho)-1}.\n"
        #     f"\tNumero total de nos expandidos: {len(expandidos)}.\n\n"
        #     f"\tTempo gasto: {round(tempo, 3)}s.\n"
        # )
        # dados_bsf[_] = [custo_total, len(caminho)-1, len(expandidos), tempo]
        # print(dados_bsf)
 

        #----------------------------------------
        # DFS Search
        #----------------------------------------
        viewer._figname = "DFS"
        caminho, custo_total, expandidos, tempo = \
                depth_first_search(labirinto, INICIO, GOAL, viewer)

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        print(
            f"DFS:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n\n"
            f"\tTempo gasto: {round(tempo, 3)}s.\n"
        )
        if len(caminho)-1 != -1:
            dados_dfs[_] = [custo_total, len(caminho)-1, len(expandidos), tempo]
            print(dados_dfs)


        #----------------------------------------
        # A-Star Search
        #----------------------------------------
        viewer._figname = "A-Star"
        caminho, custo_total, expandidos, tempo = \
                a_star_search(labirinto, INICIO, GOAL, viewer)

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        print(
            f"A-Star:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n\n"
            f"\tTempo gasto: {round(tempo, 3)}s.\n"
        )
        if len(caminho)-1 != -1:
            dados_a_star[_] = [custo_total, len(caminho)-1, len(expandidos), tempo]
            print(dados_a_star)


        #----------------------------------------
        # Uniform Cost Search (Obs: opcional)
        #----------------------------------------
        viewer._figname = "Custo Uniforme"
        caminho, custo_total, expandidos, tempo = \
                uniform_cost_search(labirinto, INICIO, GOAL, viewer)

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        print(
            f"Custo Uniforme:"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n\n"
            f"\tTempo gasto: {round(tempo, 3)}s.\n"
        )
        if len(caminho)-1 != -1:
            dados_custo_uniforme[_] = [custo_total, len(caminho)-1, len(expandidos), tempo]
            print(dados_custo_uniforme)


    media_DFS = calcular_media(dados_dfs)
    media_UCS = calcular_media(dados_custo_uniforme)
    print('\n MEDIA UCS: ', media_UCS)
    media_A_star = calcular_media(dados_a_star)

    exibir_graficos(dados_dfs)
    exibir_graficos(dados_custo_uniforme)
    exibir_graficos(dados_a_star)


    print('\n media DFS: ', media_DFS)
    print('\n media UCS: ', media_UCS)
    print('\n media A star: ', media_A_star)


    print("OK! Pressione alguma tecla pra finalizar...")
    input()


if __name__ == "__main__":
    main()
