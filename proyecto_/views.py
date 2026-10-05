from models import Cliente, Estudiante
from shared.json_manager import GestorJSON


# ============================================================
# CONTROLADOR DE CLIENTES
# ============================================================

class ClienteController:

    MODELO = Cliente
    ARCHIVO = "data/clientes.json"

    CAMPOS_BUSCABLES = (
        "nombre",
        "apellido",
        "email",
        "telefono",
        "ciudad"
    )

    _gestor = GestorJSON(ARCHIVO)

    # ========================================================
    # REGISTROS
    # ========================================================

    @classmethod
    def _registros(cls):
        return cls._gestor.leer()

    # ========================================================
    # EMAILS REGISTRADOS
    # ========================================================

    @classmethod
    def emails_registrados(cls, excepto_id=None):
        return {
            registro["email"].lower()
            for registro in cls._registros()
            if registro.get("id") != excepto_id
            and registro.get("email")
        }

    # ========================================================
    # SIGUIENTE ID
    # ========================================================

    @classmethod
    def siguiente_id(cls):
        registros = cls._registros()

        if not registros:
            return 1

        return max(
            registro["id"]
            for registro in registros
        ) + 1

    # ========================================================
    # COINCIDENCIA
    # ========================================================

    @classmethod
    def _coincide(cls, registro, texto):
        texto = str(texto).lower().strip()

        for campo in cls.CAMPOS_BUSCABLES:
            valor = str(
                registro.get(campo, "")
            ).lower()

            if texto in valor:
                return True

        return False

    # ========================================================
    # CREAR
    # ========================================================

    @classmethod
    def crear(cls, datos):

        for campo in cls.MODELO.OBLIGATORIOS:
            if not str(datos.get(campo, "")).strip():
                return (
                    False,
                    f"El campo '{campo}' es obligatorio"
                )

        email = str(
            datos.get("email", "")
        ).strip().lower()

        if email in cls.emails_registrados():
            return (
                False,
                "Ese email ya está registrado"
            )

        try:
            objeto = cls.MODELO(
                id=cls.siguiente_id(),
                **datos
            )

            registros = cls._registros()
            registros.append(
                objeto.a_diccionario()
            )

            cls._gestor.guardar(registros)

            return (
                True,
                f"{cls.MODELO.__name__} creado correctamente"
            )

        except ValueError as e:
            return False, str(e)

    # ========================================================
    # LISTAR
    # ========================================================

    @classmethod
    def listar(cls):
        return [
            cls.MODELO.desde_diccionario(registro)
            for registro in cls._registros()
        ]

    # ========================================================
    # OBTENER POR ID
    # ========================================================

    @classmethod
    def obtener(cls, id_registro):

        for registro in cls._registros():

            if registro.get("id") == id_registro:
                return cls.MODELO.desde_diccionario(
                    registro
                )

        return None

    # ========================================================
    # BUSCAR
    # ========================================================

    @classmethod
    def buscar(cls, texto):

        resultados = []

        for registro in cls._registros():

            if cls._coincide(registro, texto):
                resultados.append(
                    cls.MODELO.desde_diccionario(
                        registro
                    )
                )

        return resultados

    # ========================================================
    # ACTUALIZAR
    # ========================================================

    @classmethod
    def actualizar(cls, id_registro, cambios):

        registros = cls._registros()

        registro_encontrado = None

        for registro in registros:

            if registro.get("id") == id_registro:
                registro_encontrado = registro
                break

        if registro_encontrado is None:
            return (
                False,
                f"No existe un registro con ID {id_registro}"
            )

        # Verificar campos válidos
        campos_invalidos = (
            set(cambios.keys())
            - set(cls.MODELO.CAMPOS)
        )

        if campos_invalidos:
            return (
                False,
                "Campos no válidos: "
                + ", ".join(campos_invalidos)
            )

        # ====================================================
        # VALIDAR EMAIL REPETIDO
        # ====================================================

        if "email" in cambios:

            nuevo_email = str(
                cambios["email"]
            ).strip().lower()

            if nuevo_email in cls.emails_registrados(
                excepto_id=id_registro
            ):
                return (
                    False,
                    "Ese email ya lo usa otro registro"
                )

        # ====================================================
        # ACTUALIZAR
        # ====================================================

        datos_actualizados = registro_encontrado.copy()
        datos_actualizados.update(cambios)

        try:

            objeto = cls.MODELO.desde_diccionario(
                datos_actualizados
            )

            indice = registros.index(
                registro_encontrado
            )

            registros[indice] = (
                objeto.a_diccionario()
            )

            cls._gestor.guardar(registros)

            return (
                True,
                "Registro actualizado correctamente"
            )

        except ValueError as e:
            return False, str(e)

    # ========================================================
    # ELIMINAR
    # ========================================================

    @classmethod
    def eliminar(cls, id_registro):

        registros = cls._registros()

        nuevos_registros = [
            registro
            for registro in registros
            if registro.get("id") != id_registro
        ]

        if len(nuevos_registros) == len(registros):
            return (
                False,
                "No existe un registro con ese ID"
            )

        cls._gestor.guardar(nuevos_registros)

        return (
            True,
            "Registro eliminado correctamente"
        )

    # ========================================================
    # ESTADÍSTICAS
    # ========================================================

    @classmethod
    def estadisticas(cls):

        registros = cls._registros()

        return {
            "total": len(registros)
        }


