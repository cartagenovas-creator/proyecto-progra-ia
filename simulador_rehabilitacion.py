from typing import Any


def limitar(valor: float, minimo: float = 0, maximo: float = 100) -> float:
    """
    Mantiene un valor dentro de un rango determinado.
    """
    return max(minimo, min(maximo, valor))


def validar_datos(datos: dict[str, Any]) -> None:
    """
    Verifica que los datos necesarios existan y estén dentro
    de los rangos permitidos.
    """
    campos_obligatorios = {
        "dolor",
        "movilidad",
        "fuerza",
        "sesiones",
        "cumplimiento",
    }

    campos_faltantes = campos_obligatorios.difference(datos.keys())

    if campos_faltantes:
        raise ValueError(
            "Faltan los siguientes datos: "
            + ", ".join(sorted(campos_faltantes))
        )

    dolor = float(datos["dolor"])
    movilidad = float(datos["movilidad"])
    fuerza = float(datos["fuerza"])
    sesiones = int(datos["sesiones"])
    cumplimiento = float(datos["cumplimiento"])

    if not 0 <= dolor <= 10:
        raise ValueError("El dolor debe estar entre 0 y 10.")

    if not 0 <= movilidad <= 100:
        raise ValueError("La movilidad debe estar entre 0 y 100.")

    if not 0 <= fuerza <= 100:
        raise ValueError("La fuerza debe estar entre 0 y 100.")

    if sesiones < 0:
        raise ValueError("Las sesiones realizadas no pueden ser negativas.")

    if not 0 <= cumplimiento <= 100:
        raise ValueError("El cumplimiento debe estar entre 0 y 100.")


def obtener_estado_recuperacion(indice_progreso: float) -> str:
    """
    Clasifica el estado general según el índice de progreso.
    """
    if indice_progreso >= 80:
        return "Recuperación favorable"

    if indice_progreso >= 60:
        return "Recuperación moderadamente favorable"

    if indice_progreso >= 40:
        return "Recuperación moderada"

    if indice_progreso >= 20:
        return "Progreso limitado"

    return "Progreso inicial"


def obtener_nivel_riesgo(riesgo_retraso: float) -> str:
    """
    Clasifica el riesgo simulado de retraso.
    """
    if riesgo_retraso <= 25:
        return "Bajo"

    if riesgo_retraso <= 50:
        return "Moderado"

    if riesgo_retraso <= 75:
        return "Alto"

    return "Muy alto"


def obtener_pronostico(
    indice_progreso: float,
    riesgo_retraso: float,
    cumplimiento: float
) -> str:
    """
    Genera un pronóstico académico basado en los indicadores.
    """
    if (
        indice_progreso >= 70
        and riesgo_retraso <= 35
        and cumplimiento >= 70
    ):
        return "Favorable"

    if indice_progreso >= 45 and riesgo_retraso <= 65:
        return "Moderado"

    return "Requiere seguimiento"


def construir_protocolo(
    protocolo_recomendado: str,
    datos: dict[str, Any]
) -> dict[str, Any]:
    """
    Construye un protocolo general de rehabilitación según
    el resultado principal.
    """
    dolor = float(datos["dolor"])
    movilidad = float(datos["movilidad"])
    fuerza = float(datos["fuerza"])

    fases = [
        {
            "nombre": "Fase I - Control inicial",
            "objetivos": [
                "Reducir el dolor y las molestias asociadas a la lesión.",
                "Proteger la zona afectada frente a cargas excesivas.",
                "Mantener la movilidad dentro de límites tolerables.",
                "Evitar movimientos que aumenten los síntomas.",
            ],
        },
        {
            "nombre": "Fase II - Recuperación de movilidad",
            "objetivos": [
                "Realizar ejercicios de movilidad activa y asistida.",
                "Aumentar progresivamente el rango articular.",
                "Reducir la rigidez de la articulación afectada.",
                "Corregir movimientos compensatorios.",
            ],
        },
        {
            "nombre": "Fase III - Fortalecimiento muscular",
            "objetivos": [
                "Iniciar ejercicios isométricos y de baja resistencia.",
                "Incrementar la carga de forma progresiva.",
                "Mejorar la estabilidad de la articulación.",
                "Recuperar el control neuromuscular.",
            ],
        },
        {
            "nombre": "Fase IV - Readaptación funcional",
            "objetivos": [
                "Retomar actividades cotidianas de forma gradual.",
                "Realizar ejercicios funcionales específicos.",
                "Mejorar equilibrio, coordinación y propiocepción.",
                "Prevenir recaídas y nuevas lesiones.",
            ],
        },
    ]

    recomendaciones = []

    if dolor >= 7:
        recomendaciones.append(
            "Priorizar actividades de baja carga y control del dolor."
        )

    if movilidad < 50:
        recomendaciones.append(
            "Reforzar ejercicios de movilidad articular progresiva."
        )

    if fuerza < 50:
        recomendaciones.append(
            "Aumentar gradualmente el trabajo de fortalecimiento muscular."
        )

    if not recomendaciones:
        recomendaciones.append(
            "Mantener el avance progresivo del protocolo y vigilar la respuesta funcional."
        )

    return {
        "nombre": protocolo_recomendado,
        "fases": fases,
        "recomendaciones": recomendaciones,
    }


