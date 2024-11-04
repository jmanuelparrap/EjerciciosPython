def calcular_orden_optimo(tamano_bloque, tamano_clave, tamano_puntero):
    """
    Calcula el orden óptimo del árbol B basado en el tamaño del bloque de disco
    
    Parámetros:
    tamano_bloque: Tamaño del bloque en bytes
    tamano_clave: Tamaño de cada clave en bytes
    tamano_puntero: Tamaño de cada puntero en bytes
    """
    # En un nodo de orden m tenemos:
    # - m-1 claves
    # - m punteros
    # Todo debe caber en un bloque
    
    # Ecuación: (m-1)*tamano_clave + m*tamano_puntero <= tamano_bloque
    # Despejando m:
    m = (tamano_bloque + tamano_clave) // (tamano_clave + tamano_puntero)
    return m

def calcular_altura_maxima(n, orden):
    """
    Calcula la altura máxima de un árbol B con n elementos y orden m
    
    Parámetros:
    n: Número total de elementos
    orden: Orden del árbol B
    """
    # Número mínimo de claves por nodo (excepto raíz)
    min_claves = (orden - 1) // 2
    
    # Capacidad mínima por nivel
    capacidad = 1
    altura = 0
    
    # Mientras no podamos almacenar todos los elementos
    while capacidad < n:
        if altura == 0:
            # Nivel raíz
            capacidad *= orden - 1
        else:
            # Otros niveles, considerando ocupación mínima
            capacidad *= min_claves
        altura += 1
    
    return altura

def analizar_accesos_disco(tamano_bloque=4096,  # 4KB por bloque
                          tamano_clave=8,        # 8 bytes por clave
                          tamano_puntero=8,      # 8 bytes por puntero
                          n_elementos=1000000):   # 1 millón de elementos
    """
    Análisis completo de accesos a disco para un árbol B
    """
    # 1. Calcular el orden óptimo
    orden = calcular_orden_optimo(tamano_bloque, tamano_clave, tamano_puntero)
    
    # 2. Calcular altura máxima
    altura = calcular_altura_maxima(n_elementos, orden)
    
    # 3. Número máximo de accesos = altura + 1 (un acceso por nivel)
    max_accesos = altura + 1
    
    return {
        'orden_optimo': orden,
        'altura_arbol': altura,
        'max_accesos_disco': max_accesos,
        'tamano_nodo': (orden-1)*tamano_clave + orden*tamano_puntero,
        'claves_por_nodo': orden-1,
        'factor_ramificacion': orden
    }

# Ejemplo de uso
resultados = analizar_accesos_disco()
for key, value in resultados.items():
    print(f"{key}: {value}")