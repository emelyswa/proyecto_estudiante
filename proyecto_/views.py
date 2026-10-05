from models import Cliente, Estudiante
from shared.json_manager import GestorJSON


class ClienteController:
    """CONTROLADOR: las cinco operaciones. No imprime ni pide datos."""

    # ===== ATRIBUTOS DE CLASE: toda la configuración junta =====
    MODELO = Cliente
    ARCHIVO = "data/clientes.json"
    CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")
    _gestor = GestorJSON(ARCHIVO)        # se crea una sola vez, al importar el módulo

    # ===== AYUDAS =====
    @classmethod
    def _registros(cls):
        """LISTA de diccionarios, tal como está en el archivo."""
        return cls._gestor.leer()

    @classmethod
    def emails_registrados(cls, excepto_id=None):
        """CONJUNTO de emails ya usados: permite detectar duplicados al instante."""
        return {
            registro["email"].lower()
            for registro in cls._registros()
            if registro["id"] != excepto_id
        }

    @classmethod
    def siguiente_id(cls):
        ids = [registro["id"] for registro in cls._registros()]
        return max(ids) + 1 if ids else 1

    @staticmethod
    def _coincide(registro, termino, campos):
        """Estático: no necesita la clase, solo compara textos."""
        for campo in campos:
            if termino in str(registro.get(campo, "")).lower():
                return True
        return False

    # ===== C · CREATE =====
    @classmethod
    def crear(cls, datos):
        """datos: diccionario. Devuelve la TUPLA (exito, mensaje)."""
        try:
            faltantes = [
                campo for campo in cls.MODELO.OBLIGATORIOS
                if not str(datos.get(campo, "")).strip()
            ]
            if faltantes:
                return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

            email = str(datos.get("email", "")).strip().lower()
            if email in cls.emails_registrados():
                return False, "Ese email ya está registrado"

            valores = {campo: datos.get(campo, "") for campo in cls.MODELO.CAMPOS}

            # cls.MODELO es la clase: aquí nace el objeto y sus setters validan todo
            objeto = cls.MODELO(cls.siguiente_id(), **valores)

            registros = cls._registros()
            registros.append(objeto.a_diccionario())
            if not cls._gestor.guardar(registros):
                return False, "No se pudo escribir el archivo"

            return True, f"{objeto.nombre_completo} creado con id {objeto.id}"

        except ValueError as error:
            # Los setters del Modelo lanzan ValueError con el mensaje ya listo
            return False, str(error)

    # ===== R · READ =====
    @classmethod
    def listar(cls):
        """LISTA de objetos del Modelo."""
        return [cls.MODELO.desde_diccionario(r) for r in cls._registros()]

    @classmethod
    def obtener(cls, id_registro):
        for objeto in cls.listar():
            if objeto.id == id_registro:
                return objeto
        return None

    # ===== S · SEARCH =====
    @classmethod
    def buscar(cls, termino):
        termino = str(termino).strip().lower()
        if not termino:
            return []
        return [
            cls.MODELO.desde_diccionario(registro)
            for registro in cls._registros()
            if cls._coincide(registro, termino, cls.CAMPOS_BUSCABLES)
        ]

    # ===== U · UPDATE =====
    @classmethod
    def actualizar(cls, id_registro, cambios):
        try:
            # DIFERENCIA DE CONJUNTOS: ¿mandaron campos que no existen?
            desconocidos = set(cambios) - set(cls.MODELO.CAMPOS)
            if desconocidos:
                return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
            if not cambios:
                return False, "No se indicó ningún cambio"

            objeto = cls.obtener(id_registro)
            if objeto is None:
                return False, f"No existe un registro con id {id_registro}"

            if "email" in cambios:
                nuevo = str(cambios["email"]).strip().lower()
                if nuevo in cls.emails_registrados(excepto_id=id_registro):
                    return False, "Ese email ya lo usa otro registro"

            # setattr le asigna a la PROPIEDAD, así que cada setter valida el valor
            for campo, valor in cambios.items():
                setattr(objeto, campo, valor)

            registros = cls._registros()
            for indice, registro in enumerate(registros):
                if registro["id"] == id_registro:
                    registros[indice] = objeto.a_diccionario()
                    break

            cls._gestor.guardar(registros)
            return True, f"Registro {id_registro} actualizado ({len(cambios)} campo/s)"

        except ValueError as error:
            return False, str(error)

    # ===== D · DELETE =====
    @classmethod
    def eliminar(cls, id_registro):
        registros = cls._registros()
        # Lista nueva sin ese registro: nunca se borra mientras se recorre
        quedan = [r for r in registros if r["id"] != id_registro]

        if len(quedan) == len(registros):
            return False, f"No existe un registro con id {id_registro}"

        cls._gestor.guardar(quedan)
        return True, f"Registro {id_registro} eliminado"

    # ===== EXTRA =====
    @classmethod
    def estadisticas(cls):
        registros = cls._registros()
        ciudades = {r.get("ciudad", "") for r in registros if r.get("ciudad")}
        dominios = {r["email"].split("@")[1] for r in registros if "@" in r["email"]}
        sin_telefono = [r["nombre"] for r in registros if not r.get("telefono")]
        return {
            "total": len(registros),
            "ciudades": sorted(ciudades),
            "dominios": sorted(dominios),
            "sin_telefono": sin_telefono,
        }

