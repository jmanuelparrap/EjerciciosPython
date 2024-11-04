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
def crear_arbol_binario(letras):
    raiz = None
    for letra in letras:
        raiz = insertar(raiz, letra)
    return raiz

# Funcion para contar el numero de nodos en un nivel especifico
def contar_nodos_nivel(nodo, nivel_indicado, nivel_actual=0):
    if nodo is None:
        return 0
    # Si el nivel actual es igual al nivel deseado, contar el nodo
    if nivel_actual == nivel_indicado:
        return 1
    # Llamada recursiva para hijos izquierdo y derecho, aumentando el nivel actual en 1
    return (contar_nodos_nivel(nodo.izquierda, nivel_indicado, nivel_actual + 1) +
            contar_nodos_nivel(nodo.derecha, nivel_indicado, nivel_actual + 1))

def preorden(nodo):
    if nodo is None:
        return []
    return [nodo.valor] + preorden(nodo.izquierda) + preorden(nodo.derecha)

def enorden(nodo):
    if nodo is None:
        return []
    return enorden(nodo.izquierda) + [nodo.valor] + enorden(nodo.derecha)

def postorden(nodo):
    if nodo is None:
        return []
    return postorden(nodo.izquierda) + postorden(nodo.derecha) + [nodo.valor]

# Funcion recursiva que muestra cada nivel del arbol con lineas que conectan los nodos
def imprimir_arbol(nodo, nivel=0, prefijo=""):
    if nodo is not None: # Si el nodo no esta vacio
        # El nivel + 1, va dandole los espacios entre los nodos del arbol
        imprimir_arbol(nodo.derecha, nivel + 1, "   " * nivel + "   ┌──")
        print(f"{'   ' * nivel}{prefijo}{nodo.valor}")
        imprimir_arbol(nodo.izquierda, nivel + 1, "   " * nivel + "   └──")

# Lista de letras para crear el árbol
letras = ['A', 'B', 'C', 'D', 'E']

# Crear el árbol binario a partir de las letras
raiz = crear_arbol_binario(letras)

# Imprimir el árbol de forma gráfica
print("Árbol binario:")
imprimir_arbol(raiz)

# Recorridos
print("\nRecorrido en Preorden:", preorden(raiz))
print("Recorrido en Enorden:", enorden(raiz))
print("Recorrido en Postorden:", (postorden(raiz)))

# Contar nodos en el nivel especificado
nivel_indicado = 2
nodos_en_nivel = contar_nodos_nivel(raiz, nivel_indicado)
print(f"\nNúmero de nodos en el nivel {nivel_indicado}:", nodos_en_nivel)
