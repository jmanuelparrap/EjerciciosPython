# Clase donde se crean los nodos del arbol
class nodos_arbol:
    def __init__(self, apellido):
        self.apellido = apellido
        self.izquierda = None
        self.derecha = None

# clase donde se modifica el arbol de busqueda
class arbol_equilibrado:
    def __init__(self):
        self.arbol = None

# Metodo para insertar valores al arbol de busqueda
    def insertar (self, apellido):
        if not self.arbol: # si aun no se ha creado el arbol
            self.arbol = nodos_arbol(apellido) # crea el espacio para nuevos nodos con el valor de apellido
        else: # si el arbol ya esta creado
            self.insertar_recursivo(self.arbol, apellido) # llama la funcion y le envia los parametros

# metodo que se llama a si mismo para insertar los valores de forma organizada
    def insertar_recursivo(self, nodo_actual, apellido):
        if apellido < nodo_actual.apellido: # verifica el orden de los apellidos
            if nodo_actual.izquierda: # si su inicial va antes, 
                self.insertar_recursivo(nodo_actual.izquierda, apellido)
            else:
                nodo_actual.izquierda = nodos_arbol(apellido) # subarbol izquierdo en el arbol

        else: # si su inicial va despues que el del nodo actual
            if nodo_actual.derecha:
                self.insertar_recursivo(nodo_actual.derecha, apellido)
            else:
                nodo_actual.derecha = nodos_arbol(apellido) # subarbol derecho en el arbol

    def en_orden(self):
        # Método para recorrer el árbol en orden
        def recorrer(nodo):
            if nodo:
                recorrer(nodo.izquierda)
                print(f"{nodo.apellido}")
                recorrer(nodo.derecha)
        recorrer(self.arbol)

# imprimir el arbol con las palabras
def imprimir_arbol(nodo, nivel=0, prefijo=""):
    if nodo is not None:  # Si el nodo no está vacío
        # Imprimir el subárbol derecho
        imprimir_arbol(nodo.derecha, nivel + 1, "    " * nivel + "   ┌──")
        # imprimir los valores
        print(f"{'   ' * nivel}{prefijo}{nodo.apellido}")
        # Imprimir el subárbol izquierdo
        imprimir_arbol(nodo.izquierda, nivel + 1, "    " * nivel + "   └──")

    # Leer archivo y construir el BST
arbolEquilibrado = arbol_equilibrado()
with open('C:/Users/Mafe Yepes/Downloads/EstructurasDatosC++/problemas_pag_17/alumnos.txt', 'r') as file:
    for line in file:
        nombre_completo = line.strip()
        apellido = nombre_completo.split()[-1]  # Supone que el apellido está al final
        arbolEquilibrado.insertar(apellido)

class nodosFibonacci:
    def __init__(self, apellido):
        self.apellido = apellido
        self.izquierda = None
        self.derecha = None

# clase donde se modifica el arbol de busqueda
class arbol_fibonacci:
    def __init__(self):
        self.arbol = None

    # Aca inicia el metodo para construir con los nodos un arbol de Fibonacci
    def construir_fibonacci(self, nodo_arbol_busqueda):
        if nodo_arbol_busqueda is None:
            return None
        nodo_fibonacci = nodosFibonacci(nodo_arbol_busqueda.apellido)

        nodo_fibonacci.izquierda = self.construir_fibonacci(nodo_arbol_busqueda.izquierda)
        nodo_fibonacci.derecha = self.construir_fibonacci(nodo_arbol_busqueda.derecha)

        return nodo_fibonacci

#  crear el arbol de Fibonacci con los nodos del arbol de busqueda
Arbol_fibonacci = arbol_fibonacci()
Arbol_fibonacci.arbol = Arbol_fibonacci.construir_fibonacci(arbolEquilibrado.arbol)

# Método de recorrido en preorden para imprimir el árbol de Fibonacci
def preorden_fibonacci(nodo):
    if nodo:
        print(nodo.apellido)
        preorden_fibonacci(nodo.izquierda)
        preorden_fibonacci(nodo.derecha)


# Imprimir el árbol en orden para verificar
print("-----------------------------------------Arbol de busqueda")
arbolEquilibrado.en_orden()

print("\n Estructura del árbol de busqueda:")
print("\n")
imprimir_arbol(arbolEquilibrado.arbol)
print("\n")

print("----------------------------------------Arbol de Fibonacci")
# Imprimir el árbol de Fibonacci en preorden
preorden_fibonacci(Arbol_fibonacci.arbol)
print("\n")

print("Estructura del árbol de Fibonacci:")
print("\n")
imprimir_arbol(Arbol_fibonacci.arbol)
print("\n")
