class Book:
    def __init__(self, isbn, title):
        self.isbn = isbn
        self.title = title

class Library:
    def __init__(self):
        self.books = {}  # isbn -> (título, cantidad)

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []  # Lista de claves (números de orden)
        self.names = []  # Lista de nombres de centros
        self.books = {}  # Diccionario de libros por cada centro
        self.children = []  # Lista de hijos

class BTree:
    def __init__(self, t=2):
        self.root = BTreeNode()
        self.t = t

    def insert(self, k, name):
        root = self.root
        if len(root.keys) == (2 * self.t - 1):
            new_root = BTreeNode(leaf=False)
            self.root = new_root
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.insert_non_full(new_root, k, name)
        else:
            self.insert_non_full(root, k, name)

    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        
        x.keys.insert(i, y.keys[t-1])
        x.names.insert(i, y.names[t-1])
        x.children.insert(i+1, z)
        
        z.keys = y.keys[t:]
        z.names = y.names[t:]
        y.keys = y.keys[:t-1]
        y.names = y.names[:t-1]
        
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

    def insert_non_full(self, x, k, name):
        i = len(x.keys) - 1
        if x.leaf:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            x.keys.insert(i, k)
            x.names.insert(i, name)
            x.books[k] = {}  # Inicializar diccionario de libros para este centro
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t - 1):
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], k, name)

    def search(self, k, x=None):
        if x is None:
            x = self.root
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            return (x, i)
        elif x.leaf:
            return None
        else:
            return self.search(k, x.children[i])

    def eliminar_libro(self, center_id, isbn):
        """Elimina un libro específico de un centro dado por su ID."""
        result = self.search(center_id)
        if not result:
            return False, "Centro no encontrado"
        
        node, idx = result
        if isbn in node.books.get(center_id, {}):
            del node.books[center_id][isbn]
            return True, f"Libro con ISBN {isbn} eliminado del centro {center_id}"
        else:
            return False, "Libro no encontrado en el centro especificado"

    def eliminar_centro(self, center_id):
        """Elimina un centro del árbol B completamente."""
        result = self.search(center_id)
        if not result:
            return False, "Centro no encontrado"
        
        node, idx = result
        node.keys.pop(idx)
        node.names.pop(idx)
        if center_id in node.books:
            del node.books[center_id]
        if node.leaf:
            return True, f"Centro con ID {center_id} eliminado exitosamente"
        else:
            return False, "Eliminación de centros en nodos no hoja no está implementada"

    def eliminar_libros_por_rango(self, start_id, end_id):
        """Elimina libros duplicados en un rango de IDs de centros y devuelve el total de ejemplares liberados."""
        total_freed = 0
        
        def process_node(node):
            nonlocal total_freed
            for i, key in enumerate(node.keys):
                if start_id <= key <= end_id:
                    books = node.books.get(key, {})
                    for isbn in books:
                        if books[isbn]['quantity'] > 1:
                            total_freed += books[isbn]['quantity'] - 1
                            books[isbn]['quantity'] = 1
            
            if not node.leaf:
                for child in node.children:
                    process_node(child)
        
        process_node(self.root)
        return total_freed

    def set_book_quantity(self, center_id, isbn, title, quantity):
        """Establece la cantidad de un libro en un centro específico"""
        result = self.search(center_id)
        if not result:
            return False, "Centro no encontrado"
        
        node, idx = result
        if center_id not in node.books:
            node.books[center_id] = {}
        
        old_quantity = node.books[center_id].get(isbn, {}).get('quantity', 0)
        node.books[center_id][isbn] = {'title': title, 'quantity': quantity}
        
        if old_quantity < quantity:
            return True, f"Se han añadido {quantity - old_quantity} ejemplares"
        elif old_quantity > quantity:
            return True, f"Se han eliminado {old_quantity - quantity} ejemplares"
        else:
            return True, "La cantidad no ha cambiado"

    def listar_centros_y_libros(self):
        """Lista todos los centros y sus libros"""
        def process_node(node):
            for i, key in enumerate(node.keys):
                print(f"Centro ID: {key}, Nombre: {node.names[i]}")
                if key in node.books and node.books[key]:
                    print("  Libros en el centro:")
                    for isbn, info in node.books[key].items():
                        print(f"    - ISBN: {isbn}, Título: {info['title']}, Cantidad: {info['quantity']}")
                else:
                    print("  No hay libros registrados en este centro.")
            if not node.leaf:
                for child in node.children:
                    process_node(child)
        
        process_node(self.root)

def main():
    tree = BTree()
    
    while True:
        print("\nGestión de Centros Educativos")
        print("1. Añadir centro")
        print("2. Buscar centro")
        print("3. Añadir/Modificar libros")
        print("4. Eliminar libro específico en un centro")
        print("5. Eliminar un centro")
        print("6. Eliminar duplicados de libros en un rango de centros")
        print("7. Listar centros y libros")
        print("8. Salir")
        
        try:
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                id_centro = int(input("ID del centro: "))
                nombre = input("Nombre del centro: ")
                tree.insert(id_centro, nombre)
                print("Centro añadido exitosamente")
                
            elif opcion == "2":
                id_centro = int(input("ID del centro a buscar: "))
                result = tree.search(id_centro)
                if result:
                    node, idx = result
                    print(f"Centro encontrado: {node.names[idx]}")
                    if id_centro in node.books and node.books[id_centro]:
                        print("Libros en el centro:")
                        for isbn, info in node.books[id_centro].items():
                            print(f"- {info['title']}: {info['quantity']} ejemplares")
                    else:
                        print("No hay libros registrados en este centro")
                else:
                    print("Centro no encontrado")
                    
            elif opcion == "3":
                id_centro = int(input("ID del centro: "))
                isbn = input("ISBN del libro: ")
                titulo = input("Título del libro: ")
                cantidad = int(input("Cantidad de ejemplares: "))
                success, msg = tree.set_book_quantity(id_centro, isbn, titulo, cantidad)
                print(msg)
                
            elif opcion == "4":
                id_centro = int(input("ID del centro: "))
                isbn = input("ISBN del libro a eliminar: ")
                success, msg = tree.eliminar_libro(id_centro, isbn)
                print(msg)
                
            elif opcion == "5":
                id_centro = int(input("ID del centro a eliminar: "))
                success, msg = tree.eliminar_centro(id_centro)
                print(msg)
            
            elif opcion == "6":
                start = int(input("ID inicial del rango: "))
                end = int(input("ID final del rango: "))
                freed = tree.eliminar_libros_por_rango(start, end)
                print(f"Se han liberado {freed} ejemplares duplicados")
            
            elif opcion == "7":
                print("Listado de centros y sus libros:")
                tree.listar_centros_y_libros()
                
            elif opcion == "8":
                print("¡Hasta luego!")
                break
                
            else:
                print("Opción no válida")
                
        except ValueError:
            print("Error: Ingrese un valor numérico válido donde corresponda")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()