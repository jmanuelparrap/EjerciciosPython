import matplotlib.pyplot as plt
import networkx as nx

class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def obtener_altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if nodo is None:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

    def rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha
        x.derecha = y
        y.izquierda = T2
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))
        x.altura = 1 + max(self.obtener_altura(x.izquierda), self.obtener_altura(x.derecha))
        return x

    def rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda
        y.izquierda = x
        x.derecha = T2
        x.altura = 1 + max(self.obtener_altura(x.izquierda), self.obtener_altura(x.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))
        return y

    def insertar(self, valor):
        self.raiz = self._insertar_aux(self.raiz, valor)

    def _insertar_aux(self, nodo, valor):
        if nodo is None:
            return NodoAVL(valor)
        if valor < nodo.valor:
            nodo.izquierda = self._insertar_aux(nodo.izquierda, valor)
        else:
            nodo.derecha = self._insertar_aux(nodo.derecha, valor)

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))
        balance = self.obtener_balance(nodo)

        if balance > 1 and valor < nodo.izquierda.valor:
            return self.rotar_derecha(nodo)
        if balance < -1 and valor > nodo.derecha.valor:
            return self.rotar_izquierda(nodo)
        if balance > 1 and valor > nodo.izquierda.valor:
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)
        if balance < -1 and valor < nodo.derecha.valor:
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo

    def eliminar(self, valor):
        self.raiz = self._eliminar_aux(self.raiz, valor)

    def _eliminar_aux(self, nodo, valor):
        if nodo is None:
            return nodo

        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_aux(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_aux(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            sucesor = self._encontrar_min(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar_aux(nodo.derecha, sucesor.valor)

        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))
        balance = self.obtener_balance(nodo)

        if balance > 1 and self.obtener_balance(nodo.izquierda) >= 0:
            return self.rotar_derecha(nodo)
        if balance < -1 and self.obtener_balance(nodo.derecha) <= 0:
            return self.rotar_izquierda(nodo)
        if balance > 1 and self.obtener_balance(nodo.izquierda) < 0:
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)
        if balance < -1 and self.obtener_balance(nodo.derecha) > 0:
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo

    def _encontrar_min(self, nodo):
        while nodo.izquierda is not None:
            nodo = nodo.izquierda
        return nodo

    def mostrar_arbol(self):
        grafo = nx.DiGraph()
        pos = {}
        self._agregar_aristas(self.raiz, grafo, pos)
        plt.figure(figsize=(10, 8))
        nx.draw(grafo, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=12, font_weight="bold", arrows=False)
        plt.show()

    def _agregar_aristas(self, nodo, grafo, pos=None, nivel=0, horizontal_pos=0):
        if nodo is not None:
            grafo.add_node(nodo.valor)
            pos[nodo.valor] = (horizontal_pos, -nivel)
            if nodo.izquierda is not None:
                grafo.add_edge(nodo.valor, nodo.izquierda.valor)
                self._agregar_aristas(nodo.izquierda, grafo, pos, nivel+1, horizontal_pos-1.5/(nivel+1))
            if nodo.derecha is not None:
                grafo.add_edge(nodo.valor, nodo.derecha.valor)
                self._agregar_aristas(nodo.derecha, grafo, pos, nivel+1, horizontal_pos+1.5/(nivel+1))

# Ejemplo de uso
arbol_avl = ArbolAVL()
valores = [17, 7, 32, 6, 14, 22, 35, 4, 15, 24, 59, 21]
for valor in valores:
    arbol_avl.insertar(valor)

# Visualizar el árbol inicial
arbol_avl.mostrar_arbol()

# Eliminar la raíz repetidamente hasta que ocurra una rotación
while arbol_avl.raiz is not None:
    print(f"Eliminando la raíz: {arbol_avl.raiz.valor}")
    arbol_avl.eliminar(arbol_avl.raiz.valor)
    arbol_avl.mostrar_arbol()
