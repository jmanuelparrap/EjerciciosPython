class Node:
    def __init__(self, id_empleado, origen, destino):
        self.id_empleado = id_empleado
        self.origen = origen
        self.destino = destino
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def rightRotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = max(self.getHeight(y.left), self.getHeight(y.right)) + 1
        x.height = max(self.getHeight(x.left), self.getHeight(x.right)) + 1
        return x

    def leftRotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = max(self.getHeight(x.left), self.getHeight(x.right)) + 1
        y.height = max(self.getHeight(y.left), self.getHeight(y.right)) + 1
        return y

    def insert(self, root, id_empleado, origen, destino):
        if not root:
            return Node(id_empleado, origen, destino)
        
        if id_empleado < root.id_empleado:
            root.left = self.insert(root.left, id_empleado, origen, destino)
        elif id_empleado > root.id_empleado:
            root.right = self.insert(root.right, id_empleado, origen, destino)
        else:
            return root

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        balance = self.getBalance(root)

        # Casos de rotación
        if balance > 1 and id_empleado < root.left.id_empleado:
            return self.rightRotate(root)
        if balance < -1 and id_empleado > root.right.id_empleado:
            return self.leftRotate(root)
        if balance > 1 and id_empleado > root.left.id_empleado:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and id_empleado < root.right.id_empleado:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delete(self, root, id_empleado):
        if not root:
            return root

        if id_empleado < root.id_empleado:
            root.left = self.delete(root.left, id_empleado)
        elif id_empleado > root.id_empleado:
            root.right = self.delete(root.right, id_empleado)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.id_empleado = temp.id_empleado
            root.origen = temp.origen
            root.destino = temp.destino
            root.right = self.delete(root.right, temp.id_empleado)

        if not root:
            return root

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        balance = self.getBalance(root)

        # Casos de rotación después de eliminar
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def getMinValueNode(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    def displayTree(self, root, level=0, prefix="Root: "):
        if root is not None:
            print("  " * level + prefix + f"{root.id_empleado} (Origen: {root.origen}, Destino: {root.destino})")
            if root.left:
                self.displayTree(root.left, level + 1, "L--- ")
            if root.right:
                self.displayTree(root.right, level + 1, "R--- ")

def procesar_transferencias(nombre_archivo):
    # Inicializar los tres árboles AVL (uno para cada departamento origen)
    avl_trees = {1: AVLTree(), 2: AVLTree(), 3: AVLTree()}
    roots = {1: None, 2: None, 3: None}
    
    # Leer el archivo y crear los árboles iniciales
    try:
        with open(nombre_archivo, 'r') as file:
            for line in file:
                id_emp, origen, destino = map(int, line.strip().split())
                roots[origen] = avl_trees[origen].insert(roots[origen], id_emp, origen, destino)
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no fue encontrado.")
        return
    
    print("\nÁrboles iniciales por departamento de origen:")
    for dept in [1, 2, 3]:
        print(f"\nDepartamento {dept}:")
        avl_trees[dept].displayTree(roots[dept])
    
    # Procesar transferencias
    new_roots = {1: None, 2: None, 3: None}
    
    for origen in [1, 2, 3]:
        def transfer_nodes(root):
            if not root:
                return
            transfer_nodes(root.left)
            transfer_nodes(root.right)
            new_roots[root.destino] = avl_trees[root.destino].insert(
                new_roots[root.destino], 
                root.id_empleado, 
                root.origen, 
                root.destino
            )
        
        transfer_nodes(roots[origen])
    
    print("\nÁrboles finales por departamento de destino:")
    for dept in [1, 2, 3]:
        print(f"\nDepartamento {dept}:")
        avl_trees[dept].displayTree(new_roots[dept])

# Ejemplo de uso
print("Sistema de Redistribución de Personal")
print("=====================================")

# Crear un archivo de ejemplo
ejemplo_datos = """12345 1 2
23456 1 3
34567 2 1
45678 2 3
56789 3 1
67890 3 2
14785 2 3 
21364 1 3
45662 2 1
56165 3 2
52125 3 1"""

with open('laboral.txt', 'w') as f:
    f.write(ejemplo_datos)

# Procesar las transferencias
procesar_transferencias('laboral.txt')