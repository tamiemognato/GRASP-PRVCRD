
import logging
import json
import math
import random

def LCR_GerarCompletaAleatoria(economias, alfa):
    aux_economias = economias.copy()  # Copiar economias para não alterar a lista para os próximos loops
    ListaEconomias = []
    #contador = 0  # contador condição de parada para percorrer lista inteira
    #condicao_parada = len(aux_economias)
    while len(aux_economias) != 0:
        posicao_aux = len(aux_economias) - 1
        #print("condicao_parada: ", condicao_parada)
        #print("contador: ", contador)
        #print("posicao_aux: ", posicao_aux)
        gmin = aux_economias[posicao_aux][2]
        gmax = aux_economias[0][2]
        CorteSelecaoLCR = (gmax - alfa * (gmax - gmin))

        contador_CorteSelecaoLCR = 0
        while aux_economias[contador_CorteSelecaoLCR][2] >= CorteSelecaoLCR:
            contador_CorteSelecaoLCR += 1
            if contador_CorteSelecaoLCR == len(aux_economias): # para evitar index out of range - se rodar CMT10 sem isto dá erro
                contador_CorteSelecaoLCR -= 1
                break
        #print("CALCULOU NOVO CONTADOR CORTESELECAO")
        #print("contador_CorteSelecaoLCR: ", contador_CorteSelecaoLCR)
        #print(aux_economias[:contador_CorteSelecaoLCR+1])
        indice_CorteSelecaoLCR = 999999999999
        while indice_CorteSelecaoLCR != 0 and indice_CorteSelecaoLCR != posicao_aux:
            indice_CorteSelecaoLCR = random.randint(0, contador_CorteSelecaoLCR)
            #print("indice_CorteSelecaoLCR: ", indice_CorteSelecaoLCR)
            #print(aux_economias[indice_CorteSelecaoLCR])
            ListaEconomias.extend([aux_economias[indice_CorteSelecaoLCR]])
            del aux_economias[indice_CorteSelecaoLCR]

            if len(aux_economias) == 0: # se a lista estiver vazia, break, pois a condição do loop anterior não irá pegar dentro desse loop
                break

            # a cada vez que usamos um indice_CorteSelecaoLCR temos que descer o limite do contador_CorteSelecaoLCR
            # se começamos com contador_CorteSelecaoLCR = 8 então temos [0,1,2,3,4,5,6,7,8]
            # se sorteamos indice_CorteSelecaoLCR = 5 então devemos passar a ter [0,1,2,3,4,5,6,7] para o próximo sorteio, pois revemos a aresta de aux_economias com o comando del
            contador_CorteSelecaoLCR -= 1

            #print(aux_economias[:contador_CorteSelecaoLCR + 1])

        #print("SAIU DO WHILE INDICE CORTESELECAOLCR")

    return ListaEconomias

def VerificarPosicaoClientesRotas(rotas,aresta,posicao_rota_ArestaZero_i,posicao_ArestaZeroNaRota_i,posicao_rota_ArestaUm_j,posicao_ArestaUmNaRota_j):

    for rota in rotas:  # Para cada rota
        if aresta[0] in rota:  # Verificamos se i está contida nela
            posicao_rota_ArestaZero_i = rotas.index(rota)  # Definindo a variavel auxiliar para gravar a posição da rota em rotas de i
            posicao_ArestaZeroNaRota_i = rota.index(aresta[0])  # Definindo a variável auxiliar para gravar a posição de i na rota
            # print(f"Rota atual da aresta i: {rotas[posicao_rota_ArestaZero_i]}")

        if aresta[1] in rota:  # verificamos se j está contida nela
            posicao_rota_ArestaUm_j = rotas.index(rota)  # Definindo a variável auxiliar para gravar a posição da rota em rotas de j
            posicao_ArestaUmNaRota_j = rota.index(aresta[1])  # Definindo a variável auxiliar para gravar a posição da j na rota
            # print(f"Rota atual da aresta j: {rotas[posicao_rota_ArestaUm_j]}")

    return posicao_rota_ArestaZero_i,posicao_ArestaZeroNaRota_i,posicao_rota_ArestaUm_j,posicao_ArestaUmNaRota_j

