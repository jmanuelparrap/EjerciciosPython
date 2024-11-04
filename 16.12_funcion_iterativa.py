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

# Función iterativa para contar el número de nodos hoja
def contar_hojas(arbol):
    # si el arbol no tiene nodos
    if arbol is None:
        return 0

    # Usamos una cola para el recorrido iterativo
    cola = [arbol]
    contador_hojas = 0

    while cola:
        nodo_actual = cola.pop(0)

        # Un nodo hoja no tiene hijos
        if nodo_actual.izquierda is None and nodo_actual.derecha is None:
            contador_hojas += 1
        else:
            # Agregar los hijos del nodo actual a la cola
            if nodo_actual.izquierda:
                cola.append(nodo_actual.izquierda)
            if nodo_actual.derecha:
                cola.append(nodo_actual.derecha)

    return contador_hojas

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
arbol_binario = crear_arbol_binario(letras)

# Imprimir el árbol de forma gráfica
print("Árbol binario:")
imprimir_arbol(arbol_binario)

# numero de nodos hoja en el arbol binario
hojas = contar_hojas(arbol_binario)
print("\nEl arbol tiene ", hojas, " nodos hoja")
