from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from anthropic import Anthropic
from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pypdf import PdfReader
from sqlalchemy import delete, select
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename


# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"

UPLOADS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)

app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "clave-local-cambiala-en-el-archivo-env",
)
database_url = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DATA_DIR / 'proga_ia.db'}",
).strip()

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1,
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=(
        os.getenv("FLASK_ENV", "").lower() == "production"
    ),
)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Inicia sesión para continuar."


def clave_limite() -> str:
    if current_user.is_authenticated:
        return f"usuario:{current_user.id}"
    return get_remote_address()


limiter = Limiter(
    key_func=clave_limite,
    app=app,
    default_limits=["300 per day", "60 per hour"],
    storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
)

MAX_PDF_CHARACTERS = 60_000
MAX_QUESTION_CHARACTERS = 15_000
MAX_HISTORIAL = 50
NOTA_MINIMA = 80
DEFAULT_MODEL = "claude-sonnet-4-6"


SILABO = {
    1: {
        "nombre": "Fundamentos de programación",
        "descripcion": (
            "Aprender los conceptos esenciales para comenzar "
            "a pensar y escribir programas."
        ),
        "temas": [
            "Qué es programar",
            "Cómo funciona un programa",
            "Algoritmos",
            "Diagramas de flujo",
            "Pseudocódigo",
            "Variables",
            "Tipos de datos",
            "Entrada y salida de datos",
        ],
        "proyecto": "Calculadora básica",
    },
    2: {
        "nombre": "Lógica de programación",
        "descripcion": (
            "Aprender a tomar decisiones y repetir procesos "
            "dentro de un programa."
        ),
        "temas": [
            "Operadores aritméticos",
            "Operadores de comparación",
            "Operadores lógicos",
            "Condicionales",
            "Ciclo for",
            "Ciclo while",
            "Contadores",
            "Acumuladores",
            "Validación de datos",
            "Pruebas de escritorio",
        ],
        "proyecto": "Menú interactivo",
    },
    3: {
        "nombre": "Estructuras de datos básicas",
        "descripcion": (
            "Organizar y manipular diferentes grupos de datos."
        ),
        "temas": [
            "Listas",
            "Tuplas",
            "Conjuntos",
            "Diccionarios",
            "Matrices",
            "Recorridos",
            "Búsquedas básicas",
            "Ordenamientos básicos",
        ],
        "proyecto": "Sistema de inventario",
    },
    4: {
        "nombre": "Funciones y modularización",
        "descripcion": (
            "Dividir programas grandes en partes pequeñas "
            "que puedan reutilizarse."
        ),
        "temas": [
            "Crear funciones",
            "Parámetros",
            "Argumentos",
            "Valores de retorno",
            "Variables locales",
            "Variables globales",
            "Módulos",
            "Importación de librerías",
        ],
        "proyecto": "Biblioteca de funciones matemáticas",
    },
    5: {
        "nombre": "Programación orientada a objetos",
        "descripcion": (
            "Representar elementos mediante clases y objetos."
        ),
        "temas": [
            "Clases",
            "Objetos",
            "Atributos",
            "Métodos",
            "Constructores",
            "Encapsulamiento",
            "Herencia",
            "Polimorfismo",
            "Abstracción",
            "Composición",
        ],
        "proyecto": "Sistema bancario",
    },
    6: {
        "nombre": "Archivos y persistencia",
        "descripcion": (
            "Guardar y recuperar información para que no "
            "se pierda al cerrar el programa."
        ),
        "temas": [
            "Archivos de texto",
            "Leer archivos",
            "Escribir archivos",
            "Archivos CSV",
            "Archivos JSON",
            "Rutas con pathlib",
            "Persistencia de datos",
        ],
        "proyecto": "Agenda de contactos",
    },
    7: {
        "nombre": "Errores, depuración y pruebas",
        "descripcion": (
            "Detectar errores y crear programas más seguros."
        ),
        "temas": [
            "Errores de sintaxis",
            "Errores de ejecución",
            "Errores lógicos",
            "Try y except",
            "Else y finally",
            "Excepciones personalizadas",
            "Depuración",
            "Pruebas unitarias básicas",
        ],
        "proyecto": "Calculadora robusta",
    },
    8: {
        "nombre": "Algoritmos y complejidad",
        "descripcion": (
            "Analizar la eficiencia de los programas y "
            "resolver problemas con algoritmos conocidos."
        ),
        "temas": [
            "Complejidad algorítmica",
            "Notación Big O",
            "Búsqueda lineal",
            "Búsqueda binaria",
            "Bubble Sort",
            "Selection Sort",
            "Insertion Sort",
            "Merge Sort",
            "Quick Sort",
            "Recursividad",
        ],
        "proyecto": "Comparador de algoritmos",
    },
    9: {
        "nombre": "Estructuras de datos avanzadas",
        "descripcion": (
            "Trabajar con estructuras útiles para resolver "
            "problemas más complejos."
        ),
        "temas": [
            "Pilas",
            "Colas",
            "Colas de prioridad",
            "Listas enlazadas",
            "Árboles",
            "Árboles binarios",
            "Tablas hash",
            "Grafos",
            "Recorridos de grafos",
        ],
        "proyecto": "Sistema de rutas",
    },
    10: {
        "nombre": "Bases de datos",
        "descripcion": (
            "Guardar información estructurada y consultarla "
            "mediante SQL."
        ),
        "temas": [
            "Introducción a SQL",
            "SQLite",
            "Tablas",
            "Claves primarias",
            "Relaciones",
            "Insertar datos",
            "Consultar datos",
            "Actualizar datos",
            "Eliminar datos",
            "CRUD",
            "Consultas con JOIN",
        ],
        "proyecto": "Sistema de estudiantes",
    },
    11: {
        "nombre": "Desarrollo web",
        "descripcion": (
            "Crear aplicaciones web con frontend y backend."
        ),
        "temas": [
            "HTML",
            "CSS",
            "Flexbox",
            "Grid",
            "JavaScript",
            "DOM",
            "Eventos",
            "Flask",
            "Rutas",
            "Plantillas Jinja",
            "Formularios",
        ],
        "proyecto": "Aplicación web completa",
    },
    12: {
        "nombre": "Git y GitHub",
        "descripcion": (
            "Controlar versiones y publicar proyectos."
        ),
        "temas": [
            "Introducción a Git",
            "Repositorios",
            "Commits",
            "Branches",
            "Merge",
            "Conflictos",
            "GitHub",
            "Pull requests",
            "README",
        ],
        "proyecto": "Publicación de un proyecto en GitHub",
    },
    13: {
        "nombre": "Desarrollo de APIs",
        "descripcion": (
            "Permitir que diferentes aplicaciones compartan información."
        ),
        "temas": [
            "Qué es una API",
            "Arquitectura REST",
            "Método GET",
            "Método POST",
            "Método PUT",
            "Método DELETE",
            "JSON",
            "Códigos HTTP",
            "Autenticación",
            "Tokens",
            "FastAPI",
        ],
        "proyecto": "API de biblioteca",
    },
    14: {
        "nombre": "Inteligencia artificial aplicada",
        "descripcion": (
            "Integrar modelos de inteligencia artificial "
            "dentro de aplicaciones."
        ),
        "temas": [
            "Introducción a la inteligencia artificial",
            "Modelos de lenguaje",
            "Prompts",
            "APIs de IA",
            "Anthropic Claude",
            "OpenAI",
            "Agentes",
            "Memoria",
            "RAG",
            "Embeddings",
            "Bases de datos vectoriales",
        ],
        "proyecto": "Agente educativo con inteligencia artificial",
    },
    15: {
        "nombre": "Ingeniería de software",
        "descripcion": (
            "Organizar y construir proyectos profesionales."
        ),
        "temas": [
            "Clean Code",
            "Principios SOLID",
            "Arquitectura MVC",
            "Diseño modular",
            "UML",
            "Documentación",
            "Testing",
            "Seguridad básica",
            "Variables de entorno",
            "Despliegue",
        ],
        "proyecto": "Aplicación profesional final",
    },
}