def TestarSePeloMenosUmClienteDaArestaNaoEstaServido(aresta,lista_clientes_nao_atendidos):
    PeloMenosUmClienteDaArestaNaoEstaServido = False

    if aresta[0] in lista_clientes_nao_atendidos:
        PeloMenosUmClienteDaArestaNaoEstaServido = True

    if aresta[1] in lista_clientes_nao_atendidos:
        PeloMenosUmClienteDaArestaNaoEstaServido = True

    return PeloMenosUmClienteDaArestaNaoEstaServido

def calcula_ROUTES_DEMANDAS_E_TOTAL_POINTS(rotas,demanda):
    listaROUTES_DEMANDS = []
    listaTOTAL_POINTS = []
    for rota in rotas:
        demandarotas = 0
        contadorpontos = -2
        for k in rota:
            demandarotas = demandarotas + demanda[k]
            contadorpontos = contadorpontos + 1
        listaROUTES_DEMANDS.append(demandarotas)
        listaTOTAL_POINTS.append(contadorpontos)

    return listaROUTES_DEMANDS, listaTOTAL_POINTS

def criar_rotas_0i0(demanda):
    pontos = list(range(0, len(demanda)))
    rotas = list()

    for i in pontos:
        if i != 0:
            aux = []
            aux.append(pontos[0])
            aux.append((pontos[i]))
            aux.append(pontos[0])
            rotas.append(aux)

    return rotas

def salvar_dicionario_em_arquivo(dicionario, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dicionario, arquivo)

def calcula_custo_total(matriz_tempos, rotas):
    custo_total = 0
    custo_por_rota = []
    for rota in rotas:
        aux = 0
        #print('rota:',rota)
        for i in range(len(rota) - 1):
            par = (rota[i], rota[i + 1])
            #print('par:',par)
            #print('matriz_distancias[rota[i]]:', matriz_distancias[rota[i]])
            #print('matriz_distancias[rota[i]][rota[i + 1]]:', matriz_distancias[rota[i]][rota[i + 1]])
            custo_total += matriz_tempos[rota[i]][rota[i + 1]]
            #print('custo_total:', custo_total)
            aux += matriz_tempos[rota[i]][rota[i + 1]]

        custo_por_rota.append(aux)

    return custo_total, custo_por_rota

def calcula_custo_rota(matriz_tempos, rota, aresta):
    aux = 0
    for j in aresta:
        if j not in rota:
            aux = j
    #print(rota)
    #print(aux)

    aux_rota = []
    #print("aux_rota:",aux_rota)
    for k in rota:
        aux_rota.append(k)
    #print("aux_rota:",aux_rota)

    aux_rota.insert(len(rota)-1,aux)
    #print("aux_rota:",aux_rota)


    custo_rota = 0
    for i in range(len(aux_rota) - 1):
        custo_rota += matriz_tempos[aux_rota[i]][aux_rota[i + 1]]



    return custo_rota

def DemandaTotal(ListaDemanda,rota,aresta):

    ListaPontosUnicos  = []
    DemandaTotalSoma = 0
    for j in aresta:
        ListaPontosUnicos.append(j)

    for i in rota:
        if i not in ListaPontosUnicos:
            ListaPontosUnicos.append(i)

    for k in ListaPontosUnicos:
        DemandaTotalSoma = DemandaTotalSoma + ListaDemanda[k]


    return DemandaTotalSoma

#mudar para lista 
def calculate_savings_dici(distance_matrix):
    savings = dict()
    linha = 0
    while linha < len(distance_matrix):     #Para toda linha
        coluna = 0
        while coluna < len(distance_matrix):    #Passar por toda coluna
            if coluna != linha :    #Ignorar distancias igual a 0
                a = min(linha, coluna)
                b = max(linha, coluna)
                key = '(' + str(a) + ',' + str(b) + ')'     #Fazer chave de coordenada
                savings[key] = distance_matrix[0][linha] + distance_matrix[0][coluna] - distance_matrix[coluna][linha]  # Calcula a economia para a coordenada dada por Key

            coluna +=1
        linha +=1

    savings = sort_dictionary_desc(savings)
    arestasRemover = []
    for aresta in savings:
        if not savings[aresta]:
            arestasRemover.append(aresta)

    for aresta in arestasRemover:
        del savings[aresta]

    return savings




