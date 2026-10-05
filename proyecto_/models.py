class Cliente:
    """MODELO: un cliente válido."""

    CAMPOS = (
        "nombre",
        "apellido",
        "email",
        "telefono",
        "ciudad",
        "direccion"
    )

    OBLIGATORIOS = (
        "nombre",
        "apellido",
        "email"
    )

    total_creados = 0

    def __init__(
        self,
        id,
        nombre,
        apellido,
        email,
        telefono="",
        ciudad="",
        direccion=""
    ):
        self.__id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad
        self.direccion = direccion

        Cliente.total_creados += 1

    @staticmethod
    def limpiar(valor):
        return str(valor).strip()

    @staticmethod
    def es_email_valido(texto):
        texto = str(texto).strip()

        if texto.count("@") != 1:
            return False

        usuario, dominio = texto.split("@")

        return (
            len(usuario) > 0
            and "." in dominio
            and not dominio.endswith(".")
        )

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self.limpiar(valor)

        if not valor:
            raise ValueError("El nombre es obligatorio")

        self.__nombre = valor

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        valor = self.limpiar(valor)

        if not valor:
            raise ValueError("El apellido es obligatorio")

        self.__apellido = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = self.limpiar(valor)

        if not self.es_email_valido(valor):
            raise ValueError("El email no tiene un formato válido")

        self.__email = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self.limpiar(valor)

        if valor and not valor.isdigit():
            raise ValueError("El teléfono solo debe contener números")

        self.__telefono = valor

    @property
    def ciudad(self):
        return self.__ciudad

    @ciudad.setter
    def ciudad(self, valor):
        self.__ciudad = self.limpiar(valor)

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        self.__direccion = self.limpiar(valor)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def dominio_email(self):
        return self.email.split("@")[1]

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "direccion": self.direccion
        }

    def __str__(self):
        return (
            f"Cliente #{self.id}: "
            f"{self.nombre_completo} - {self.email}"
        )

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            id=datos["id"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            email=datos["email"],
            telefono=datos.get("telefono", ""),
            ciudad=datos.get("ciudad", ""),
            direccion=datos.get("direccion", "")
        )


# ============================================================
# ESTUDIANTE
# ============================================================

class Estudiante(Cliente):

    CAMPOS = (
        "nombre",
        "apellido",
        "carnet",
        "email",
        "cedula",
        "celular"
    )

    OBLIGATORIOS = (
        "nombre",
        "apellido",
        "carnet",
        "email",
        "cedula",
        "celular"
    )

    NOTA_MINIMA = 0
    NOTA_MAXIMA = 20
    NOTA_APROBACION = 14

    def __init__(
        self,
        id,
        nombre,
        apellido,
        carnet,
        email,
        cedula,
        celular,
        notas=None,
        materias=None
    ):
        self.__id = id
        self.nombre = nombre
        self.apellido = apellido
        self.carnet = carnet
        self.email = email
        self.cedula = cedula
        self.celular = celular

        self.__notas = notas or {}
        self.__materias = materias or []

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = str(valor).strip()

        if not valor:
            raise ValueError("El nombre es obligatorio")

        self.__nombre = valor

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        valor = str(valor).strip()

        if not valor:
            raise ValueError("El apellido es obligatorio")

        self.__apellido = valor

    # --------------------------------------------------------
    # CARNET
    # --------------------------------------------------------

    @property
    def carnet(self):
        return self.__carnet

    @carnet.setter
    def carnet(self, valor):
        valor = str(valor).strip()

        if not valor:
            raise ValueError("El carnet es obligatorio")

        self.__carnet = valor

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = str(valor).strip()

        if not self.es_email_valido(valor):
            raise ValueError("El email no tiene un formato válido")

        self.__email = valor.lower()

    # --------------------------------------------------------
    # CÉDULA
    # --------------------------------------------------------

    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, valor):
        valor = str(valor).strip()

        if not valor:
            raise ValueError("La cédula es obligatoria")

        if not valor.isdigit():
            raise ValueError("La cédula solo debe contener números")

        self.__cedula = valor

    # --------------------------------------------------------
    # CELULAR
    # --------------------------------------------------------

    @property
    def celular(self):
        return self.__celular

    @celular.setter
    def celular(self, valor):
        valor = str(valor).strip()

        if not valor:
            raise ValueError("El celular es obligatorio")

        if not valor.isdigit():
            raise ValueError("El celular solo debe contener números")

        self.__celular = valor

    # --------------------------------------------------------
    # MATERIAS
    # --------------------------------------------------------

    @property
    def materias(self):
        return self.__materias

    # --------------------------------------------------------
    # NOTAS
    # --------------------------------------------------------

    @property
    def promedio(self):
        if not self.__notas:
            return 0

        return sum(self.__notas.values()) / len(self.__notas)

    @property
    def estado(self):
        if not self.__notas:
            return "Sin notas"

        if self.promedio >= self.NOTA_APROBACION:
            return "Aprobado"

        return "Reprobado"

    def inscribir_materia(self, materia):
        materia = str(materia).strip()

        if not materia:
            raise ValueError("La materia no puede estar vacía")

        if materia not in self.__materias:
            self.__materias.append(materia)

    def agregar_nota(self, materia, nota):
        materia = str(materia).strip()

        try:
            nota = float(nota)
        except ValueError:
            raise ValueError("La nota debe ser numérica")

        if nota < self.NOTA_MINIMA or nota > self.NOTA_MAXIMA:
            raise ValueError(
                f"La nota debe estar entre "
                f"{self.NOTA_MINIMA} y {self.NOTA_MAXIMA}"
            )

        self.inscribir_materia(materia)
        self.__notas[materia] = nota

    def notas_de(self, materia):
        return self.__notas.get(materia)

    def materias_en_comun(self, otro_estudiante):
        return list(
            set(self.__materias).intersection(
                set(otro_estudiante.materias)
            )
        )

    # --------------------------------------------------------
    # DICCIONARIO
    # --------------------------------------------------------

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "carnet": self.carnet,
            "email": self.email,
            "cedula": self.cedula,
            "celular": self.celular,
            "notas": self.__notas,
            "materias": self.__materias
        }

    def __str__(self):
        return (
            f"Estudiante #{self.id}: "
            f"{self.nombre} {self.apellido} - "
            f"Carnet: {self.carnet} - "
            f"Cédula: {self.cedula}"
        )

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            id=datos["id"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            carnet=datos["carnet"],
            email=datos["email"],
            cedula=datos["cedula"],
            celular=datos["celular"],
            notas=datos.get("notas", {}),
            materias=datos.get("materias", [])
        )