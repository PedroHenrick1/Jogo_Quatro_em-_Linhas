from xmlrpc.server import SimpleXMLRPCServer

# Variáveis globais para controlar o jogo
tabuleiro = None
jogadores = {'X': None, 'O': None} # Dicionários dos Jogadores a serem registrados
jogador_atual = 'X'  # Começa com o jogador 'X'
jogo_iniciado = False

def criar_tabuleiro():
    global tabuleiro
    tabuleiro = [[' '] * 8 for _ in range(8)]

def inserir_peca(coluna, jogador):
    global tabuleiro
    coluna -= 1  # Ajusta para o índice da lista
    if jogador == jogador_atual:
        for linha in reversed(tabuleiro):
            if linha[coluna] == ' ':
                linha[coluna] = jogador
                return True  # Peça inserida com sucesso
        return False  # Coluna cheia, não foi possível inserir a peça
    else:
        return False  # Não é a vez do jogador atual

def alternar_jogador():
    global jogador_atual
    jogador_atual = 'O' if jogador_atual == 'X' else 'X'  # Alterna entre 'X' e 'O'

def get_jogador_atual():
    return jogador_atual

def registrar_jogador(jogador):
    global jogadores, jogo_iniciado
    if jogador not in jogadores.values():  # Se o jogador não está no dicionário
        for key, value in jogadores.items():
            if value is None:
                jogadores[key] = jogador
                if None not in jogadores.values(): # Verifica se não há mais jogadores não registrados
                    jogo_iniciado = True  # Ambos os jogadores estão prontos, inicia o jogo
                return key # Retorna a chave do jogador recém-registrado
    return None  # Todos os jogadores já estão registrados

def jogo_iniciado():
    global jogo_iniciado
    return jogo_iniciado

# Funções que serão chamadas remotamente
def jogar(coluna, jogador):
    global tabuleiro, jogador_atual
    if not jogo_iniciado:
        return tabuleiro, "O jogo ainda não começou."
    if jogador == jogador_atual and inserir_peca(coluna, jogador):
        alternar_jogador()
        return tabuleiro, "Jogada válida."  # Retorna o tabuleiro atualizado e mensagem de jogada válida
    else:
        return tabuleiro, "Jogada inválida."  # Retorna o tabuleiro atual (sem alterações) e mensagem de erro

def reiniciar_jogo():
    global tabuleiro, jogador_atual, jogo_iniciado
    criar_tabuleiro()
    jogador_atual = 'X'  # Começa novamente com o jogador 'X'
    jogo_iniciado = False
    return True

def lista_jogadores():
    return jogadores

def get_tabuleiro_adversario(jogador_atual):
    global jogadores, tabuleiro

    jogador_adversario = 'X' if jogador_atual == 'O' else 'O'
    if jogador_atual in jogadores.values() and jogador_adversario in jogadores.values():
        return tabuleiro, None  # Retorna o tabuleiro atualizado do jogador adversário
    else:
        return None, "Jogadores não registrados corretamente."
    
def ganhou(tabuleiro):
    for jogador in ['X', 'O']:
        # Verificar vitória na horizontal e vertical
        cont = 0
        for linha in tabuleiro:
            for coluna in linha:
                if coluna == jogador:
                    cont += 1
                    if cont == 4:
                        return jogador
                else:
                    cont = 0

        cont = 0
        for coluna in range(len(tabuleiro[0])): # Itera sobre todas as colunas da linha
            for linha in range(len(tabuleiro)):
                if tabuleiro[linha][coluna] == jogador:
                    cont += 1
                    if cont == 4:
                        return jogador
                else:
                    cont = 0

        # Verificar vitória nas diagonais
        for i in range(len(tabuleiro)):
            for j in range(len(tabuleiro[0])):
                if tabuleiro[i][j] == jogador:
                    # Verificar diagonal \
                    if i + 3 < len(tabuleiro) and j + 3 < len(tabuleiro[0]): # Verifica os limites da barreira do tabuleiro
                        if tabuleiro[i + 1][j + 1] == jogador and tabuleiro[i + 2][j + 2] == jogador and tabuleiro[i + 3][j + 3] == jogador: # (i + 1, j + 1), (i + 2, j + 2), e (i + 3, j + 3)
                            return jogador
                    # Verificar diagonal /
                    if i + 3 < len(tabuleiro) and j - 3 >= 0: # Verifica os limites da barreira do tabuleiro
                        if tabuleiro[i + 1][j - 1] == jogador and tabuleiro[i + 2][j - 2] == jogador and tabuleiro[i + 3][j - 3] == jogador: # (i + 1, j - 1), (i + 2, j - 2), e (i + 3, j - 3)
                            return jogador

    return None  # Nenhum jogador ganhou ainda



# Criação do servidor RPC
server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
print("Servidor RPC iniciado")

# Registrando as funções no servidor
server.register_function(jogar, "jogar")
server.register_function(criar_tabuleiro, "criar_tabuleiro")
server.register_function(get_jogador_atual, "get_jogador_atual")
server.register_function(registrar_jogador, "registrar_jogador")
server.register_function(reiniciar_jogo, "reiniciar_jogo")
server.register_function(lista_jogadores, "lista_jogadores")
server.register_function(jogo_iniciado, "jogo_iniciado")
server.register_function(get_tabuleiro_adversario, "get_tabuleiro_adversario")
server.register_function(ganhou, "ganhou")

# Rodando o servidor indefinidamente
server.serve_forever()
