class nodo_arbol:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1  # La altura inicial de un nodo hijo recién creado es 1

class arbol_busqueda:
    def __init__(self):
        self.arbol = None

    def insertar(self, nodo, valor):
        if not nodo:
            return nodo_arbol(valor)
        
        # Insertar el valor en el subárbol izquierdo o derecho según corresponda
        if valor < nodo.valor:
            nodo.izquierdo = self.insertar(nodo.izquierdo, valor)
        else:
            nodo.derecho = self.insertar(nodo.derecho, valor)

        # Actualizar la altura del nodo actual
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierdo), self.obtener_altura(nodo.derecho))

        # Obtener el factor de balanceo para verificar si el nodo está balanceado
        balance = self.obtener_balance(nodo)

        # Rotaciones para mantener el balance AVL
        # Caso Izquierda-Izquierda
        if balance > 1 and valor < nodo.izquierdo.valor:
            return self.rotar_derecha(nodo)

        # Caso Derecha-Derecha
        if balance < -1 and valor > nodo.derecho.valor:
            return self.rotar_izquierda(nodo)

        # Caso Izquierda-Derecha
        if balance > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)

        # Caso Derecha-Izquierda
        if balance < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)

        return nodo

    def rotar_izquierda(self, z):
        y = z.derecho
        T2 = y.izquierdo
        y.izquierdo = z
        z.derecho = T2
        z.altura = 1 + max(self.obtener_altura(z.izquierdo), self.obtener_altura(z.derecho))
        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))
        return y

    def rotar_derecha(self, z):
        y = z.izquierdo
        T3 = y.derecho
        y.derecho = z
        z.izquierdo = T3
        z.altura = 1 + max(self.obtener_altura(z.izquierdo), self.obtener_altura(z.derecho))
        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))
        return y

    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)

    def buscar_nivel(self, nodo, valor, nivel_actual=0):
        # Busca el nodo con el valor especificado y devuelve el nivel si lo encuentra
        if nodo is None:
            return -1
        if nodo.valor == valor:
            return nivel_actual
        elif valor < nodo.valor:
            return self.buscar_nivel(nodo.izquierdo, valor, nivel_actual + 1)
        else:
            return self.buscar_nivel(nodo.derecho, valor, nivel_actual + 1)

    def obtener_nodos_nivel(self, nodo, nivel_objetivo, nivel_actual=0, nodos_en_nivel=None):
        # Obtiene todos los nodos en un nivel específico
        if nodos_en_nivel is None:
            nodos_en_nivel = []
        if nodo is None:
            return nodos_en_nivel
        if nivel_actual == nivel_objetivo:
            nodos_en_nivel.append(nodo.valor)
        else:
            self.obtener_nodos_nivel(nodo.izquierdo, nivel_objetivo, nivel_actual + 1, nodos_en_nivel)
            self.obtener_nodos_nivel(nodo.derecho, nivel_objetivo, nivel_actual + 1, nodos_en_nivel)
        return nodos_en_nivel

    def insertar_valor(self, valor):
        # Método auxiliar para insertar un valor en el árbol
        self.arbol = self.insertar(self.arbol, valor)

    def buscar_y_mostrar_nivel(self, valor):
        nivel = self.buscar_nivel(self.arbol, valor)
        if nivel == -1:
            print(f"El valor {valor} no se encuentra en el árbol.")
        else:
            nodos_en_nivel = self.obtener_nodos_nivel(self.arbol, nivel)
            print(f"Valores en el mismo nivel que {valor}: {nodos_en_nivel}")

              # imprimir el arbol con las palabras
def imprimir_arbol(nodo, nivel=0, prefijo=""):
    if nodo is not None:  # Si el nodo no está vacío
        # Imprimir el subárbol derecho
        imprimir_arbol(nodo.derecho, nivel + 1, "   " * nivel + "   ┌──")
        # Imprimir el nodo actual con su valor, frecuencia y altura
        print(f"{'   ' * nivel}{prefijo}{nodo.valor}")
        # Imprimir el subárbol izquierdo
        imprimir_arbol(nodo.izquierdo, nivel + 1, "   " * nivel + "   └──")  

# Leer el archivo y construir el árbol AVL
arbol_equilibrado = arbol_busqueda()
with open('C:/Users/Mafe Yepes/Downloads/EstructurasDatosC++/problemas_pag_17/numPositivos.txt', 'r') as file:
    for line in file:
        numero = int(line.strip())
        arbol_equilibrado.insertar_valor(numero)

# Pedir al usuario que ingrese un número a buscar
numero_buscar = int(input("Ingrese el número a buscar en el árbol: "))
arbol_equilibrado.buscar_y_mostrar_nivel(numero_buscar)

# estuctura del arbol
print("\n")
print("Estuctura del arbol")
print("\n")
imprimir_arbol(arbol_equilibrado.arbol)
print("\n")
