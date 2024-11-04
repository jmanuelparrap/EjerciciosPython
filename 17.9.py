class NodoAVL:
    def __init__(self, nombre):
        self.nombre = nombre
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class Pueblo:
    def __init__(self, nombre, num_habitantes):
        self.nombre = nombre
        self.num_habitantes = num_habitantes
        self.arbol_habitantes = None
        
    def __str__(self):
        return f"Pueblo: {self.nombre}, Habitantes: {self.num_habitantes}"

class SistemaPueblos:
    def __init__(self, pueblos_info):
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
        if not nodo:
            return NodoAVL(nombre)
        if nombre < nodo.nombre:
            nodo.izquierda = self._insertar_avl(nodo.izquierda, nombre)
        elif nombre > nodo.nombre:
            nodo.derecha = self._insertar_avl(nodo.derecha, nombre)
        else:
            return nodo

        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)

        if balance > 1 and nombre < nodo.izquierda.nombre:
            return self._rotacion_derecha(nodo)
        if balance < -1 and nombre > nodo.derecha.nombre:
            return self._rotacion_izquierda(nodo)
        if balance > 1 and nombre > nodo.izquierda.nombre:
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)
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
                # Verificar si el habitante ya existe en algún pueblo
                if self.buscar_habitante(nombre_habitante):
                    return False
                pueblo.arbol_habitantes = self._insertar_avl(
                    pueblo.arbol_habitantes, nombre_habitante)
                return True
        return False

    def _eliminar_nodo(self, nodo, nombre):
        if not nodo:
            return nodo

        if nombre < nodo.nombre:
            nodo.izquierda = self._eliminar_nodo(nodo.izquierda, nombre)
        elif nombre > nodo.nombre:
            nodo.derecha = self._eliminar_nodo(nodo.derecha, nombre)
        else:
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda

            sucesor = self._obtener_minimo(nodo.derecha)
            nodo.nombre = sucesor.nombre
            nodo.derecha = self._eliminar_nodo(nodo.derecha, sucesor.nombre)

        self._actualizar_altura(nodo)
        balance = self._factor_balance(nodo)

        if balance > 1 and self._factor_balance(nodo.izquierda) >= 0:
            return self._rotacion_derecha(nodo)
        if balance > 1 and self._factor_balance(nodo.izquierda) < 0:
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)
        if balance < -1 and self._factor_balance(nodo.derecha) <= 0:
            return self._rotacion_izquierda(nodo)
        if balance < -1 and self._factor_balance(nodo.derecha) > 0:
            nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)

        return nodo

    def _obtener_minimo(self, nodo):
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual

    def _obtener_habitantes_lista(self, nodo, habitantes):
        if not nodo:
            return
        self._obtener_habitantes_lista(nodo.izquierda, habitantes)
        habitantes.append(nodo.nombre)
        self._obtener_habitantes_lista(nodo.derecha, habitantes)

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

    def cambiar_nombre_habitante(self, nombre_pueblo, nombre_actual, nuevo_nombre):
        """
        Cambia el nombre de un habitante manteniendo la estructura AVL
        """
        for pueblo in self.pueblos:
            if pueblo.nombre == nombre_pueblo:
                # Verificar si existe el nuevo nombre
                if self.buscar_habitante(nuevo_nombre):
                    return False, "El nuevo nombre ya existe en algún pueblo"
                
                # Eliminar el nombre actual
                pueblo.arbol_habitantes = self._eliminar_nodo(pueblo.arbol_habitantes, nombre_actual)
                # Insertar el nuevo nombre
                pueblo.arbol_habitantes = self._insertar_avl(pueblo.arbol_habitantes, nuevo_nombre)
                return True, "Nombre cambiado exitosamente"
        return False, "Pueblo no encontrado"

    def fusionar_pueblos(self, pueblo_origen, pueblo_destino):
        """
        Fusiona dos pueblos, moviendo todos los habitantes del pueblo origen al destino
        """
        pueblo_orig = None
        pueblo_dest = None
        
        # Encontrar los pueblos
        for pueblo in self.pueblos:
            if pueblo.nombre == pueblo_origen:
                pueblo_orig = pueblo
            elif pueblo.nombre == pueblo_destino:
                pueblo_dest = pueblo
        
        if not pueblo_orig or not pueblo_dest:
            return False, "Uno o ambos pueblos no existen"
        
        # Obtener lista de habitantes del pueblo origen
        habitantes = []
        self._obtener_habitantes_lista(pueblo_orig.arbol_habitantes, habitantes)
        
        # Añadir habitantes al pueblo destino
        for habitante in habitantes:
            pueblo_dest.arbol_habitantes = self._insertar_avl(
                pueblo_dest.arbol_habitantes, habitante)
        
        # Actualizar número de habitantes
        pueblo_dest.num_habitantes += pueblo_orig.num_habitantes
        
        # Eliminar pueblo origen de la lista de pueblos
        self.pueblos.remove(pueblo_orig)
        
        return True, f"Fusión completada. {len(habitantes)} habitantes transferidos"

    def guardar_en_archivo(self, nombre_archivo):
        """
        Guarda la información de todos los pueblos y sus habitantes en un archivo
        """
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                for pueblo in self.pueblos:
                    f.write(f"### Pueblo: {pueblo.nombre} ###\n")
                    f.write(f"Número de habitantes: {pueblo.num_habitantes}\n")
                    f.write("Habitantes:\n")
                    
                    habitantes = []
                    self._obtener_habitantes_lista(pueblo.arbol_habitantes, habitantes)
                    for habitante in sorted(habitantes):
                        f.write(f"- {habitante}\n")
                    f.write("\n")
            return True, f"Datos guardados exitosamente en {nombre_archivo}"
        except Exception as e:
            return False, f"Error al guardar el archivo: {str(e)}"

# Ejemplo de uso
def main():
    # Crear el sistema con información inicial
    pueblos_info = [
        ("Peñablanca", 3),
        ("Rocaalta", 4)
    ]
    
    sistema = SistemaPueblos(pueblos_info)
    
    # Agregar algunos habitantes
    habitantes = [
        ("Peñablanca", "Ana García"),
        ("Peñablanca", "Carlos Ruiz"),
        ("Peñablanca", "Beatriz López"),
        ("Rocaalta", "David Martín"),
        ("Rocaalta", "Elena Torres")
    ]
    
    for pueblo, habitante in habitantes:
        sistema.agregar_habitante(pueblo, habitante)
    
    # Probar cambio de nombre
    exito, mensaje = sistema.cambiar_nombre_habitante("Peñablanca", "Ana García", "Ana Martínez")
    print(f"\nCambio de nombre: {mensaje}")
    
    # Probar fusión de pueblos
    exito, mensaje = sistema.fusionar_pueblos("Peñablanca", "Rocaalta")
    print(f"\nFusión de pueblos: {mensaje}")
    
    # Guardar en archivo
    exito, mensaje = sistema.guardar_en_archivo("pueblos_registro.txt")
    print(f"\nGuardado de datos: {mensaje}")

if __name__ == "__main__":
    main()