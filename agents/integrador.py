def integrar_resultados(datos, resultado, reporte_chatgpt, revision_claude):
    return f"""
    REPORTE FINAL ORTHOREHAB SIM IA

    Paciente simulado: {datos['nombre']}
    Lesión: {datos['lesion']}

    Índice de progreso: {resultado['indice_progreso']}%
    Riesgo simulado de retraso: {resultado['riesgo_retraso']}%
    Protocolo más compatible: {resultado['protocolo_recomendado']}

    Interpretación ChatGPT:
    {reporte_chatgpt}

    Revisión Claude:
    {revision_claude}

    Nota: Este sistema es una simulación académica y no reemplaza una evaluación médica profesional.
    """
