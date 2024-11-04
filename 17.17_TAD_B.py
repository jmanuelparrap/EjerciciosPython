import pickle
import os

# Configuración para el grado mínimo del árbol B
MIN_GRADO = 2  # Este es el grado mínimo (B-Tree de orden 2)

class NodoB:
    def __init__(self, es_hoja):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []

class ArbolB:
    def __init__(self, nombre_archivo):
        self.raiz = NodoB(es_hoja=True)
        self.nombre_archivo = nombre_archivo
        self._guardar()

    def _guardar(self):
        # Guarda el árbol B completo en un archivo.
        with open(self.nombre_archivo, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def cargar(nombre_archivo):
        # Carga un árbol B desde un archivo.
        if os.path.exists(nombre_archivo):
            with open(nombre_archivo, 'rb') as f:
                return pickle.load(f)
        else:
            return ArbolB(nombre_archivo)

    def buscar(self, nodo, clave):
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1
        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return (nodo, i)
        elif nodo.es_hoja:
            return None
        else:
            hijo = self._cargar_nodo(nodo.hijos[i])
            return self.buscar(hijo, clave)

    def insertar(self, clave):
        raiz = self.raiz
        if len(raiz.claves) == (2 * MIN_GRADO) - 1:
            nueva_raiz = NodoB(es_hoja=False)
            nueva_raiz.hijos.append(self._guardar_nodo(raiz))
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz = nueva_raiz
            self._insertar_no_lleno(self.raiz, clave)
        else:
            self._insertar_no_lleno(raiz, clave)
        self._guardar()

    def _dividir_hijo(self, nodo, indice):
        y = self._cargar_nodo(nodo.hijos[indice])
        z = NodoB(es_hoja=y.es_hoja)
        nodo.claves.insert(indice, y.claves[MIN_GRADO - 1])
        nodo.hijos.insert(indice + 1, self._guardar_nodo(z))
        z.claves = y.claves[MIN_GRADO:]
        y.claves = y.claves[:MIN_GRADO - 1]

        if not y.es_hoja:
            z.hijos = y.hijos[MIN_GRADO:]
            y.hijos = y.hijos[:MIN_GRADO]
        self._guardar_nodo(y)
        self._guardar_nodo(z)

    def _insertar_no_lleno(self, nodo, clave):
        i = len(nodo.claves) - 1
        if nodo.es_hoja:
            nodo.claves.append(0)
            while i >= 0 and clave < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = clave
            self._guardar_nodo(nodo)
        else:
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1
            hijo = self._cargar_nodo(nodo.hijos[i])
            if len(hijo.claves) == (2 * MIN_GRADO) - 1:
                self._dividir_hijo(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1
            hijo = self._cargar_nodo(nodo.hijos[i])
            self._insertar_no_lleno(hijo, clave)

    def eliminar(self, clave):
        self._eliminar_en_nodo(self.raiz, clave)
        if len(self.raiz.claves) == 0:
            if not self.raiz.es_hoja:
                self.raiz = self._cargar_nodo(self.raiz.hijos[0])
            else:
                self.raiz = NodoB(es_hoja=True)
        self._guardar()

    def _eliminar_en_nodo(self, nodo, clave):
        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and clave == nodo.claves[i]:
            if nodo.es_hoja:
                nodo.claves.pop(i)
                self._guardar_nodo(nodo)
            else:
                if len(self._cargar_nodo(nodo.hijos[i]).claves) >= MIN_GRADO:
                    pred = self._obtener_predecesor(nodo, i)
                    nodo.claves[i] = pred
                    self._eliminar_en_nodo(self._cargar_nodo(nodo.hijos[i]), pred)
                elif len(self._cargar_nodo(nodo.hijos[i + 1]).claves) >= MIN_GRADO:
                    succ = self._obtener_sucesor(nodo, i)
                    nodo.claves[i] = succ
                    self._eliminar_en_nodo(self._cargar_nodo(nodo.hijos[i + 1]), succ)
                else:
                    self._fusionar(nodo, i)
                    self._eliminar_en_nodo(self._cargar_nodo(nodo.hijos[i]), clave)
        elif not nodo.es_hoja:
            hijo = self._cargar_nodo(nodo.hijos[i])
            if len(hijo.claves) < MIN_GRADO:
                self._asegurar_minimo(hijo, nodo, i)
            self._eliminar_en_nodo(hijo, clave)

    def _guardar_nodo(self, nodo):
        # Genera un nombre de archivo único para cada nodo y lo guarda
        filename = f"{self.nombre_archivo}_node_{id(nodo)}.pkl"
        with open(filename, 'wb') as f:
            pickle.dump(nodo, f)
        return filename

    def _cargar_nodo(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def _obtener_predecesor(self, nodo, i):
        actual = self._cargar_nodo(nodo.hijos[i])
        while not actual.es_hoja:
            actual = self._cargar_nodo(actual.hijos[-1])
        return actual.claves[-1]

    def _obtener_sucesor(self, nodo, i):
        actual = self._cargar_nodo(nodo.hijos[i + 1])
        while not actual.es_hoja:
            actual = self._cargar_nodo(actual.hijos[0])
        return actual.claves[0]

    def _fusionar(self, nodo, i):
        hijo_izq = self._cargar_nodo(nodo.hijos[i])
        hijo_der = self._cargar_nodo(nodo.hijos[i + 1])
        hijo_izq.claves.append(nodo.claves[i])
        hijo_izq.claves.extend(hijo_der.claves)
        if not hijo_izq.es_hoja:
            hijo_izq.hijos.extend(hijo_der.hijos)
        nodo.claves.pop(i)
        nodo.hijos.pop(i + 1)
        self._guardar_nodo(hijo_izq)
        self._guardar_nodo(nodo)

    def _asegurar_minimo(self, nodo, padre, indice):
        # Implementa la lógica para asegurar que `nodo` tenga al menos MIN_GRADO claves.
        pass

# Ejemplo de uso
nombre_archivo = "arbol_b.pkl"
arbol = ArbolB.cargar(nombre_archivo)
arbol.insertar(10)
arbol.insertar(20)
arbol.insertar(5)
arbol.insertar(6)
arbol.insertar(12)
print("Árbol B guardado y cargado en disco con inserciones.")
arbol.eliminar(10)
print("Clave 10 eliminada.")
