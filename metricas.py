import matplotlib.pyplot as plt
import numpy as np


def calcular_media(iteracoes):
    if not iteracoes:
        return None

    num_iteracoes = len(iteracoes)
    media_custos = 0
    media_tamanhos = 0
    media_tempos = 0
    print(iteracoes)
    for key in iteracoes.keys():
        iteracao = iteracoes[key]
        media_custos += iteracao[0]
        media_tamanhos += iteracao[1]
        media_tempos += iteracao[3]

    media_custos /= num_iteracoes
    media_tamanhos /= num_iteracoes
    media_tempos /= num_iteracoes


    return {'media_custo':media_custos, 'media_tamanho':media_tamanhos, 'media_tempo':media_tempos}


def exibir_graficos(data_dict):
    iterations = list(data_dict.keys())
    cost_totals = [data[0] for data in data_dict.values()]
    path_lengths = [data[1] for data in data_dict.values()]
    expanded_nodes = [data[2] for data in data_dict.values()]
    execution_times = [data[3] for data in data_dict.values()]

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 2, 1)
    plt.plot(iterations, cost_totals, marker='o')
    plt.title('Custo Total por Iteração')
    plt.xlabel('Iteração')
    plt.ylabel('Custo Total')

    plt.subplot(2, 2, 2)
    plt.plot(iterations, path_lengths, marker='o', color='g')
    plt.title('Comprimento do Caminho por Iteração')
    plt.xlabel('Iteração')
    plt.ylabel('Comprimento do Caminho')

    plt.subplot(2, 2, 3)
    plt.plot(iterations, expanded_nodes, marker='o', color='r')
    plt.title('Total de Nós Expandidos por Iteração')
    plt.xlabel('Iteração')
    plt.ylabel('Total de Nós Expandidos')

    plt.subplot(2, 2, 4)
    plt.plot(iterations, execution_times, marker='o', color='c')
    plt.title('Tempo de Execução por Iteração')
    plt.xlabel('Iteração')
    plt.ylabel('Tempo de Execução (segundos)')

    plt.tight_layout()
    plt.show()


    return 0
# Exemplo de dicionário


