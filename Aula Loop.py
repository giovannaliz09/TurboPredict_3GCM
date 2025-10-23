# #criação da variável com um valor inicial
# resposta = "0"
# #enquanto a resposta não for 42, a repetição ocorre
# while (resposta != "42"):
#     #para cada uma das repetições, o usuário vai submeter uma resposta
#     resposta = input("Qual a resposta para a vida, o universo e tudo mais?")
# #quanto o laço terminar, a mensagem é exibida
# print("Parabéns, você acertou!")

#criação da variável com um valor inicial
# i = 0
# #enquanto a variável contadora não chegar ao limite
# while (i<10):
#     #para cada uma das repetições uma mensagem é exibida
#     print("Mais uma mensagem, com i valendo: {}".format(i))
#     i = i + 1

#a variável contadora deverá assumir valores no intervalo entre 0 e 9
# for x in range(10):
#     #para cada um desses valores, vamos printar o valor da variável
#     print(x)
#a variável contadora deverá assumir valores no intervalo entre 1 e 9 com incremento 2
# for x in range(1,10,2):
#     #para cada um desses valores, vamos printar o valor da variável
#     print(x)



# variável de menu que servirá para receber a opção do usuário
op = -1
# enquanto o usuário não digitar a opção de saída
while op != 4:
    # exibição das opções do menu
    print("SUPER PROGRAMA MARAVILHOSO")
    print("1 - Rodar código 1")
    print("2 - Rodar código 2")
    print("3 - Rodar código 3")
    print("4 - Sair do programa")
    op = int(input("Informe sua opção: "))

    # verificação das opções disponíveis
    if op == 1:
        # O que ocorrerá se a opção 1 for selecionada
        print("CÓDIGO 1 RODANDO!")
    elif op == 2:
        # O que ocorrerá se a opção 2 for selecionada
        print("CÓDIGO 2 RODANDO!")
    elif op == 3:
        # O que ocorrerá se a opção 3 for selecionada
        print("CÓDIGO 3 RODANDO!")
# Quando o looping terminar de rodar, exibir essa mensagem
print("OK! O programa está encerrado...")