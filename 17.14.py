class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []  # Lista de claves (números de orden)
        self.names = []  # Lista de nombres de centros
        self.children = []  # Lista de hijos
        
    def to_dict(self):
        """Convierte el nodo a un diccionario para serialización"""
        return {
            'leaf': self.leaf,
            'keys': self.keys,
            'names': self.names,
            'children': [child.to_dict() if child else None for child in self.children]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un nodo a partir de un diccionario"""
        node = cls(leaf=data['leaf'])
        node.keys = data['keys']
        node.names = data['names']
        node.children = [cls.from_dict(child) if child else None for child in data['children']]
        return node

class BTree:
    def __init__(self, t=2):  # t=2 significa máximo 4 claves por nodo
        self.root = BTreeNode()
        self.t = t  # Grado mínimo del árbol
        
    def to_dict(self):
        """Convierte el árbol completo a un diccionario"""
        return {
            't': self.t,
            'root': self.root.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un árbol a partir de un diccionario"""
        tree = cls(t=data['t'])
        tree.root = BTreeNode.from_dict(data['root'])
        return tree
        
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

import json
import os

def save_btree(btree, filename='centros.txt'):
    """Guarda el árbol B en un archivo"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(btree.to_dict(), f, ensure_ascii=False, indent=2)
    print(f"Árbol guardado en {filename}")

def load_btree(filename='centros.txt'):
    """Carga el árbol B desde un archivo"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return BTree.from_dict(data)
    except FileNotFoundError:
        print(f"No se encontró el archivo {filename}. Creando nuevo árbol...")
        return BTree()
    except json.JSONDecodeError:
        print(f"Error al leer el archivo {filename}. Creando nuevo árbol...")
        return BTree()

def validate_school_number(num):
    return 1 <= num <= 50000

def main():
    # Cargar el árbol desde el archivo al inicio
    btree = load_btree()
    
    while True:
        print("\nGestión de Centros Educativos")
        print("1. Añadir centro")
        print("2. Eliminar centro")
        print("3. Buscar centro")
        print("4. Listar centros")
        print("5. Guardar y salir")
        
        option = input("\nSeleccione una opción: ")
        
        if option == "1":
            try:
                num = int(input("Número de orden del centro (1-50000): "))
                if not validate_school_number(num):
                    print("Número de centro no válido")
                    continue
                name = input("Nombre del centro: ")
                btree.insert(num, name)
                print("Centro añadido correctamente")
            except ValueError:
                print("Por favor, introduzca un número válido")
                
        elif option == "2":
            try:
                num = int(input("Número de orden del centro a eliminar: "))
                if btree.remove(num):
                    print("Centro eliminado correctamente")
                else:
                    print("Centro no encontrado")
            except ValueError:
                print("Por favor, introduzca un número válido")
                
        elif option == "3":
            try:
                num = int(input("Número de orden del centro a buscar: "))
                result = btree.search(num)
                if result:
                    node, idx = result
                    print(f"Centro encontrado: {node.names[idx]}")
                else:
                    print("Centro no encontrado")
            except ValueError:
                print("Por favor, introduzca un número válido")
                
        elif option == "4":
            print("\nListado de centros:")
            btree.display()
            
        elif option == "5":
            # Guardar el árbol en el archivo antes de salir
            save_btree(btree)
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()