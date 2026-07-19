from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db, login_manager


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
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

    imagenes = db.relationship(
        "AnalisisImagen",
        backref="usuario",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def establecer_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verificar_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Evaluacion(db.Model):
    __tablename__ = "evaluaciones"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )

    nombre_paciente = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    lesion = db.Column(db.String(120), nullable=False)
    dolor = db.Column(db.Integer, nullable=False)
    movilidad = db.Column(db.Integer, nullable=False)
    fuerza = db.Column(db.Integer, nullable=False)
    sesiones = db.Column(db.Integer, nullable=False)
    cumplimiento = db.Column(db.Integer, nullable=False)

    indice_progreso = db.Column(db.Float, nullable=False)
    riesgo_retraso = db.Column(db.Float, nullable=False)
    protocolo_recomendado = db.Column(db.String(150), nullable=False)
    informe = db.Column(db.Text, nullable=True)

    fecha = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class AnalisisImagen(db.Model):
    __tablename__ = "analisis_imagenes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )

    nombre_archivo = db.Column(db.String(255), nullable=False)
    resultado = db.Column(db.Text, nullable=False)

    fecha = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


@login_manager.user_loader
def cargar_usuario(usuario_id: str):
    return db.session.get(Usuario, int(usuario_id))
