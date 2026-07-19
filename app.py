from __future__ import annotations

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
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
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)
from chatgpt_agent import generar_reporte_chatgpt
from claude_agent import revisar_con_claude
from integrador import integrar_resultados

# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "clave-local-cambiar-en-produccion",
)

database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///rehabilitacion.db",
)

# Compatibilidad con algunas URL antiguas de PostgreSQL.
if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1,
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# -------------------------------------------------
# BASE DE DATOS Y SESIONES
# -------------------------------------------------

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = (
    "Inicia sesión para continuar."
)
login_manager.login_message_category = "warning"


# -------------------------------------------------
# MODELO DE USUARIO
# -------------------------------------------------

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    nombre = db.Column(
        db.String(100),
        nullable=False,
    )

    correo = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    fecha_registro = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    evaluaciones = db.relationship(
        "Evaluacion",
        backref="usuario",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def establecer_password(
        self,
        password: str,
    ) -> None:
        self.password_hash = generate_password_hash(
            password
        )

    def verificar_password(
        self,
        password: str,
    ) -> bool:
        return check_password_hash(
            self.password_hash,
            password,
        )


# -------------------------------------------------
# MODELO DE EVALUACIÓN
# -------------------------------------------------

class Evaluacion(db.Model):
    __tablename__ = "evaluaciones"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )

    nombre_paciente = db.Column(
        db.String(100),
        nullable=False,
    )

    edad = db.Column(
        db.Integer,
        nullable=False,
    )

    lesion = db.Column(
        db.String(150),
        nullable=False,
    )

    dolor = db.Column(
        db.Integer,
        nullable=False,
    )

    movilidad = db.Column(
        db.Integer,
        nullable=False,
    )

    fuerza = db.Column(
        db.Integer,
        nullable=False,
    )

    sesiones = db.Column(
        db.Integer,
        nullable=False,
    )

    cumplimiento = db.Column(
        db.Integer,
        nullable=False,
    )

    indice_progreso = db.Column(
        db.Float,
        nullable=False,
    )

    riesgo_retraso = db.Column(
        db.Float,
        nullable=False,
    )

    protocolo_recomendado = db.Column(
        db.String(200),
        nullable=False,
    )

    informe = db.Column(
        db.Text,
        nullable=True,
    )

    fecha = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


# -------------------------------------------------
# CARGAR USUARIO
# -------------------------------------------------

@login_manager.user_loader
def cargar_usuario(usuario_id: str):
    try:
        return db.session.get(
            Usuario,
            int(usuario_id),
        )
    except (TypeError, ValueError):
        return None


# -------------------------------------------------
# CREAR TABLAS
# -------------------------------------------------

with app.app_context():
    db.create_all()


# -------------------------------------------------
# REGISTRO
# -------------------------------------------------

@app.route(
    "/registro",
    methods=["GET", "POST"],
)
def registro():
    if current_user.is_authenticated:
        return redirect(
            url_for("index")
        )

    if request.method == "POST":
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

        if (
            not nombre
            or not correo
            or not password
            or not confirmar_password
        ):
            flash(
                "Completa todos los campos.",
                "danger",
            )
            return render_template(
                "registro.html"
            )

        if "@" not in correo or "." not in correo:
            flash(
                "Ingresa un correo válido.",
                "danger",
            )
            return render_template(
                "registro.html"
            )

        if len(password) < 8:
            flash(
                "La contraseña debe tener al menos 8 caracteres.",
                "danger",
            )
            return render_template(
                "registro.html"
            )

        if password != confirmar_password:
            flash(
                "Las contraseñas no coinciden.",
                "danger",
            )
            return render_template(
                "registro.html"
            )

        usuario_existente = Usuario.query.filter_by(
            correo=correo
        ).first()

        if usuario_existente:
            flash(
                "Ya existe una cuenta con ese correo.",
                "warning",
            )
            return render_template(
                "registro.html"
            )

        usuario = Usuario(
            nombre=nombre,
            correo=correo,
        )

        usuario.establecer_password(
            password
        )

        try:
            db.session.add(usuario)
            db.session.commit()

        except Exception:
            db.session.rollback()

            app.logger.exception(
                "Error al registrar usuario"
            )

            flash(
                "No se pudo crear la cuenta.",
                "danger",
            )

            return render_template(
                "registro.html"
            )

        login_user(usuario)

        flash(
            "Cuenta creada correctamente.",
            "success",
        )

        return redirect(
            url_for("index")
        )

    return render_template(
        "registro.html"
    )


# -------------------------------------------------
# INICIO DE SESIÓN
# -------------------------------------------------

@app.route(
    "/login",
    methods=["GET", "POST"],
)
def login():
    if current_user.is_authenticated:
        return redirect(
            url_for("index")
        )

    if request.method == "POST":
        correo = request.form.get(
            "correo",
            "",
        ).strip().lower()

        password = request.form.get(
            "password",
            "",
        )

        usuario = Usuario.query.filter_by(
            correo=correo
        ).first()

        if (
            usuario
            and usuario.verificar_password(password)
        ):
            login_user(
                usuario,
                remember=True,
            )

            flash(
                "Sesión iniciada correctamente.",
                "success",
            )

            return redirect(
                url_for("index")
            )

        flash(
            "Correo o contraseña incorrectos.",
            "danger",
        )

    return render_template(
        "login.html"
    )


