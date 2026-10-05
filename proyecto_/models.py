class Cliente:
    """MODELO: un cliente válido. Si los datos están mal, el objeto no se crea."""

    # ===== ATRIBUTOS DE CLASE =====
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
        id_cliente,
        nombre,
        apellido,
        email,
        telefono="",
        ciudad="",
        direccion=""
    ):
        self.__id = id_cliente

        # Se asignan mediante propiedades para validar los datos
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad
        self.direccion = direccion

        Cliente.total_creados += 1

    # ===== MÉTODOS ESTÁTICOS =====

    @staticmethod
    def limpiar(texto):
        return str(texto).strip()

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

    # ===== PROPIEDADES =====

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = Cliente.limpiar(valor)

        if not valor:
            raise ValueError("El nombre es obligatorio")

        self.__nombre = valor.title()

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        valor = Cliente.limpiar(valor)

        if not valor:
            raise ValueError("El apellido es obligatorio")

        self.__apellido = valor.title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = Cliente.limpiar(valor)

        if not Cliente.es_email_valido(valor):
            raise ValueError(
                f"Email inválido: '{valor}'"
            )

        self.__email = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = Cliente.limpiar(valor)

        if valor and not valor.isdigit():
            raise ValueError(
                "El teléfono solo puede tener números"
            )

        self.__telefono = valor

    @property
    def ciudad(self):
        return self.__ciudad

    @ciudad.setter
    def ciudad(self, valor):
        self.__ciudad = Cliente.limpiar(valor).title()

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, valor):
        self.__direccion = Cliente.limpiar(valor)

    # ===== PROPIEDADES CALCULADAS =====

    @property
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"

    @property
    def dominio_email(self):
        return self.__email.split("@")[1]

    # ===== MÉTODOS DE INSTANCIA =====

    def a_diccionario(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "email": self.__email,
            "telefono": self.__telefono,
            "ciudad": self.__ciudad,
            "direccion": self.__direccion,
        }

    def __str__(self):
        return (
            f"[{self.__id}] "
            f"{self.nombre_completo} - "
            f"{self.__email}"
        )

    # ===== MÉTODO DE CLASE =====

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos.get("telefono", ""),
            datos.get("ciudad", ""),
            datos.get("direccion", ""),
        )


class Estudiante:
    """MODELO: un estudiante con materias y notas."""

    # ===== ATRIBUTOS DE CLASE =====

    CAMPOS = (
        "nombre",
        "apellido",
        "email",
        "cedula",
        "celular"
    )

    OBLIGATORIOS = (
        "nombre",
        "apellido",
        "email",
        "cedula",
        "celular"
    )

    NOTA_MINIMA = 0
    NOTA_MAXIMA = 20
    NOTA_APROBACION = 14

    total_creados = 0

    def __init__(
        self,
        id_estudiante,
        nombre,
        apellido,
        email,
        cedula,
        celular,
        notas=None,
        materias=None
    ):
        self.__id = id_estudiante

        # Se utilizan las propiedades para validar
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.cedula = cedula
        self.celular = celular

        self.__notas = dict(notas) if notas else {}
        self.__materias = set(materias) if materias else set()

        Estudiante.total_creados += 1

    # ===== MÉTODOS ESTÁTICOS =====

    @staticmethod
    def limpiar(texto):
        return str(texto).strip()

    @staticmethod
    def es_nota_valida(nota):
        return (
            isinstance(nota, (int, float))
            and Estudiante.NOTA_MINIMA <= nota <= Estudiante.NOTA_MAXIMA
        )

    # ===== PROPIEDADES =====

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = Estudiante.limpiar(valor)

        if not valor:
            raise ValueError("El nombre es obligatorio")

        self.__nombre = valor.title()

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        valor = Estudiante.limpiar(valor)

        if not valor:
            raise ValueError("El apellido es obligatorio")

        self.__apellido = valor.title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = Estudiante.limpiar(valor)

        if "@" not in valor:
            raise ValueError(
                f"Email inválido: '{valor}'"
            )

        self.__email = valor.lower()

    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, valor):
        valor = Estudiante.limpiar(valor)

        if not valor:
            raise ValueError(
                "La cédula es obligatoria"
            )

        if not valor.isdigit():
            raise ValueError(
                "La cédula solo puede tener números"
            )

        self.__cedula = valor

    @property
    def celular(self):
        return self.__celular

    @celular.setter
    def celular(self, valor):
        valor = Estudiante.limpiar(valor)

        if not valor:
            raise ValueError(
                "El celular es obligatorio"
            )

        if not valor.isdigit():
            raise ValueError(
                "El celular solo puede tener números"
            )

        self.__celular = valor

    @property
    def materias(self):
        return set(self.__materias)

    @property
    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}"

    @property
    def promedio(self):
        todas = []

        for lista_notas in self.__notas.values():
            todas.extend(lista_notas)

        if not todas:
            return 0

        return round(
            sum(todas) / len(todas),
            2
        )

    @property
    def estado(self):
        if self.promedio >= self.NOTA_APROBACION:
            return "Aprobado"

        return "Reprobado"

    # ===== MÉTODOS DE INSTANCIA =====

    def inscribir_materia(self, materia):
        materia = Estudiante.limpiar(materia).title()

        if not materia:
            raise ValueError(
                "La materia no puede estar vacía"
            )

        self.__materias.add(materia)

        return materia

    def agregar_nota(self, materia, nota):
        if not Estudiante.es_nota_valida(nota):
            raise ValueError(
                f"La nota debe estar entre "
                f"{Estudiante.NOTA_MINIMA} y "
                f"{Estudiante.NOTA_MAXIMA}"
            )

        materia = self.inscribir_materia(materia)

        self.__notas.setdefault(
            materia,
            []
        ).append(nota)

        return materia

    def notas_de(self, materia):
        materia = Estudiante.limpiar(
            materia
        ).title()

        return list(
            self.__notas.get(
                materia,
                []
            )
        )

    def materias_en_comun(self, otro):
        return self.__materias & otro.materias

    def a_diccionario(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "apellido": self.__apellido,
            "email": self.__email,
            "cedula": self.__cedula,
            "celular": self.__celular,
            "notas": self.__notas,
            "materias": sorted(self.__materias),
        }

    def __str__(self):
        return (
            f"[{self.__cedula}] "
            f"{self.nombre_completo} - "
            f"Promedio: {self.promedio}"
        )

    # ===== MÉTODO DE CLASE =====

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["cedula"],
            datos["celular"],
            notas=datos.get("notas", {}),
            materias=set(
                datos.get("materias", [])
            ),
        )
