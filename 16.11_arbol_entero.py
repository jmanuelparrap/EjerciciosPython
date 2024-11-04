# Clase constructora, crea nodos
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

# Va comparando las letras ingresadas y organizandolas 
def insertar(nodo, valor):
    # Si el árbol está vacío, crear un nuevo nodo
    if nodo is None:
        return Nodo(valor)
    # Insertar en el subárbol izquierdo si el valor es menor al nodo actual
    if valor < nodo.valor:
        nodo.izquierda = insertar(nodo.izquierda, valor)
    # Insertar en el subárbol derecho si el valor es mayor al nodo actual
    else:
        nodo.derecha = insertar(nodo.derecha, valor)
    return nodo

# recibe el array, inserta cada letra en el arbol y devuelve la raiz del arbol construido
def crear_arbol_binario(numeros):
    raiz = None
    for numero in numeros:
        raiz = insertar(raiz, numero)
    return raiz

# funcion para la suma de sus elementos, va recibiendo los nodos del arbol
def suma_elementos(nodo):
    if nodo is None: # si el nodo esta vacio, no devuelve nada
        return 0
    
    # suma el nodo actual y los nodos de los subarboles izquierdo y derecho
    return nodo.valor + suma_elementos(nodo.izquierda) + suma_elementos(nodo.derecha)

# la suma de sus elementos que son multiplos de 3
def suma_elementos_multiplos(nodo):
    if nodo is None: # si el nodo esta vacio, no devuelve nada
        return 0

# Operacion para validar que el valor del nodo sea un multiplo de 3
    comprobar_multiplo = nodo.valor if nodo.valor % 3 == 0 else 0

    # suma el nodo actual y los nodos de los subarboles izquierdo y derecho
    return comprobar_multiplo + suma_elementos_multiplos(nodo.izquierda) + suma_elementos_multiplos(nodo.derecha)

# Funcion recursiva que muestra cada nivel del arbol con lineas que conectan los nodos
def imprimir_arbol(nodo, nivel=0, prefijo=""):
    if nodo is not None: # Si el nodo no esta vacio
        # El nivel + 1, va dandole los espacios entre los nodos del arbol
        imprimir_arbol(nodo.derecha, nivel + 1, "   " * nivel + "   ┌──")
        print(f"{'   ' * nivel}{prefijo}{nodo.valor}")
        imprimir_arbol(nodo.izquierda, nivel + 1, "   " * nivel + "   └──")

# Lista de letras para crear el árbol
letras = [10, 2, 15, 30, 5]

# Crear el árbol binario a partir de las letras
arbol = crear_arbol_binario(letras)

# Imprimir el árbol de forma gráfica
print("Árbol binario:")
imprimir_arbol(arbol)

# ver la suma total de elementos
suma_total = suma_elementos(arbol)
print("La suma total de los elementos del arbol binario es ", suma_total)

# ver la suma de los elementos que son multiplos de 3
suma_multiplos = suma_elementos_multiplos(arbol)
print("La suma de sus elementos que son multiplos de 3 es ", suma_multiplos)