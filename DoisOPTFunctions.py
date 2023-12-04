def GerarLCPNA(rota):
    # melhor_versao_da_rota:  [0, 17, 37, 44, 42, 19, 40, 41, 13, 25, 14, 0]
    LCPNA = []  # LCPA - Lista combinação pontos não adjacentes - lista de listas [i,j]
    lista_posicoes = list(range(1,len(rota)-1,1))
    for posicao_i in lista_posicoes:
        for posicao_j in lista_posicoes[posicao_i+1:]:
            aux_LCPNA = []
            aux_LCPNA.append(rota[posicao_i])  # Adicione i
            aux_LCPNA.append(rota[posicao_j])  # Adicione j
            LCPNA.append(aux_LCPNA)
    return LCPNA


def calcula_custo_rota_doisopt(custos, rota):
    custo_rota = 0
    for i in range(len(rota) - 1):
        par = (rota[i], rota[i + 1])
        custo_rota += custos[rota[i]][rota[i + 1]]
    return custo_rota