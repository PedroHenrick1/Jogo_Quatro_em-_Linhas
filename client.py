import os
import xmlrpc.client
import time

def clear_screen():
    # Limpar o terminal de acordo com o sistema operacional
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_tabuleiro(tabuleiro):
    clear_screen()  # Limpar o terminal antes de imprimir o tabuleiro
    print("  1 2 3 4 5 6 7 8")
    for linha in tabuleiro:
        print('| ' + ' '.join(linha) + ' |')

try:
    # Conectando ao servidor RPC
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    # Criar o tabuleiro no servidor
    proxy.criar_tabuleiro()

    # Escolher a peça ('X' ou 'O')
    while True:
        jogador = input("Escolha a peça (X ou O): ").upper()
        if jogador in ['X', 'O']:
            break
        else:
            print("Escolha inválida.")

    jogador_atual = proxy.registrar_jogador(jogador)
    if jogador_atual:
        print(f"Você é o jogador {jogador_atual}. Aguarde o início do jogo.")
    else:
        print("Todos os jogadores já estão registrados.")

    # Esperar até que o jogo comece
    while not proxy.jogo_iniciado():
        print("Aguardando o início do jogo...")
        time.sleep(1)

    jogo_terminado = False
    resultado = None
    ganhador = None
    coluna = None
    while not jogo_terminado:
        jogador_atual_servidor = proxy.get_jogador_atual()  # Obter o jogador atual do servidor
        tabuleiro_adversario = proxy.get_tabuleiro_adversario(jogador_atual_servidor)[0] # Obter o tabuleiro adversário

        if proxy.ganhou(tabuleiro_adversario) == 'X': 
            ganhador = 'X'
            jogo_terminado = True
            imprimir_tabuleiro(tabuleiro_adversario)
        elif proxy.ganhou(tabuleiro_adversario) == 'O':
            ganhador = 'O'
            jogo_terminado = True
            imprimir_tabuleiro(tabuleiro_adversario)
        
        if jogador_atual == jogador_atual_servidor and jogo_terminado == False:
            imprimir_tabuleiro(tabuleiro_adversario)  # Imprime o tabuleiro atualizado do adversário
            coluna = int(input(f"Sua vez, jogador {jogador_atual}. Escolha a coluna (1-8): "))
            resultado, mensagem_erro = proxy.jogar(coluna, jogador_atual)

            if proxy.ganhou(resultado) == 'X':
                ganhador = 'X'
                jogo_terminado = True
            elif proxy.ganhou(resultado) == 'O':
                ganhador = 'O'
                jogo_terminado = True
            
            # Verificar se houve um erro na jogada
            # if mensagem_erro:
            #     print(mensagem_erro)
            #     imprimir_tabuleiro(resultado)
            # else:
            imprimir_tabuleiro(resultado)
                

    if jogo_terminado:
        print(f"O jogador {ganhador} ganhou o jogo")

    input("Pressione Enter para fechar o cliente.")

except Exception as e:
    print("Erro ao conectar ou chamar função remota:", e)
