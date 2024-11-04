class Node:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolEquilibrado:
    def __init__(self):
        self.raiz = None
    
    def altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura
    
    def actualizar_altura(self, nodo):
        if not nodo:
            return
        nodo.altura = max(self.altura(nodo.izquierda), self.altura(nodo.derecha)) + 1
    
    def balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)
    
    def rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha
        x.derecha = y
        y.izquierda = T2
        y.altura = max(self.altura(y.izquierda), self.altura(y.derecha)) + 1
        x.altura = max(self.altura(x.izquierda), self.altura(x.derecha)) + 1
        return x
    
    def rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda
        y.izquierda = x
        x.derecha = T2
        x.altura = max(self.altura(x.izquierda), self.altura(x.derecha)) + 1
        y.altura = max(self.altura(y.izquierda), self.altura(y.derecha)) + 1
        return y
    
    def insertar(self, valor):
        if not self.raiz:
            self.raiz = Node(valor)
        else:
            self.raiz = self._insertar_recursivo(self.raiz, valor)
    
    def _insertar_recursivo(self, nodo, valor):
        if not nodo:
            return Node(valor)
        
        if valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)
        
        nodo.altura = max(self.altura(nodo.izquierda), self.altura(nodo.derecha)) + 1
        
        balance = self.balance(nodo)
        
        if balance > 1:
            if valor < nodo.izquierda.valor:
                return self.rotar_derecha(nodo)
            else:
                nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
                return self.rotar_derecha(nodo)
        
        if balance < -1:
            if valor > nodo.derecha.valor:
                return self.rotar_izquierda(nodo)
            else:
                nodo.derecha = self.rotar_derecha(nodo.derecha)
                return self.rotar_izquierda(nodo)
        
        return nodo
    
    def buscarMin(self):
        """
        Encuentra el valor mínimo en el árbol de forma iterativa usando una pila
        para el recorrido de los nodos.
        """
        if not self.raiz:
            return None
            
        pila = []
        nodo_actual = self.raiz
        min_valor = float('inf')
        
        # Usamos una pila para recorrer el árbol de forma iterativa
        while True:
            # Mientras haya un nodo, lo agregamos a la pila
            if nodo_actual:
                pila.append(nodo_actual)
                nodo_actual = nodo_actual.izquierda
            # Si no hay nodo actual pero hay elementos en la pila
            elif pila:
                nodo_actual = pila.pop()
                # Actualizamos el mínimo si encontramos un valor menor
                min_valor = min(min_valor, nodo_actual.valor)
                nodo_actual = nodo_actual.derecha
            # Si no hay nodo actual ni elementos en la pila, terminamos
            else:
                break
                
        return Node(min_valor)
    
    def buscarMax(self):
        """
        Encuentra el valor máximo en el árbol de forma iterativa usando una pila
        para el recorrido de los nodos.
        """
        if not self.raiz:
            return None
            
        pila = []
        nodo_actual = self.raiz
        max_valor = float('-inf')
        
        # Similar a buscarMin, pero actualizando el máximo
        while True:
            if nodo_actual:
                pila.append(nodo_actual)
                nodo_actual = nodo_actual.izquierda
            elif pila:
                nodo_actual = pila.pop()
                # Actualizamos el máximo si encontramos un valor mayor
                max_valor = max(max_valor, nodo_actual.valor)
                nodo_actual = nodo_actual.derecha
            else:
                break
                
        return Node(max_valor)

# Ejemplo de uso
if __name__ == "__main__":
    arbol = ArbolEquilibrado()
    valores = [5, 3, 7, 1, 4, 6, 8]
    
    # Insertamos los valores
    for valor in valores:
        arbol.insertar(valor)
    
    # Probamos ambos métodos
    nodo_minimo = arbol.buscarMin()
    nodo_maximo = arbol.buscarMax()
    
    print(f"El valor mínimo en el árbol es: {nodo_minimo.valor}")  # Debería imprimir 1
    print(f"El valor máximo en el árbol es: {nodo_maximo.valor}")  # Debería imprimir 8