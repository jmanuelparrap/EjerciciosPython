# Implementación del Nodo AVL para almacenar habitantes
class NodoAVL:
    def __init__(self, nombre):
        self.nombre = nombre
        self.izquierda = None
        self.derecha = None
        self.altura = 1

# Implementación de la estructura Pueblo
class Pueblo:
    def __init__(self, nombre, num_habitantes):
        self.nombre = nombre
        self.num_habitantes = num_habitantes
        self.arbol_habitantes = None  # Raíz del árbol AVL
        
    def __str__(self):
        return f"Pueblo: {self.nombre}, Habitantes: {self.num_habitantes}"

class SistemaPueblos:
    def __init__(self, pueblos_info):
        """
        Inicializa el sistema con la información básica de los pueblos
        pueblos_info: lista de tuplas (nombre_pueblo, num_habitantes)
        """
        self.pueblos = [Pueblo(nombre, habitantes) 
                       for nombre, habitantes in pueblos_info]
        
    def _obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura
    
    def _factor_balance(self, nodo):
        if not nodo:
            return 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)
    
    def _actualizar_altura(self, nodo):
        if not nodo:
            return
        nodo.altura = max(self._obtener_altura(nodo.izquierda),
                         self._obtener_altura(nodo.derecha)) + 1
    
    def _rotacion_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha
        
        x.derecha = y
        y.izquierda = T2
        
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        
        return x
    
    def _rotacion_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda
        
        y.izquierda = x
        x.derecha = T2
        
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        
        return y
    
    def _insertar_avl(self, nodo, nombre):
        # Inserción normal BST
        if not nodo:
            return NodoAVL(nombre)
            
        if nombre < nodo.nombre:
            nodo.izquierda = self._insertar_avl(nodo.izquierda, nombre)
        elif nombre > nodo.nombre:
            nodo.derecha = self._insertar_avl(nodo.derecha, nombre)
        else:
            return nodo  # No se permiten nombres duplicados
        
        # Actualizar altura
        self._actualizar_altura(nodo)
        
        # Obtener factor de balance
        balance = self._factor_balance(nodo)
        
        # Casos de desbalance
        # Izquierda Izquierda
        if balance > 1 and nombre < nodo.izquierda.nombre:
            return self._rotacion_derecha(nodo)
        
        # Derecha Derecha
        if balance < -1 and nombre > nodo.derecha.nombre:
            return self._rotacion_izquierda(nodo)
        
        # Izquierda Derecha
        if balance > 1 and nombre > nodo.izquierda.nombre:
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)
        
        # Derecha Izquierda
        if balance < -1 and nombre < nodo.derecha.nombre:
            nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)
        
        return nodo
    
    def agregar_habitante(self, nombre_pueblo, nombre_habitante):
        """
        Agrega un habitante al árbol AVL del pueblo correspondiente
        """
        for pueblo in self.pueblos:
            if pueblo.nombre == nombre_pueblo:
                pueblo.arbol_habitantes = self._insertar_avl(
                    pueblo.arbol_habitantes, nombre_habitante)
                return True
        return False
    
    def _imprimir_arbol(self, nodo, nivel=0):
        if not nodo:
            return
        
        self._imprimir_arbol(nodo.derecha, nivel + 1)
        print('  ' * nivel + str(nodo.nombre))
        self._imprimir_arbol(nodo.izquierda, nivel + 1)
    
    def mostrar_habitantes_pueblo(self, nombre_pueblo):
        """
        Muestra los habitantes de un pueblo específico en orden alfabético
        """
        for pueblo in self.pueblos:
            if pueblo.nombre == nombre_pueblo:
                print(f"\nHabitantes de {pueblo.nombre}:")
                self._imprimir_arbol(pueblo.arbol_habitantes)
                return True
        return False
    
    def _contar_habitantes(self, nodo):
        if not nodo:
            return 0
        return 1 + self._contar_habitantes(nodo.izquierda) + \
               self._contar_habitantes(nodo.derecha)
    
    def verificar_cantidad_habitantes(self):
        """
        Verifica que el número de habitantes en el árbol coincida 
        con el número registrado
        """
        for pueblo in self.pueblos:
            habitantes_arbol = self._contar_habitantes(pueblo.arbol_habitantes)
            if habitantes_arbol != pueblo.num_habitantes:
                print(f"¡Advertencia! En {pueblo.nombre}:")
                print(f"Habitantes registrados: {pueblo.num_habitantes}")
                print(f"Habitantes en árbol: {habitantes_arbol}")
    
    def buscar_habitante(self, nombre_habitante):
        """
        Busca un habitante en todos los pueblos
        """
        def _buscar_en_arbol(nodo, nombre):
            if not nodo:
                return False
            if nombre == nodo.nombre:
                return True
            if nombre < nodo.nombre:
                return _buscar_en_arbol(nodo.izquierda, nombre)
            return _buscar_en_arbol(nodo.derecha, nombre)
        
        for pueblo in self.pueblos:
            if _buscar_en_arbol(pueblo.arbol_habitantes, nombre_habitante):
                return pueblo.nombre
        return None

# Ejemplo de uso
def main():
    # Crear el sistema con información inicial de pueblos
    pueblos_info = [
        ("Peñablanca", 3),
        ("Rocaalta", 4),
        ("Montepino", 2)
    ]
    
    sistema = SistemaPueblos(pueblos_info)
    
    # Agregar habitantes a los pueblos
    habitantes = [
        ("Peñablanca", "Ana García"),
        ("Peñablanca", "Carlos Ruiz"),
        ("Peñablanca", "Beatriz López"),
        ("Rocaalta", "David Martín"),
        ("Rocaalta", "Elena Torres"),
        ("Rocaalta", "Francisco Pérez"),
        ("Rocaalta", "Gloria Sánchez"),
        ("Montepino", "Hugo Díaz"),
        ("Montepino", "Isabel Jiménez")
    ]
    
    for pueblo, habitante in habitantes:
        sistema.agregar_habitante(pueblo, habitante)
    
    # Mostrar habitantes de cada pueblo
    for pueblo in pueblos_info:
        sistema.mostrar_habitantes_pueblo(pueblo[0])
    
    # Verificar cantidades
    sistema.verificar_cantidad_habitantes()
    
    # Buscar un habitante
    nombre_buscar = "Elena Torres"
    pueblo = sistema.buscar_habitante(nombre_buscar)
    if pueblo:
        print(f"\n{nombre_buscar} vive en {pueblo}")
    else:
        print(f"\n{nombre_buscar} no encontrado")

if __name__ == "__main__":
    main()

# Crear el sistema
pueblos_info = [
    ("Pueblo1", 100),
    ("Pueblo2", 150)
]
sistema = SistemaPueblos(pueblos_info)

# Agregar habitantes
sistema.agregar_habitante("Pueblo1", "Juan Pérez")
sistema.agregar_habitante("Pueblo1", "María López")

# Mostrar habitantes
sistema.mostrar_habitantes_pueblo("Pueblo1")

# Buscar habitante
pueblo = sistema.buscar_habitante("Juan Pérez")