INSTRUCCION_SISTEMA = """
Eres Proyecto Proga IA, un tutor académico especializado en programación.

Tu objetivo es enseñar programación desde cero hasta un nivel avanzado,
siguiendo la ruta de aprendizaje entregada en el contexto.

Debes enseñar como un profesor paciente, claro y organizado.

Forma de enseñar:
1. Explica el concepto con palabras sencillas.
2. Presenta un ejemplo cotidiano.
3. Muestra un ejemplo corto de código.
4. Explica las líneas importantes.
5. Propón un ejercicio guiado.
6. Propón un ejercicio para que el estudiante lo resuelva.
7. Recomienda realizar un quiz para comprobar el aprendizaje.

Reglas de aprendizaje:
- Adapta la dificultad al nivel actual del estudiante.
- No des por aprobado un tema solo porque fue explicado.
- El estudiante debe obtener al menos 80% en el quiz.
- Si falla, explica qué concepto debe repasar.
- No avances al siguiente tema si el estudiante todavía no aprobó el actual.
- Cuando complete un nivel, recomienda realizar su proyecto.
- Si pide aprender desde cero, empieza desde el primer tema disponible.
- Si pide continuar, enseña el tema actual indicado en el contexto.

Puedes ayudar con:
- Python
- Algoritmos
- Lógica
- Estructuras de datos
- Programación orientada a objetos
- Archivos
- Bases de datos
- Desarrollo web
- APIs
- Git y GitHub
- Inteligencia artificial
- Ingeniería de software
- Corrección de código
- Pruebas de escritorio
- Ejercicios y proyectos

Reglas de idioma:
- Responde siempre en español.
- Usa palabras fáciles.
- Evita tecnicismos innecesarios.
- No trates al estudiante como experto.

Reglas de formato:
- Usa párrafos cortos.
- No uses tablas.
- No uses separadores como ---.
- No uses demasiados títulos.
- No uses Markdown complejo.
- No pongas emojis.
- No repitas la pregunta.
- No hagas respuestas exageradamente largas.

Cuando muestres código:
- Usa un solo bloque de código por respuesta.
- Explica el código después del bloque.
- Evita entregar soluciones demasiado avanzadas para el nivel actual.

Cuando corrijas código:
- Identifica el error.
- Explica por qué sucede.
- Presenta la corrección.
- Explica qué cambió.
- Propón una pequeña práctica similar.

Uso del PDF:
- Si hay un PDF cargado, úsalo como fuente principal.
- No inventes información que no aparezca en el PDF.
- Si el PDF no contiene la respuesta, indícalo brevemente.
- Después puedes complementar con conocimientos generales.
""".strip()



# -------------------------------------------------
# MODELOS DE LA BASE DE DATOS
# -------------------------------------------------

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(
        db.String(180),
        unique=True,
        nullable=False,
        index=True,
    )
    password_hash = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    progreso = db.relationship(
        "Progreso",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan",
    )
    conversaciones = db.relationship(
        "Conversacion",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
    resultados_quiz = db.relationship(
        "ResultadoQuiz",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )


class Progreso(db.Model):
    __tablename__ = "progresos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        unique=True,
        nullable=False,
        index=True,
    )

    nivel_actual = db.Column(db.Integer, default=1, nullable=False)
    tema_actual = db.Column(db.String(250), nullable=False)
    porcentaje_general = db.Column(db.Integer, default=0, nullable=False)

    consultas = db.Column(db.Integer, default=0, nullable=False)
    ejercicios = db.Column(db.Integer, default=0, nullable=False)
    quizzes_realizados = db.Column(db.Integer, default=0, nullable=False)
    quizzes_aprobados = db.Column(db.Integer, default=0, nullable=False)

    temas_estudiados_json = db.Column(db.Text, default="[]", nullable=False)
    temas_aprobados_json = db.Column(db.Text, default="[]", nullable=False)
    temas_por_repasar_json = db.Column(db.Text, default="[]", nullable=False)
    niveles_completados_json = db.Column(db.Text, default="[]", nullable=False)
    proyectos_desbloqueados_json = db.Column(
        db.Text,
        default="[]",
        nullable=False,
    )

    curso_completado = db.Column(db.Boolean, default=False, nullable=False)

    usuario = db.relationship("Usuario", back_populates="progreso")


