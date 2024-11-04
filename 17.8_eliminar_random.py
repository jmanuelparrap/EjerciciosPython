import random

class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, raiz, valor):
        if not raiz:
            return NodoAVL(valor)
        
        if valor < raiz.valor:
            raiz.izquierdo = self.insertar(raiz.izquierdo, valor)
        elif valor > raiz.valor:
            raiz.derecho = self.insertar(raiz.derecho, valor)
        else:
            return raiz

        raiz.altura = 1 + max(self.obtener_altura(raiz.izquierdo), self.obtener_altura(raiz.derecho))
        balance = self.obtener_balance(raiz)

        # Rotaciones para balancear el árbol AVL
        if balance > 1 and valor < raiz.izquierdo.valor:
            return self.rotacion_derecha(raiz)
        if balance < -1 and valor > raiz.derecho.valor:
            return self.rotacion_izquierda(raiz)
        if balance > 1 and valor > raiz.izquierdo.valor:
            raiz.izquierdo = self.rotacion_izquierda(raiz.izquierdo)
            return self.rotacion_derecha(raiz)
        if balance < -1 and valor < raiz.derecho.valor:
            raiz.derecho = self.rotacion_derecha(raiz.derecho)
            return self.rotacion_izquierda(raiz)

        return raiz

    def obtener_minimo(self, nodo):
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def obtener_maximo(self, nodo):
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo

    def eliminar(self, raiz, valor):
        if not raiz:
            return raiz

        if valor < raiz.valor:
            raiz.izquierdo = self.eliminar(raiz.izquierdo, valor)
        elif valor > raiz.valor:
            raiz.derecho = self.eliminar(raiz.derecho, valor)
        else:
            # Nodo con uno o ningún hijo
            if raiz.izquierdo is None:
                return raiz.derecho
            elif raiz.derecho is None:
                return raiz.izquierdo

            # Nodo con dos hijos: elige aleatoriamente el sucesor o el predecesor
            if random.choice([True, False]):
                temp = self.obtener_maximo(raiz.izquierdo)  # predecesor
                raiz.valor = temp.valor
                raiz.izquierdo = self.eliminar(raiz.izquierdo, temp.valor)
            else:
                temp = self.obtener_minimo(raiz.derecho)  # sucesor
                raiz.valor = temp.valor
                raiz.derecho = self.eliminar(raiz.derecho, temp.valor)

        raiz.altura = 1 + max(self.obtener_altura(raiz.izquierdo), self.obtener_altura(raiz.derecho))
        balance = self.obtener_balance(raiz)

        # Rotaciones para balancear el árbol AVL tras la eliminación
        if balance > 1 and self.obtener_balance(raiz.izquierdo) >= 0:
            return self.rotacion_derecha(raiz)
        if balance > 1 and self.obtener_balance(raiz.izquierdo) < 0:
            raiz.izquierdo = self.rotacion_izquierda(raiz.izquierdo)
            return self.rotacion_derecha(raiz)
        if balance < -1 and self.obtener_balance(raiz.derecho) <= 0:
            return self.rotacion_izquierda(raiz)
        if balance < -1 and self.obtener_balance(raiz.derecho) > 0:
            raiz.derecho = self.rotacion_derecha(raiz.derecho)
            return self.rotacion_izquierda(raiz)

        return raiz

    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)

    def rotacion_derecha(self, z):
        y = z.izquierdo
        T3 = y.derecho
        y.derecho = z
        z.izquierdo = T3
        z.altura = 1 + max(self.obtener_altura(z.izquierdo), self.obtener_altura(z.derecho))
        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))
        return y

    def rotacion_izquierda(self, z):
        y = z.derecho
        T2 = y.izquierdo
        y.izquierdo = z
        z.derecho = T2
        z.altura = 1 + max(self.obtener_altura(z.izquierdo), self.obtener_altura(z.derecho))
        y.altura = 1 + max(self.obtener_altura(y.izquierdo), self.obtener_altura(y.derecho))
        return y

    def preorden(self, nodo):
        if not nodo:
            return
        print(nodo.valor, end=" ")
        self.preorden(nodo.izquierdo)
        self.preorden(nodo.derecho)

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
arbol_avl = ArbolAVL()
valores = [20, 10, 30, 5, 15, 25, 35, 2, 7, 12, 17, 22, 27]

for valor in valores:
    arbol_avl.raiz = arbol_avl.insertar(arbol_avl.raiz, valor)

print("Árbol AVL en preorden antes de eliminar:")
arbol_avl.preorden(arbol_avl.raiz)
print("\n")
imprimir_arbol(arbol_avl.raiz)
print("\n")

# Eliminar un nodo con dos hijos
arbol_avl.raiz = arbol_avl.eliminar(arbol_avl.raiz, 10)
print("Árbol AVL en preorden después de eliminar 10:")
arbol_avl.preorden(arbol_avl.raiz)
print("\n")
imprimir_arbol(arbol_avl.raiz)
print("\n")