class NodoB:
    def __init__(self, es_hoja=True):
        self.claves = []        # Lista de claves en el nodo
        self.hijos = []         # Lista de referencias a los hijos
        self.es_hoja = es_hoja  # Indica si el nodo es hoja
        
    def buscar_clave_en_nodo(self, clave):
        """Busca la posición de una clave en el nodo actual"""
        i = 0
        while i < len(self.claves) and clave > self.claves[i]:
            i += 1
        return i

class ArbolB:
    def __init__(self, orden):
        self.raiz = NodoB()
        self.orden = orden      # Orden del árbol B
        
    def buscar_iterativo(self, clave):
        """
        Implementación iterativa de búsqueda en árbol B.
        Retorna una tupla (nodo, indice) si encuentra la clave,
        o None si no la encuentra.
        """
        nodo_actual = self.raiz
        
        while True:
            # Buscar la posición donde debería estar la clave en el nodo actual
            i = nodo_actual.buscar_clave_en_nodo(clave)
            
            # Si encontramos la clave en el nodo actual
            if i < len(nodo_actual.claves) and nodo_actual.claves[i] == clave:
                return (nodo_actual, i)
            
            # Si es hoja y no encontramos la clave, entonces no existe
            if nodo_actual.es_hoja:
                return None
            
            # Si no es hoja, continuamos la búsqueda en el hijo correspondiente
            nodo_actual = nodo_actual.hijos[i]

# Ejemplo de uso
def ejemplo_busqueda():
    # Crear un árbol B de orden 5
    arbol = ArbolB(5)
    
    # Crear un árbol B de ejemplo
    raiz = NodoB(es_hoja=False)
    raiz.claves = [10, 20, 30]
    
    hijo1 = NodoB()
    hijo1.claves = [5, 7, 9]
    
    hijo2 = NodoB()
    hijo2.claves = [15, 17, 19]
    
    hijo3 = NodoB()
    hijo3.claves = [22, 25, 27]
    
    hijo4 = NodoB()
    hijo4.claves = [32, 35, 37]
    
    raiz.hijos = [hijo1, hijo2, hijo3, hijo4]
    arbol.raiz = raiz
    
    # Realizar búsquedas
    resultados = []
    for clave in [7, 15, 30, 40]:
        resultado = arbol.buscar_iterativo(clave)
        if resultado:
            nodo, indice = resultado
            resultados.append(f"Clave {clave} encontrada en posición {indice}")
        else:
            resultados.append(f"Clave {clave} no encontrada")
    
    return resultados

# Ejecutar ejemplo
resultados = ejemplo_busqueda()
for r in resultados:
    print(r)