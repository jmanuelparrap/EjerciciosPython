class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []  # Lista de claves (números de orden)
        self.names = []  # Lista de nombres de centros
        self.children = []  # Lista de hijos
        
class BTree:
    def __init__(self, t=2):  # t=2 significa máximo 4 claves por nodo
        self.root = BTreeNode()
        self.t = t  # Grado mínimo del árbol
        
    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        
        # Mover las claves y nombres
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
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            
            if len(x.children[i].keys) == (2 * self.t - 1):
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], k, name)
            
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
            
    def remove(self, k):
        result = self.search(k)
        if result is None:
            return False
        
        node, idx = result
        if node.leaf:
            node.keys.pop(idx)
            node.names.pop(idx)
        else:
            # Implementación de eliminación para nodos internos
            pred = self._get_pred(node, idx)
            node.keys[idx] = pred[0]
            node.names[idx] = pred[1]
            self._remove_pred(node.children[idx], pred[0])
        return True
    
    def _get_pred(self, node, idx):
        current = node.children[idx]
        while not current.leaf:
            current = current.children[-1]
        return (current.keys[-1], current.names[-1])
    
    def _remove_pred(self, node, k):
        i = len(node.keys) - 1
        while i >= 0 and k < node.keys[i]:
            i -= 1
        if node.leaf:
            node.keys.pop(i)
            node.names.pop(i)
        else:
            self._remove_pred(node.children[i+1], k)
            
    def display(self, x=None, level=0):
        if x is None:
            x = self.root
        print("  " * level + f"Nivel {level}:", end=" ")
        for i in range(len(x.keys)):
            print(f"({x.keys[i]}: {x.names[i]})", end=" ")
        print()
        
        if not x.leaf:
            for child in x.children:
                self.display(child, level + 1)

def validate_school_number(num):
    return 1 <= num <= 50000  # Asumiendo 50 provincias máximo

def main():
    btree = BTree()
    
    while True:
        print("\nGestión de Centros Educativos")
        print("1. Añadir centro")
        print("2. Eliminar centro")
        print("3. Buscar centro")
        print("4. Listar centros")
        print("5. Salir")
        
        option = input("\nSeleccione una opción: ")
        
        if option == "1":
            num = int(input("Número de orden del centro (1-50000): "))
            if not validate_school_number(num):
                print("Número de centro no válido")
                continue
            name = input("Nombre del centro: ")
            btree.insert(num, name)
            print("Centro añadido correctamente")
            
        elif option == "2":
            num = int(input("Número de orden del centro a eliminar: "))
            if btree.remove(num):
                print("Centro eliminado correctamente")
            else:
                print("Centro no encontrado")
                
        elif option == "3":
            num = int(input("Número de orden del centro a buscar: "))
            result = btree.search(num)
            if result:
                node, idx = result
                print(f"Centro encontrado: {node.names[idx]}")
            else:
                print("Centro no encontrado")
                
        elif option == "4":
            print("\nListado de centros:")
            btree.display()
            
        elif option == "5":
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()