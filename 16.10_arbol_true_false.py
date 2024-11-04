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

# Funcion para verificar si un arbol binario es completo o incompleto
def verificar_arbol (arbol):
    if arbol is None:
        return True
    
#  recorrer el arbol por niveles
    nodos_nivel = [arbol]
    nodos_sin_hijos = False
    # marcador para nodos vacios

    while nodos_nivel:
        nodo_actual = nodos_nivel.pop(0)

        # verificar el nodo izquierdo
        if nodo_actual.izquierda:
            if nodos_sin_hijos:
                return False # si hay un nodo despues de un None, no es completo
            nodos_nivel.append(nodo_actual.izquierda)
        else:
            nodos_sin_hijos = True

# verificar el nodo derecho
        if nodo_actual.derecha:
            if nodos_sin_hijos:
                return False # si hay un nodo despues de un None, no es completo
            nodos_nivel.append(nodo_actual.derecha)
        else:
            nodos_sin_hijos = True

    return True

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

# verificar si el arbol es completo o incompleto
if verificar_arbol(raiz):
    print("\n El arbol binario es completo")
else:
    print("\n El arbol binario no es completo")

# Recorridos
print("\nRecorrido en Preorden:", preorden(raiz))
print("Recorrido en Enorden:", enorden(raiz))
print("Recorrido en Postorden:", (postorden(raiz)))