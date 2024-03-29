tabuleiro = [['O', 'O', 'O', 'O'],
             ['O', 'O', 'O', 'X'],
             ['O', 'O', 'X', 'X'],
             ['O', 'X', 'X', 'X']]

diagonal = 0
cont = 0
ganhou = False
# Iteração reversa nas linhas
print("Iteração reversa nas linhas:")
for i, linha in enumerate(reversed(tabuleiro)):
    if ganhou:
        break
    for j, elemento in enumerate(linha):
        lin = i
        col = j
        for k in range(4):
            if lin+1 < len(tabuleiro) and col+1 < len(linha):
                if elemento == tabuleiro[lin+1][col+1]:
                    cont += 1
            lin += 1
            col += 1
        if cont == 4:
            ganhou = True
            print(f'elemento {elemento} ganhou')
            break

        # if tabuleiro[diagonal][diagonal] == elemento:
        #     cont += 1
        #     for l, linha in enumerate(reversed(tabuleiro)):
        #         for c, elemento in enumerate(linha):
        #             diagonal += 1
        #             cont += 1
        #             print(cont)


# Iteração reversa nas colunas
print("\nIteração reversa nas colunas:")
for j in reversed(range(len(tabuleiro[0]))):
    for i in range(len(tabuleiro)):
        elemento = tabuleiro[i][j]
        print(f'Índice: ({i}, {j}) - Elemento: {elemento}')
