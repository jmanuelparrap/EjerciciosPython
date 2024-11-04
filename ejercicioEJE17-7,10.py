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
        
        # Casos de desequilibrio y rotaciones
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
        if self.raiz is None:
            return None
        return self._buscarMin_recursivo(self.raiz)
    
    def _buscarMin_recursivo(self, nodo):
        if nodo is None:
            return None
            
        # Encontramos el mínimo comparando el valor actual con los mínimos
        # de los subárboles izquierdo y derecho
        min_valor = nodo.valor
        
        min_izq = self._buscarMin_recursivo(nodo.izquierda)
        if min_izq is not None:
            min_valor = min(min_valor, min_izq.valor)
            
        min_der = self._buscarMin_recursivo(nodo.derecha)
        if min_der is not None:
            min_valor = min(min_valor, min_der.valor)
        
        # Creamos un nuevo nodo con el valor mínimo encontrado
        return Node(min_valor)
    def buscarMax(self):
        if self.raiz is None:
            return None
        return self._buscarMax_recursivo(self.raiz)
    
    def _buscarMax_recursivo(self, nodo):
        if nodo is None:
            return None
            
        # Encontramos el máximo comparando el valor actual con los máximos
        # de los subárboles izquierdo y derecho
        max_valor = nodo.valor
        
        max_izq = self._buscarMax_recursivo(nodo.izquierda)
        if max_izq is not None:
            max_valor = max(max_valor, max_izq.valor)
            
        max_der = self._buscarMax_recursivo(nodo.derecha)
        if max_der is not None:
            max_valor = max(max_valor, max_der.valor)
        
        # Creamos un nuevo nodo con el valor máximo encontrado
        return Node(max_valor)

# Ejemplo de uso
if __name__ == "__main__":
    arbol = ArbolEquilibrado()
    valores = [5, 3, 7, 1, 4, 6, 8]
    
    for valor in valores:
        arbol.insertar(valor)
    
    nodo_minimo = arbol.buscarMin()
    print(f"El valor mínimo en el árbol es: {nodo_minimo.valor}")
    
    nodo_maximo = arbol.buscarMax()
    print(f"El valor máximo en el árbol es: {nodo_maximo.valor}")