def calcular_rehabilitacion(datos: dict[str, Any]) -> dict[str, Any]:
    """
    Calcula indicadores simulados del progreso de rehabilitación.

    Este módulo tiene fines académicos y no reemplaza
    una valoración médica profesional.
    """
    validar_datos(datos)

    dolor = float(datos["dolor"])
    movilidad = float(datos["movilidad"])
    fuerza = float(datos["fuerza"])
    sesiones = int(datos["sesiones"])
    cumplimiento = float(datos["cumplimiento"])

    valor_sesiones = limitar(sesiones * 5)

    progreso_base = (
        movilidad * 0.35
        + fuerza * 0.30
        + cumplimiento * 0.25
        + valor_sesiones * 0.10
    )

    penalizacion_dolor = dolor * 3

    indice_progreso = limitar(
        progreso_base - penalizacion_dolor
    )

    riesgo_retraso = limitar(
        100
        - indice_progreso
        + dolor * 2
        + max(0, 60 - cumplimiento) * 0.25
    )

    protocolos = {
        "Movilidad articular": (
            movilidad * 0.50
            + cumplimiento * 0.30
            + (100 - dolor * 10) * 0.20
        ),
        "Fortalecimiento muscular": (
            fuerza * 0.50
            + cumplimiento * 0.30
            + limitar(sesiones * 2, 0, 20)
        ),
        "Reeducación funcional": (
            indice_progreso * 0.60
            + movilidad * 0.20
            + fuerza * 0.20
        ),
        "Control del dolor y baja carga": (
            (100 - dolor * 8) * 0.50
            + movilidad * 0.30
            + cumplimiento * 0.20
        ),
        "Propiocepción y estabilidad": (
            movilidad * 0.30
            + fuerza * 0.30
            + cumplimiento * 0.25
            + valor_sesiones * 0.15
        ),
    }

    protocolos = {
        nombre: round(limitar(valor), 2)
        for nombre, valor in protocolos.items()
    }

    protocolo_recomendado = max(
        protocolos,
        key=protocolos.get
    )

    estado_recuperacion = obtener_estado_recuperacion(
        indice_progreso
    )

    nivel_riesgo = obtener_nivel_riesgo(
        riesgo_retraso
    )

    pronostico = obtener_pronostico(
        indice_progreso,
        riesgo_retraso,
        cumplimiento
    )

    protocolo_detallado = construir_protocolo(
        protocolo_recomendado,
        datos
    )

    return {
        "indice_progreso": round(indice_progreso, 2),
        "riesgo_retraso": round(riesgo_retraso, 2),
        "estado_recuperacion": estado_recuperacion,
        "nivel_riesgo": nivel_riesgo,
        "pronostico": pronostico,
        "protocolos": protocolos,
        "protocolo_recomendado": protocolo_recomendado,
        "protocolo_detallado": protocolo_detallado,
        "nota": (
            "Resultado académico y simulado. "
            "No sustituye una evaluación médica o fisioterapéutica."
        ),
    }