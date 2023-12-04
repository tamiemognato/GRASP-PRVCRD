import math


def time(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def generate_time_matrix(list):
    n = len(list)
    time_matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            x1, y1 = list[i]
            x2, y2 = list[j]
            time_matrix[i][j] = time(x1, y1, x2, y2)

    return time_matrix

def GerarListaClientes(dimension):
    lista_clientes = []
    contador = 1
    while contador < dimension:
        lista_clientes.append(contador)
        contador += 1

    return lista_clientes

