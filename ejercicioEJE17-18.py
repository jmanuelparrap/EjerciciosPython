class NodoB:
    def __init__(self, orden):
        self.orden = orden
        self.claves = []
        self.hijos = []
        self.hoja = True
        # Calculamos el mínimo de ocupación (2/3 del máximo)
        self.min_claves = (2 * orden - 1) * 2 // 3

    def esta_lleno(self):
        return len(self.claves) >= 2 * self.orden - 1

    def puede_prestar(self):
        # Puede prestar si tiene más del mínimo de claves
        return len(self.claves) > self.min_claves

class ArbolBStar:
    def __init__(self, orden):
        self.orden = orden
        self.raiz = NodoB(orden)

    def insertar(self, clave):
        raiz = self.raiz
        if raiz.esta_lleno():
            nueva_raiz = NodoB(self.orden)
            nueva_raiz.hoja = False
            nueva_raiz.hijos.append(self.raiz)
            self.raiz = nueva_raiz
            self._manejar_nodo_lleno(nueva_raiz, 0)
            self._insertar_no_lleno(nueva_raiz, clave)
        else:
            self._insertar_no_lleno(raiz, clave)

    def _insertar_no_lleno(self, nodo, clave):
        i = len(nodo.claves) - 1

        if nodo.hoja:
            # Insertar la clave en la posición correcta
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            nodo.claves.insert(i + 1, clave)
        else:
            # Encontrar el hijo correcto
            while i >= 0 and clave < nodo.claves[i]:
                i -= 1
            i += 1

            if nodo.hijos[i].esta_lleno():
                self._manejar_nodo_lleno(nodo, i)
                if clave > nodo.claves[i]:
                    i += 1
            self._insertar_no_lleno(nodo.hijos[i], clave)

    def _manejar_nodo_lleno(self, padre, indice_hijo):
        hijo = padre.hijos[indice_hijo]
        
        # Intentar redistribuir con hermanos
        if self._intentar_redistribucion(padre, indice_hijo):
            return

        # Si no se puede redistribuir, dividir en tres nodos
        self._dividir_en_tres(padre, indice_hijo)

    def _intentar_redistribucion(self, padre, indice_hijo):
        # Intentar redistribuir con hermano izquierdo
        if indice_hijo > 0:
            hermano_izq = padre.hijos[indice_hijo - 1]
            if not hermano_izq.esta_lleno():
                return self._redistribuir_con_izquierdo(
                    padre, indice_hijo, hermano_izq)

        # Intentar redistribuir con hermano derecho
        if indice_hijo < len(padre.hijos) - 1:
            hermano_der = padre.hijos[indice_hijo + 1]
            if not hermano_der.esta_lleno():
                return self._redistribuir_con_derecho(
                    padre, indice_hijo, hermano_der)

        return False

    def _redistribuir_con_izquierdo(self, padre, indice_hijo, hermano_izq):
        hijo = padre.hijos[indice_hijo]
        total_claves = len(hermano_izq.claves) + len(hijo.claves)
        
        # Calcular nueva distribución
        claves_por_nodo = total_claves // 2
        
        # Si la redistribución mantiene los nodos sobre 2/3 llenos
        if claves_por_nodo >= hijo.min_claves:
            # Mover la clave del padre
            hijo.claves.insert(0, padre.claves[indice_hijo - 1])
            
            # Mover claves del hermano izquierdo
            claves_a_mover = len(hermano_izq.claves) - claves_por_nodo
            padre.claves[indice_hijo - 1] = hermano_izq.claves[-claves_a_mover]
            
            # Actualizar claves y hijos
            hijo.claves = hermano_izq.claves[-claves_a_mover + 1:] + hijo.claves
            hermano_izq.claves = hermano_izq.claves[:-claves_a_mover]
            
            if not hijo.hoja:
                hijo.hijos = (hermano_izq.hijos[-claves_a_mover:] + 
                            hijo.hijos)
                hermano_izq.hijos = hermano_izq.hijos[:-claves_a_mover]
            
            return True
        return False

    def _redistribuir_con_derecho(self, padre, indice_hijo, hermano_der):
        hijo = padre.hijos[indice_hijo]
        total_claves = len(hermano_der.claves) + len(hijo.claves)
        
        # Calcular nueva distribución
        claves_por_nodo = total_claves // 2
        
        # Si la redistribución mantiene los nodos sobre 2/3 llenos
        if claves_por_nodo >= hijo.min_claves:
            # Mover la clave del padre
            hijo.claves.append(padre.claves[indice_hijo])
            
            # Mover claves del hermano derecho
            claves_a_mover = len(hermano_der.claves) - claves_por_nodo
            padre.claves[indice_hijo] = hermano_der.claves[claves_a_mover - 1]
            
            # Actualizar claves y hijos
            hijo.claves.extend(hermano_der.claves[:claves_a_mover - 1])
            hermano_der.claves = hermano_der.claves[claves_a_mover:]
            
            if not hijo.hoja:
                hijo.hijos.extend(hermano_der.hijos[:claves_a_mover])
                hermano_der.hijos = hermano_der.hijos[claves_a_mover:]
            
            return True
        return False

    def _dividir_en_tres(self, padre, indice_hijo):
        hijo = padre.hijos[indice_hijo]
        
        # Crear dos nuevos nodos
        nuevo_izq = NodoB(self.orden)
        nuevo_der = NodoB(self.orden)
        nuevo_izq.hoja = hijo.hoja
        nuevo_der.hoja = hijo.hoja
        
        # Calcular puntos de división para tres nodos
        total_claves = len(hijo.claves)
        claves_por_nodo = total_claves // 3
        
        # Distribuir claves
        nuevo_izq.claves = hijo.claves[:claves_por_nodo]
        nuevo_der.claves = hijo.claves[-claves_por_nodo:]
        
        # Mover claves al padre
        padre.claves.insert(indice_hijo, hijo.claves[claves_por_nodo])
        padre.claves.insert(indice_hijo + 1, hijo.claves[-claves_por_nodo - 1])
        
        # Actualizar hijos si no es hoja
        if not hijo.hoja:
            nuevo_izq.hijos = hijo.hijos[:claves_por_nodo + 1]
            nuevo_der.hijos = hijo.hijos[-claves_por_nodo - 1:]
            hijo.hijos = hijo.hijos[claves_por_nodo + 1:-claves_por_nodo - 1]
            
        # Actualizar hijo central
        hijo.claves = hijo.claves[claves_por_nodo + 1:-claves_por_nodo - 1]
        
        # Actualizar hijos del padre
        padre.hijos[indice_hijo] = nuevo_izq
        padre.hijos.insert(indice_hijo + 1, hijo)
        padre.hijos.insert(indice_hijo + 2, nuevo_der)

    def buscar(self, clave, nodo=None):
        if nodo is None:
            nodo = self.raiz

        i = 0
        while i < len(nodo.claves) and clave > nodo.claves[i]:
            i += 1

        if i < len(nodo.claves) and clave == nodo.claves[i]:
            return True
        elif nodo.hoja:
            return False
        else:
            return self.buscar(clave, nodo.hijos[i])

    def imprimir_arbol(self):
        self._imprimir_nodo(self.raiz, 0)

    def _imprimir_nodo(self, nodo, nivel):
        print(f"Nivel {nivel}:", end=" ")
        print(nodo.claves)
        if not nodo.hoja:
            for hijo in nodo.hijos:
                self._imprimir_nodo(hijo, nivel + 1)
# Crear un árbol B* con orden 5
arbol = ArbolBStar(5)

# Insertar valores
for i in range(50):
    arbol.insertar(i)

# Imprimir el árbol
arbol.imprimir_arbol()

# Buscar valores
print(arbol.buscar(25))  # True
print(arbol.buscar(100)) # False