class Conversacion(db.Model):
    __tablename__ = "conversaciones"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )
    pregunta = db.Column(db.Text, nullable=False)
    respuesta = db.Column(db.Text, nullable=False)
    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    usuario = db.relationship("Usuario", back_populates="conversaciones")


class ResultadoQuiz(db.Model):
    __tablename__ = "resultados_quiz"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )
    tema = db.Column(db.String(250), nullable=False)
    correctas = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    porcentaje = db.Column(db.Integer, nullable=False)
    aprobado = db.Column(db.Boolean, nullable=False)
    partes_a_repasar_json = db.Column(db.Text, default="[]", nullable=False)
    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    usuario = db.relationship("Usuario", back_populates="resultados_quiz")


class MaterialPDF(db.Model):
    __tablename__ = "materiales_pdf"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        unique=True,
        nullable=False,
        index=True,
    )
    nombre = db.Column(db.String(255), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    paginas = db.Column(db.Integer, default=0, nullable=False)
    fecha_actualizacion = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


# -------------------------------------------------
# SESIONES Y AUTENTICACIÓN
# -------------------------------------------------

@login_manager.user_loader
def cargar_usuario(usuario_id: str) -> Usuario | None:
    try:
        return db.session.get(Usuario, int(usuario_id))
    except (TypeError, ValueError):
        return None


@login_manager.unauthorized_handler
def usuario_no_autorizado():
    rutas_api = {
        "/progreso",
        "/silabo",
        "/clase-actual",
        "/proyecto-actual",
        "/historial",
        "/limpiar-historial",
        "/reiniciar-progreso",
        "/generar-quiz",
        "/guardar-resultado-quiz",
        "/subir-pdf",
        "/consultar",
    }

    if request.path in rutas_api:
        return respuesta_error(
            "Tu sesión terminó. Inicia sesión nuevamente.",
            401,
        )

    return redirect(url_for("login"))


# -------------------------------------------------
# PDF ACTUAL DE CADA USUARIO
# -------------------------------------------------


def obtener_material_actual() -> dict:
    material = db.session.execute(
        select(MaterialPDF).where(
            MaterialPDF.usuario_id == current_user.id
        )
    ).scalar_one_or_none()

    if material is None:
        return {
            "nombre": None,
            "texto": "",
            "paginas": 0,
        }

    return {
        "nombre": material.nombre,
        "texto": material.texto,
        "paginas": material.paginas,
    }


# -------------------------------------------------
# FUNCIONES GENERALES
# -------------------------------------------------

def respuesta_error(mensaje: str, estado: int = 400):
    return jsonify({
        "ok": False,
        "respuesta": mensaje,
    }), estado


def lista_desde_json(valor: str | None) -> list:
    if not valor:
        return []

    try:
        resultado = json.loads(valor)
    except (json.JSONDecodeError, TypeError):
        return []

    return resultado if isinstance(resultado, list) else []


def lista_a_json(valor: list) -> str:
    return json.dumps(
        valor,
        ensure_ascii=False,
    )


def obtener_progreso_inicial() -> dict:
    primer_tema = SILABO[1]["temas"][0]

    return {
        "nivel_actual": 1,
        "tema_actual": primer_tema,
        "porcentaje_general": 0,
        "consultas": 0,
        "ejercicios": 0,
        "quizzes_realizados": 0,
        "quizzes_aprobados": 0,
        "temas_estudiados": [],
        "temas_aprobados": [],
        "temas_por_repasar": [],
        "niveles_completados": [],
        "proyectos_desbloqueados": [],
        "curso_completado": False,
    }


def crear_progreso_usuario(usuario_id: int) -> Progreso:
    inicial = obtener_progreso_inicial()

    progreso = Progreso(
        usuario_id=usuario_id,
        nivel_actual=inicial["nivel_actual"],
        tema_actual=inicial["tema_actual"],
        porcentaje_general=inicial["porcentaje_general"],
        consultas=0,
        ejercicios=0,
        quizzes_realizados=0,
        quizzes_aprobados=0,
        temas_estudiados_json="[]",
        temas_aprobados_json="[]",
        temas_por_repasar_json="[]",
        niveles_completados_json="[]",
        proyectos_desbloqueados_json="[]",
        curso_completado=False,
    )

    db.session.add(progreso)
    db.session.flush()

    return progreso


def obtener_modelo_progreso() -> Progreso:
    progreso = db.session.execute(
        select(Progreso).where(
            Progreso.usuario_id == current_user.id
        )
    ).scalar_one_or_none()

    if progreso is None:
        progreso = crear_progreso_usuario(int(current_user.id))
        db.session.commit()

    return progreso


def progreso_a_dict(progreso: Progreso) -> dict:
    return {
        "nivel_actual": progreso.nivel_actual,
        "tema_actual": progreso.tema_actual,
        "porcentaje_general": progreso.porcentaje_general,
        "consultas": progreso.consultas,
        "ejercicios": progreso.ejercicios,
        "quizzes_realizados": progreso.quizzes_realizados,
        "quizzes_aprobados": progreso.quizzes_aprobados,
        "temas_estudiados": lista_desde_json(
            progreso.temas_estudiados_json
        ),
        "temas_aprobados": lista_desde_json(
            progreso.temas_aprobados_json
        ),
        "temas_por_repasar": lista_desde_json(
            progreso.temas_por_repasar_json
        ),
        "niveles_completados": lista_desde_json(
            progreso.niveles_completados_json
        ),
        "proyectos_desbloqueados": lista_desde_json(
            progreso.proyectos_desbloqueados_json
        ),
        "curso_completado": bool(progreso.curso_completado),
    }


def guardar_dict_en_progreso(
    modelo: Progreso,
    datos: dict,
    confirmar: bool = True,
) -> None:
    modelo.nivel_actual = int(datos.get("nivel_actual", 1))
    modelo.tema_actual = str(
        datos.get("tema_actual", SILABO[1]["temas"][0])
    )
    modelo.porcentaje_general = int(
        datos.get("porcentaje_general", 0)
    )
    modelo.consultas = int(datos.get("consultas", 0))
    modelo.ejercicios = int(datos.get("ejercicios", 0))
    modelo.quizzes_realizados = int(
        datos.get("quizzes_realizados", 0)
    )
    modelo.quizzes_aprobados = int(
        datos.get("quizzes_aprobados", 0)
    )

    modelo.temas_estudiados_json = lista_a_json(
        datos.get("temas_estudiados", [])
    )
    modelo.temas_aprobados_json = lista_a_json(
        datos.get("temas_aprobados", [])
    )
    modelo.temas_por_repasar_json = lista_a_json(
        datos.get("temas_por_repasar", [])
    )
    modelo.niveles_completados_json = lista_a_json(
        datos.get("niveles_completados", [])
    )
    modelo.proyectos_desbloqueados_json = lista_a_json(
        datos.get("proyectos_desbloqueados", [])
    )
    modelo.curso_completado = bool(
        datos.get("curso_completado", False)
    )

    if confirmar:
        db.session.commit()


def todos_los_temas() -> list[str]:
    temas: list[str] = []

    for nivel in SILABO.values():
        temas.extend(nivel["temas"])

    return temas


def calcular_porcentaje_general(progreso: dict) -> int:
    total = len(todos_los_temas())

    if total == 0:
        return 0

    aprobados = len(set(progreso.get("temas_aprobados", [])))

    return min(
        100,
        round((aprobados / total) * 100),
    )


def obtener_primer_tema_pendiente(
    nivel_numero: int,
    temas_aprobados: list[str],
) -> str | None:
    nivel = SILABO.get(nivel_numero)

    if not nivel:
        return None

    for tema in nivel["temas"]:
        if tema not in temas_aprobados:
            return tema

    return None


def actualizar_ruta_aprendizaje(progreso: dict) -> None:
    temas_aprobados = progreso.setdefault(
        "temas_aprobados",
        [],
    )

    niveles_completados: list[int] = []
    proyectos_desbloqueados: list[str] = []

    for numero, nivel in SILABO.items():
        completado = all(
            tema in temas_aprobados
            for tema in nivel["temas"]
        )

        if completado:
            niveles_completados.append(numero)
            proyectos_desbloqueados.append(
                nivel["proyecto"]
            )

    progreso["niveles_completados"] = niveles_completados
    progreso["proyectos_desbloqueados"] = proyectos_desbloqueados

    tema_actual = None
    nivel_actual = 1

    for numero in SILABO:
        pendiente = obtener_primer_tema_pendiente(
            numero,
            temas_aprobados,
        )

        if pendiente is not None:
            nivel_actual = numero
            tema_actual = pendiente
            break

    if tema_actual is None:
        progreso["curso_completado"] = True
        progreso["nivel_actual"] = len(SILABO)
        progreso["tema_actual"] = "Curso completado"
    else:
        progreso["curso_completado"] = False
        progreso["nivel_actual"] = nivel_actual
        progreso["tema_actual"] = tema_actual

    progreso["porcentaje_general"] = (
        calcular_porcentaje_general(progreso)
    )


def cargar_progreso() -> dict:
    modelo = obtener_modelo_progreso()
    progreso = progreso_a_dict(modelo)

    actualizar_ruta_aprendizaje(progreso)
    guardar_dict_en_progreso(modelo, progreso)

    return progreso


def obtener_clase_actual(
    progreso: dict | None = None,
) -> dict | None:
    if progreso is None:
        progreso = cargar_progreso()

    actualizar_ruta_aprendizaje(progreso)

    if progreso.get("curso_completado"):
        return None

    numero = int(progreso["nivel_actual"])
    nivel = SILABO[numero]

    return {
        "nivel": numero,
        "unidad": nivel["nombre"],
        "descripcion": nivel["descripcion"],
        "tema": progreso["tema_actual"],
        "proyecto": nivel["proyecto"],
        "porcentaje_general": progreso["porcentaje_general"],
    }


def detectar_tema(pregunta: str) -> str:
    texto = pregunta.casefold()

    grupos = {
        "Aprendizaje desde cero": [
            "desde cero",
            "aprender programación",
            "aprender programacion",
            "aprender python",
            "sílabo",
            "silabo",
            "curso completo",
            "ruta de aprendizaje",
            "empezar a programar",
            "continuar aprendizaje",
        ],
        "Variables": [
            "variable",
            "variables",
            "input",
            "print",
            "tipo de dato",
            "entero",
            "float",
            "string",
            "booleano",
        ],
        "Condicionales": [
            "condicional",
            "condicionales",
            "if",
            "elif",
            "else",
        ],
        "Ciclos": [
            "ciclo",
            "ciclos",
            "bucle",
            "for",
            "while",
            "range",
            "contador",
            "acumulador",
        ],
        "Listas": [
            "lista",
            "listas",
            "append",
            "remove",
            "pop",
            "insert",
            "índice",
            "indice",
        ],
        "Matrices": [
            "matriz",
            "matrices",
            "fila",
            "filas",
            "columna",
            "columnas",
            "bidimensional",
        ],
        "Diccionarios": [
            "diccionario",
            "diccionarios",
            "clave",
            "claves",
            "keys",
            "values",
        ],
        "Funciones": [
            "función",
            "funcion",
            "funciones",
            "def",
            "return",
            "parámetro",
            "parametro",
        ],
        "Programación orientada a objetos": [
            "clase",
            "objeto",
            "constructor",
            "herencia",
            "polimorfismo",
            "encapsulamiento",
        ],
        "Bases de datos": [
            "base de datos",
            "sql",
            "sqlite",
            "mysql",
            "postgresql",
            "crud",
        ],
        "Desarrollo web": [
            "html",
            "css",
            "javascript",
            "flask",
            "página web",
            "pagina web",
            "frontend",
            "backend",
        ],
        "APIs": [
            "api",
            "endpoint",
            "rest",
        ],
        "Inteligencia artificial": [
            "inteligencia artificial",
            "agente",
            "claude",
            "openai",
            "chatgpt",
            "rag",
            "embedding",
        ],
        "Algoritmos": [
            "algoritmo",
            "algoritmos",
            "pseudocódigo",
            "pseudocodigo",
            "diagrama de flujo",
            "big o",
            "ordenamiento",
            "búsqueda",
            "busqueda",
        ],
        "Prueba de escritorio": [
            "prueba de escritorio",
            "tabla de seguimiento",
            "seguir variables",
        ],
        "Errores de código": [
            "error",
            "no funciona",
            "depurar",
            "debug",
            "corregir código",
            "corregir codigo",
            "revisar código",
            "revisar codigo",
        ],
    }

    for tema, palabras in grupos.items():
        if any(
            palabra.casefold() in texto
            for palabra in palabras
        ):
            return tema

    for nivel in SILABO.values():
        for tema in nivel["temas"]:
            if tema.casefold() in texto:
                return tema

    return "Otros"


def es_ejercicio(pregunta: str) -> bool:
    texto = pregunta.casefold()

    palabras = [
        "ejercicio",
        "ejercicios",
        "practicar",
        "práctica",
        "practica",
        "quiz",
        "examen",
        "prueba",
        "reto",
        "actividad",
    ]

    return any(
        palabra in texto
        for palabra in palabras
    )


def registrar_progreso_consulta(pregunta: str) -> None:
    modelo = obtener_modelo_progreso()
    progreso = progreso_a_dict(modelo)

    progreso["consultas"] += 1

    tema_detectado = detectar_tema(pregunta)

    if (
        tema_detectado != "Otros"
        and tema_detectado
        not in progreso["temas_estudiados"]
    ):
        progreso["temas_estudiados"].append(
            tema_detectado
        )

    clase = obtener_clase_actual(progreso)

    if clase:
        tema_actual = clase["tema"]

        if tema_actual not in progreso["temas_estudiados"]:
            progreso["temas_estudiados"].append(
                tema_actual
            )

    if es_ejercicio(pregunta):
        progreso["ejercicios"] += 1

    actualizar_ruta_aprendizaje(progreso)
    guardar_dict_en_progreso(modelo, progreso)


# -------------------------------------------------
# HISTORIAL POR USUARIO
# -------------------------------------------------

def guardar_historial(
    pregunta: str,
    respuesta: str,
) -> None:
    conversacion = Conversacion(
        usuario_id=current_user.id,
        pregunta=pregunta,
        respuesta=respuesta[:5000],
    )

    db.session.add(conversacion)
    db.session.commit()


# -------------------------------------------------
# CLAUDE
# -------------------------------------------------

def obtener_cliente_claude() -> tuple[Anthropic, str]:
    api_key = os.getenv(
        "ANTHROPIC_API_KEY",
        "",
    ).strip()

    if (
        not api_key
        or api_key == "PEGA_AQUI_TU_CLAVE"
    ):
        raise ValueError(
            "Falta la clave de Anthropic. "
            "Revisa tu archivo .env."
        )

    modelo = (
        os.getenv(
            "ANTHROPIC_MODEL",
            DEFAULT_MODEL,
        ).strip()
        or DEFAULT_MODEL
    )

    return Anthropic(api_key=api_key), modelo


def extraer_bloques_texto(respuesta) -> str:
    bloques = [
        bloque.text
        for bloque in respuesta.content
        if getattr(bloque, "type", "") == "text"
    ]

    texto = "\n".join(bloques).strip()

    if not texto:
        raise RuntimeError(
            "La IA no devolvió una respuesta de texto."
        )

    return texto


def obtener_contexto_aprendizaje() -> str:
    progreso = cargar_progreso()
    clase = obtener_clase_actual(progreso)

    if clase:
        nivel_actual = clase["nivel"]
        unidad_actual = clase["unidad"]
        tema_actual = clase["tema"]
        proyecto_actual = clase["proyecto"]
    else:
        nivel_actual = len(SILABO)
        unidad_actual = "Curso completado"
        tema_actual = "Curso completado"
        proyecto_actual = SILABO[len(SILABO)]["proyecto"]

    return f"""
Estudiante: {current_user.nombre}
Nivel actual: {nivel_actual}
Unidad actual: {unidad_actual}
Tema actual: {tema_actual}
Proyecto del nivel: {proyecto_actual}
Porcentaje general: {progreso.get("porcentaje_general", 0)}%
Temas aprobados recientemente: {progreso.get("temas_aprobados", [])[-10:]}
Temas por repasar: {progreso.get("temas_por_repasar", [])[-10:]}

Adapta la explicación al nivel actual.
No marques un tema como aprobado sin un quiz.
No avances automáticamente al siguiente tema.
""".strip()


def extraer_texto_pdf(
    ruta_pdf: Path,
) -> tuple[str, int, bool]:
    lector = PdfReader(str(ruta_pdf))

    if lector.is_encrypted:
        raise ValueError(
            "El PDF tiene contraseña y no se puede leer."
        )

    partes: list[str] = []
    caracteres = 0
    recortado = False

    for pagina in lector.pages:
        texto_pagina = (
            pagina.extract_text() or ""
        ).strip()

        if not texto_pagina:
            continue

        disponible = MAX_PDF_CHARACTERS - caracteres

        if disponible <= 0:
            recortado = True
            break

        if len(texto_pagina) > disponible:
            partes.append(
                texto_pagina[:disponible]
            )
            recortado = True
            break

        partes.append(texto_pagina)
        caracteres += len(texto_pagina)

    return (
        "\n\n".join(partes).strip(),
        len(lector.pages),
        recortado,
    )


def obtener_respuesta_claude(
    pregunta: str,
) -> str:
    cliente, modelo = obtener_cliente_claude()
    material = obtener_material_actual()

    if material["texto"]:
        contexto_pdf = f"""
Hay un PDF cargado llamado:
{material["nombre"]}

Contenido del PDF:
{material["texto"]}
""".strip()
    else:
        contexto_pdf = (
            "No hay un PDF cargado. "
            "Puedes usar conocimientos generales de programación."
        )

    mensaje_usuario = f"""
{obtener_contexto_aprendizaje()}

{contexto_pdf}

Pregunta del estudiante:
{pregunta}

Responde de forma clara y fácil de entender.

Cuando pida continuar:
- Enseña únicamente el tema actual.
- Incluye explicación, ejemplo y práctica.
- Recomienda usar el botón del quiz.
""".strip()

    respuesta = cliente.messages.create(
        model=modelo,
        max_tokens=1800,
        system=INSTRUCCION_SISTEMA,
        messages=[
            {
                "role": "user",
                "content": mensaje_usuario,
            }
        ],
    )

    return extraer_bloques_texto(respuesta)


# -------------------------------------------------
# QUIZZES
# -------------------------------------------------

def extraer_json_de_respuesta(texto: str) -> dict:
    texto = (
        texto
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    inicio = texto.find("{")
    final = texto.rfind("}")

    if inicio == -1 or final == -1:
        raise ValueError(
            "La IA no devolvió un JSON válido."
        )

    try:
        resultado = json.loads(
            texto[inicio:final + 1]
        )
    except json.JSONDecodeError as error:
        raise ValueError(
            "La IA devolvió un quiz con formato inválido."
        ) from error

    if not isinstance(resultado, dict):
        raise ValueError(
            "El quiz recibido no es válido."
        )

    return resultado


def validar_quiz(quiz: dict) -> dict:
    tema = str(quiz.get("tema", "")).strip()
    preguntas = quiz.get("preguntas", [])

    if not tema:
        raise ValueError(
            "El quiz no contiene un tema."
        )

    if (
        not isinstance(preguntas, list)
        or len(preguntas) != 5
    ):
        raise ValueError(
            "El quiz debe contener exactamente 5 preguntas."
        )

    resultado = {
        "tema": tema,
        "preguntas": [],
    }

    for numero, pregunta in enumerate(
        preguntas,
        start=1,
    ):
        if not isinstance(pregunta, dict):
            raise ValueError(
                f"La pregunta {numero} no es válida."
            )

        opciones = pregunta.get("opciones", {})

        opciones_limpias = {
            letra: str(
                opciones.get(letra, "")
            ).strip()
            for letra in ("A", "B", "C")
        }

        correcta = str(
            pregunta.get("correcta", "")
        ).strip().upper()

        texto_pregunta = str(
            pregunta.get("pregunta", "")
        ).strip()

        if not texto_pregunta:
            raise ValueError(
                f"La pregunta {numero} está vacía."
            )

        if any(
            not valor
            for valor in opciones_limpias.values()
        ):
            raise ValueError(
                f"La pregunta {numero} no tiene "
                "las opciones A, B y C."
            )

        if correcta not in {"A", "B", "C"}:
            raise ValueError(
                f"La respuesta de la pregunta "
                f"{numero} no es válida."
            )

        resultado["preguntas"].append({
            "pregunta": texto_pregunta,
            "opciones": opciones_limpias,
            "correcta": correcta,
            "explicacion": str(
                pregunta.get(
                    "explicacion",
                    "Revisa nuevamente el concepto.",
                )
            ).strip(),
            "parte_a_repasar": str(
                pregunta.get(
                    "parte_a_repasar",
                    tema,
                )
            ).strip(),
        })

    return resultado


def generar_quiz_con_claude(
    tema: str,
) -> dict:
    cliente, modelo = obtener_cliente_claude()
    progreso = cargar_progreso()

    instruccion = f"""
Crea un quiz educativo sobre: "{tema}".

Nivel del estudiante: {progreso["nivel_actual"]}.

Condiciones:
- Exactamente 5 preguntas.
- Opciones A, B y C.
- Solo una respuesta correcta.
- Mezcla teoría y código.
- Incluye explicación.
- Incluye la parte que debe repasar.

Devuelve únicamente JSON válido:

{{
  "tema": "{tema}",
  "preguntas": [
    {{
      "pregunta": "Texto",
      "opciones": {{
        "A": "Opción A",
        "B": "Opción B",
        "C": "Opción C"
      }},
      "correcta": "A",
      "explicacion": "Explicación",
      "parte_a_repasar": "Concepto"
    }}
  ]
}}
""".strip()

    respuesta = cliente.messages.create(
        model=modelo,
        max_tokens=1800,
        system=(
            "Eres profesor de programación. "
            "Devuelve exclusivamente JSON válido."
        ),
        messages=[
            {
                "role": "user",
                "content": instruccion,
            }
        ],
    )

    return validar_quiz(
        extraer_json_de_respuesta(
            extraer_bloques_texto(respuesta)
        )
    )


def guardar_resultado_quiz_en_progreso(
    tema: str,
    correctas: int,
    total: int,
    partes_a_repasar: list[str],
) -> dict:
    if total <= 0:
        raise ValueError(
            "El total de preguntas no es válido."
        )

    if correctas < 0 or correctas > total:
        raise ValueError(
            "La cantidad de respuestas correctas "
            "no es válida."
        )

    porcentaje = round(
        (correctas / total) * 100
    )
    aprobado = porcentaje >= NOTA_MINIMA

    modelo = obtener_modelo_progreso()
    progreso = progreso_a_dict(modelo)

    progreso["quizzes_realizados"] += 1

    if tema not in progreso["temas_estudiados"]:
        progreso["temas_estudiados"].append(tema)

    if aprobado:
        progreso["quizzes_aprobados"] += 1

        if tema not in progreso["temas_aprobados"]:
            progreso["temas_aprobados"].append(tema)

        if tema in progreso["temas_por_repasar"]:
            progreso["temas_por_repasar"].remove(tema)
    else:
        if tema not in progreso["temas_por_repasar"]:
            progreso["temas_por_repasar"].append(tema)

    resultado = ResultadoQuiz(
        usuario_id=current_user.id,
        tema=tema,
        correctas=correctas,
        total=total,
        porcentaje=porcentaje,
        aprobado=aprobado,
        partes_a_repasar_json=lista_a_json(
            partes_a_repasar
        ),
    )

    db.session.add(resultado)

    actualizar_ruta_aprendizaje(progreso)
    guardar_dict_en_progreso(
        modelo,
        progreso,
        confirmar=False,
    )
    db.session.commit()

    return {
        "aprobado": aprobado,
        "porcentaje": porcentaje,
        "nota_minima": NOTA_MINIMA,
        "progreso": progreso,
        "siguiente_clase": obtener_clase_actual(
            progreso
        ),
    }


# -------------------------------------------------
# RUTAS DE AUTENTICACIÓN
# -------------------------------------------------

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    if request.method == "GET":
        return render_template("registro.html")

    nombre = request.form.get(
        "nombre",
        "",
    ).strip()

    correo = request.form.get(
        "correo",
        "",
    ).strip().lower()

    password = request.form.get(
        "password",
        "",
    )

    confirmar_password = request.form.get(
        "confirmar_password",
        "",
    )

    if not nombre or not correo or not password:
        return render_template(
            "registro.html",
            error="Completa todos los campos.",
            nombre=nombre,
            correo=correo,
        )

    if "@" not in correo or "." not in correo:
        return render_template(
            "registro.html",
            error="Escribe un correo válido.",
            nombre=nombre,
            correo=correo,
        )

    if len(password) < 8:
        return render_template(
            "registro.html",
            error=(
                "La contraseña debe tener "
                "al menos 8 caracteres."
            ),
            nombre=nombre,
            correo=correo,
        )

    if password != confirmar_password:
        return render_template(
            "registro.html",
            error="Las contraseñas no coinciden.",
            nombre=nombre,
            correo=correo,
        )

    existente = db.session.execute(
        select(Usuario).where(
            Usuario.correo == correo
        )
    ).scalar_one_or_none()

    if existente:
        return render_template(
            "registro.html",
            error=(
                "Ya existe una cuenta con ese correo."
            ),
            nombre=nombre,
            correo=correo,
        )

    usuario = Usuario(
        nombre=nombre,
        correo=correo,
        password_hash=generate_password_hash(
            password
        ),
    )

    db.session.add(usuario)
    db.session.flush()

    crear_progreso_usuario(usuario.id)
    db.session.commit()

    login_user(usuario)

    return redirect(url_for("inicio"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    if request.method == "GET":
        return render_template("login.html")

    correo = request.form.get(
        "correo",
        "",
    ).strip().lower()

    password = request.form.get(
        "password",
        "",
    )

    usuario = db.session.execute(
        select(Usuario).where(
            Usuario.correo == correo
        )
    ).scalar_one_or_none()

    if (
        usuario is None
        or not check_password_hash(
            usuario.password_hash,
            password,
        )
    ):
        return render_template(
            "login.html",
            error="Correo o contraseña incorrectos.",
            correo=correo,
        )

    login_user(usuario)

    return redirect(url_for("inicio"))


@app.post("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# -------------------------------------------------
# RUTAS PRINCIPALES
# -------------------------------------------------

@app.get("/")
@login_required
def inicio():
    return render_template(
        "index.html",
        usuario=current_user,
    )


@app.get("/progreso")
@login_required
def obtener_progreso():
    progreso = cargar_progreso()

    return jsonify({
        "ok": True,
        "progreso": progreso,
        "clase_actual": obtener_clase_actual(
            progreso
        ),
    })


@app.get("/silabo")
@login_required
def obtener_silabo():
    progreso = cargar_progreso()

    niveles = []

    for numero, nivel in SILABO.items():
        niveles.append({
            "numero": numero,
            "nombre": nivel["nombre"],
            "descripcion": nivel["descripcion"],
            "temas": nivel["temas"],
            "proyecto": nivel["proyecto"],
            "completado": (
                numero
                in progreso["niveles_completados"]
            ),
            "desbloqueado": (
                numero <= progreso["nivel_actual"]
                or progreso["curso_completado"]
            ),
        })

    return jsonify({
        "ok": True,
        "niveles": niveles,
        "nivel_actual": progreso["nivel_actual"],
        "tema_actual": progreso["tema_actual"],
        "porcentaje_general": progreso["porcentaje_general"],
    })


@app.get("/clase-actual")
@login_required
def clase_actual():
    progreso = cargar_progreso()
    clase = obtener_clase_actual(progreso)

    if clase is None:
        return jsonify({
            "ok": True,
            "completado": True,
            "mensaje": (
                "Has completado todos los niveles "
                "del curso de programación."
            ),
            "porcentaje_general": 100,
        })

    return jsonify({
        "ok": True,
        "completado": False,
        "clase": clase,
    })


@app.get("/proyecto-actual")
@login_required
def proyecto_actual():
    progreso = cargar_progreso()
    proyectos = progreso.get(
        "proyectos_desbloqueados",
        [],
    )

    if not proyectos:
        return respuesta_error(
            "Todavía no has desbloqueado "
            "un proyecto de nivel.",
            404,
        )

    return jsonify({
        "ok": True,
        "proyectos": proyectos,
        "ultimo_proyecto": proyectos[-1],
    })


@app.get("/historial")
@login_required
def obtener_historial():
    conversaciones = db.session.execute(
        select(Conversacion)
        .where(
            Conversacion.usuario_id == current_user.id
        )
        .order_by(Conversacion.fecha.desc())
        .limit(MAX_HISTORIAL)
    ).scalars().all()

    historial = [
        {
            "id": conversacion.id,
            "fecha": conversacion.fecha.strftime(
                "%d/%m/%Y %H:%M"
            ),
            "pregunta": conversacion.pregunta,
            "respuesta": conversacion.respuesta,
        }
        for conversacion in conversaciones
    ]

    return jsonify({
        "ok": True,
        "historial": historial,
    })


@app.post("/limpiar-historial")
@login_required
def limpiar_historial():
    db.session.execute(
        delete(Conversacion).where(
            Conversacion.usuario_id == current_user.id
        )
    )
    db.session.commit()

    return jsonify({
        "ok": True,
        "respuesta": "Tu historial fue eliminado.",
    })


@app.post("/reiniciar-progreso")
@login_required
def reiniciar_progreso():
    modelo = obtener_modelo_progreso()
    inicial = obtener_progreso_inicial()

    guardar_dict_en_progreso(
        modelo,
        inicial,
        confirmar=False,
    )

    db.session.execute(
        delete(ResultadoQuiz).where(
            ResultadoQuiz.usuario_id == current_user.id
        )
    )
    db.session.commit()

    return jsonify({
        "ok": True,
        "respuesta": "Tu progreso fue reiniciado.",
        "progreso": inicial,
        "clase_actual": obtener_clase_actual(
            inicial
        ),
    })


# -------------------------------------------------
# QUIZ
# -------------------------------------------------

@app.post("/generar-quiz")
@login_required
@limiter.limit("10 per hour")
def generar_quiz():
    datos = request.get_json(
        silent=True
    ) or {}

    tema = str(
        datos.get("tema", "")
    ).strip()

    progreso = cargar_progreso()

    if not tema:
        tema = progreso["tema_actual"]

    try:
        quiz = generar_quiz_con_claude(tema)

        return jsonify({
            "ok": True,
            "quiz": quiz,
            "nota_minima": NOTA_MINIMA,
        })

    except ValueError as error:
        return respuesta_error(
            str(error),
            500,
        )

    except Exception:
        app.logger.exception(
            "Error al generar quiz"
        )

        return respuesta_error(
            "No se pudo generar el quiz. "
            "Intenta nuevamente.",
            502,
        )


@app.post("/guardar-resultado-quiz")
@login_required
def guardar_resultado_quiz():
    datos = request.get_json(
        silent=True
    ) or {}

    tema = str(
        datos.get("tema", "")
    ).strip()

    partes = datos.get(
        "partes_a_repasar",
        [],
    )

    try:
        correctas = int(
            datos.get("correctas", 0)
        )
        total = int(
            datos.get("total", 0)
        )
    except (TypeError, ValueError):
        return respuesta_error(
            "Las calificaciones no son válidas."
        )

    if not tema:
        return respuesta_error(
            "No se recibió el tema del quiz."
        )

    if not isinstance(partes, list):
        partes = []

    partes_limpias: list[str] = []

    for parte in partes:
        texto = str(parte).strip()

        if texto and texto not in partes_limpias:
            partes_limpias.append(texto)

    try:
        resultado = guardar_resultado_quiz_en_progreso(
            tema=tema,
            correctas=correctas,
            total=total,
            partes_a_repasar=partes_limpias,
        )

        return jsonify({
            "ok": True,
            **resultado,
        })

    except ValueError as error:
        return respuesta_error(str(error))


# -------------------------------------------------
# PDF
# -------------------------------------------------

@app.post("/subir-pdf")
@login_required
@limiter.limit("10 per hour")
def subir_pdf():
    if "archivo" not in request.files:
        return respuesta_error(
            "No se recibió ningún archivo PDF."
        )

    archivo = request.files["archivo"]
    nombre_original = archivo.filename or ""

    if not nombre_original.strip():
        return respuesta_error(
            "Selecciona un PDF antes de subirlo."
        )

    if Path(nombre_original).suffix.lower() != ".pdf":
        return respuesta_error(
            "Solo puedes subir archivos PDF."
        )

    nombre_seguro = (
        secure_filename(nombre_original)
        or "material.pdf"
    )

    ruta_guardada = (
        UPLOADS_DIR
        / f"{current_user.id}_{uuid4().hex}_{nombre_seguro}"
    )

    try:
        archivo.save(ruta_guardada)

        texto, paginas, recortado = extraer_texto_pdf(
            ruta_guardada
        )

    except Exception as error:
        ruta_guardada.unlink(
            missing_ok=True
        )

        return respuesta_error(
            f"No se pudo leer el PDF: {error}",
            422,
        )

    if not texto:
        ruta_guardada.unlink(
            missing_ok=True
        )

        return respuesta_error(
            "El PDF no tiene texto seleccionable. "
            "Probablemente es una imagen escaneada.",
            422,
        )

    material = db.session.execute(
        select(MaterialPDF).where(
            MaterialPDF.usuario_id == current_user.id
        )
    ).scalar_one_or_none()

    if material is None:
        material = MaterialPDF(
            usuario_id=current_user.id,
            nombre=nombre_seguro,
            texto=texto,
            paginas=paginas,
        )
        db.session.add(material)
    else:
        material.nombre = nombre_seguro
        material.texto = texto
        material.paginas = paginas
        material.fecha_actualizacion = datetime.utcnow()

    db.session.commit()

    ruta_guardada.unlink(missing_ok=True)

    detalle = f"Se leyeron {paginas} página(s)."

    if recortado:
        detalle += (
            " Solo se usó la parte inicial "
            "porque el PDF es muy extenso."
        )

    return jsonify({
        "ok": True,
        "respuesta": (
            f"PDF cargado correctamente: "
            f"{nombre_seguro}. {detalle}"
        ),
        "documento": nombre_seguro,
        "paginas": paginas,
        "recortado": recortado,
    })


# -------------------------------------------------
# CHAT
# -------------------------------------------------

@app.post("/consultar")
@login_required
@limiter.limit("20 per hour")
def consultar():
    datos = request.get_json(
        silent=True
    ) or {}

    pregunta = str(
        datos.get("pregunta", "")
    ).strip()

    if not pregunta:
        return respuesta_error(
            "Escribe una pregunta o pega tu código."
        )

    if len(pregunta) > MAX_QUESTION_CHARACTERS:
        return respuesta_error(
            "La pregunta es demasiado larga."
        )

    try:
        texto = obtener_respuesta_claude(
            pregunta
        )

        registrar_progreso_consulta(
            pregunta
        )

        guardar_historial(
            pregunta,
            texto,
        )

        progreso = cargar_progreso()

        return jsonify({
            "ok": True,
            "respuesta": texto,
            "progreso": progreso,
            "clase_actual": obtener_clase_actual(
                progreso
            ),
        })

    except ValueError as error:
        return respuesta_error(
            str(error),
            500,
        )

    except Exception:
        app.logger.exception(
            "Error al consultar la API"
        )

        return respuesta_error(
            "No se pudo conectar con la IA. "
            "Revisa la clave API, el modelo "
            "y tu conexión.",
            502,
        )


# -------------------------------------------------
# ERRORES
# -------------------------------------------------

@app.errorhandler(RequestEntityTooLarge)
def archivo_muy_grande(_error):
    return respuesta_error(
        "El PDF supera el tamaño máximo de 12 MB.",
        413,
    )


@app.errorhandler(404)
def ruta_no_encontrada(_error):
    if request.path.startswith("/static/"):
        return _error

    return respuesta_error(
        "La ruta solicitada no existe.",
        404,
    )


@app.errorhandler(405)
def metodo_no_permitido(_error):
    return respuesta_error(
        "El método utilizado no está permitido.",
        405,
    )


# -------------------------------------------------
# CREAR BASE DE DATOS
# -------------------------------------------------

with app.app_context():
    db.create_all()


# -------------------------------------------------
# EJECUTAR
# -------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )