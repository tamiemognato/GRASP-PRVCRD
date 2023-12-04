import time

from Functions.DoisOPT import DOIS_OPT
from Functions.SavingsHeuristicClarkeAndWright import SHCW_paralelo_randomizado




def GRASP_MaxTime(NumeroMaximoIteracoesSemMelhoria,capacidade,demanda,economias,custos,lista_clientes_nao_atendidos_aux,maxtime,alfa,semente,maxtime_grasp):
    start_time = time.time()
    #print("GRASP: ")
    iteracao = 1
    tempomaximo = maxtime_grasp
    lista_registros_melhoras = [] # [[custo, iteração, tempo],[custo, iteração, tempo],...]
    # 001: MelhorSolução  ∞
    MelhorSolucao = []
    CustoMelhorSolucao = 99999999999999999999999999999
    # #print("MelhorSolucao: ",MelhorSolucao)
    # 002: Conta_iterações_sem_melhoria  0
    ContadorIteracoesSemMelhoria = 0
    ContadorTempoMaximo = 0

    # 003: Enquanto Conta_iterações_sem_melhoria <= Número_máximo_iterações_sem_melhoria :
    start_ContadorTempoMaximo = time.time()
    while ContadorIteracoesSemMelhoria < NumeroMaximoIteracoesSemMelhoria and ContadorTempoMaximo < tempomaximo:
        start_iteracaoGRASP = time.time()
        aux = [] # [custo, iteração, tempo]
        # 004: SoluçãoSavingsAleatório  SavingsAleatório(Instância, α)
        start_time_savings_inteiro = time.time()
        SoluçãoSavingsAleatório, CustoSoluçãoSavingsAleatório,elapsed_time_LCR,elapsed_time_AdTestes  = SHCW_paralelo_randomizado(capacidade,demanda,economias,custos,lista_clientes_nao_atendidos_aux,maxtime,alfa)
        end_time_savings_inteiro = time.time()
        elapsed_time_savings_inteiro = end_time_savings_inteiro - start_time_savings_inteiro
        # 005: Solução2OPT  2OPT(SoluçãoSavingsAleatório)
        start_time_doisopt_inteiro = time.time()
        Solucao2OPT, CustoSolucao2OPT,quantidade_iteracoes_totaldoisopt = DOIS_OPT(SoluçãoSavingsAleatório,custos)
        end_time_doisopt_inteiro = time.time()
        elapsed_time_doisopt_inteiro = end_time_doisopt_inteiro - start_time_doisopt_inteiro
        # 006: Se o custo de Solução2OPT < MelhorSolução, fazer:
        if CustoSolucao2OPT < CustoMelhorSolucao:
            # 007: MelhorSolução  Solução2OPT
            MelhorSolucao = Solucao2OPT
            CustoMelhorSolucao = CustoSolucao2OPT
            iteracoesMelhorSolucao = iteracao
            tempoMelhorSolucao = time.time() - start_ContadorTempoMaximo
            # 008: Conta_iterações_sem_melhoria  0
            ContadorIteracoesSemMelhoria = 0
            improvement_time = time.time() - start_time
            lista_registros_melhoras.append((alfa, semente, NumeroMaximoIteracoesSemMelhoria, CustoMelhorSolucao, iteracao, improvement_time, elapsed_time_LCR, elapsed_time_AdTestes, elapsed_time_savings_inteiro,elapsed_time_doisopt_inteiro))
            iteracao += 1

        # 009: Senão, fazer:
        else:
            # 010: Conta_iterações_sem_melhoria  Conta_iterações_sem_melhoria + 1
            ContadorIteracoesSemMelhoria += 1
            iteracao += 1

        ContadorTempoMaximo = time.time() - start_ContadorTempoMaximo


    return MelhorSolucao, CustoMelhorSolucao, iteracoesMelhorSolucao, tempoMelhorSolucao, ContadorTempoMaximo, lista_registros_melhoras


