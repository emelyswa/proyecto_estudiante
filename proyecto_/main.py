from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar
)

from views import ClienteController, EstudianteController


# ============================================================
# MENU DE CLIENTES
# ============================================================

class MenuClientes:

    TITULO = "SISTEMA DE GESTIÓN DE CLIENTES"
    ENTIDAD = "cliente"
    ENTIDADES = "clientes"
    TEXTO_BUSQUEDA = (
        "Nombre, apellido, email, teléfono o ciudad"
    )
    ANCHO = 85

    def __init__(self):
        self.__controlador = ClienteController()

        self.__opciones = {
            1: ("Crear usuario", self.crear),
            2: ("Ver todos", self.listar),
            3: ("Buscar", self.buscar),
            4: ("Ver por ID", self.ver_por_id),
            5: ("Actualizar", self.actualizar),
            6: ("Eliminar", self.eliminar),
            7: ("Estadísticas", self.estadisticas),
            0: ("Salir", self.salir)
        }

    @property
    def controlador(self):
        return self.__controlador

    def agregar_opcion(self, numero, texto, metodo):
        self.__opciones[numero] = (texto, metodo)

    @staticmethod
    def pausa():
        input("\nPresione ENTER para continuar...")

    @staticmethod
    def pedir_entero(mensaje):
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                imprimir_error(
                    "Debe ingresar un número entero."
                )

    def mostrar_resultado(self, resultado):

        if isinstance(resultado, tuple):

            exito, mensaje = resultado

            if exito:
                imprimir_exito(mensaje)
            else:
                imprimir_error(mensaje)

            return exito

        imprimir_info(str(resultado))
        return True

    # --------------------------------------------------------
    # TABLA CLIENTES
    # --------------------------------------------------------

    def mostrar_tabla(self, clientes):

        print(
            f"{'ID':<5}"
            f"{'NOMBRE':<18}"
            f"{'APELLIDO':<18}"
            f"{'EMAIL':<30}"
            f"{'TELÉFONO':<15}"
            f"{'CIUDAD':<15}"
        )

        print("-" * self.ANCHO)

        for cliente in clientes:

            print(
                f"{cliente.id:<5}"
                f"{cliente.nombre:<18}"
                f"{cliente.apellido:<18}"
                f"{cliente.email:<30}"
                f"{cliente.telefono:<15}"
                f"{cliente.ciudad:<15}"
            )

        print("-" * self.ANCHO)

        imprimir_info(
            f"Total: {len(clientes)} {self.ENTIDADES}"
        )

    # --------------------------------------------------------
    # CREAR
    # --------------------------------------------------------

    def crear(self):

        imprimir_titulo(
            f"CREAR {self.ENTIDAD.upper()}"
        )

        datos = {}

        for campo in self.controlador.MODELO.CAMPOS:

            datos[campo] = input(
                f"{campo.capitalize()}: "
            ).strip()

        resultado = self.controlador.crear(
            datos
        )

        self.mostrar_resultado(resultado)
        self.pausa()

    # --------------------------------------------------------
    # LISTAR
    # --------------------------------------------------------

    def listar(self):

        imprimir_titulo(
            f"LISTA DE {self.ENTIDADES.upper()}"
        )

        registros = self.controlador.listar()

        if not registros:
            imprimir_info(
                f"No hay {self.ENTIDADES} registrados."
            )
        else:
            self.mostrar_tabla(registros)

        self.pausa()

    # --------------------------------------------------------
    # BUSCAR
    # --------------------------------------------------------

    def buscar(self):

        imprimir_titulo(
            f"BUSCAR {self.ENTIDAD.upper()}"
        )

        texto = input(
            f"{self.TEXTO_BUSQUEDA}: "
        ).strip()

        resultados = self.controlador.buscar(
            texto
        )

        if not resultados:
            imprimir_info(
                f"No se encontraron {self.ENTIDADES}."
            )
        else:
            self.mostrar_tabla(resultados)

        self.pausa()

    # --------------------------------------------------------
    # VER POR ID
    # --------------------------------------------------------

    def ver_por_id(self):

        imprimir_titulo(
            f"VER {self.ENTIDAD.upper()} POR ID"
        )

        id_registro = self.pedir_entero(
            "ID: "
        )

        registro = self.controlador.obtener(
            id_registro
        )

        if not registro:

            imprimir_error(
                f"No existe un {self.ENTIDAD} con ese ID."
            )

        else:

            print(f"ID: {registro.id}")
            print(f"Nombre: {registro.nombre}")
            print(f"Apellido: {registro.apellido}")
            print(f"Email: {registro.email}")
            print(f"Teléfono: {registro.telefono}")
            print(f"Ciudad: {registro.ciudad}")
            print(f"Dirección: {registro.direccion}")

        self.pausa()

    # --------------------------------------------------------
    # ACTUALIZAR
    # --------------------------------------------------------

    def actualizar(self):

        imprimir_titulo(
            f"ACTUALIZAR {self.ENTIDAD.upper()}"
        )

        id_registro = self.pedir_entero(
            "ID: "
        )

        registro = self.controlador.obtener(
            id_registro
        )

        if not registro:

            imprimir_error(
                f"No existe un {self.ENTIDAD} con ese ID."
            )

            self.pausa()
            return

        print(
            "\nDeje vacío un campo si no desea modificarlo."
        )

        cambios = {}

        for campo in self.controlador.MODELO.CAMPOS:

            valor = input(
                f"{campo.capitalize()} "
                f"[{getattr(registro, campo)}]: "
            ).strip()

            if valor:
                cambios[campo] = valor

        if not cambios:

            imprimir_info(
                "No se realizaron cambios."
            )

            self.pausa()
            return

        resultado = self.controlador.actualizar(
            id_registro,
            cambios
        )

        self.mostrar_resultado(resultado)
        self.pausa()

    # --------------------------------------------------------
    # ELIMINAR
    # --------------------------------------------------------

    def eliminar(self):

        imprimir_titulo(
            f"ELIMINAR {self.ENTIDAD.upper()}"
        )

        id_registro = self.pedir_entero(
            "ID: "
        )

        registro = self.controlador.obtener(
            id_registro
        )

        if not registro:

            imprimir_error(
                f"No existe un {self.ENTIDAD} con ese ID."
            )

            self.pausa()
            return

        print(
            f"Se eliminará: "
            f"{registro.nombre} {registro.apellido}"
        )

        if not confirmar(
            "¿Está seguro de eliminarlo?"
        ):

            imprimir_info(
                "Operación cancelada."
            )

            self.pausa()
            return

        resultado = self.controlador.eliminar(
            id_registro
        )

        self.mostrar_resultado(resultado)
        self.pausa()

    # --------------------------------------------------------
    # ESTADÍSTICAS
    # --------------------------------------------------------

    def estadisticas(self):

        imprimir_titulo(
            f"ESTADÍSTICAS DE {self.ENTIDADES.upper()}"
        )

        datos = self.controlador.estadisticas()

        for clave, valor in datos.items():
            print(f"{clave}: {valor}")

        self.pausa()

    # --------------------------------------------------------
    # SALIR
    # --------------------------------------------------------

    def salir(self):

        imprimir_info(
            f"Saliendo del menú de {self.ENTIDADES}..."
        )

    # --------------------------------------------------------
    # MENÚ
    # --------------------------------------------------------

    def mostrar_menu(self):

        imprimir_titulo(self.TITULO)

        for numero, (texto, _) in self.__opciones.items():
            print(f"{numero}. {texto}")

    def ejecutar(self):

        while True:

            self.mostrar_menu()

            opcion = self.pedir_entero(
                "\nSeleccione una opción: "
            )

            if opcion not in self.__opciones:

                imprimir_error(
                    "Opción no válida."
                )

                self.pausa()
                continue

            metodo = self.__opciones[opcion][1]

            if opcion == 0:

                metodo()
                break

            metodo()


