class TorreDeHanoi:
    def __init__(self, n_discos):
        """
        Constructor de la clase.
        - n_discos: cantidad de discos del rompecabezas.
        - movimientos: lista donde se almacenarán todos los pasos necesarios
                       para resolver la Torre de Hanoi.
        """
        self.n_discos = n_discos      # Guarda cuántos discos tiene el puzzle
        self.movimientos = []         # Lista donde se registran los movimientos

    # ------------------------------------------------------------
    # MÉTODO mover()
    # Este método implementa el algoritmo RECURSIVO clásico.
    # n         → cantidad de discos a mover
    # origen    → torre de donde salen los discos
    # destino   → torre a donde deben llegar
    # auxiliar  → torre de apoyo para realizar los movimientos
    #
    # La lógica:
    # - Si hay 1 disco, se mueve directamente de origen a destino.
    # - Si hay más de 1, se divide el problema en:
    #    1. Mover n-1 discos desde origen → auxiliar.
    #    2. Mover el disco más grande (el n) a destino.
    #    3. Mover los n-1 discos desde auxiliar → destino.
    #
    # Esto genera todos los pasos necesarios para resolver el puzzle.
    # ------------------------------------------------------------
    def mover(self, n, origen, destino, auxiliar):

        # Caso base: Solo hay 1 disco → movimiento directo
        if n == 1:
            self.movimientos.append((origen, destino))  # Guardamos el movimiento
        else:
            # Paso 1: Mover n-1 discos del origen al auxiliar
            self.mover(n - 1, origen, auxiliar, destino)

            # Paso 2: Mover el disco más grande al destino
            self.movimientos.append((origen, destino))

            # Paso 3: Mover los n-1 discos del auxiliar al destino
            self.mover(n - 1, auxiliar, destino, origen)

    # ------------------------------------------------------------
    # MÉTODO resolver()
    # Prepara la lista y llama al método recursivo para generar todos
    # los movimientos de la Torre de Hanoi.
    # Simula mover los discos desde la torre A hasta la torre C usando B.
    # ------------------------------------------------------------
    def resolver(self):
        self.movimientos = []  # Limpiamos cualquier resultado previo

        # Llamada inicial del algoritmo:
        # Mover todos los discos desde A → C usando B como torre auxiliar.
        self.mover(self.n_discos, "A", "C", "B")

        return self.movimientos  # Devolvemos la lista con los pasos
