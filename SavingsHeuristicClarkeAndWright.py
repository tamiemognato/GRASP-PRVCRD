import random
import time

from Functions.SavingsHeuristicClarkeAndWrightFunctions import CalculaDemandaTotalNovaRota, \
    CalculaTempoConsumidoNovaRota, UnirRotas, calcula_custo_total, TestarSePeloMenosUmClienteDaArestaNaoEstaServido, \
    VerificarPosicaoClientesRotas, LCR_GerarCompletaAleatoria

def SHCW_paralelo_randomizado(capacidade,demanda,economias,custos,lista_clientes_nao_atendidos_aux,maxtime,alfa):
    rotas = []
    #print(f"rotas: {rotas}")
    lista_clientes_nao_atendidos = lista_clientes_nao_atendidos_aux.copy() # Copiar lista de clientes não atendidos para não esvaziar a original para as próximas iterações do gerador de soluções
    #print(f"lista_clientes_nao_atendidos: ", lista_clientes_nao_atendidos)

    if alfa == 0:
        start_time_LCR = time.time()
        ListaEconomias = economias.copy()
        end_time_LCR = time.time()
        elapsed_time_LCR = end_time_LCR - start_time_LCR

    else:
        start_time_LCR = time.time()
        ListaEconomias = LCR_GerarCompletaAleatoria(economias,alfa)
        #ListaEconomias = economias.copy()
        end_time_LCR = time.time()

        elapsed_time_LCR = end_time_LCR - start_time_LCR
        #print("elapsed_time_LCR_GerarCompletaAleatoria:", elapsed_time_LCR_GerarCompletaAleatoria)

    start_time_AdTestes = time.time()
    #print(f"ListaEconomias: {ListaEconomias}")
    for ArestaEconomia in ListaEconomias:
        #print(f"lista_clientes_nao_atendidos: ", lista_clientes_nao_atendidos)

        if len(lista_clientes_nao_atendidos) == 0:
            #print(f"lista_clientes_nao_atendidos: ", lista_clientes_nao_atendidos)
            break

        aresta = ArestaEconomia[:2]
        # Testamos se os clientes da aresta (i e j) já não foram atendidos - para isso temos que verificar se eles ainda estão contidos na lista de clientes não atendidos
        PeloMenosUmClienteDaArestaNaoEstaServido = TestarSePeloMenosUmClienteDaArestaNaoEstaServido(aresta,lista_clientes_nao_atendidos)
        #print(f"rotas: {rotas}")
        #print("PeloMenosUmClienteDaArestaNaoEstaServido: ",PeloMenosUmClienteDaArestaNaoEstaServido)

        # Iniciar variáveis de posição de i e j e suas respectivas rotas
        posicao_rota_ArestaZero_i = -1
        posicao_ArestaZeroNaRota_i = -1
        posicao_rota_ArestaUm_j = -2
        posicao_ArestaUmNaRota_j = -2

        # Fazendo a verificação para atualizar a(s) rota(s) e posição(ões) de i e j
        posicao_rota_ArestaZero_i, posicao_ArestaZeroNaRota_i, posicao_rota_ArestaUm_j, posicao_ArestaUmNaRota_j = VerificarPosicaoClientesRotas(
            rotas, aresta, posicao_rota_ArestaZero_i, posicao_ArestaZeroNaRota_i, posicao_rota_ArestaUm_j,
            posicao_ArestaUmNaRota_j)

        #print("posicao_ArestaZeroNaRota_i :", posicao_ArestaZeroNaRota_i)
        #print("posicao_ArestaUmNaRota_j :", posicao_ArestaUmNaRota_j)

        # Se pelo menos um cliente não foi atendido, podemos testar se ele pode ser adicionado a rota do outro atendido
        # Se os dois clientes não foram atendidos, podemos testar a construção de uma nova rota
        if PeloMenosUmClienteDaArestaNaoEstaServido == True:
            # Mas aqui ainda não sabemos o que está acontecendo, se 1 ou se ambos não foram atendidos

            # Caso 1 - Se posição i = -1 e posição j = -2 - i e j ainda não foram atribuidos a nenhuma aresta e podemos testar a consutrção de uma nova rota
            if posicao_rota_ArestaZero_i == -1 and posicao_rota_ArestaUm_j == -2:
                #print("CASO 1 - i e j ainda não estão em uma rota")
                # Construir possível nova rota
                nova_rota = [0, aresta[0], aresta[1], 0]  # Por padrão construímos 0ij0, como i vem antes de j, e não 0ji0
                # Calcular demanda e tempo consumido
                DemandaTotal_nova_rota = CalculaDemandaTotalNovaRota(nova_rota, demanda)
                TempoConsumido_nova_rota = CalculaTempoConsumidoNovaRota(nova_rota, custos)
                # Definindo variáveis de demanda e tempo
                RespeitaLimiteDeCarga = False
                RespeitaBateria = False

                # Verificar se 0ij0 respeita as restrições de
                # Capacidade de carga do veículo
                if DemandaTotal_nova_rota <= capacidade:
                    RespeitaLimiteDeCarga = True

                # Capacidade de bateria do veículo
                if TempoConsumido_nova_rota <= maxtime:
                    RespeitaBateria = True

                # Se todas as condições são respeitadas
                if RespeitaLimiteDeCarga == True and RespeitaBateria == True: # Se as restrições são respeitadas, então podemos de fato construir essa rota

                    # Adicionar nova rota a rotas
                    #print(f"rotas antes: {rotas}")
                    rotas.append([0, aresta[0], aresta[1], 0])  # Adiciono a rota em construção na lista de rotas
                    #print("Nova rota: ",rotas[(len(rotas)-1)])
                    #print(f"rotas depois: {rotas}")

                    # Remover i e j da lista de clientes não atendidos
                    indice_i = lista_clientes_nao_atendidos.index(aresta[0])
                    lista_clientes_nao_atendidos.pop(indice_i)
                    indice_j = lista_clientes_nao_atendidos.index(aresta[1])
                    lista_clientes_nao_atendidos.pop(indice_j)
                    #print(f"lista_clientes_nao_atendidos: ", lista_clientes_nao_atendidos)

                    # Vá para a próxima aresta
                    continue

                else:
                    #print("Rota nova não respeitaria as restrições")
                    continue

            # Caso 2 - i foi atendido e j não - testamos adicionar j a rota de i - i estando na extremidade direita ou esquerda
            elif (posicao_rota_ArestaZero_i != -1 and posicao_rota_ArestaUm_j == -2):
                #print("CASO 2 - i está em uma rota e j não")
                # Criar cópia da rota de i para testar adição de j
                copia_rota_ArestaZero_i = rotas[posicao_rota_ArestaZero_i].copy()
                #print("copia_rota_ArestaZero_i: ",copia_rota_ArestaZero_i)
                iEstaNaExtremidadeDireita = False
                iEstaNaExtremidadeEsquerda = False

                #i na extremidade direita
                if posicao_ArestaZeroNaRota_i == (len(rotas[posicao_rota_ArestaZero_i]) - 2):
                    copia_rota_ArestaZero_i.insert(len(rotas[posicao_rota_ArestaZero_i]) - 1,aresta[1])
                    iEstaNaExtremidadeDireita = True
                    #print("i está na extremidade direita")
                    #print("copia_rota_ArestaZero_i: ",copia_rota_ArestaZero_i)
                #i na extremidade esquerda
                if posicao_ArestaZeroNaRota_i == 1:
                    copia_rota_ArestaZero_i.insert(1,aresta[1])
                    iEstaNaExtremidadeEsquerda = True
                    #print("i está na extremidade esquerda")
                    #print("copia_rota_ArestaZero_i: ",copia_rota_ArestaZero_i)

                if iEstaNaExtremidadeDireita == False and iEstaNaExtremidadeEsquerda == False:
                    #print("i não está em nenhuma das extremidades, portanto j não pode ser adicionado a rota.")
                    continue

                else:

                    # Calcular demanda e tempo consumido
                    DemandaTotal_nova_rota = CalculaDemandaTotalNovaRota(copia_rota_ArestaZero_i, demanda)
                    TempoConsumido_nova_rota = CalculaTempoConsumidoNovaRota(copia_rota_ArestaZero_i, custos)
                    # Definindo variáveis de demanda e tempo
                    RespeitaLimiteDeCarga = False
                    RespeitaBateria = False

                    # Verificar se 0ij0 respeita as restrições de
                    # Capacidade de carga do veículo
                    if DemandaTotal_nova_rota <= capacidade:
                        RespeitaLimiteDeCarga = True

                    # Capacidade de bateria do veículo
                    if TempoConsumido_nova_rota <= maxtime:
                        RespeitaBateria = True

                    # Se todas as condições são respeitadas
                    if RespeitaLimiteDeCarga == True and RespeitaBateria == True: # Se as restrições são respeitadas, então podemos de fato construir essa rota

                        # Adicionar nova rota a rotas
                        #print(f"rotas antes: {rotas}")
                        if iEstaNaExtremidadeDireita == True:
                            rotas[posicao_rota_ArestaZero_i].insert(len(rotas[posicao_rota_ArestaZero_i]) - 1,aresta[1])
                        if iEstaNaExtremidadeEsquerda == True:
                            rotas[posicao_rota_ArestaZero_i].insert(1,aresta[1])
                        #print(f"rotas depois: {rotas}")


                        # Remover j da lista de clientes não atendidos
                        indice_j = lista_clientes_nao_atendidos.index(aresta[1])
                        lista_clientes_nao_atendidos.pop(indice_j)
                        #print(f"lista_clientes_nao_atendidos: ", lista_clientes_nao_atendidos)

                        # Vá para a próxima aresta
                        continue
                    else:
                        #print("Rota nova não respeitaria as restrições")
                        continue

            # Caso 3 - j foi atendido e i não - testamos adicionar i a rota de j - j estando na extremidade direita ou esquerda
            elif (posicao_rota_ArestaZero_i == -1 and posicao_rota_ArestaUm_j != -2):
                #print("CASO 3 - j está em uma rota e i não")
                # Criar cópia da rota de j para testar adição de i
                copia_rota_ArestaZero_j = rotas[posicao_rota_ArestaUm_j].copy()
                #print("copia_rota_ArestaZero_j: ",copia_rota_ArestaZero_j)

                jEstaNaExtremidadeDireita = False
                jEstaNaExtremidadeEsquerda = False

                # j na extremidade direita
                if posicao_ArestaUmNaRota_j == (len(rotas[posicao_rota_ArestaUm_j]) - 2):
                    copia_rota_ArestaZero_j.insert(len(rotas[posicao_rota_ArestaUm_j]) - 1,aresta[0])
                    jEstaNaExtremidadeDireita = True
                    #print("j está na extremidade direita")
                    #print("copia_rota_ArestaZero_j: ", copia_rota_ArestaZero_j)
                # j na extremidade esquerda
                if posicao_ArestaUmNaRota_j == 1:
                    copia_rota_ArestaZero_j.insert(1,aresta[0])
                    jEstaNaExtremidadeEsquerda = True
                    #print("j está na extremidade esquerda")
                    #print("copia_rota_ArestaZero_j: ", copia_rota_ArestaZero_j)

                if jEstaNaExtremidadeDireita == False and jEstaNaExtremidadeEsquerda == False:
                    #print("j não está em nenhuma das extremidades, portanto i não pode ser adicionado a rota.")
                    continue

                else:
                    # Calcular demanda e tempo consumido
                    DemandaTotal_nova_rota = CalculaDemandaTotalNovaRota(copia_rota_ArestaZero_j, demanda)
                    TempoConsumido_nova_rota = CalculaTempoConsumidoNovaRota(copia_rota_ArestaZero_j, custos)
                    # Definindo variáveis de demanda e tempo
                    RespeitaLimiteDeCarga = False
                    RespeitaBateria = False

                    # Verificar se 0ij0 respeita as restrições de
                    # Capacidade de carga do veículo
                    if DemandaTotal_nova_rota <= capacidade:
                        RespeitaLimiteDeCarga = True

                    # Capacidade de bateria do veículo
                    if TempoConsumido_nova_rota <= maxtime:
                        RespeitaBateria = True

                    # Se todas as condições são respeitadas
                    if RespeitaLimiteDeCarga == True  and RespeitaBateria == True: # Se as restrições são respeitadas, então podemos de fato construir essa rota

                        # Adicionar nova rota a rotas
                        #print(f"rotas antes: {rotas}")
                        if jEstaNaExtremidadeDireita == True:
                            rotas[posicao_rota_ArestaUm_j].insert(len(rotas[posicao_rota_ArestaUm_j]) - 1,aresta[0])
                        if jEstaNaExtremidadeEsquerda == True:
                            rotas[posicao_rota_ArestaUm_j].insert(1,aresta[0])
                        #print(f"rotas depois: {rotas}")

                        # Remover j da lista de clientes não atendidos
                        indice_i = lista_clientes_nao_atendidos.index(aresta[0])
                        lista_clientes_nao_atendidos.pop(indice_i)
                        #print(f"lista_clientes_nao_atendidos: ", lista_clientes_nao_atendidos)

                        # Vá para a próxima aresta
                        continue
                    else:
                        #print("Rota nova não respeitaria as restrições")
                        continue

        # Se os dois clientes da aresta (i e j) já foram atendidos, podemos testar se as rotas podem ser unidas
        # Mas precisamos testar se estõa em rotas diferentes
        else:
            if posicao_rota_ArestaZero_i != posicao_rota_ArestaUm_j:
                #print("Caso 4 - i e j já estão em rotas diferentes")

                iEstaNaExtremidadeDireita = False
                iEstaNaExtremidadeEsquerda = False
                jEstaNaExtremidadeDireita = False
                jEstaNaExtremidadeEsquerda = False

                #i na extremidade direita
                if posicao_ArestaZeroNaRota_i == (len(rotas[posicao_rota_ArestaZero_i]) - 2):
                    iEstaNaExtremidadeDireita = True
                    #print("i está na extremidade direita")
                #i na extremidade esquerda
                if posicao_ArestaZeroNaRota_i == 1:
                    iEstaNaExtremidadeEsquerda = True
                    #print("i está na extremidade esquerda")
                # j na extremidade direita
                if posicao_ArestaUmNaRota_j == (len(rotas[posicao_rota_ArestaUm_j]) - 2):
                    jEstaNaExtremidadeDireita = True
                    #print("j está na extremidade direita")
                # j na extremidade esquerda
                if posicao_ArestaUmNaRota_j == 1:
                    jEstaNaExtremidadeEsquerda = True
                    #print("j está na extremidade esquerda")


                #i na extremidade direita e j na extremidade esquerda
                if iEstaNaExtremidadeDireita == True and jEstaNaExtremidadeEsquerda == True:
                    #print("Caso 4.1 - i na extremidade direita e j na extremidade esquerda")

                    copia_rota_ArestaZero_i = rotas[posicao_rota_ArestaZero_i].copy()
                    copia_rota_ArestaUm_j = rotas[posicao_rota_ArestaUm_j].copy()
                    #print("copia_rota_ArestaZero_i: ",copia_rota_ArestaZero_i)
                    #print("copia_rota_ArestaUm_j: ",copia_rota_ArestaUm_j)
                    nova_rota = UnirRotas(copia_rota_ArestaZero_i, copia_rota_ArestaUm_j)
                    #print("Nova rota: ", nova_rota)

                    DemandaTotal_nova_rota = CalculaDemandaTotalNovaRota(nova_rota, demanda)
                    TempoConsumido_nova_rota = CalculaTempoConsumidoNovaRota(nova_rota, custos)

                    RespeitaLimiteDeCarga = False
                    RespeitaBateria = False

                    # Verificar se 0ij0 respeita as restrições de
                    # Capacidade de carga do veículo
                    if DemandaTotal_nova_rota <= capacidade:
                        RespeitaLimiteDeCarga = True

                    # # Capacidade de bateria do veículo
                    if TempoConsumido_nova_rota <= maxtime:
                        RespeitaBateria = True

                    if RespeitaLimiteDeCarga == True and RespeitaBateria == True:  # Se as restrições são respeitadas, então podemos de fato adicionar j a rota em construção
                        #print(f"rotas antes: {rotas}")
                        rotas.remove(copia_rota_ArestaZero_i)  # Precisamos remover a rota de i
                        rotas.remove(copia_rota_ArestaUm_j)  # Precisamos remover a rota de j
                        rotas.append(nova_rota)  # Adicionamos a nova rota
                        #print(f"rotas depois: {rotas}")
                        continue

                    else:
                        #print("Rota nova não respeitaria as restrições")
                        continue



                #i na extremidade esquerda e j na extremidade direita
                elif iEstaNaExtremidadeEsquerda == True and jEstaNaExtremidadeDireita == True:
                    #print("Caso 4.2 - i na extremidade esquerda e j na extremidade direita")

                    copia_rota_ArestaZero_i = rotas[posicao_rota_ArestaZero_i].copy()
                    copia_rota_ArestaUm_j = rotas[posicao_rota_ArestaUm_j].copy()
                    #print("copia_rota_ArestaZero_i: ",copia_rota_ArestaZero_i)
                    #print("copia_rota_ArestaUm_j: ",copia_rota_ArestaUm_j)
                    nova_rota = UnirRotas(copia_rota_ArestaUm_j, copia_rota_ArestaZero_i)
                    #print("Nova rota: ", nova_rota)

                    DemandaTotal_nova_rota = CalculaDemandaTotalNovaRota(nova_rota, demanda)
                    TempoConsumido_nova_rota = CalculaTempoConsumidoNovaRota(nova_rota, custos)

                    RespeitaLimiteDeCarga = False
                    RespeitaBateria = False

                    # Verificar se 0ij0 respeita as restrições de
                    # Capacidade de carga do veículo
                    if DemandaTotal_nova_rota <= capacidade:
                        RespeitaLimiteDeCarga = True

                    # Capacidade de bateria do veículo
                    if TempoConsumido_nova_rota <= maxtime:
                        RespeitaBateria = True

                    if RespeitaLimiteDeCarga == True and RespeitaBateria == True:  # Se as restrições são respeitadas, então podemos de fato adicionar j a rota em construção
                        #print(f"rotas antes: {rotas}")
                        rotas.remove(copia_rota_ArestaZero_i)  # Precisamos remover a rota de i
                        rotas.remove(copia_rota_ArestaUm_j)  # Precisamos remover a rota de j
                        rotas.append(nova_rota)  # Adicionamos a nova rota
                        #print(f"rotas depois: {rotas}")
                        continue

                    else:
                        #print("Rota nova não respeitaria as restrições")
                        continue

                else:
                    #print("i e j estão nas extremidades esquerdas ou direitas de suas respectivas rotas")
                    continue

            else:
                #print("Caso 5 - i e j estão na mesma rota")
                continue

    # Se houver algum cliente que não foi possível adionar as rotas construídas:
    if len(lista_clientes_nao_atendidos) != 0:
        for cliente_nao_atendido_nao_adicionavel_a_outras_rotas in lista_clientes_nao_atendidos:
            rotas.append([0,cliente_nao_atendido_nao_adicionavel_a_outras_rotas,0])
            lista_clientes_nao_atendidos.pop(lista_clientes_nao_atendidos.index(cliente_nao_atendido_nao_adicionavel_a_outras_rotas))

    end_time_AdTestes = time.time()
    elapsed_time_AdTestes = end_time_AdTestes - start_time_AdTestes
    custo_total, custo_por_rota = calcula_custo_total(custos, rotas)

    return rotas, custo_total, elapsed_time_LCR, elapsed_time_AdTestes

