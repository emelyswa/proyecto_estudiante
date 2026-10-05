from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar
)

from views import ClienteController, EstudianteController


class MenuClientes:
    """VISTA: muestra, pide y presenta. No decide reglas del negocio."""

    TITULO = "SISTEMA DE GESTIÓN DE CLIENTES"
    ANCHO = 85

    def __init__(self, controlador=ClienteController):
        self.__controlador = controlador
        self.__activo = True

        self.__opciones = {
            "1": ("Crear cliente", self.crear),
            "2": ("Ver todos", self.listar),
            "3": ("Buscar", self.buscar),
            "4": ("Ver por id", self.ver_por_id),
            "5": ("Actualizar", self.actualizar),
            "6": ("Eliminar", self.eliminar),
            "7": ("Estadísticas", self.estadisticas),
            "0": ("Salir", self.salir),
        }

    # ===== PROPIEDAD PARA ACCEDER AL CONTROLADOR =====
    @property
    def controlador(self):
        return self.__controlador

    # ===== AGREGAR OPCIONES =====
    def agregar_opcion(self, tecla, texto, metodo):
        self.__opciones[tecla] = (texto, metodo)

    # ===== ESTÁTICOS =====
    @staticmethod
    def pausa():
        input("\nPresione Enter para continuar...")

    @staticmethod
    def pedir_entero(etiqueta):
        try:
            return int(input(etiqueta))
        except ValueError:
            return None

    @staticmethod
    def mostrar_resultado(exito, mensaje):
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)

    # ===== MOSTRAR TABLA =====
    def mostrar_tabla(self, clientes):
        print(
            f"{'ID':<5}"
            f"{'NOMBRE':<25}"
            f"{'EMAIL':<28}"
            f"{'CIUDAD':<15}"
            f"{'TELÉFONO':<12}"
        )

        print("-" * self.ANCHO)

        for cliente in clientes:
            print(
                f"{cliente.id:<5}"
                f"{cliente.nombre_completo:<25}"
                f"{cliente.email:<28}"
                f"{cliente.ciudad:<15}"
                f"{cliente.telefono:<12}"
            )

        print("-" * self.ANCHO)
        imprimir_info(f"Total: {len(clientes)} cliente(s)")

    # ===== CREAR =====
    def crear(self):
        imprimir_titulo("CREAR NUEVO CLIENTE")

        datos = {}

        for campo in self.__controlador.MODELO.CAMPOS:
            datos[campo] = input(f"{campo.capitalize()}: ")

        exito, mensaje = self.__controlador.crear(datos)

        self.mostrar_resultado(exito, mensaje)
        self.pausa()

    # ===== LISTAR =====
    def listar(self):
        imprimir_titulo("LISTA DE CLIENTES")

        clientes = self.__controlador.listar()

        if not clientes:
            imprimir_info(
                "Todavía no hay clientes. "
                "Use la opción 1 para crear el primero."
            )
        else:
            self.mostrar_tabla(clientes)

        self.pausa()

    # ===== BUSCAR =====
    def buscar(self):
        imprimir_titulo("BUSCAR CLIENTE")

        termino = input(
            "Nombre, email, teléfono o ciudad: "
        )

        encontrados = self.__controlador.buscar(termino)

        if not encontrados:
            imprimir_info(
                f"Ningún cliente coincide con '{termino}'."
            )
        else:
            self.mostrar_tabla(encontrados)

        self.pausa()

    # ===== VER POR ID =====
    def ver_por_id(self):
        imprimir_titulo("VER CLIENTE POR ID")

        id_cliente = self.pedir_entero(
            "Id del cliente: "
        )

        if id_cliente is None:
            imprimir_error(
                "El id debe ser un número entero"
            )
            return self.pausa()

        cliente = self.__controlador.obtener(id_cliente)

        if cliente is None:
            imprimir_error(
                f"No existe un cliente con id {id_cliente}"
            )
        else:
            for clave, valor in cliente.a_diccionario().items():
                print(
                    f"  {clave.capitalize():<12}: {valor}"
                )

            imprimir_info(
                f"Dominio del email: {cliente.dominio_email}"
            )

        self.pausa()

    # ===== ACTUALIZAR =====
    def actualizar(self):
        imprimir_titulo("ACTUALIZAR CLIENTE")

        id_cliente = self.pedir_entero(
            "Id del cliente: "
        )

        if id_cliente is None:
            imprimir_error(
                "El id debe ser un número entero"
            )
            return self.pausa()

        cliente = self.__controlador.obtener(id_cliente)

        if cliente is None:
            imprimir_error(
                f"No existe un cliente con id {id_cliente}"
            )
            return self.pausa()

        imprimir_info(
            f"Editando a {cliente.nombre_completo}"
        )

        print(
            "Deje en blanco el campo que no quiera cambiar.\n"
        )

        cambios = {}

        for campo in self.__controlador.MODELO.CAMPOS:
            actual = getattr(cliente, campo)

            nuevo = input(
                f"{campo.capitalize()} [{actual}]: "
            ).strip()

            if nuevo:
                cambios[campo] = nuevo

        self.mostrar_resultado(
            *self.__controlador.actualizar(
                id_cliente,
                cambios
            )
        )

        self.pausa()

    # ===== ELIMINAR =====
    def eliminar(self):
        imprimir_titulo("ELIMINAR CLIENTE")

        id_cliente = self.pedir_entero(
            "Id del cliente: "
        )

        if id_cliente is None:
            imprimir_error(
                "El id debe ser un número entero"
            )
            return self.pausa()

        cliente = self.__controlador.obtener(id_cliente)

        if cliente is None:
            imprimir_error(
                f"No existe un cliente con id {id_cliente}"
            )
            return self.pausa()

        imprimir_info(
            f"Se eliminará: {cliente}"
        )

        if confirmar("¿Confirma la eliminación?"):
            self.mostrar_resultado(
                *self.__controlador.eliminar(id_cliente)
            )
        else:
            imprimir_info("Operación cancelada")

        self.pausa()

    # ===== ESTADÍSTICAS =====
    def estadisticas(self):
        imprimir_titulo("ESTADÍSTICAS")

        datos = self.__controlador.estadisticas()

        print(
            f"  Clientes registrados : {datos['total']}"
        )

        print(
            f"  Ciudades distintas   : "
            f"{len(datos['ciudades'])} -> "
            f"{', '.join(datos['ciudades'])}"
        )

        print(
            f"  Dominios de email    : "
            f"{', '.join(datos['dominios'])}"
        )

        print(
            f"  Sin teléfono         : "
            f"{len(datos['sin_telefono'])}"
        )

        self.pausa()

    # ===== SALIR =====
    def salir(self):
        self.__activo = False
        imprimir_info("¡Hasta luego! 👋")

    # ===== MOSTRAR MENÚ =====
    def mostrar_menu(self):
        imprimir_titulo(self.TITULO)

        for tecla, (texto, _metodo) in self.__opciones.items():
            print(f"  {tecla}. {texto}")

        print()

    # ===== EJECUTAR =====
    def ejecutar(self):
        while self.__activo:
            self.mostrar_menu()

            tecla = input(
                "Seleccione una opción: "
            ).strip()

            if tecla not in self.__opciones:
                imprimir_error("Opción no válida")
                self.pausa()
                continue

            _texto, metodo = self.__opciones[tecla]
            metodo()