# -------------------------------------------------
# CERRAR SESIÓN
# -------------------------------------------------

@app.get("/logout")
@login_required
def logout():
    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success",
    )

    return redirect(
        url_for("login")
    )


# -------------------------------------------------
# PÁGINA PRINCIPAL
# -------------------------------------------------

@app.get("/")
@login_required
def index():
    evaluaciones_totales = Evaluacion.query.filter_by(
        usuario_id=current_user.id
    ).count()

    ultima_evaluacion = (
        Evaluacion.query
        .filter_by(
            usuario_id=current_user.id
        )
        .order_by(
            Evaluacion.fecha.desc()
        )
        .first()
    )

    return render_template(
        "index.html",
        evaluaciones_totales=evaluaciones_totales,
        ultima_evaluacion=ultima_evaluacion,
    )


# -------------------------------------------------
# GENERAR EVALUACIÓN
# -------------------------------------------------

@app.post("/analizar")
@login_required
def analizar():
    try:
        datos = {
            # El nombre se toma automáticamente
            # del usuario que inició sesión.
            "nombre": current_user.nombre,

            "edad": int(
                request.form["edad"]
            ),

            "lesion": request.form[
                "lesion"
            ].strip(),

            "dolor": int(
                request.form["dolor"]
            ),

            "movilidad": int(
                request.form["movilidad"]
            ),

            "fuerza": int(
                request.form["fuerza"]
            ),

            "sesiones": int(
                request.form["sesiones"]
            ),

            "cumplimiento": int(
                request.form["cumplimiento"]
            ),
        }

        if not 1 <= datos["edad"] <= 120:
            raise ValueError(
                "La edad debe estar entre 1 y 120 años."
            )

        if not datos["lesion"]:
            raise ValueError(
                "Selecciona un tipo de lesión."
            )

        if not 0 <= datos["dolor"] <= 10:
            raise ValueError(
                "El dolor debe estar entre 0 y 10."
            )

        if not 0 <= datos["movilidad"] <= 100:
            raise ValueError(
                "La movilidad debe estar entre 0 y 100."
            )

        if not 0 <= datos["fuerza"] <= 100:
            raise ValueError(
                "La fuerza debe estar entre 0 y 100."
            )

        if datos["sesiones"] < 0:
            raise ValueError(
                "Las sesiones no pueden ser negativas."
            )

        if not 0 <= datos["cumplimiento"] <= 100:
            raise ValueError(
                "El cumplimiento debe estar entre 0 y 100."
            )

        evaluacion = calcular_rehabilitacion(
            datos
        )

        interpretacion = generar_reporte_chatgpt(
            datos,
            evaluacion,
        )

        observaciones = revisar_con_claude(
            datos,
            evaluacion,
        )

        informe_final = integrar_resultados(
            datos,
            evaluacion,
            interpretacion,
            observaciones,
        )

        registro = Evaluacion(
            usuario_id=current_user.id,
            nombre_paciente=current_user.nombre,
            edad=datos["edad"],
            lesion=datos["lesion"],
            dolor=datos["dolor"],
            movilidad=datos["movilidad"],
            fuerza=datos["fuerza"],
            sesiones=datos["sesiones"],
            cumplimiento=datos["cumplimiento"],
            indice_progreso=evaluacion[
                "indice_progreso"
            ],
            riesgo_retraso=evaluacion[
                "riesgo_retraso"
            ],
            protocolo_recomendado=evaluacion[
                "protocolo_recomendado"
            ],
            informe=informe_final,
        )

        db.session.add(registro)
        db.session.commit()

        return render_template(
            "resultado.html",
            datos=datos,
            resultado=evaluacion,
            interpretacion=interpretacion,
            observaciones=observaciones,
            final=informe_final,
        )

    except (
        ValueError,
        KeyError,
        TypeError,
    ) as error:
        db.session.rollback()

        return render_template(
            "index.html",
            error=str(error),
            evaluaciones_totales=(
                Evaluacion.query.filter_by(
                    usuario_id=current_user.id
                ).count()
            ),
            ultima_evaluacion=None,
        ), 400

    except Exception:
        db.session.rollback()

        app.logger.exception(
            "Error durante el análisis"
        )

        return render_template(
            "index.html",
            error=(
                "No se pudo completar la evaluación. "
                "Revisa las claves API y vuelve a intentarlo."
            ),
            evaluaciones_totales=(
                Evaluacion.query.filter_by(
                    usuario_id=current_user.id
                ).count()
            ),
            ultima_evaluacion=None,
        ), 500


# -------------------------------------------------
# EVOLUCIÓN DEL PACIENTE
# -------------------------------------------------

