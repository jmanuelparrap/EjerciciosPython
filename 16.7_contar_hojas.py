# clase constructora
class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

# va añadiendo los nodos al arbol de manera organizada
def insertar_por_niveles(arr, raiz, indice_actual, tamaño):
    # Caso base para construir el árbol
    if indice_actual < tamaño:
        temporal = NodoArbol(arr[indice_actual])
        raiz = temporal

        # Insertar hijos izquierdo y derecho
        raiz.izquierdo = insertar_por_niveles(arr, raiz.izquierdo, 2 * indice_actual + 1, tamaño)
        raiz.derecho = insertar_por_niveles(arr, raiz.derecho, 2 * indice_actual + 2, tamaño)
    return raiz

# recorre el arbol en busca de hojas, y las agrega a una lista de hojas
def contar_y_obtener_hojas(raiz, hojas):
    if raiz is None:
        return 0
    if raiz.izquierdo is None and raiz.derecho is None:
        hojas.append(raiz.valor)
        return 1
    return contar_y_obtener_hojas(raiz.izquierdo, hojas) + contar_y_obtener_hojas(raiz.derecho, hojas)

# Función principal
def construir_y_analizar_arbol(arr):
    tamaño = len(arr)
    raiz = insertar_por_niveles(arr, None, 0, tamaño)  # Construimos el árbol

    hojas = []
    numero_hojas = contar_y_obtener_hojas(raiz, hojas)  # Contamos hojas y obtenemos sus valores

    print("Número de hojas:", numero_hojas)
    print("Hojas:", hojas)

# Ejemplo de uso
array = ['A', 'B', 'C', 'D', 'E']
construir_y_analizar_arbol(array)
