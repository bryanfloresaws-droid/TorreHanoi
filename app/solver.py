from app.hanoi import TorreDeHanoi   # Importamos la clase que contiene la lógica del algoritmo recursivo

# -------------------------------------------------------------
# FUNCIÓN: generar_pasos(n_discos)
# Esta función recibe un número de discos y genera una lista
# detallada de todos los movimientos necesarios para resolver
# la Torre de Hanoi usando la clase TorreDeHanoi.
# -------------------------------------------------------------
def generar_pasos(n_discos):

    # ---------------------------------------------------------
    # Se crea una instancia del solucionador con el número de discos.
    # TorreDeHanoi(n) ya contiene el algoritmo para resolver el puzzle.
    # ---------------------------------------------------------
    hanoi = TorreDeHanoi(n_discos)

    # Ejecutamos el algoritmo y obtenemos la lista de movimientos.
    # Cada movimiento normalmente es una tupla con formato:
    #   (poste_origen, poste_destino)
    # ---------------------------------------------------------
    movimientos = hanoi.resolver()

    # Lista donde guardaremos todos los pasos con formato más amigable
    pasos = []

    # Contador de pasos (1, 2, 3, 4, ...)
    paso_num = 1

    # ---------------------------------------------------------
    # Convertimos cada movimiento en un diccionario estructurado
    # para que sea más fácil de consumir por una API, frontend
    # o para mostrarlo paso a paso en pantalla.
    # ---------------------------------------------------------
    for mov in movimientos:
        pasos.append({
            "paso": paso_num,   # Número de paso actual
            "origen": mov[0],   # Poste de origen del movimiento
            "destino": mov[1]   # Poste de destino
        })

        paso_num += 1  # Avanza al siguiente paso

    # Retornamos la lista completa con todos los movimientos
    return pasos