@app.get("/evolucion")
@login_required
def evolucion():
    evaluaciones = (
        Evaluacion.query
        .filter_by(
            usuario_id=current_user.id
        )
        .order_by(
            Evaluacion.fecha.asc()
        )
        .all()
    )

    etiquetas = [
        evaluacion.fecha.strftime(
            "%d/%m/%Y"
        )
        for evaluacion in evaluaciones
    ]

    dolor = [
        evaluacion.dolor
        for evaluacion in evaluaciones
    ]

    movilidad = [
        evaluacion.movilidad
        for evaluacion in evaluaciones
    ]

    fuerza = [
        evaluacion.fuerza
        for evaluacion in evaluaciones
    ]

    cumplimiento = [
        evaluacion.cumplimiento
        for evaluacion in evaluaciones
    ]

    progreso = [
        round(
            evaluacion.indice_progreso,
            2,
        )
        for evaluacion in evaluaciones
    ]

    resumen = None

    if evaluaciones:
        primera = evaluaciones[0]
        ultima = evaluaciones[-1]

        cambio_dolor = (
            primera.dolor
            - ultima.dolor
        )

        cambio_movilidad = (
            ultima.movilidad
            - primera.movilidad
        )

        cambio_fuerza = (
            ultima.fuerza
            - primera.fuerza
        )

        cambio_progreso = round(
            ultima.indice_progreso
            - primera.indice_progreso,
            2,
        )

        if cambio_progreso >= 10:
            estado = "Evolución favorable"

        elif cambio_progreso > 0:
            estado = "Evolución moderada"

        elif cambio_progreso == 0:
            estado = "Sin cambios importantes"

        else:
            estado = "Requiere revisión"

        resumen = {
            "total": len(evaluaciones),
            "estado": estado,
            "cambio_dolor": cambio_dolor,
            "cambio_movilidad": cambio_movilidad,
            "cambio_fuerza": cambio_fuerza,
            "cambio_progreso": cambio_progreso,
            "ultimo_progreso": round(
                ultima.indice_progreso,
                2,
            ),
            "ultima_fecha": ultima.fecha.strftime(
                "%d/%m/%Y"
            ),
        }

    return render_template(
        "evolucion.html",
        evaluaciones=evaluaciones,
        etiquetas=etiquetas,
        dolor=dolor,
        movilidad=movilidad,
        fuerza=fuerza,
        cumplimiento=cumplimiento,
        progreso=progreso,
        resumen=resumen,
    )


# -------------------------------------------------
# HISTORIAL
# -------------------------------------------------

@app.get("/historial")
@login_required
def historial():
    evaluaciones = (
        Evaluacion.query
        .filter_by(
            usuario_id=current_user.id
        )
        .order_by(
            Evaluacion.fecha.desc()
        )
        .all()
    )

    return render_template(
        "historial.html",
        evaluaciones=evaluaciones,
    )
# -------------------------------------------------
# PANEL DEL FISIOTERAPEUTA
# -------------------------------------------------

@app.get("/panel-fisioterapeuta")
@login_required
def panel_fisioterapeuta():

    evaluaciones = (
        Evaluacion.query
        .order_by(Evaluacion.fecha.desc())
        .all()
    )

    total_pacientes = (
        db.session.query(Evaluacion.usuario_id)
        .distinct()
        .count()
    )

    total_evaluaciones = len(evaluaciones)

    if total_evaluaciones:

        promedio = round(
            sum(
                e.indice_progreso
                for e in evaluaciones
            ) / total_evaluaciones,
            1,
        )

    else:

        promedio = 0

    pacientes_riesgo = sum(
        1
        for e in evaluaciones
        if e.riesgo_retraso >= 60
    )

    return render_template(
        "panel_fisioterapeuta.html",
        evaluaciones=evaluaciones,
        total_pacientes=total_pacientes,
        total_evaluaciones=total_evaluaciones,
        promedio=promedio,
        pacientes_riesgo=pacientes_riesgo,
    )
# -------------------------------------------------
# ELIMINAR EVALUACIÓN
# -------------------------------------------------

@app.post(
    "/eliminar-evaluacion/<int:evaluacion_id>"
)
@login_required
def eliminar_evaluacion(
    evaluacion_id: int,
):
    evaluacion = Evaluacion.query.filter_by(
        id=evaluacion_id,
        usuario_id=current_user.id,
    ).first_or_404()

    db.session.delete(evaluacion)
    db.session.commit()

    flash(
        "Evaluación eliminada correctamente.",
        "success",
    )

    return redirect(
        url_for("historial")
    )


# -------------------------------------------------
# ERROR 404
# -------------------------------------------------

@app.errorhandler(404)
def pagina_no_encontrada(_error):
    if current_user.is_authenticated:
        flash(
            "La página solicitada no existe.",
            "warning",
        )

        return redirect(
            url_for("index")
        )

    return redirect(
        url_for("login")
    )


# -------------------------------------------------
# EJECUTAR APLICACIÓN
# -------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
