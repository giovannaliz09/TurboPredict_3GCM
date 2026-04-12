import json

#Função lambda ICMS = 18%
calcula_icms = lambda valor: round(valor * 0.18, 2)

produtos = []

print("=== Cadastro de Produtos (SGV) ===")

#Loop: pergunta se deseja continuar
while True:
    descricao = input("Descrição do produto: ").strip()

    #Tratamento de exceção específica
    try:
        valor = float(input("Valor do produto: ").strip().replace(",", "."))
        valor = round(valor, 2)
    except ValueError:
        print("Valor inválido. Tente novamente.")
        continue

    embalagem = input("Tipo de embalagem: ").strip()

    icms = calcula_icms(valor)

    produto = {
        "descricao": descricao,
        "valor": valor,
        "embalagem": embalagem,
        "icms": icms}

    produtos.append(produto)
    print("Produto cadastrado!")

    valores_permitidos = ('s', 'sim')
    valores_n_permitidos = ('n', 'nao', 'não')

    resposta_continuar = ""
    while True:
        resposta_continuar = input("Deseja cadastrar um novo produto? (s/n): ").strip().lower()

        if resposta_continuar in valores_permitidos:
            break

        elif resposta_continuar in valores_n_permitidos:
            if len(produtos) < 5:
                faltam = 5 - len(produtos)
                print(f"Necessário ter no mínimo 5 produtos. Faltam {faltam}.")
                continue

            if len(produtos) >= 5:
                print("Limite mínimo de 5 produtos atingido.")
                break

        else:
            print("Valor inválido. Responda apenas com 's' para sim ou 'n' para não.")
            continue

    if resposta_continuar in valores_n_permitidos and len(produtos) >= 5:
        break

#Gerar arquivo JSON
try:
    with open("1_5_arquivo_produto.json", "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=2)
    print("Arquivo 1_5_arquivo_produto.json gerado com", len(produtos), "produto(s).")
except Exception as e:
    print("Erro ao salvar o arquivo:", e)