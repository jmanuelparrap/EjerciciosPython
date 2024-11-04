class nodo_arbol:
    def __init__(self, apellido):
        self.apellido = apellido
        self.izquierdo = None
        self.derecho = None

class arbol_busqueda:
    def __init__(self):
        self.arbol = None

    def insertar(self, apellido):
        nuevo_nodo = nodo_arbol(apellido)
        
        # Si el árbol está vacío, el nuevo nodo se convierte en la raíz
        if not self.arbol:
            self.arbol = nuevo_nodo
            return
        
        # Utilizamos un nodo actual para ir recorriendo el árbol y otro para mantener el nodo padre
        nodo_actual = self.arbol
        nodo_padre = None
        
        while nodo_actual:
            nodo_padre = nodo_actual
            
            # Determinar si ir a la izquierda o a la derecha
            if apellido < nodo_actual.apellido:
                nodo_actual = nodo_actual.izquierdo
            else:
                nodo_actual = nodo_actual.derecho
        
        # Insertamos el nuevo nodo en el lugar apropiado
        if apellido < nodo_padre.apellido:
            nodo_padre.izquierdo = nuevo_nodo
        else:
            nodo_padre.derecho = nuevo_nodo

    def en_orden(self):
        def _en_orden(nodo):
            if nodo:
                _en_orden(nodo.izquierdo)
                print(nodo.apellido)
                _en_orden(nodo.derecho)
        _en_orden(self.arbol)

    # imprimir el arbol con las palabras
def imprimir_arbol(nodo, nivel=0, prefijo=""):
    if nodo is not None:  # Si el nodo no está vacío
        # Imprimir el subárbol derecho
        imprimir_arbol(nodo.derecho, nivel + 1, "   " * nivel + "   ┌──")
        # Imprimir el nodo actual con su valor, frecuencia y altura
        print(f"{'   ' * nivel}{prefijo}{nodo.apellido}")
        # Imprimir el subárbol izquierdo
        imprimir_arbol(nodo.izquierdo, nivel + 1, "   " * nivel + "   └──")

# Prueba de inserción iterativa
arbol_de_busqueda = arbol_busqueda()
apellidos = ["Perez", "Gomez", "Lopez", "Sanchez", "Torres", "Diaz"]

for apellido in apellidos:
    arbol_de_busqueda.insertar(apellido)

# Imprimir el árbol en orden para verificar la inserción
print("Arbol Equilibrado")
arbol_de_busqueda.en_orden()

# estuctura del arbol
print("\n")
print("Estuctura del arbol")
print("\n")
imprimir_arbol(arbol_de_busqueda.arbol)
print("\n")