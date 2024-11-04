class NodoB:
    def __init__(self, min_grado, es_hoja=True):
        self.min_grado = min_grado
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []

class ArbolB:
    def __init__(self, min_grado):
        self.min_grado = min_grado
        self.raiz = NodoB(min_grado)

    def insertar(self, clave):
        # Inserta una clave en el árbol B.
        raiz = self.raiz
        if len(raiz.claves) == (2 * self.min_grado) - 1:
            nueva_raiz = NodoB(self.min_grado, es_hoja=False)
            nueva_raiz.hijos.append(raiz)
            self._dividir(nueva_raiz, 0)
            self.raiz = nueva_raiz
            self._insertar_no_lleno(nueva_raiz, clave)
        else:
            self._insertar_no_lleno(raiz, clave)

    def _insertar_no_lleno(self, nodo, clave):
        i = len(nodo.claves) - 1
        if nodo.es_hoja:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            nodo.claves.insert(i + 1, clave)
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            if len(nodo.hijos[i].claves) == (2 * self.min_grado) - 1:
                self._dividir(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], clave)

    def _dividir(self, nodo, indice):
        min_grado = nodo.min_grado
        hijo = nodo.hijos[indice]
        nuevo_hijo = NodoB(min_grado, es_hoja=hijo.es_hoja)
        nodo.claves.insert(indice, hijo.claves[min_grado - 1])
        nodo.hijos.insert(indice + 1, nuevo_hijo)
        nuevo_hijo.claves = hijo.claves[min_grado:(2 * min_grado) - 1]
        hijo.claves = hijo.claves[0:min_grado - 1]
        if not hijo.es_hoja:
            nuevo_hijo.hijos = hijo.hijos[min_grado:2 * min_grado]
            hijo.hijos = hijo.hijos[0:min_grado]

    def imprimir_arbol(self, nodo=None):
        # Imprime las claves en orden natural (creciente).
        if nodo is None:
            nodo = self.raiz
        for i in range(len(nodo.claves)):
            if not nodo.es_hoja:
                self.imprimir_arbol(nodo.hijos[i])
            print(nodo.claves[i], end=" ")
        if not nodo.es_hoja:
            self.imprimir_arbol(nodo.hijos[len(nodo.claves)])

    def listado_decreciente(self, nodo):
        # Muestra las claves en orden decreciente.
        if nodo is None:
            return

        i = len(nodo.claves) - 1
        # Recorre en orden inverso
        while i >= 0:
            # Primero procesa el hijo derecho si no es una hoja
            if not nodo.es_hoja:
                self.listado_decreciente(nodo.hijos[i + 1])
            # Luego muestra la clave actual
            print(nodo.claves[i], end=' ')
            i -= 1
        # Procesa el último hijo izquierdo si no es hoja
        if not nodo.es_hoja:
            self.listado_decreciente(nodo.hijos[0])

    def imprimir_arbol_b(self, nodo, nivel=0, prefijo=""):
        # Imprime el árbol B en formato visual.
        if nodo is not None:
            print("   " * nivel + prefijo + str(nodo.claves))
            if not nodo.es_hoja:
                for i, hijo in enumerate(nodo.hijos):
                    nuevo_prefijo = "   ├──" if i < len(nodo.claves) else "   └──"
                    self.imprimir_arbol_b(hijo, nivel + 1, nuevo_prefijo)

    def mostrar_arbol(self):
        # Método público para imprimir el árbol desde la raíz.
        print("Árbol B:")
        self.imprimir_arbol_b(self.raiz)
        print()

    def mostrar_listado_decreciente(self):
        # Método público para mostrar las claves en orden decreciente desde la raíz.
        print("Claves en orden decreciente:")
        self.listado_decreciente(self.raiz)
        print()

# Ejemplo de uso
arbol = ArbolB(min_grado=2)
claves_a_insertar = [10, 20, 5, 6, 12, 30, 7, 17]
for clave in claves_a_insertar:
    arbol.insertar(clave)

# Mostrar las claves en orden decreciente
arbol.mostrar_listado_decreciente()

# Listado en orden natural (creciente)
print("Listado en orden natural:")
arbol.imprimir_arbol()
print()
