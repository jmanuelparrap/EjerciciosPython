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
            # La raíz está llena, se necesita dividir
            nueva_raiz = NodoB(self.min_grado, es_hoja=False)
            nueva_raiz.hijos.append(raiz)
            self._dividir(nueva_raiz, 0)
            self.raiz = nueva_raiz
            self._insertar_no_lleno(nueva_raiz, clave)
        else:
            self._insertar_no_lleno(raiz, clave)

    def _insertar_no_lleno(self, nodo, clave):
        # Inserta una clave en un nodo que no está lleno.
        i = len(nodo.claves) - 1

        if nodo.es_hoja:
            # Encuentra la posición para insertar la clave
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            nodo.claves.insert(i + 1, clave)
        else:
            # Encuentra el hijo adecuado para insertar la clave
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1  # Mueve hacia el hijo correspondiente

            if len(nodo.hijos[i].claves) == (2 * self.min_grado) - 1:
                # El hijo está lleno, se necesita dividir
                self._dividir(nodo, i)
                # Determina cuál de los dos hijos a los que insertar la clave
                if clave > nodo.claves[i]:
                    i += 1

            self._insertar_no_lleno(nodo.hijos[i], clave)

    def _dividir(self, nodo, indice):
        # Divide el hijo del nodo en el índice dado.
        min_grado = nodo.min_grado
        hijo = nodo.hijos[indice]
        nuevo_hijo = NodoB(min_grado, es_hoja=hijo.es_hoja)

        # Mover la mitad de las claves al nuevo hijo
        nodo.claves.insert(indice, hijo.claves[min_grado - 1])
        nodo.hijos.insert(indice + 1, nuevo_hijo)

        nuevo_hijo.claves = hijo.claves[min_grado:(2 * min_grado) - 1]
        hijo.claves = hijo.claves[0:min_grado - 1]

        # Mover los hijos si no es hoja
        if not hijo.es_hoja:
            nuevo_hijo.hijos = hijo.hijos[min_grado:2 * min_grado]
            hijo.hijos = hijo.hijos[0:min_grado]

    def listado_en_rango(self, nodo, c1, c2):
        # Muestra las claves en el rango (c1, c2) en el árbol B.
        if nodo is None:
            return

        i = 0
        while i < len(nodo.claves):
            if not nodo.es_hoja:
                self.listado_en_rango(nodo.hijos[i], c1, c2)
            if c1 < nodo.claves[i] < c2:
                print(nodo.claves[i], end=' ')
            i += 1

        if not nodo.es_hoja:
            self.listado_en_rango(nodo.hijos[i], c1, c2)

    def mostrar_listado_en_rango(self, c1, c2):
        # Método público para comenzar desde la raíz.
        print(f"Claves en el rango ({c1}, {c2}):")
        self.listado_en_rango(self.raiz, c1, c2)
        print()


# Ejemplo de uso
arbol = ArbolB(min_grado=2)

# Insertar algunas claves
claves_a_insertar = [10, 20, 5, 6, 12, 30, 7, 17]
for clave in claves_a_insertar:
    arbol.insertar(clave)

# Mostrar las claves en el rango (10, 30)
arbol.mostrar_listado_en_rango(5, 30)
