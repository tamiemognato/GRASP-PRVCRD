from Functions.DoisOPTFunctions import calcula_custo_rota_doisopt, GerarLCPNA
from Functions.SavingsHeuristicClarkeAndWrightFunctions import calcula_custo_total


def DOIS_OPT(rotas,custos):
    quantidade_iteracoes_total = 0
    melhores_rotas = []
    # 001: Para cada rota em rotas, fazer:
    for rota in rotas:
        # 002: atual_melhor_versao_da_rota  rota
        melhor_versao_da_rota = rota
        melhor_custo = calcula_custo_rota_doisopt(custos, rota)
        houve_melhora = True

        quantidade_iteracoes_total += 1

        # 003:	Enquanto houver alguma melhoria na atual_melhor_versao_da_rota, fazer:
        while houve_melhora == True:
            possiveis_trocas = []  #Lista de listas [[rota_linha, custo],...]

            # 004: Criar todas as combinações possíveis entre os pontos não adjacentes da rota, exceto com o depósito 0 (Lista de listas [i,j])
            LCPNA = GerarLCPNA(melhor_versao_da_rota) # LCPA - Lista combinação pontos não adjacentes - lista de listas [i,j]

            # 005: Para cada par de ponto em Lista de listas [i,j], fazer:
            if len(LCPNA) != 0:
                for par in LCPNA:

                    # 006: Fragmentar a rota com base em i e j
                    posicao_i_na_rota = melhor_versao_da_rota.index(par[0])
                    posicao_j_na_rota = melhor_versao_da_rota.index(par[1])
                    # A primeira parte vai do primeiro elemento da rota até o primeiro elemento do par - i
                    primeira_parte = melhor_versao_da_rota[:posicao_i_na_rota+1]
                    # A segunda parte vai do elemento posterior ao primeiro da troca até o segundo elemento do par - j
                    segunda_parte = melhor_versao_da_rota[posicao_i_na_rota+1:posicao_j_na_rota+1]
                    # A terceira parte vai do elemento posterior ao segundo da troca até o último elemento da rota
                    terceira_parte = melhor_versao_da_rota[posicao_j_na_rota+1:]

                    # 007: Recombinar a rota em rota’
                    segunda_parte.reverse()
                    rota_linha = primeira_parte + segunda_parte + terceira_parte

                    # 008:	Calcular custo de rota’
                    custo_rota_linha = calcula_custo_rota_doisopt(custos, rota_linha)

                    # 009:	Se custo rota’ < custo rota:
                    if custo_rota_linha < melhor_custo:
                        possiveis_trocas.append([rota_linha,custo_rota_linha])


                if len(possiveis_trocas) != 0:
                    #ordenar de forma crescente a lista de listas a partir do custo [[rota_linha, custo],...] - assim a primeira lista terá a rota_linha com menor custo e que emprega, portanto, a melhor melhora na atual melhor rota a ser substituida
                    possiveis_trocas_ordenadas = sorted(possiveis_trocas, key=lambda x: x[1])
                    # 010:	atual_melhor_versao_da_rota  rota_linha
                    melhor_versao_da_rota = possiveis_trocas_ordenadas[0][0]
                    melhor_custo = possiveis_trocas_ordenadas[0][1]
                    # como houve_melhora ainda igual a true, continue o while

                else: #se nada tiver sido adicionado a possiveis_trocas - não houve nenhuma melhora após testar toda a LCPNA para a atual_melhor_versao_da_rota, parar e seguir o for
                    houve_melhora = False

            # Se não houver pontos não adjacentes, parar o while
            else:
                break

        # Adicionar a lista das melhores rotas após ter encontrado a melhor rota definitivamente
        melhores_rotas.append(melhor_versao_da_rota)

    custo_total_melhores_rotas, custo_por_rota_melhores_rotas = calcula_custo_total(custos, melhores_rotas)

    return melhores_rotas, custo_total_melhores_rotas, quantidade_iteracoes_total