class MenuEstudiantes(MenuClientes):
    """VISTA de estudiantes."""

    TITULO = "SISTEMA DE GESTIÓN DE ESTUDIANTES"
    ENTIDAD = "estudiante"
    ENTIDADES = "estudiantes"
    TEXTO_BUSQUEDA = "Nombre, apellido, email, cedula o celular"
    ANCHO = 110

    def __init__(self, controlador=EstudianteController):
        super().__init__(controlador)

        self.agregar_opcion(
            "8",
            "Agregar nota",
            self.agregar_nota
        )

        self.agregar_opcion(
            "9",
            "Ver promedio",
            self.ver_promedio
        )

        self.agregar_opcion(
            "10",
            "Materias en común",
            self.materias_en_comun
        )

    @staticmethod
    def pedir_numero(etiqueta):
        try:
            valor = float(
                input(etiqueta).strip().replace(",", ".")
            )
        except ValueError:
            return None

        return int(valor) if valor.is_integer() else valor

    # ===== TABLA DE ESTUDIANTES =====
    def mostrar_tabla(self, estudiantes):
        print(
            f"{'ID':<5}"
            f"{'NOMBRE':<25}"
            f"{'CEDULA':<14}"
            f"{'CELULAR':<14}"
            f"{'EMAIL':<28}"
            f"{'PROM.':<8}"
            f"{'ESTADO':<10}"
        )

        print("-" * self.ANCHO)

        for estudiante in estudiantes:
            print(
                f"{estudiante.id:<5}"
                f"{estudiante.nombre_completo:<25}"
                f"{estudiante.cedula:<14}"
                f"{estudiante.celular:<14}"
                f"{estudiante.email:<28}"
                f"{estudiante.promedio:<8}"
                f"{estudiante.estado:<10}"
            )

        print("-" * self.ANCHO)

        imprimir_info(
            f"Total: {len(estudiantes)} estudiante(s)"
        )

    # ===== ESTADÍSTICAS =====
    def estadisticas(self):
        imprimir_titulo("ESTADÍSTICAS")

        datos = self.controlador.estadisticas()

        print(
            f"  Estudiantes registrados : {datos['total']}"
        )

        print(
            f"  Aprobados               : {datos['aprobados']}"
        )

        print(
            f"  Reprobados              : {datos['reprobados']}"
        )

        print(
            f"  Materias ofertadas      : "
            f"{len(datos['materias'])} -> "
            f"{', '.join(datos['materias'])}"
        )

        self.pausa()

    # ===== AGREGAR NOTA =====
    def agregar_nota(self):
        imprimir_titulo("AGREGAR NOTA")

        id_estudiante = self.pedir_entero(
            "Id del estudiante: "
        )

        if id_estudiante is None:
            imprimir_error(
                "El id debe ser un número entero"
            )
            return self.pausa()

        materia = input("Materia: ")

        nota = self.pedir_numero(
            "Nota (0 a 20): "
        )

        if nota is None:
            imprimir_error(
                "La nota debe ser un número"
            )
            return self.pausa()

        self.mostrar_resultado(
            *self.controlador.agregar_nota(
                id_estudiante,
                materia,
                nota
            )
        )

        self.pausa()

    # ===== VER PROMEDIO =====
    def ver_promedio(self):
        imprimir_titulo(
            "PROMEDIO DE UN ESTUDIANTE"
        )

        id_estudiante = self.pedir_entero(
            "Id del estudiante: "
        )

        if id_estudiante is None:
            imprimir_error(
                "El id debe ser un número entero"
            )
            return self.pausa()

        estudiante = self.controlador.obtener(
            id_estudiante
        )

        if estudiante is None:
            imprimir_error(
                f"No existe un estudiante con id {id_estudiante}"
            )
            return self.pausa()

        print(
            f"  Estudiante: {estudiante.nombre_completo} "
            f"({estudiante.cedula})\n"
        )

        if not estudiante.materias:
            imprimir_info(
                "Todavía no tiene materias ni notas."
            )

        for materia in sorted(estudiante.materias):
            print(
                f"  {materia:<20}: "
                f"{estudiante.notas_de(materia)}"
            )

        print()
        print(
            f"  Promedio general: "
            f"{estudiante.promedio}"
        )

        self.mostrar_resultado(
            estudiante.estado == "Aprobado",
            f"Estado: {estudiante.estado}"
        )

        self.pausa()

    # ===== MATERIAS EN COMÚN =====
    def materias_en_comun(self):
        imprimir_titulo("MATERIAS EN COMÚN")

        id_a = self.pedir_entero(
            "Id del primer estudiante: "
        )

        id_b = self.pedir_entero(
            "Id del segundo estudiante: "
        )

        if id_a is None or id_b is None:
            imprimir_error(
                "Los ids deben ser números enteros"
            )
            return self.pausa()

        exito, resultado = (
            self.controlador.materias_en_comun(
                id_a,
                id_b
            )
        )

        if not exito:
            imprimir_error(resultado)

        elif not resultado:
            imprimir_info(
                "No tienen materias en común."
            )

        else:
            imprimir_exito(
                f"Materias en común ({len(resultado)}):"
            )

            for materia in sorted(resultado):
                print(f"  - {materia}")

        self.pausa()


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":
    try:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Gestión de clientes")
        print("2. Gestión de estudiantes")
        print("0. Salir")

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        if opcion == "1":
            MenuClientes().ejecutar()

        elif opcion == "2":
            MenuEstudiantes().ejecutar()

        elif opcion == "0":
            print("\nPrograma finalizado.")

        else:
            print("\nOpción no válida.")

    except KeyboardInterrupt:
        print(
            "\nPrograma interrumpido por el usuario."
        )