class EstudianteController(ClienteController):
    """CONTROLADOR de estudiantes."""

    # ===== CONFIGURACIÓN =====
    MODELO = Estudiante
    ARCHIVO = "data/estudiantes.json"
    CAMPOS_BUSCABLES = (
        "nombre",
        "apellido",
        "email",
        "cedula",
        "celular"
    )

    _gestor = GestorJSON(ARCHIVO)

    # ===== CÉDULAS: DETECTAR DUPLICADOS =====
    @classmethod
    def cedulas_registradas(cls, excepto_id=None):
        """Obtiene las cédulas que ya están registradas."""
        return {
            registro["cedula"]
            for registro in cls._registros()
            if registro.get("id") != excepto_id
            and registro.get("cedula")
        }

    # ===== CREATE =====
    @classmethod
    def crear(cls, datos):
        cedula = str(datos.get("cedula", "")).strip()

        if cedula and cedula in cls.cedulas_registradas():
            return False, "Esa cédula ya está registrada"

        return super().crear(datos)

    # ===== UPDATE =====
    @classmethod
    def actualizar(cls, id_registro, cambios):
        if "cedula" in cambios:
            nueva_cedula = str(cambios["cedula"]).strip()

            if (
                nueva_cedula
                and nueva_cedula in cls.cedulas_registradas(
                    excepto_id=id_registro
                )
            ):
                return False, "Esa cédula ya la usa otro estudiante"

        return super().actualizar(id_registro, cambios)

    # ===== NOTAS =====
    @classmethod
    def agregar_nota(cls, id_estudiante, materia, nota):
        """Registra una nota utilizando las validaciones del modelo."""

        estudiante = cls.obtener(id_estudiante)

        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        try:
            materia = estudiante.agregar_nota(materia, nota)
        except ValueError as error:
            return False, str(error)

        # Guardar los cambios
        registros = cls._registros()

        for indice, registro in enumerate(registros):
            if registro.get("id") == id_estudiante:
                registros[indice] = estudiante.a_diccionario()
                break

        if not cls._gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return (
            True,
            f"Nota {nota} registrada en {materia} "
            f"para {estudiante.nombre_completo}"
        )

    # ===== CONJUNTOS: UNIÓN E INTERSECCIÓN =====
    @classmethod
    def materias_ofertadas(cls):
        """Obtiene todas las materias de los estudiantes sin repetir."""

        ofertadas = set()

        for estudiante in cls.listar():
            ofertadas |= estudiante.materias

        return ofertadas

    @classmethod
    def materias_en_comun(cls, id_a, id_b):
        """Devuelve las materias que tienen en común dos estudiantes."""

        if id_a == id_b:
            return False, "Elija dos estudiantes distintos"

        estudiante_a = cls.obtener(id_a)
        estudiante_b = cls.obtener(id_b)

        if estudiante_a is None or estudiante_b is None:
            return False, "Alguno de los dos ids no existe"

        return True, estudiante_a.materias_en_comun(estudiante_b)

    # ===== ESTADÍSTICAS =====
    @classmethod
    def estadisticas(cls):
        estudiantes = cls.listar()

        aprobados = [
            estudiante
            for estudiante in estudiantes
            if estudiante.estado == "Aprobado"
        ]

        return {
            "total": len(estudiantes),
            "aprobados": len(aprobados),
            "reprobados": len(estudiantes) - len(aprobados),
            "materias": sorted(cls.materias_ofertadas()),
        }
