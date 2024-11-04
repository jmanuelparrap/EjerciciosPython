import json
from datetime import datetime

class LibraryBook:
    def __init__(self, title, author, year, isbn, copies=1):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.copies = copies
        
class BSTNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None
        
    def to_dict(self):
        """Convierte el nodo BST a diccionario"""
        return {
            'book': {
                'title': self.book.title,
                'author': self.book.author,
                'year': self.book.year,
                'isbn': self.book.isbn,
                'copies': self.book.copies
            },
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un nodo BST desde un diccionario"""
        if data is None:
            return None
        book = LibraryBook(
            data['book']['title'],
            data['book']['author'],
            data['book']['year'],
            data['book']['isbn'],
            data['book']['copies']
        )
        node = cls(book)
        node.left = cls.from_dict(data['left'])
        node.right = cls.from_dict(data['right'])
        return node

class BST:
    def __init__(self):
        self.root = None
        
    def insert(self, book):
        if not self.root:
            self.root = BSTNode(book)
        else:
            self._insert_recursive(self.root, book)
            
    def _insert_recursive(self, node, book):
        if book.title < node.book.title:
            if node.left is None:
                node.left = BSTNode(book)
            else:
                self._insert_recursive(node.left, book)
        else:
            if node.right is None:
                node.right = BSTNode(book)
            else:
                self._insert_recursive(node.right, book)
                
    def search(self, title):
        return self._search_recursive(self.root, title)
    
    def _search_recursive(self, node, title):
        if node is None or node.book.title == title:
            return node
        if title < node.book.title:
            return self._search_recursive(node.left, title)
        return self._search_recursive(node.right, title)
    
    def to_dict(self):
        """Convierte el BST completo a diccionario"""
        return {
            'root': self.root.to_dict() if self.root else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un BST desde un diccionario"""
        bst = cls()
        if data and data['root']:
            bst.root = BSTNode.from_dict(data['root'])
        return bst

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []  # números de orden
        self.names = []  # nombres de centros
        self.libraries = []  # árboles BST de bibliotecas
        self.children = []
        
    def to_dict(self):
        return {
            'leaf': self.leaf,
            'keys': self.keys,
            'names': self.names,
            'libraries': [lib.to_dict() for lib in self.libraries],
            'children': [child.to_dict() if child else None for child in self.children]
        }
    
    @classmethod
    def from_dict(cls, data):
        node = cls(leaf=data['leaf'])
        node.keys = data['keys']
        node.names = data['names']
        node.libraries = [BST.from_dict(lib) for lib in data['libraries']]
        node.children = [cls.from_dict(child) if child else None for child in data['children']]
        return node

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
            self._insert_non_full(new_root, k, name, BST())
        else:
            self._insert_non_full(root, k, name, BST())
            
    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        
        x.keys.insert(i, y.keys[t-1])
        x.names.insert(i, y.names[t-1])
        x.libraries.insert(i, y.libraries[t-1])
        x.children.insert(i+1, z)
        
        z.keys = y.keys[t:]
        z.names = y.names[t:]
        z.libraries = y.libraries[t:]
        y.keys = y.keys[:t-1]
        y.names = y.names[:t-1]
        y.libraries = y.libraries[:t-1]
        
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]
            
    def _insert_non_full(self, x, k, name, library):
        i = len(x.keys) - 1
        if x.leaf:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            x.keys.insert(i, k)
            x.names.insert(i, name)
            x.libraries.insert(i, library)
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t - 1):
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k, name, library)
            
    def search(self, k):
        return self._search_recursive(self.root, k)
    
    def _search_recursive(self, x, k):
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            return (x, i)
        elif x.leaf:
            return None
        else:
            return self._search_recursive(x.children[i], k)
    
    def add_book_to_center(self, center_id, book):
        result = self.search(center_id)
        if result:
            node, idx = result
            node.libraries[idx].insert(book)
            return True
        return False
    
    def display(self, x=None, level=0, show_books=False):
        if x is None:
            x = self.root
        print("  " * level + f"Nivel {level}:", end=" ")
        for i in range(len(x.keys)):
            print(f"({x.keys[i]}: {x.names[i]})", end=" ")
            if show_books:
                print("\nLibros:", end=" ")
                self._display_books(x.libraries[i].root)
        print()
        if not x.leaf:
            for child in x.children:
                self.display(child, level + 1, show_books)
                
    def _display_books(self, node):
        if node:
            self._display_books(node.left)
            print(f"[{node.book.title}]", end=" ")
            self._display_books(node.right)

def main():
    btree = BTree()
    
    while True:
        print("\nGestión de Centros Educativos y Bibliotecas")
        print("1. Añadir centro")
        print("2. Añadir libro a centro")
        print("3. Buscar centro")
        print("4. Buscar libro en centro")
        print("5. Listar centros")
        print("6. Listar centros con libros")
        print("7. Guardar y salir")
        
        option = input("\nSeleccione una opción: ")
        
        if option == "1":
            try:
                num = int(input("Número de orden del centro (1-50000): "))
                name = input("Nombre del centro: ")
                btree.insert(num, name)
                print("Centro añadido correctamente")
            except ValueError:
                print("Error: Ingrese un número válido")
                
        elif option == "2":
            try:
                center_id = int(input("Número de orden del centro: "))
                title = input("Título del libro: ")
                author = input("Autor: ")
                year = int(input("Año de publicación: "))
                isbn = input("ISBN: ")
                copies = int(input("Número de copias: "))
                
                book = LibraryBook(title, author, year, isbn, copies)
                if btree.add_book_to_center(center_id, book):
                    print("Libro añadido correctamente")
                else:
                    print("Centro no encontrado")
            except ValueError:
                print("Error: Datos inválidos")
                
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
                print("Error: Ingrese un número válido")
                
        elif option == "4":
            try:
                center_id = int(input("Número de orden del centro: "))
                title = input("Título del libro a buscar: ")
                result = btree.search(center_id)
                if result:
                    node, idx = result
                    book_node = node.libraries[idx].search(title)
                    if book_node:
                        book = book_node.book
                        print(f"\nLibro encontrado:")
                        print(f"Título: {book.title}")
                        print(f"Autor: {book.author}")
                        print(f"Año: {book.year}")
                        print(f"ISBN: {book.isbn}")
                        print(f"Copias: {book.copies}")
                    else:
                        print("Libro no encontrado en este centro")
                else:
                    print("Centro no encontrado")
            except ValueError:
                print("Error: Datos inválidos")
                
        elif option == "5":
            print("\nListado de centros:")
            btree.display()
            
        elif option == "6":
            print("\nListado de centros y sus libros:")
            btree.display(show_books=True)
            
        elif option == "7":
            # Aquí se implementaría la persistencia
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción no válida")

if __name__ == "__main__":
    main()