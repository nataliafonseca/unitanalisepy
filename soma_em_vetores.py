def soma_em_vetores(vetor_exemplo, valor_buscado):
    for indice_a, valor_a in enumerate(vetor_exemplo):
        for indice_b, valor_b in enumerate(vetor_exemplo):
            if valor_a != valor_b and valor_a + valor_b == valor_buscado:
                return [indice_a, indice_b]


# Teste:
print(soma_em_vetores([11, 3, 9, 2], 20))
