from __future__ import annotations

import base64
import io
import os
from pathlib import Path

import numpy as np
import pydicom
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

register_heif_opener()

FORMATOS_DICOM = {".dcm", ".dicom"}

FORMATOS_IMAGEN = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".heic",
    ".heif",
}

TAMANO_MAXIMO = 20 * 1024 * 1024
DIMENSION_MAXIMA = 2048


def convertir_dicom_a_imagen(ruta: Path) -> Image.Image:
    """
    Convierte la primera imagen de un archivo DICOM
    en una imagen PIL en escala de grises.
    """
    try:
        dataset = pydicom.dcmread(str(ruta))
        matriz = dataset.pixel_array.astype(float)
    except Exception as error:
        raise ValueError(
            "No se pudo leer el archivo DICOM."
        ) from error

    if matriz.ndim > 2:
        matriz = matriz[0]

    minimo = float(np.min(matriz))
    maximo = float(np.max(matriz))

    if maximo <= minimo:
        raise ValueError(
            "El archivo DICOM no contiene una imagen válida."
        )

    matriz = (
        (matriz - minimo)
        / (maximo - minimo)
        * 255
    ).astype(np.uint8)

    imagen = Image.fromarray(matriz, mode="L")

    if getattr(dataset, "PhotometricInterpretation", "") == "MONOCHROME1":
        imagen = ImageOps.invert(imagen)

    return imagen


def abrir_imagen(ruta: Path) -> Image.Image:
    """
    Abre una imagen común o un archivo DICOM.
    """
    extension = ruta.suffix.lower()

    if extension in FORMATOS_DICOM:
        return convertir_dicom_a_imagen(ruta)

    if extension not in FORMATOS_IMAGEN:
        raise ValueError(
            "Formato no compatible. Utiliza JPG, PNG, WEBP, GIF, "
            "BMP, TIFF, HEIC, HEIF o DICOM."
        )

    try:
        imagen = Image.open(ruta)
        imagen.load()
        return imagen
    except UnidentifiedImageError as error:
        raise ValueError(
            "El archivo no contiene una imagen válida."
        ) from error
    except OSError as error:
        raise ValueError(
            "No se pudo abrir la imagen."
        ) from error


def normalizar_imagen(ruta: Path) -> tuple[str, dict]:
    """
    Convierte cualquier formato admitido a PNG RGB,
    corrige orientación y reduce dimensiones excesivas.
    """
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(
            "La imagen no existe."
        )

    if ruta.stat().st_size > TAMANO_MAXIMO:
        raise ValueError(
            "La imagen supera el máximo permitido de 20 MB."
        )

    imagen = abrir_imagen(ruta)

    imagen = ImageOps.exif_transpose(imagen)

    if getattr(imagen, "is_animated", False):
        imagen.seek(0)

    if imagen.mode not in ("RGB", "L"):
        imagen = imagen.convert("RGB")

    imagen.thumbnail(
        (DIMENSION_MAXIMA, DIMENSION_MAXIMA),
        Image.Resampling.LANCZOS,
    )

    # Mejora suave del contraste sin modificar agresivamente la imagen.
    if imagen.mode == "L":
        imagen = ImageEnhance.Contrast(imagen).enhance(1.08)
        imagen = imagen.convert("RGB")
    else:
        imagen = ImageEnhance.Contrast(imagen).enhance(1.04)

    salida = io.BytesIO()
    imagen.save(
        salida,
        format="PNG",
        optimize=True,
    )

    contenido = salida.getvalue()

    datos = {
        "ancho": imagen.width,
        "alto": imagen.height,
        "formato_original": ruta.suffix.lower(),
        "tamano_original_kb": round(
            ruta.stat().st_size / 1024,
            2,
        ),
    }

    imagen_base64 = base64.b64encode(
        contenido
    ).decode("utf-8")

    return (
        f"data:image/png;base64,{imagen_base64}",
        datos,
    )


def analizar_imagen_medica(ruta_imagen: Path) -> dict:
    """
    Genera una descripción visual académica y orientativa.
    No reemplaza un informe radiológico.
    """
    api_key = os.getenv(
        "OPENAI_API_KEY",
        "",
    ).strip()

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY no está configurada."
        )

    modelo = os.getenv(
        "OPENAI_VISION_MODEL",
        "gpt-4.1-mini",
    ).strip()

    imagen_base64, metadatos = normalizar_imagen(
        Path(ruta_imagen)
    )

    instrucciones = """
Eres un asistente académico de análisis visual de imágenes médicas.

Analiza solamente lo visible en la imagen.

Reglas:
- No emitas un diagnóstico definitivo.
- No confirmes fracturas, tumores, infecciones ni enfermedades.
- No inventes hallazgos.
- No recomiendes medicamentos.
- No reemplaces el informe de un radiólogo.
- Explica las limitaciones de una sola imagen.
- Responde en español.
- Utiliza lenguaje claro y prudente.

Devuelve la respuesta usando exactamente estas secciones:

TIPO DE ESTUDIO
Indica qué tipo de imagen parece ser.

REGIÓN ANATÓMICA
Indica la zona corporal visible.

CALIDAD DE LA IMAGEN
Describe nitidez, contraste, orientación y posibles limitaciones.

DESCRIPCIÓN VISUAL
Describe estructuras, alineación y características visibles sin diagnosticar.

ÁREAS QUE REQUIEREN REVISIÓN PROFESIONAL
Menciona zonas que deberían ser revisadas por un especialista.

LIMITACIONES
Explica qué información falta para una interpretación médica completa.

RECOMENDACIÓN
Indica que debe revisarla un radiólogo, traumatólogo o profesional autorizado.
""".strip()

    cliente = OpenAI(api_key=api_key)

    try:
        respuesta = cliente.responses.create(
            model=modelo,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": instrucciones,
                        },
                        {
                            "type": "input_image",
                            "image_url": imagen_base64,
                            "detail": "high",
                        },
                    ],
                }
            ],
        )
    except Exception as error:
        raise RuntimeError(
            "No se pudo completar el análisis. "
            "Revisa la clave API, el modelo, el saldo y los logs."
        ) from error

    texto = respuesta.output_text.strip()

    if not texto:
        raise RuntimeError(
            "El modelo no devolvió resultados."
        )

    return {
        "informe": texto,
        "metadatos": metadatos,
    }