def calculate_savings(distance_matrix):
    savings = []
    processed_pairs = set()

    for linha in range(1, len(distance_matrix)):  # Começamos a partir de 1 para ignorar a linha 0
        for coluna in range(1, len(distance_matrix)):  # Começamos a partir de 1 para ignorar a coluna 0
            if coluna != linha:
                a = min(linha, coluna)
                b = max(linha, coluna)
                pair = (a, b)

                if pair not in processed_pairs: # Não adicionar arestas repetidas
                    saving = distance_matrix[0][linha] + distance_matrix[0][coluna] - distance_matrix[coluna][linha]
                    savings.append([a, b, saving])
                    processed_pairs.add(pair)

    filtro_savings = [sublista for sublista in savings if sublista[2] > 0]

    savings_sorted = sorted(filtro_savings, key=lambda x: x[2], reverse=True)


    return savings_sorted



def gerar_combinacoes(rotas, clientes_nao_atendidos):
    lista_pares = []

    for lista in rotas:
        for ponto in clientes_nao_atendidos:
            # Adiciona a combinação [ponto, elemento da lista] à lista final
            lista_pares.append([ponto, lista[1]])
            lista_pares.append([ponto, lista[-2]])
    return lista_pares

def calculate_savings_final(distance_matrix,lista_pares):
    savings = []
    processed_pairs = set()

    for par in lista_pares:
        saving = distance_matrix[0][par[0]] + distance_matrix[0][par[1]] - distance_matrix[par[0]][par[1]]
        savings.append([par[0], par[1], saving])

    filtro_savings = [sublista for sublista in savings if sublista[2] > 0]

    savings_sorted = sorted(filtro_savings, key=lambda x: x[2], reverse=True)

    return savings_sorted

def sort_dictionary_desc(dictionary):
    sorted_dict = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
    return sorted_dict

def get_node(link):     #Converte o link em string para inteiros
    link = link[1:]
    link = link[:-1]
    nodes = link.split(',')
    return [int(nodes[0]), int(nodes[1])]

def procurar_sequencia(lista, sequencia):
    tamanho_sequencia = len(sequencia)
    for i in range(len(lista) - tamanho_sequencia + 1):
        if lista[i:i+tamanho_sequencia] == sequencia:
            return i
    return -1









def VerificaJaEstaoNaMesmaRota(rota,aresta1):
    indice = procurar_sequencia(rota, aresta1)
    if indice == -1:
        JaEstaoNaMesmaRota = False
        logging.info(f"JaEstaoNaMesmaRota: {JaEstaoNaMesmaRota}")
    else:
        JaEstaoNaMesmaRota = True
        logging.info(f"JaEstaoNaMesmaRota: {JaEstaoNaMesmaRota}")

    return JaEstaoNaMesmaRota




def VerificaArestaZeroArestaUmJaEstaNaRota(rota,aresta1):
    ArestaZeroJaEstaNaRota = []
    ArestaUmJaEstaNaRota = []
    NenhumaEsta = True

    if aresta1[0] in rota:
        ArestaZeroJaEstaNaRota = rota
        #logging.info(f"ArestaZeroJaEstaNaRota: {ArestaZeroJaEstaNaRota}")

    if aresta1[1] in rota:
        ArestaUmJaEstaNaRota = rota
        #logging.info(f"ArestaUmJaEstaNaRota: {ArestaUmJaEstaNaRota}")

    if len(ArestaUmJaEstaNaRota) != 0 or len(ArestaZeroJaEstaNaRota) !=0:
        NenhumaEsta = False

    return ArestaZeroJaEstaNaRota, ArestaUmJaEstaNaRota, NenhumaEsta




def GeraListaArestasContendoPontosEmComumComAresta1(economias,aresta1):
    ListaArestasContendoPontosEmComumComAresta1 = []
    for aresta2 in economias:  # eu deveria fazer isso só depois de ver que posso adicionar a primeira aresta1 a uma rota
        if get_node(aresta2)[0] == aresta1[0] or get_node(aresta2)[1] == aresta1[0] or get_node(aresta2)[0] == aresta1[1] or get_node(aresta2)[1] == aresta1[1]:
            ListaArestasContendoPontosEmComumComAresta1.append(get_node(aresta2))

    return ListaArestasContendoPontosEmComumComAresta1