# ============================================================
# MENU DE ESTUDIANTES
# ============================================================

class MenuEstudiantes(MenuClientes):

    TITULO = "SISTEMA DE GESTIÓN DE ESTUDIANTES"
    ENTIDAD = "estudiante"
    ENTIDADES = "estudiantes"

    TEXTO_BUSQUEDA = (
        "Nombre, apellido, carnet, email, cédula o celular"
    )

    ANCHO = 110

    def __init__(self):

        super().__init__()

        self.__controlador = EstudianteController()

        self.agregar_opcion(
            8,
            "Agregar nota",
            self.agregar_nota
        )

        self.agregar_opcion(
            9,
            "Ver promedio",
            self.ver_promedio
        )

        self.agregar_opcion(
            10,
            "Materias en común",
            self.materias_en_comun
        )

    @property
    def controlador(self):
        return self.__controlador

    # --------------------------------------------------------
    # TABLA ESTUDIANTES
    # --------------------------------------------------------

    def mostrar_tabla(self, estudiantes):

        print(
            f"{'ID':<5}"
            f"{'NOMBRE':<15}"
            f"{'APELLIDO':<18}"
            f"{'CARNET':<15}"
            f"{'CEDULA':<14}"
            f"{'CELULAR':<14}"
            f"{'PROM.':<8}"
            f"{'ESTADO':<12}"
        )

        print("-" * self.ANCHO)

        for estudiante in estudiantes:

            print(
                f"{estudiante.id:<5}"
                f"{estudiante.nombre:<15}"
                f"{estudiante.apellido:<18}"
                f"{estudiante.carnet:<15}"
                f"{estudiante.cedula:<14}"
                f"{estudiante.celular:<14}"
                f"{estudiante.promedio:<8.2f}"
                f"{estudiante.estado:<12}"
            )

        print("-" * self.ANCHO)

        imprimir_info(
            f"Total: {len(estudiantes)} estudiante(s)"
        )

    # --------------------------------------------------------
    # NÚMERO
    # --------------------------------------------------------

    @staticmethod
    def pedir_numero(mensaje):

        while True:

            try:
                return float(input(mensaje))

            except ValueError:

                imprimir_error(
                    "Debe ingresar un número."
                )

    # --------------------------------------------------------
    # ESTADÍSTICAS
    # --------------------------------------------------------

    def estadisticas(self):

        imprimir_titulo(
            "ESTADÍSTICAS DE ESTUDIANTES"
        )

        datos = self.controlador.estadisticas()

        print(
            f"Total de estudiantes: "
            f"{datos.get('total', 0)}"
        )

        print(
            f"Aprobados: "
            f"{datos.get('aprobados', 0)}"
        )

        print(
            f"Reprobados: "
            f"{datos.get('reprobados', 0)}"
        )

        print(
            f"Materias ofertadas: "
            f"{datos.get('materias_ofertadas', 0)}"
        )

        self.pausa()

    # --------------------------------------------------------
    # AGREGAR NOTA
    # --------------------------------------------------------

    def agregar_nota(self):

        imprimir_titulo(
            "AGREGAR NOTA"
        )

        id_estudiante = self.pedir_entero(
            "ID del estudiante: "
        )

        materia = input(
            "Materia: "
        ).strip()

        nota = self.pedir_numero(
            "Nota (0-20): "
        )

        resultado = self.controlador.agregar_nota(
            id_estudiante,
            materia,
            nota
        )

        self.mostrar_resultado(resultado)
        self.pausa()

    # --------------------------------------------------------
    # VER PROMEDIO
    # --------------------------------------------------------

    def ver_promedio(self):

        imprimir_titulo(
            "PROMEDIO DEL ESTUDIANTE"
        )

        id_estudiante = self.pedir_entero(
            "ID del estudiante: "
        )

        estudiante = self.controlador.obtener(
            id_estudiante
        )

        if not estudiante:

            imprimir_error(
                "No existe un estudiante con ese ID."
            )

            self.pausa()
            return

        print(
            f"\nEstudiante: "
            f"{estudiante.nombre} "
            f"{estudiante.apellido}"
        )

        print(
            f"Carnet: {estudiante.carnet}"
        )

        print(
            f"Cédula: {estudiante.cedula}"
        )

        print(
            f"Celular: {estudiante.celular}"
        )

        print(
            f"Promedio: "
            f"{estudiante.promedio:.2f}"
        )

        print(
            f"Estado: "
            f"{estudiante.estado}"
        )

        self.pausa()

    # --------------------------------------------------------
    # MATERIAS EN COMÚN
    # --------------------------------------------------------

    def materias_en_comun(self):

        imprimir_titulo(
            "MATERIAS EN COMÚN"
        )

        id_1 = self.pedir_entero(
            "ID del primer estudiante: "
        )

        id_2 = self.pedir_entero(
            "ID del segundo estudiante: "
        )

        resultado = self.controlador.materias_en_comun(
            id_1,
            id_2
        )

        if not resultado[0]:

            imprimir_error(resultado[1])

        else:

            materias = resultado[1]

            if materias:

                imprimir_info(
                    "Materias en común:"
                )

                for materia in materias:
                    print(f"- {materia}")

            else:

                imprimir_info(
                    "No tienen materias en común."
                )

        self.pausa()


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

if __name__ == "__main__":

    try:

        while True:

            imprimir_titulo(
                "SISTEMA DE GESTIÓN"
            )

            print("1. Gestión de clientes")
            print("2. Gestión de estudiantes")
            print("0. Salir")

            opcion = input(
                "\nSeleccione una opción: "
            ).strip()

            if opcion == "1":

                MenuClientes().ejecutar()

            elif opcion == "2":

                MenuEstudiantes().ejecutar()

            elif opcion == "0":

                imprimir_exito(
                    "Programa finalizado correctamente."
                )

                break

            else:

                imprimir_error(
                    "Opción no válida."
                )

    except KeyboardInterrupt:

        print()

        imprimir_info(
            "Programa interrumpido por el usuario."
        )