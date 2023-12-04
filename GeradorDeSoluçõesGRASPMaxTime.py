import random
import os
import glob
import time

from Functions.GRASP import GRASP_MaxTime
from Functions.InstancesReader import insert_instance_in_the_dictionary
from Functions.PosProcessing import Testa_Solucao_Retorna_Erros_EVRPST, CriarExcel_lista_registros_melhoras_GRASP, \
    CriarExcelTabelaComparativa_GRASPMaxTime, GerarDicionarioSolucao
from Functions.PreProcessing import generate_time_matrix, GerarListaClientes
from Functions.SavingsHeuristicClarkeAndWrightFunctions import calculate_savings

os.chdir("Instances")

files_inputrun = glob.glob('*.vrp')
if len(files_inputrun) == 0:
    print("There is no valid input file to read in the folder.")
else:
    print(files_inputrun)

for file in files_inputrun:
    dic_instance = insert_instance_in_the_dictionary(file)
    print("----------------------------------------------------------------------------------------------------------")
    print(dic_instance)

    custos = generate_time_matrix(dic_instance['NODE_COORD'])
    demanda = dic_instance['DEMAND']
    capacidade = dic_instance['CAPACITY']
    lista_clientes = GerarListaClientes(dic_instance['DIMENSION'])
    economias = calculate_savings(custos)  #Calcula o savings e ordena de forma descrescente

    lista_semente = [1,2,3,4,5,6,7,8,9,10]
    lista_NumeroMaximoIteracoesSemMelhoria = [15]
    TempoMaximo = [600]
    lista_alfa = [0.1]
    s = 0
    maxtime = dic_instance['MAXTIME'] - (dic_instance['MAXTIME'] * s)
    lista_dicicionarios_solucoes = []
    listas_lista_registros_melhoras = []
    lista_dicicionarios_solucoes_aux = []

    for tempomaximo in TempoMaximo:
        for NumeroMaximoIteracoesSemMelhoria in lista_NumeroMaximoIteracoesSemMelhoria:
            for alfa in lista_alfa:
                for semente in lista_semente:
                    random.seed(semente)
                    start_time = time.time()
                    MelhorSolucao, CustoMelhorSolucao, iteracoesMelhorSolucao, tempoMelhorSolucao, ContadorTempoMaximo, lista_registros_melhoras = GRASP_MaxTime(NumeroMaximoIteracoesSemMelhoria, capacidade, demanda, economias, custos, lista_clientes, maxtime, alfa,semente,tempomaximo)
                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    lista_dicicionarios_solucoes_aux.append([MelhorSolucao,elapsed_time,semente,ContadorTempoMaximo,tempomaximo,iteracoesMelhorSolucao,tempoMelhorSolucao])
                    listas_lista_registros_melhoras.append(lista_registros_melhoras)


    for aux in lista_dicicionarios_solucoes_aux:
        dic_solucao = GerarDicionarioSolucao(aux[0], aux[1], demanda, custos, dic_instance['NAME'], s, alfa,
                                             aux[2], maxtime, capacidade, NumeroMaximoIteracoesSemMelhoria)

        Erro = Testa_Solucao_Retorna_Erros_EVRPST(dic_instance, dic_solucao)
        dic_conferencia_erro = {'Erro': Erro}
        dic_solucao.update(dic_conferencia_erro)

        dic_ContadorTempoMaximo = {'ContadorTempoMaximo': aux[3]}
        dic_solucao.update(dic_ContadorTempoMaximo)

        dic_TempoMaximo = {"TempoMaximo": aux[4]}
        dic_solucao.update(dic_TempoMaximo)

        dic_iteracoesMelhorSolucao = {"iteracoesMelhorSolucao" : aux[5]}
        dic_solucao.update(dic_iteracoesMelhorSolucao)

        dic_tempoMelhorSolucao = {"tempoMelhorSolucao" : aux[6]}
        dic_solucao.update(dic_tempoMelhorSolucao)

        lista_dicicionarios_solucoes.append(dic_solucao)

    CriarExcelTabelaComparativa_GRASPMaxTime(lista_dicicionarios_solucoes,file)
    CriarExcel_lista_registros_melhoras_GRASP(listas_lista_registros_melhoras,file)