# ============================================================
# CONTROLADOR DE ESTUDIANTES
# ============================================================

class EstudianteController(ClienteController):

    MODELO = Estudiante
    ARCHIVO = "data/estudiantes.json"

    CAMPOS_BUSCABLES = (
        "nombre",
        "apellido",
        "carnet",
        "email",
        "cedula",
        "celular"
    )

    _gestor = GestorJSON(ARCHIVO)

    # ========================================================
    # CARNETS REGISTRADOS
    # ========================================================

    @classmethod
    def carnets_registrados(cls, excepto_id=None):
        return {
            registro["carnet"]
            for registro in cls._registros()
            if registro.get("id") != excepto_id
            and registro.get("carnet")
        }

    # ========================================================
    # CÉDULAS REGISTRADAS
    # ========================================================

    @classmethod
    def cedulas_registradas(cls, excepto_id=None):
        return {
            registro["cedula"]
            for registro in cls._registros()
            if registro.get("id") != excepto_id
            and registro.get("cedula")
        }

    # ========================================================
    # CREAR ESTUDIANTE
    # ========================================================

    @classmethod
    def crear(cls, datos):

        carnet = str(
            datos.get("carnet", "")
        ).strip()

        cedula = str(
            datos.get("cedula", "")
        ).strip()

        # Validar carnet repetido
        if carnet in cls.carnets_registrados():
            return (
                False,
                "Ese carnet ya está registrado"
            )

        # Validar cédula repetida
        if cedula in cls.cedulas_registradas():
            return (
                False,
                "Esa cédula ya está registrada"
            )

        return super().crear(datos)

    # ========================================================
    # ACTUALIZAR ESTUDIANTE
    # ========================================================

    @classmethod
    def actualizar(cls, id_registro, cambios):

        # ----------------------------------------------------
        # VALIDAR CARNET
        # ----------------------------------------------------

        if "carnet" in cambios:

            nuevo_carnet = str(
                cambios["carnet"]
            ).strip()

            if nuevo_carnet in cls.carnets_registrados(
                excepto_id=id_registro
            ):
                return (
                    False,
                    "Ese carnet ya lo usa otro estudiante"
                )

        # ----------------------------------------------------
        # VALIDAR CÉDULA
        # ----------------------------------------------------

        if "cedula" in cambios:

            nueva_cedula = str(
                cambios["cedula"]
            ).strip()

            if nueva_cedula in cls.cedulas_registradas(
                excepto_id=id_registro
            ):
                return (
                    False,
                    "Esa cédula ya la usa otro estudiante"
                )

        return super().actualizar(
            id_registro,
            cambios
        )

    # ========================================================
    # AGREGAR NOTA
    # ========================================================

    @classmethod
    def agregar_nota(
        cls,
        id_estudiante,
        materia,
        nota
    ):

        registros = cls._registros()

        for registro in registros:

            if registro.get("id") == id_estudiante:

                try:

                    estudiante = (
                        cls.MODELO.desde_diccionario(
                            registro
                        )
                    )

                    estudiante.agregar_nota(
                        materia,
                        nota
                    )

                    indice = registros.index(
                        registro
                    )

                    registros[indice] = (
                        estudiante.a_diccionario()
                    )

                    cls._gestor.guardar(
                        registros
                    )

                    return (
                        True,
                        "Nota agregada correctamente"
                    )

                except ValueError as e:
                    return False, str(e)

        return (
            False,
            "No existe ese estudiante"
        )

    # ========================================================
    # MATERIAS OFERTADAS
    # ========================================================

    @classmethod
    def materias_ofertadas(cls):

        materias = set()

        for registro in cls._registros():

            for materia in registro.get(
                "materias",
                []
            ):
                materias.add(materia)

        return sorted(materias)

    # ========================================================
    # MATERIAS EN COMÚN
    # ========================================================

    @classmethod
    def materias_en_comun(
        cls,
        id_estudiante_1,
        id_estudiante_2
    ):

        estudiante_1 = cls.obtener(
            id_estudiante_1
        )

        estudiante_2 = cls.obtener(
            id_estudiante_2
        )

        if not estudiante_1:
            return (
                False,
                "No existe el primer estudiante"
            )

        if not estudiante_2:
            return (
                False,
                "No existe el segundo estudiante"
            )

        materias = estudiante_1.materias_en_comun(
            estudiante_2
        )

        return True, materias

    # ========================================================
    # ESTADÍSTICAS
    # ========================================================

    @classmethod
    def estadisticas(cls):

        estudiantes = cls.listar()

        aprobados = sum(
            1
            for estudiante in estudiantes
            if estudiante.estado == "Aprobado"
        )

        reprobados = sum(
            1
            for estudiante in estudiantes
            if estudiante.estado == "Reprobado"
        )

        return {
            "total": len(estudiantes),
            "aprobados": aprobados,
            "reprobados": reprobados,
            "materias_ofertadas": len(
                cls.materias_ofertadas()
            )
        }