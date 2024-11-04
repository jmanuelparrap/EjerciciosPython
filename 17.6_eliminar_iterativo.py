class nodo_arbol:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class arbol_busqueda:
    def __init__(self):
        self.arbol = None

    def insertar(self, valor):
        nuevo_nodo = nodo_arbol(valor)
        if not self.arbol:
            self.arbol = nuevo_nodo
            return

        nodo_actual = self.arbol
        while True:
            if valor < nodo_actual.valor:
                if nodo_actual.izquierdo is None:
                    nodo_actual.izquierdo = nuevo_nodo
                    return
                nodo_actual = nodo_actual.izquierdo
            else:
                if nodo_actual.derecho is None:
                    nodo_actual.derecho = nuevo_nodo
                    return
                nodo_actual = nodo_actual.derecho

    def eliminar(self, valor):
        nodo_actual = self.arbol
        nodo_padre = None
        es_izquierdo = True

        # Buscar el nodo a eliminar
        while nodo_actual and nodo_actual.valor != valor:
            nodo_padre = nodo_actual
            if valor < nodo_actual.valor:
                nodo_actual = nodo_actual.izquierdo
                es_izquierdo = True
            else:
                nodo_actual = nodo_actual.derecho
                es_izquierdo = False

        # Si el nodo no se encuentra, termina el proceso
        if nodo_actual is None:
            print("El valor no se encuentra en el árbol.")
            return

        # Caso 1: El nodo es una hoja
        if nodo_actual.izquierdo is None and nodo_actual.derecho is None:
            if nodo_actual == self.arbol:
                self.arbol = None
            elif es_izquierdo:
                nodo_padre.izquierdo = None
            else:
                nodo_padre.derecho = None

        # Caso 2: El nodo tiene un solo hijo
        elif nodo_actual.izquierdo is None:  # Solo tiene hijo derecho
            if nodo_actual == self.arbol:
                self.arbol = nodo_actual.derecho
            elif es_izquierdo:
                nodo_padre.izquierdo = nodo_actual.derecho
            else:
                nodo_padre.derecho = nodo_actual.derecho

        elif nodo_actual.derecho is None:  # Solo tiene hijo izquierdo
            if nodo_actual == self.arbol:
                self.arbol = nodo_actual.izquierdo
            elif es_izquierdo:
                nodo_padre.izquierdo = nodo_actual.izquierdo
            else:
                nodo_padre.derecho = nodo_actual.izquierdo

        # Caso 3: El nodo tiene dos hijos
        else:
            sucesor = self.obtener_sucesor(nodo_actual)
            if nodo_actual == self.arbol:
                self.arbol = sucesor
            elif es_izquierdo:
                nodo_padre.izquierdo = sucesor
            else:
                nodo_padre.derecho = sucesor
            sucesor.izquierdo = nodo_actual.izquierdo

    def obtener_sucesor(self, nodo):
        sucesor_padre = nodo
        sucesor = nodo
        nodo_actual = nodo.derecho

        while nodo_actual:
            sucesor_padre = sucesor
            sucesor = nodo_actual
            nodo_actual = nodo_actual.izquierdo

        if sucesor != nodo.derecho:
            sucesor_padre.izquierdo = sucesor.derecho
            sucesor.derecho = nodo.derecho

        return sucesor

    def en_orden(self):
        def _en_orden(nodo):
            if nodo:
                _en_orden(nodo.izquierdo)
                print(nodo.valor, end=' ')
                _en_orden(nodo.derecho)
        _en_orden(self.arbol)
        print()

# imprimir el arbol de busqueda
def imprimir_arbol(nodo, nivel=0, prefijo=""):
    if nodo is not None:  # Si el nodo no está vacío
        # Imprimir el subárbol derecho
        imprimir_arbol(nodo.derecho, nivel + 1, "   " * nivel + "   ┌──")
        # Imprimir el nodo actual con su valor, frecuencia y altura
        print(f"{'   ' * nivel}{prefijo}{nodo.valor}")
        # Imprimir el subárbol izquierdo
        imprimir_arbol(nodo.izquierdo, nivel + 1, "   " * nivel + "   └──")

# Ejemplo de uso
arbol_busqueda = arbol_busqueda()
valores = [50, 30, 70, 20, 40, 60, 80]
for valor in valores:
    arbol_busqueda.insertar(valor)

print("Árbol en orden antes de la eliminación:")
imprimir_arbol(arbol_busqueda.arbol)
print("\n")

# Pedir al usuario que ingrese un número a buscar
numero_eliminar = int(input("Ingrese el número a eliminar en el árbol: "))
arbol_busqueda.eliminar(numero_eliminar)  # Eliminar la raíz (con dos hijos)
print("Árbol en orden después de eliminar 50:")
imprimir_arbol(arbol_busqueda.arbol)
print("\n")
