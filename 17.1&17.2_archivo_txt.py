class nodoAVL:
    def __init__(self, palabra):
        self.palabra = palabra
        self.frecuencia = 1
        self.altura = 1
        self.izquierda = None
        self.derecha = None

class arbolAVL:
    def __init__(self):
        self.arbol = None

    def insertar(self, nodo, palabras):
        if not nodo:
            return nodoAVL(palabras)
        
        # Comparar palabras
        if palabras < nodo.palabra:
            nodo.izquierda = self.insertar(nodo.izquierda, palabras)
        elif palabras > nodo.palabra:
            nodo.derecha = self.insertar(nodo.derecha, palabras)
        else:
            nodo.frecuencia += 1  # Incrementar frecuencia si ya existe
            return nodo

        # Actualizar la altura del nodo actual
        nodo.altura = 1 + max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha))

        # Obtener el factor de balanceo para verificar si está equilibrado
        balance = self.obtener_balance(nodo)

        # Rotaciones para balancear el árbol AVL
        # Caso 1: Rotación derecha
        if balance > 1 and palabras < nodo.izquierda.palabra:
            return self.rotar_derecha(nodo)

        # Caso 2: Rotación izquierda
        if balance < -1 and palabras > nodo.derecha.palabra:
            return self.rotar_izquierda(nodo)

        # Caso 3: Rotación doble izquierda-derecha
        if balance > 1 and palabras > nodo.izquierda.palabra:
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)

        # Caso 4: Rotación doble derecha-izquierda
        if balance < -1 and palabras < nodo.derecha.palabra:
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo

    def rotar_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        # variable temporal que almacena el subarbol izquierdo

        y.izquierda = z
        z.derecha = T2

        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))

        return y

    def rotar_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        # variable temporal que almacena el subarbol derecho del arbol

        y.derecha = z
        z.izquierda = T3

        z.altura = 1 + max(self.obtener_altura(z.izquierda), self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha))

        return y

    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

    def insertar_palabra(self, palabra):
        self.arbol = self.insertar(self.arbol, palabra)

    def en_orden_traversal(self, nodo):
        if not nodo:
            return
        self.en_orden_traversal(nodo.izquierda)
        print(f"{nodo.palabra}: {nodo.frecuencia}")
        self.en_orden_traversal(nodo.derecha)

# Función para procesar el archivo y construir el árbol AVL
def cargar_arbol_avl_desde_archivo(ruta_archivo):
    arbol = arbolAVL()
    with open(ruta_archivo, 'r') as archivo:
        for line in archivo:
            # Dividir en palabras y limpiar caracteres no deseados
            palabras = line.strip().split()
            palabras = [palabra.strip(".,;!?").lower() for palabra in palabras]
            for palabra in palabras:
                if palabra:  # Ignorar palabras vacías
                    arbol.insertar_palabra(palabra)
    return arbol

# imprimir el arbol con las palabras
def imprimir_arbol(nodo, nivel=0, prefijo=""):
    if nodo is not None:  # Si el nodo no está vacío
        # Imprimir el subárbol derecho
        imprimir_arbol(nodo.derecha, nivel + 1, "   " * nivel + "   ┌──")
        # Imprimir el nodo actual con su valor, frecuencia y altura
        print(f"{'   ' * nivel}{prefijo}{nodo.palabra} (Freq: {nodo.frecuencia}, Height: {nodo.altura})")
        # Imprimir el subárbol izquierdo
        imprimir_arbol(nodo.izquierda, nivel + 1, "   " * nivel + "   └──")

# Construcción y visualización del árbol AVL
file_path = 'C:/Users/Mafe Yepes/Downloads/EstructurasDatosC++/problemas_pag_17/carta.txt'
arbol_avl = cargar_arbol_avl_desde_archivo(file_path)
print("Palabras y frecuencias en orden alfabético:")
arbol_avl.en_orden_traversal(arbol_avl.arbol)

# Mostrar el arbol en consola
print("\n Estructura del árbol AVL:")
print("\n")
imprimir_arbol(arbol_avl.arbol)
print("\n")
