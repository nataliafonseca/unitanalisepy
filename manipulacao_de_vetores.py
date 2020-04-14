n = int(input("Informe o valor de n "))
print()
vetor1 = []
for i in range(n):
    vetor1.append(float(input(f"Informe o valor na posição {i} ")))


def imprimir_elementos(vetor):
    v = vetor.copy()
    print(v[0])
    v.pop(0)
    if len(v) > 0:
        imprimir_elementos(v)


def imprimir_elementos_ordem_inversa(vetor):
    v = vetor.copy()
    print(v[-1])
    v.pop()
    if len(v) > 0:
        imprimir_elementos_ordem_inversa(v)

print()
imprimir_elementos(vetor1)
print()
imprimir_elementos_ordem_inversa(vetor1)
