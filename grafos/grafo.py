from prettytable import PrettyTable
from datetime import datetime
from jsonpickle import encode, decode
from colorama import Fore, init as color
from time import sleep

color()


# <editor-fold desc="Métodos da Inteface">

def leiaint(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print(Fore.RED + "ERRO: por favor, digite um número inteiro"
                  + Fore.RESET)
        except KeyboardInterrupt:
            print(Fore.RED + "Usuário preferiu não digitar esse número" +
                  Fore.RESET)
            return 0
        else:
            return n


def linha(tam=50):
    return "-" * tam


def cabecalho(txt):
    print(linha())
    print(txt)
    print(linha())


def menu(lista):
    cabecalho("MENU PRINCIPAL")
    for i, item in enumerate(lista):
        print(Fore.YELLOW + f"{i + 1} - " + Fore.BLUE + f"{item}" + Fore.RESET)
    print(linha())
    opc = leiaint("Sua opção: ")
    return opc


def teste_grafo_definido(grafo):
    grafo_exemplo = Grafo(False, False, ["A", "B", "C", "D", "E", "F", "G",
                                         "H", "I", "J", "K", "L"],
                          ["A-B", "A-C", "B-C", "B-E", "B-F", "C-D", "C-F",
                           "D-G", "E-F", "E-J", "E-I", "F-G", "F-K", "G-H",
                           "G-L", "H-L"])
    grafo_exemplo._id_grafo = 'simples'
    if not grafo:
        print(Fore.RED + "ATENÇÃO! Você ainda não definiu um grafo, "
                         "serão impressas as informações correspondentes "
                         "ao grafo representado em 'exemplo.png'. "
                         "Para adicionar seu proprio grafo, selecione a "
                         "opção 1."
              + Fore.RESET)
        print()
        return grafo_exemplo, False
    return grafo, True


def definir_grafo():
    """
    Método que solicita informações sobre o grafo (se é direcionado,
    se é valorado, vértices e arestas) e retorna uma instância da
    classe Grafo.
    """
    print(Fore.BLUE + "O grafo é direcionado? Digite 1 para sim ou 0 para "
                      "não:" + Fore.RESET)
    digrafo = bool(int(input()))
    print()

    print(Fore.BLUE + "O grafo é valorado? Digite 1 para sim ou 0 para "
                      "não:" + Fore.RESET)
    valorado = bool(int(input()))
    print()

    print(Fore.BLUE + "Informe os vértices do grafo, separando por "
                      "vírgula: " + Fore.RESET)
    _vertices = list(input().upper().split(','))
    vertices = []
    for elemento in _vertices:
        vertices.append(elemento.strip())
    print()

    if valorado:
        print(
            Fore.BLUE + "Informe as arestas do grafo (deve-se separar os "
                        "vertices adjacentes e peso por traços e cada "
                        "par de vertices deve ser separado por virgula, "
                        "obtendo o formato: "
            + Fore.YELLOW + "vinicial-vfinal-peso, vinicial-vfinal-peso, "
            + Fore.YELLOW + "vinicial-vfinal-peso, vinicial-vfinal-peso, "
                            "..., vinicial-vfinal-peso"
            + Fore.BLUE + ". Por exemplo: "
            + Fore.YELLOW + "A-B-4, A-C-10, A-D-20, B-C-5"
            + Fore.BLUE + "):"
            + Fore.RESET)
    else:
        print(
            Fore.BLUE + "Informe as arestas do grafo (deve-se separar os "
                        "vertices adjacentes por traços e cada par de "
                        "vertices deve ser separado por virgula, obtendo "
                        "o formato: "
            + Fore.YELLOW + "vinicial-vfinal, vinicial-vfinal, ..., "
                            "vinicial-vfinal"
            + Fore.BLUE + ". Por exemplo: "
            + Fore.YELLOW + "A-B, A-C, A-D, B-C" + Fore.BLUE + "):"
            + Fore.RESET)
    _arestas = list(input().upper().split(','))
    arestas = []
    for elemento in _arestas:
        arestas.append(elemento.strip())
    print()

    return Grafo(digrafo, valorado, vertices, arestas)


def _cadastrar_grafo(grafo, grafo_id=None):
    if grafo_id:
        grafo._id_grafo = grafo_id

    with open("grafos.json", "a") as grafos_json:
        grafos_json.write(encode(grafo) + "\n")


def cadastrar_grafo(grafo):
    """Método que adiciona as informações da instância da classe
    Grafo ao arquivo 'grafos.json', permitindo que seja resgatado
    mais tarde."""
    print(
        Fore.BLUE + "Se desejar, informe uma id para o seu grafo, se "
                    "não, aperte ENTER e ele será salvo com um nome "
                    "genérico:" + Fore.RESET)
    grafo_id = input()
    if grafo_id:
        _cadastrar_grafo(grafo, grafo_id)


def imprimir_informacoes(grafo):
    """
    Método que imprime as informações do grafo (vértices, arestas,
    se é digrafo, se é valorado, se é regular, se é completo, se é
    conexo, fortemente conexo, a quantidade de componentes conexos
    e fortemente conexos, se aplicável).
    """
    cabecalho(Fore.BLUE + f"{grafo._id_grafo}" + Fore.RESET)
    print(f"{Fore.YELLOW}Vertices:{Fore.RESET} {grafo._vertices}")
    print(f"{Fore.YELLOW}Arestas:{Fore.RESET} {grafo._arestas}")
    print(f"{Fore.YELLOW}Digrafo:{Fore.RESET} {grafo._digrafo}")
    print(f"{Fore.YELLOW}Valorado:{Fore.RESET} {grafo._valorado}")


def listar_grafos_salvos():
    """
    Método que imprime a lista de grafos salvos no arquivo 'grafos.json'
     e suas informações.
    """
    with open("grafos.json", "r") as grafos_json:
        for line in grafos_json:
            grafo = decode(line)
            imprimir_informacoes(grafo)


def retorna_grafo(grafo_id):
    """
    Método que retorna o grafo correspondente à id, caso este esteja
    no arquivo grafos.json
    """
    with open("grafos.json", "r") as grafos_json:
        for line in grafos_json:
            grafo = decode(line)
            if grafo._id_grafo == grafo_id:
                return grafo
        print()
        print(Fore.RED + "Grafo não encontrado, tente novamente."
              + Fore.RESET)


def resgatar_grafo():
    """
    Método que lista os grafos salvos e retorna a instância
    escolhida pelo usuário.
    """
    listar_grafos_salvos()
    print(
        Fore.BLUE + "\nInforme a id do grafo que deseja retorna_grafo "
                    "(para evitar erros, copie da lista acima): "
        + Fore.RESET)
    id_r = input().strip()
    return retorna_grafo(id_r)


# </editor-fold>


class Grafo:
    """
    Classe para implementação da representação e algorítmos de grafos.
    """

    def __init__(self, digrafo, valorado, vertices, arestas):
        """
        Construtor da Classe
        :param digrafo: True se o grafo for direcionado, False se não.
        :param valorado: True se o grafo for valorado, False se não.
        :param vertices: Lista de Vértices do grafo.
        :param arestas: Lista de Arestas do grafo.
        """
        self._id_grafo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self._digrafo = digrafo
        self._valorado = valorado
        self._vertices = vertices
        self._arestas = arestas
        self._max_peso = 1

    def estrutura_adjacencia(self):
        """
        Método que retorna um dicionário correspondente à estrutura de
        adjacencia que representa o grafo.
        """
        estrutura_adjacencia = {}
        for i in range(len(self._vertices)):
            estrutura_adjacencia.update({self._vertices[i]: []})
        arestas = self._arestas
        if self._valorado:
            for trio in arestas:
                i, j, p = trio.strip().split("-")
                p = float(p)
                estrutura_adjacencia[i].append({'vertice_id': j, 'peso': p})
                if not self._digrafo:
                    estrutura_adjacencia[j].append({'vertice_id': i,
                                                    'peso': p})
                if p > self._max_peso:
                    self._max_peso = p
        else:
            for par in arestas:
                i, j = par.strip().split("-")
                estrutura_adjacencia[i].append({'vertice_id': j, 'peso': 1})
                if not self._digrafo:
                    estrutura_adjacencia[j].append({'vertice_id': i,
                                                    'peso': 1})
        return estrutura_adjacencia

    def imprimir_estrutura_adjacencia(self):
        """
        Metodo que imprime a estutura de adjacencia do grafo, formatada
        para facilitar a leitura.
        """
        estrutura_adjacencia = self.estrutura_adjacencia()
        wg = len((max(estrutura_adjacencia, key=len)))
        wp = len(str(self._max_peso))
        if self._valorado:
            for i in estrutura_adjacencia:
                print(f"{Fore.YELLOW}{i:<{wg}}", end=' -> ')
                for j in estrutura_adjacencia[i]:
                    print(f"{Fore.RESET}{j['vertice_id']:<{wg}}"
                          f"_P{j['peso']:<{wp}}", end=' | ')
                print()
        else:
            for i in estrutura_adjacencia:
                print(f"{Fore.YELLOW}{i:<{wg}}", end=' -> ')
                for j in estrutura_adjacencia[i]:
                    print(f"{Fore.RESET}{j['vertice_id']:<{wg}}", end=' | ')
                print()

    def matriz_adjacencia(self):
        """
        Método que retorna uma matriz correspondente à matriz de
        adjacencia que representa o grafo.
        """
        matriz_adjacencia = []
        for i in range(len(self._vertices)):
            matriz_adjacencia.append([0] * len(self._vertices))
        arestas = self._arestas
        if self._valorado:
            for trio in arestas:
                i, j, p = trio.replace(" ", "").split("-")
                i, j = self._vertices.index(i), self._vertices.index(j)
                p = float(p)
                matriz_adjacencia[i][j] = p
                if not self._digrafo:
                    matriz_adjacencia[j][i] = p
        else:
            for par in arestas:
                i, j = par.replace(" ", "").split("-")
                i, j = self._vertices.index(i), self._vertices.index(j)
                matriz_adjacencia[i][j] = 1
                if not self._digrafo:
                    matriz_adjacencia[j][i] = 1
        return matriz_adjacencia

    def imprimir_matriz_adjacencia(self):
        """
        Metodo que imprime a matriz de adjacencia do grafo, formatada
        para facilitar a leitura.
        """
        matriz_adjacencia = self.matriz_adjacencia()

        x = PrettyTable([Fore.YELLOW + "*" + Fore.RESET] +
                        [f"{Fore.YELLOW}{vertice}{Fore.RESET}"
                         for vertice in self._vertices])
        for idx, vertice in enumerate(self._vertices):
            x.add_row([f"{Fore.YELLOW}{vertice}{Fore.RESET}"] +
                      matriz_adjacencia[idx])
        print(x)

    def get_adjacentes(self, vertice):
        """
        Método que recebe um vértice do grafo e retorna uma lista
        contendo os vértices adjacentes a ele.
        """
        grafo = self.estrutura_adjacencia()
        adjacentes = []
        for i in grafo[vertice]:
            adjacentes.append(i['vertice_id'])
        return adjacentes

# <editor-fold desc="Questões">

# cabecalho("Questão 1")
# 1. Usando os conceitos de orientação a objetos: Implementar uma Matriz
# de Adjacência e uma Lista de Adjacência, ambos representando o grafo
# da imagem.

# Geração e cadastro do grafo:
#
# g1_digrafo = True
# g1_valorado = False
# g1_vertices = ['2', '3', '5', '7', '8', '9', '10', '11']
# g1_arestas = ['3-8', '3-10', '5-11', '7-8', '7-11', '8-9', '11-2', '11-9',
#               '11-10']
# grafo1 = Grafo(g1_digrafo, g1_valorado, g1_vertices, g1_arestas)
# _cadastrar_grafo(grafo1, grafo_id='grafo1')

# grafo1 = retorna_grafo('grafo1')
# cabecalho("Matriz de Adjacencia")
# grafo1.imprimir_matriz_adjacencia()
# cabecalho("Estrutura de Adjacencia")
# grafo1.imprimir_estrutura_adjacencia()
#
# cabecalho("Questão 2")
# 2. Escolha uma estrutura de dados de grafos (Matriz ou Lista de
# Adjacência), para fazer a seguinte implementação:
# a) Ler o grafo contigo no arquivo "com-friendster.top5000.cmty.txt");
# b) Carregar o grafo em memória (na estrutura de dados escolhida);
# c) Imprimir o grafo;

# Extração e cadastro do grafo:
#
# g2_digrafo = True
# g2_valorado = False
# g2_vertices = set()
# g2_arestas = []
#
# with open("com-friendster.top5000.cmty.txt", "r") as file:
#     for line in file:
#         vertices = line.strip().split("	")
#         g2_vertices.add(vertices[0])
#         for vertice in vertices[1::]:
#             g2_vertices.add(vertice)
#             g2_arestas.append(f"{vertices[0]}-{vertice}")
#
# grafo2 = Grafo(g2_digrafo, g2_valorado, list(g2_vertices), g2_arestas)
# _cadastrar_grafo(grafo2, grafo_id='grafo2')

# grafo2 = retorna_grafo('grafo2')
# cabecalho("Matriz de Adjacencia")
# grafo2.imprimir_matriz_adjacencia()  # Estourando a memória
# cabecalho("Estrutura de Adjacencia")
# grafo2.imprimir_estrutura_adjacencia()

cabecalho("Questão 3")
# Dado um grafo qualquer, descrito em um arquivo TXT, fazer:
# 1. Criar um método para calcular a quantidade numérica dos vértices do grafo;
# 2. Criar um método para imprimir os vértices do grafo descrito no arquivo TXT, e a
# quantidade numérica de vértices adjacentes;
# 3. Um método que informa a complexidade do grafo. {n + m | n = número de vértices do grafo e m = número de arestas}

# Extração e cadastro do grafo:

# g3_digrafo = True
# g3_valorado = False
# g3_vertices = set()
# g3_arestas = []

# with open("grafo-5000.txt", "r") as file:
#     i = 1
#     for line in file:
#         vertices = line.strip().split("	")
#         g3_vertices.add(vertices[0])
#         for vertice in vertices[1::]:
#             g3_vertices.add(vertice)
#             g3_arestas.append(f"{vertices[0]}-{vertice}")
#         print(f"linha {i} ok!")
#         i += 1
# grafo3 = Grafo(g3_digrafo, g3_valorado, list(g3_vertices), g3_arestas)
# _cadastrar_grafo(grafo3, grafo_id='grafo3')

grafo3 = retorna_grafo('grafo3')

for vertice in grafo3._vertices:
    adjacentes = grafo3.get_adjacentes(vertice)
    print(f"Vértice {vertice}: {len(adjacentes)} adjacentes")

q_vertices = len(grafo3._vertices)
q_arestas = len(grafo3._arestas)
print(f"\nQuantidade de Vértices: {q_vertices}")
print(f"Quantidade de Arestas: {q_arestas}")

print(f"\nComplexidade do Grafo: {q_vertices + q_arestas}")

# </editor-fold>