def RemoverARotaDaSegundaAresta(rotas, aresta1):
    # remover a rota da segunda aresta - converter para função
    QuantasVezesApareceAresta1 = 0
    QuantasVezesApareceAresta0 = 0

    for rota in rotas:
        if aresta1[1] in rota:
            QuantasVezesApareceAresta1 = QuantasVezesApareceAresta1 + 1
            # if QuantasVezesApareceAresta1 > 1 and len(rota) == 3:
            #     rotas.remove(rota)

        if aresta1[0] in rota:
            QuantasVezesApareceAresta0 = QuantasVezesApareceAresta0 + 1
            # if QuantasVezesApareceAresta0 > 1 and len(rota) == 3:
            #     rotas.remove(rota)

    for rota in rotas:
        if aresta1[1] in rota:
            if QuantasVezesApareceAresta1 > 1 and len(rota) == 3:
                rotas.remove(rota)
        if aresta1[0] in rota:
            if QuantasVezesApareceAresta0 > 1 and len(rota) == 3:
                rotas.remove(rota)

    return




def TesteSeAOutraArestaJaEstaEmUmaRotaDeLenMaiorQueTres(aresta,rotas):
    ArestaZeroJaEstaEmUmaRotaDeLenMaiorQueTres = False
    ArestaUmJaEstaEmUmaRotaDeLenMaiorQueTres = False
    contatorArestaZero = 0
    contadorArestaUm = 0
    for rota in rotas:
        if aresta[0] in rota and len(rota) > 3:
            contatorArestaZero = contatorArestaZero + 1

        if aresta[1] in rota and len(rota) > 3:
            contadorArestaUm = contadorArestaUm + 1

    if contatorArestaZero > 0:
        ArestaZeroJaEstaEmUmaRotaDeLenMaiorQueTres = True

    if contadorArestaUm > 0:
        ArestaUmJaEstaEmUmaRotaDeLenMaiorQueTres = True

    return ArestaZeroJaEstaEmUmaRotaDeLenMaiorQueTres, ArestaUmJaEstaEmUmaRotaDeLenMaiorQueTres



def ContadorPontosCheckDoisOpt(lista):
    contadorClientes = 0
    for i in lista:
        contadorClientes += 1

    return contadorClientes


def GerarListaDeArestasDoDicionarioDeEconomias(economias):
    # ENTRA - economias {'(35,36)': 77.25712373315542, '(20,35)': 64.7870146577865, '(3,36)': 64.40636049158243,...
    # RETORNA - lista_arestas [[35, 36], [20, 35], [3, 36],...

    lista_arestas = []

    for economia in economias:
        aux = get_node(economia)
        #aux.append("NÃO AVALIADA")
        lista_arestas.append(aux)

    return lista_arestas

def GerarListaDePontos(total_clientes):
    lista_pontos = []

    return lista_pontos




def CalculaDemandaTotalNovaRota(nova_rota,demanda):
    DemandaTotal_nova_rota = 0
    for k in nova_rota:
        if k != 0:
            DemandaTotal_nova_rota = DemandaTotal_nova_rota + demanda[k]

    return DemandaTotal_nova_rota

def CalculaTempoConsumidoNovaRota(rota,custos):
    TempoConsumido_nova_rota = 0
    i = 0
    while i < len(rota) - 1:
        TempoConsumido_nova_rota += custos[rota[i]][rota[i+1]]
        #print(rota[i])
        #print(rota[i+1])
        #print(custos[rota[i]][rota[i+1]])
        i += 1
    #print(TempoConsumido_nova_rota)
    return TempoConsumido_nova_rota


def UnirRotas(rota1, rota2):
    # Remover os pontos de partida e chegada das rotas
    rota1 = rota1[1:-1]
    rota2 = rota2[1:-1]

    # Unir as rotas
    rota_unida = rota1 + rota2

    # Adicionar os pontos de partida e chegada de volta à rota unida
    rota_unida = [0] + rota_unida + [0]

    return rota_unida

def GerarDicionarioDeEconomiasApenasComArestasRestantes(lista_arestas, economias):
    economias_lista_arestas = {}

    for aresta in lista_arestas:
        chave = f'({aresta[0]},{aresta[1]})'
        if chave in economias:
            economias_lista_arestas[chave] = economias[chave]

    return economias_lista_arestas


def GerarLCR(economias_lista_arestas, CorteSelecaoLCR):
    LCR = {chave: valor for chave, valor in economias_lista_arestas.items() if valor >= CorteSelecaoLCR}
    #LCR = GerarListaDeArestasDoDicionarioDeEconomias(LCR_aux)
    return LCR



