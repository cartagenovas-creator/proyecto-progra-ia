"use strict";


/* =================================================
   CONFIGURACIÓN GENERAL
================================================= */

const RUTAS = window.PROGAIA?.rutas || {
    progreso: "/progreso",
    silabo: "/silabo",
    claseActual: "/clase-actual",
    proyectoActual: "/proyecto-actual",
    historial: "/historial",
    limpiarHistorial: "/limpiar-historial",
    reiniciarProgreso: "/reiniciar-progreso",
    generarQuiz: "/generar-quiz",
    guardarResultadoQuiz: "/guardar-resultado-quiz",
    subirPdf: "/subir-pdf",
    consultar: "/consultar",
    logout: "/logout"
};

const USUARIO = window.PROGAIA?.usuario || {
    nombre: "Estudiante",
    correo: ""
};


/* =================================================
   ELEMENTOS PRINCIPALES
================================================= */

const chat = document.getElementById("chat");
const chatForm = document.getElementById("chatForm");
const questionInput = document.getElementById("question");
const sendButton = document.getElementById("sendButton");

const connectionStatus = document.getElementById(
    "connectionStatus"
);

const statusText = document.getElementById(
    "statusText"
);


/* =================================================
   BOTONES SUPERIORES
================================================= */

const btnVerSilabo = document.getElementById(
    "btn-ver-silabo"
);

const btnVerProyectos = document.getElementById(
    "btn-ver-proyectos"
);

const btnVerHistorial = document.getElementById(
    "btn-ver-historial"
);

const btnVerPerfil = document.getElementById(
    "btn-ver-perfil"
);


/* =================================================
   PANEL PRINCIPAL
================================================= */

const btnContinuarAprendizaje = document.getElementById(
    "btn-continuar-aprendizaje"
);

const btnAprenderDesdeCero = document.getElementById(
    "btn-aprender-desde-cero"
);

const porcentajeCurso = document.getElementById(
    "porcentaje-curso"
);

const barraProgresoCurso = document.getElementById(
    "barra-progreso-curso"
);

const courseProgressFill = document.getElementById(
    "course-progress-fill"
);

const mensajeProgreso = document.getElementById(
    "mensaje-progreso"
);


/* =================================================
   TARJETAS DEL RESUMEN
================================================= */

const resumenNivel = document.getElementById(
    "resumen-nivel"
);

const resumenNombreNivel = document.getElementById(
    "resumen-nombre-nivel"
);

const resumenTema = document.getElementById(
    "resumen-tema"
);

const resumenXp = document.getElementById(
    "resumen-xp"
);

const resumenRacha = document.getElementById(
    "resumen-racha"
);

const resumenEstado = document.getElementById(
    "resumen-estado"
);


/* =================================================
   ACCIONES RÁPIDAS
================================================= */

const btnContinuarClase = document.getElementById(
    "btn-continuar-clase"
);

const btnGenerarQuiz = document.getElementById(
    "btn-generar-quiz"
);

const btnAbrirProyecto = document.getElementById(
    "btn-abrir-proyecto"
);


/* =================================================
   RUTA DE APRENDIZAJE
================================================= */

const nombreNivel = document.getElementById(
    "nombre-nivel"
);

const descripcionNivel = document.getElementById(
    "descripcion-nivel"
);

const insigniaNivel = document.getElementById(
    "insignia-nivel"
);

const temaActual = document.getElementById(
    "tema-actual"
);

const descripcionTemaActual = document.getElementById(
    "descripcion-tema-actual"
);

const unidadActual = document.getElementById(
    "unidad-actual"
);

const dificultadTema = document.getElementById(
    "dificultad-tema"
);

const duracionTema = document.getElementById(
    "duracion-tema"
);

const btnIniciarTema = document.getElementById(
    "btn-iniciar-tema"
);

const btnRepasarTema = document.getElementById(
    "btn-repasar-tema"
);


/* =================================================
   PROYECTO DEL NIVEL
================================================= */

const proyectoNivel = document.getElementById(
    "proyecto-nivel"
);

const descripcionProyecto = document.getElementById(
    "descripcion-proyecto"
);

const estadoProyecto = document.getElementById(
    "estado-proyecto"
);

const requisitoProyecto = document.getElementById(
    "requisito-proyecto"
);

const btnProyectoNivel = document.getElementById(
    "btn-proyecto-nivel"
);


/* =================================================
   PROGRESO DEL NIVEL
================================================= */

const porcentajeNivel = document.getElementById(
    "porcentaje-nivel"
);

const temasNivelCompletados = document.getElementById(
    "temas-nivel-completados"
);

const barraProgresoNivel = document.getElementById(
    "barra-progreso-nivel"
);

const rellenoProgresoNivel = document.getElementById(
    "relleno-progreso-nivel"
);


/* =================================================
   ESTADÍSTICAS PERSONALES
================================================= */

const numeroConsultas = document.getElementById(
    "numero-consultas"
);

const numeroEjercicios = document.getElementById(
    "numero-ejercicios"
);

const numeroQuizzesRealizados = document.getElementById(
    "numero-quizzes-realizados"
);

const numeroQuizzesAprobados = document.getElementById(
    "numero-quizzes-aprobados"
);

const numeroNivelesCompletados = document.getElementById(
    "numero-niveles-completados"
);

const numeroProyectosDesbloqueados = document.getElementById(
    "numero-proyectos-desbloqueados"
);

const btnReiniciarProgreso = document.getElementById(
    "btn-reiniciar-progreso"
);


/* =================================================
   LISTAS DE TEMAS
================================================= */

const listaTemas = document.getElementById(
    "lista-temas"
);

const listaTemasAprobados = document.getElementById(
    "lista-temas-aprobados"
);

const listaTemasRepasar = document.getElementById(
    "lista-temas-repasar"
);


/* =================================================
   PDF
================================================= */

const uploadButton = document.getElementById(
    "uploadButton"
);

const pdfInput = document.getElementById(
    "pdfInput"
);

const documentStatus = document.getElementById(
    "documentStatus"
);

const documentName = document.getElementById(
    "documentName"
);

const documentDetails = document.getElementById(
    "documentDetails"
);


/* =================================================
   MODAL DEL HISTORIAL
================================================= */

const modalHistorial = document.getElementById(
    "modal-historial"
);

const cerrarHistorial = document.getElementById(
    "cerrar-historial"
);

const limpiarHistorial = document.getElementById(
    "limpiar-historial"
);

const contenidoHistorial = document.getElementById(
    "contenido-historial"
);


/* =================================================
   MODAL DEL QUIZ
================================================= */

const modalQuiz = document.getElementById(
    "modal-quiz"
);

const cerrarQuiz = document.getElementById(
    "cerrar-quiz"
);

const contenidoQuiz = document.getElementById(
    "contenido-quiz"
);


/* =================================================
   MODAL DEL SÍLABO
================================================= */

const modalSilabo = document.getElementById(
    "modal-silabo"
);

const cerrarSilabo = document.getElementById(
    "cerrar-silabo"
);

const contenidoSilabo = document.getElementById(
    "contenido-silabo"
);


/* =================================================
   MODAL DE PROYECTOS
================================================= */

const modalProyectos = document.getElementById(
    "modal-proyectos"
);

const cerrarProyectos = document.getElementById(
    "cerrar-proyectos"
);

const contenidoProyectos = document.getElementById(
    "contenido-proyectos"
);


/* =================================================
   MODAL DEL PERFIL
================================================= */

const modalPerfil = document.getElementById(
    "modal-perfil"
);

const cerrarPerfil = document.getElementById(
    "cerrar-perfil"
);

const perfilConsultas = document.getElementById(
    "perfil-consultas"
);

const perfilQuizzes = document.getElementById(
    "perfil-quizzes"
);

const perfilProgreso = document.getElementById(
    "perfil-progreso"
);

const perfilNivel = document.getElementById(
    "perfil-nivel"
);


/* =================================================
   VARIABLES DE ESTADO
================================================= */

let enviandoPregunta = false;
let subiendoPdf = false;
let generandoQuiz = false;

let progresoActual = null;
let claseActualDatos = null;
let silaboActual = [];
let quizActual = null;


/* =================================================
   ESTADO DE CONEXIÓN
================================================= */

function cambiarEstado(
    texto,
    tipo = "ready"
) {
    if (!connectionStatus || !statusText) {
        return;
    }

    statusText.textContent = texto;

    connectionStatus.classList.remove(
        "busy",
        "error"
    );

    if (tipo === "busy") {
        connectionStatus.classList.add("busy");
    }

    if (tipo === "error") {
        connectionStatus.classList.add("error");
    }
}


/* =================================================
   RESPUESTAS DEL SERVIDOR
================================================= */

async function leerRespuesta(response) {
    if (response.status === 401) {
        window.location.href = "/login";

        return {
            ok: false,
            respuesta: "Tu sesión terminó."
        };
    }

    try {
        return await response.json();

    } catch (error) {
        console.error(
            "No se pudo interpretar la respuesta:",
            error
        );

        return {
            ok: false,
            respuesta:
                "El servidor devolvió una respuesta inválida."
        };
    }
}


/* =================================================
   FUNCIONES DE PORCENTAJE
================================================= */

function limitarPorcentaje(valor) {
    const numero = Number(valor) || 0;

    return Math.min(
        100,
        Math.max(0, numero)
    );
}


/* =================================================
   CREACIÓN DE ELEMENTOS
================================================= */

function crearElemento(
    etiqueta,
    clase = "",
    texto = ""
) {
    const elemento = document.createElement(
        etiqueta
    );

    if (clase) {
        elemento.className = clase;
    }

    if (texto !== undefined && texto !== null) {
        elemento.textContent = String(texto);
    }

    return elemento;
}


function limpiarElemento(elemento) {
    if (!elemento) {
        return;
    }

    elemento.innerHTML = "";
}


function mostrarMensajeVacio(
    contenedor,
    mensaje
) {
    if (!contenedor) {
        return;
    }

    limpiarElemento(contenedor);

    const parrafo = crearElemento(
        "p",
        "empty-history",
        mensaje
    );

    contenedor.appendChild(parrafo);
}


/* =================================================
   MODALES
================================================= */

function abrirModal(modal) {
    if (!modal) {
        return;
    }

    modal.classList.remove("hidden");

    document.body.classList.add(
        "modal-open"
    );
}


function cerrarModal(modal) {
    if (!modal) {
        return;
    }

    modal.classList.add("hidden");

    const modalAbierto = document.querySelector(
        ".history-modal:not(.hidden)"
    );

    if (!modalAbierto) {
        document.body.classList.remove(
            "modal-open"
        );
    }
}


/* =================================================
   TEXTAREA
================================================= */

function ajustarTextarea() {
    if (!questionInput) {
        return;
    }

    questionInput.style.height = "auto";

    const nuevaAltura = Math.min(
        questionInput.scrollHeight,
        180
    );

    questionInput.style.height =
        `${nuevaAltura}px`;
}


/* =================================================
   MOVIMIENTO DEL CHAT
================================================= */

function moverChatAbajo() {
    if (!chat) {
        return;
    }

    chat.scrollTop = chat.scrollHeight;
}


/* =================================================
   MENSAJES DEL CHAT
================================================= */

function agregarMensaje(
    texto,
    tipo = "assistant",
    opciones = {}
) {
    if (!chat) {
        return null;
    }

    const article = crearElemento(
        "article",
        `message ${tipo}`
    );

    if (opciones.id) {
        article.id = opciones.id;
    }

    if (opciones.pending) {
        article.classList.add("pending");
    }

    if (opciones.error) {
        article.classList.add("error");
    }

    const avatar = crearElemento(
        "div",
        tipo === "user"
            ? "avatar user-avatar"
            : "avatar assistant-avatar",
        tipo === "user"
            ? "TÚ"
            : "IA"
    );

    const bubble = crearElemento(
        "div",
        "bubble"
    );

    if (
        tipo === "assistant"
        && !opciones.pending
    ) {
        const label = crearElemento(
            "p",
            "message-label",
            opciones.error
                ? "AVISO"
                : "PROYECTO PROGA IA"
        );

        bubble.appendChild(label);
    }

    const contenido = crearElemento(
        "p",
        "message-text",
        texto
    );

    bubble.appendChild(contenido);

    article.append(
        avatar,
        bubble
    );

    chat.appendChild(article);

    moverChatAbajo();

    return article;
}


function eliminarMensaje(id) {
    const mensaje = document.getElementById(id);

    if (mensaje) {
        mensaje.remove();
    }
}
/* =================================================
   ENVÍO DE PREGUNTAS
================================================= */

async function enviarPregunta(
    preguntaForzada = null
) {
    const pregunta = (
        preguntaForzada
        ?? questionInput?.value
        ?? ""
    ).trim();

    if (!pregunta || enviandoPregunta) {
        return;
    }

    enviandoPregunta = true;

    if (sendButton) {
        sendButton.disabled = true;
    }

    cambiarEstado(
        "Pensando...",
        "busy"
    );

    agregarMensaje(
        pregunta,
        "user"
    );

    if (questionInput) {
        questionInput.value = "";
        ajustarTextarea();
    }

    agregarMensaje(
        "Estoy analizando tu consulta...",
        "assistant",
        {
            id: "mensaje-pendiente",
            pending: true
        }
    );

    try {
        const response = await fetch(
            RUTAS.consultar,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    pregunta
                })
            }
        );

        const data = await leerRespuesta(response);

        eliminarMensaje(
            "mensaje-pendiente"
        );

        if (!response.ok || !data.ok) {
            agregarMensaje(
                data.respuesta
                || "No se pudo procesar la consulta.",
                "assistant",
                {
                    error: true
                }
            );

            cambiarEstado(
                "No se pudo responder",
                "error"
            );

            return;
        }

        agregarMensaje(
            data.respuesta,
            "assistant"
        );

        if (data.progreso) {
            actualizarPanelCompleto(
                data.progreso,
                data.clase_actual
            );
        } else {
            await cargarProgreso();
        }

        cambiarEstado(
            "Listo para ayudarte"
        );

    } catch (error) {
        console.error(
            "Error al enviar la pregunta:",
            error
        );

        eliminarMensaje(
            "mensaje-pendiente"
        );

        agregarMensaje(
            "No se pudo conectar con el servidor. "
            + "Verifica que app.py esté ejecutándose.",
            "assistant",
            {
                error: true
            }
        );

        cambiarEstado(
            "Sin conexión",
            "error"
        );

    } finally {
        enviandoPregunta = false;

        if (sendButton) {
            sendButton.disabled = false;
        }

        if (questionInput) {
            questionInput.focus();
        }
    }
}


/* =================================================
   FORMULARIO DEL CHAT
================================================= */

if (chatForm) {
    chatForm.addEventListener(
        "submit",
        function (event) {
            event.preventDefault();

            enviarPregunta();
        }
    );
}


if (questionInput) {
    questionInput.addEventListener(
        "input",
        ajustarTextarea
    );

    questionInput.addEventListener(
        "keydown",
        function (event) {
            if (
                event.key === "Enter"
                && !event.shiftKey
            ) {
                event.preventDefault();

                enviarPregunta();
            }
        }
    );
}


/* =================================================
   BOTONES CON DATA-PROMPT
================================================= */

function prepararBotonesPrompt() {
    document
        .querySelectorAll("[data-prompt]")
        .forEach((boton) => {
            boton.addEventListener(
                "click",
                function () {
                    const prompt =
                        boton.dataset.prompt || "";

                    if (!questionInput) {
                        return;
                    }

                    questionInput.value = prompt;

                    ajustarTextarea();
                    questionInput.focus();
                }
            );
        });
}


/* =================================================
   CARGAR CLASE ACTUAL
================================================= */

async function cargarClaseActual() {
    try {
        const response = await fetch(
            RUTAS.claseActual
        );

        const data = await leerRespuesta(
            response
        );

        if (!response.ok || !data.ok) {
            throw new Error(
                data.respuesta
                || "No se pudo cargar la clase actual."
            );
        }

        if (data.completado) {
            claseActualDatos = null;

            return {
                completado: true,
                mensaje: data.mensaje
            };
        }

        claseActualDatos = data.clase;

        return {
            completado: false,
            clase: data.clase
        };

    } catch (error) {
        console.error(
            "Error al cargar la clase actual:",
            error
        );

        return null;
    }
}


/* =================================================
   CONTINUAR CLASE
================================================= */

async function continuarClase() {
    cambiarEstado(
        "Preparando tu clase...",
        "busy"
    );

    const resultado = await cargarClaseActual();

    if (!resultado) {
        agregarMensaje(
            "No se pudo obtener tu tema actual.",
            "assistant",
            {
                error: true
            }
        );

        cambiarEstado(
            "No se pudo cargar la clase",
            "error"
        );

        return;
    }

    if (resultado.completado) {
        agregarMensaje(
            resultado.mensaje
            || "Has completado todo el curso.",
            "assistant"
        );

        cambiarEstado(
            "Curso completado"
        );

        return;
    }

    const clase = resultado.clase;

    const pregunta =
        `Enséñame el tema "${clase.tema}" `
        + `del nivel ${clase.nivel}: `
        + `"${clase.unidad}". `
        + "Explícalo desde cero con un ejemplo sencillo, "
        + "un bloque de código, un ejercicio guiado "
        + "y una práctica para resolver solo. "
        + "Al final indícame que debo realizar el quiz.";

    await enviarPregunta(
        pregunta
    );
}


/* =================================================
   APRENDER DESDE CERO
================================================= */

async function aprenderDesdeCero() {
    const pregunta =
        "Quiero aprender programación desde cero. "
        + "Enséñame el tema actual de mi ruta de aprendizaje "
        + "con una explicación sencilla, un ejemplo, "
        + "un ejercicio guiado y una práctica.";

    await enviarPregunta(
        pregunta
    );
}


/* =================================================
   REPASAR TEMA ACTUAL
================================================= */

async function repasarTemaActual() {
    const tema =
        claseActualDatos?.tema
        ?? progresoActual?.tema_actual
        ?? "mi tema actual";

    const pregunta =
        `Necesito repasar "${tema}". `
        + "Explícamelo de una forma más sencilla, "
        + "usa un ejemplo diferente y dame un ejercicio corto.";

    await enviarPregunta(
        pregunta
    );
}


/* =================================================
   INICIAR TEMA
================================================= */

async function iniciarTemaActual() {
    const tema =
        claseActualDatos?.tema
        ?? progresoActual?.tema_actual
        ?? "";

    if (!tema) {
        await continuarClase();
        return;
    }

    const pregunta =
        `Enséñame el tema "${tema}" desde cero. `
        + "Incluye una explicación clara, un ejemplo cotidiano, "
        + "un ejemplo en Python y una práctica.";

    await enviarPregunta(
        pregunta
    );
}


/* =================================================
   EVENTOS DE APRENDIZAJE
================================================= */

if (btnContinuarAprendizaje) {
    btnContinuarAprendizaje.addEventListener(
        "click",
        continuarClase
    );
}


if (btnContinuarClase) {
    btnContinuarClase.addEventListener(
        "click",
        continuarClase
    );
}


if (btnAprenderDesdeCero) {
    btnAprenderDesdeCero.addEventListener(
        "click",
        aprenderDesdeCero
    );
}


if (btnIniciarTema) {
    btnIniciarTema.addEventListener(
        "click",
        iniciarTemaActual
    );
}


if (btnRepasarTema) {
    btnRepasarTema.addEventListener(
        "click",
        repasarTemaActual
    );
}
/* =================================================
   ETIQUETAS DE TEMAS
================================================= */

function renderizarEtiquetas(
    contenedor,
    elementos,
    mensajeVacio,
    claseExtra = ""
) {
    if (!contenedor) {
        return;
    }

    limpiarElemento(contenedor);

    if (
        !Array.isArray(elementos)
        || elementos.length === 0
    ) {
        const vacio = crearElemento(
            "span",
            "no-topics",
            mensajeVacio
        );

        contenedor.appendChild(vacio);
        return;
    }

    elementos.forEach((texto) => {
        const etiqueta = crearElemento(
            "span",
            `topic-tag ${claseExtra}`.trim(),
            texto
        );

        contenedor.appendChild(etiqueta);
    });
}


/* =================================================
   CÁLCULOS VISUALES
================================================= */

function calcularXp(progreso) {
    const consultas =
        Number(progreso?.consultas) || 0;

    const ejercicios =
        Number(progreso?.ejercicios) || 0;

    const quizzesAprobados =
        Number(progreso?.quizzes_aprobados) || 0;

    const nivelesCompletados =
        Array.isArray(
            progreso?.niveles_completados
        )
            ? progreso.niveles_completados.length
            : 0;

    return (
        consultas * 5
        + ejercicios * 10
        + quizzesAprobados * 40
        + nivelesCompletados * 120
    );
}


function calcularRacha(progreso) {
    const consultas =
        Number(progreso?.consultas) || 0;

    if (consultas === 0) {
        return 0;
    }

    return Math.min(
        30,
        Math.max(
            1,
            Math.ceil(consultas / 3)
        )
    );
}


function obtenerEstadoCurso(progreso) {
    if (progreso?.curso_completado) {
        return "Completado";
    }

    const porcentaje = limitarPorcentaje(
        progreso?.porcentaje_general
    );

    if (porcentaje >= 75) {
        return "Avanzado";
    }

    if (porcentaje >= 40) {
        return "En progreso";
    }

    if (porcentaje > 0) {
        return "Comenzando";
    }

    return "Sin iniciar";
}


/* =================================================
   PROGRESO GENERAL
================================================= */

function actualizarProgresoGeneral(progreso) {
    const porcentaje = limitarPorcentaje(
        progreso?.porcentaje_general
    );

    if (porcentajeCurso) {
        porcentajeCurso.textContent =
            `${porcentaje}%`;
    }

    if (courseProgressFill) {
        courseProgressFill.style.width =
            `${porcentaje}%`;
    }

    if (barraProgresoCurso) {
        barraProgresoCurso.setAttribute(
            "aria-valuenow",
            String(porcentaje)
        );
    }

    if (mensajeProgreso) {
        if (progreso?.curso_completado) {
            mensajeProgreso.textContent =
                "Has completado toda la ruta de aprendizaje.";
        } else if (porcentaje >= 75) {
            mensajeProgreso.textContent =
                "Estás muy cerca de completar el curso.";
        } else if (porcentaje >= 40) {
            mensajeProgreso.textContent =
                "Vas avanzando muy bien. Continúa aprendiendo.";
        } else if (porcentaje > 0) {
            mensajeProgreso.textContent =
                "Buen comienzo. Sigue completando temas.";
        } else {
            mensajeProgreso.textContent =
                "Comienza tu primera clase para avanzar.";
        }
    }
}


/* =================================================
   TARJETAS DEL DASHBOARD
================================================= */

function actualizarResumenDashboard(
    progreso,
    clase
) {
    const nivel =
        clase?.nivel
        ?? progreso?.nivel_actual
        ?? 1;

    const unidad =
        clase?.unidad
        ?? `Nivel ${nivel}`;

    const tema =
        clase?.tema
        ?? progreso?.tema_actual
        ?? "Tema pendiente";

    const xp = calcularXp(progreso);
    const racha = calcularRacha(progreso);
    const estado = obtenerEstadoCurso(progreso);

    if (resumenNivel) {
        resumenNivel.textContent =
            `Nivel ${nivel}`;
    }

    if (resumenNombreNivel) {
        resumenNombreNivel.textContent =
            unidad;
    }

    if (resumenTema) {
        resumenTema.textContent =
            tema;
    }

    if (resumenXp) {
        resumenXp.textContent =
            `${xp} XP`;
    }

    if (resumenRacha) {
        resumenRacha.textContent =
            `${racha} ${
                racha === 1
                    ? "día"
                    : "días"
            }`;
    }

    if (resumenEstado) {
        resumenEstado.textContent =
            estado;
    }
}


/* =================================================
   RUTA DE APRENDIZAJE
================================================= */

function actualizarRutaAprendizaje(
    progreso,
    clase
) {
    if (progreso?.curso_completado) {
        if (nombreNivel) {
            nombreNivel.textContent =
                "Curso completado";
        }

        if (descripcionNivel) {
            descripcionNivel.textContent =
                "Has completado todos los niveles disponibles.";
        }

        if (insigniaNivel) {
            insigniaNivel.textContent =
                "Completado";
        }

        if (temaActual) {
            temaActual.textContent =
                "Curso completado";
        }

        if (descripcionTemaActual) {
            descripcionTemaActual.textContent =
                "Ya puedes desarrollar tu proyecto final.";
        }

        if (unidadActual) {
            unidadActual.textContent =
                "Curso completo";
        }

        if (btnIniciarTema) {
            btnIniciarTema.disabled = true;
            btnIniciarTema.textContent =
                "Curso completado";
        }

        if (btnRepasarTema) {
            btnRepasarTema.disabled = false;
        }

        return;
    }

    const nivel =
        clase?.nivel
        ?? progreso?.nivel_actual
        ?? 1;

    const unidad =
        clase?.unidad
        ?? `Nivel ${nivel}`;

    const descripcion =
        clase?.descripcion
        ?? "Continúa avanzando en tu ruta de programación.";

    const tema =
        clase?.tema
        ?? progreso?.tema_actual
        ?? "Tema pendiente";

    const proyecto =
        clase?.proyecto
        ?? "Proyecto pendiente";

    if (nombreNivel) {
        nombreNivel.textContent =
            `Nivel ${nivel}: ${unidad}`;
    }

    if (descripcionNivel) {
        descripcionNivel.textContent =
            descripcion;
    }

    if (insigniaNivel) {
        insigniaNivel.textContent =
            `Nivel ${nivel}`;
    }

    if (temaActual) {
        temaActual.textContent =
            tema;
    }

    if (descripcionTemaActual) {
        descripcionTemaActual.textContent =
            `Aprende los conceptos principales de ${tema} `
            + "con explicación, ejemplos y práctica.";
    }

    if (unidadActual) {
        unidadActual.textContent =
            unidad;
    }

    if (dificultadTema) {
        dificultadTema.textContent =
            nivel <= 4
                ? "Principiante"
                : nivel <= 9
                    ? "Intermedio"
                    : "Avanzado";
    }

    if (duracionTema) {
        duracionTema.textContent =
            nivel <= 4
                ? "20 minutos"
                : nivel <= 9
                    ? "30 minutos"
                    : "40 minutos";
    }

    if (proyectoNivel) {
        proyectoNivel.textContent =
            proyecto;
    }

    if (descripcionProyecto) {
        descripcionProyecto.textContent =
            `Desarrolla "${proyecto}" aplicando `
            + `los conocimientos del nivel ${nivel}.`;
    }

    if (btnIniciarTema) {
        btnIniciarTema.disabled = false;
        btnIniciarTema.innerHTML =
            "<span>▶</span> Iniciar tema";
    }
}


/* =================================================
   PROGRESO DEL NIVEL
================================================= */

function obtenerTemasNivelActual(
    nivelActual
) {
    if (!Array.isArray(silaboActual)) {
        return [];
    }

    const nivel = silaboActual.find(
        (item) =>
            Number(item.numero)
            === Number(nivelActual)
    );

    return Array.isArray(nivel?.temas)
        ? nivel.temas
        : [];
}


function actualizarProgresoNivel(
    progreso
) {
    const nivelActual =
        progreso?.nivel_actual || 1;

    const temasNivel =
        obtenerTemasNivelActual(
            nivelActual
        );

    const temasAprobados =
        Array.isArray(
            progreso?.temas_aprobados
        )
            ? progreso.temas_aprobados
            : [];

    const completados = temasNivel.filter(
        (tema) =>
            temasAprobados.includes(tema)
    ).length;

    const total = temasNivel.length;

    const porcentaje =
        total > 0
            ? Math.round(
                (completados / total) * 100
            )
            : 0;

    if (porcentajeNivel) {
        porcentajeNivel.textContent =
            `${porcentaje}%`;
    }

    if (temasNivelCompletados) {
        temasNivelCompletados.textContent =
            `${completados} de ${total} `
            + "temas completados";
    }

    if (rellenoProgresoNivel) {
        rellenoProgresoNivel.style.width =
            `${porcentaje}%`;
    }

    if (barraProgresoNivel) {
        barraProgresoNivel.setAttribute(
            "aria-valuenow",
            String(porcentaje)
        );
    }
}


/* =================================================
   ESTADO DEL PROYECTO
================================================= */

function actualizarProyectoNivel(
    progreso,
    clase
) {
    const proyectos =
        Array.isArray(
            progreso?.proyectos_desbloqueados
        )
            ? progreso.proyectos_desbloqueados
            : [];

    const proyecto =
        clase?.proyecto
        ?? proyectoNivel?.textContent
        ?? "";

    const desbloqueado =
        proyectos.includes(proyecto);

    if (estadoProyecto) {
        estadoProyecto.textContent =
            desbloqueado
                ? "Desbloqueado"
                : "Bloqueado";
    }

    if (requisitoProyecto) {
        requisitoProyecto.textContent =
            desbloqueado
                ? "Ya puedes comenzar este proyecto."
                : "Completa todos los temas del nivel para desbloquearlo.";
    }

    if (btnProyectoNivel) {
        btnProyectoNivel.disabled =
            !desbloqueado;

        btnProyectoNivel.textContent =
            desbloqueado
                ? "Abrir proyecto"
                : "Proyecto bloqueado";
    }
}


/* =================================================
   ESTADÍSTICAS PERSONALES
================================================= */

function actualizarEstadisticas(
    progreso
) {
    const consultas =
        Number(progreso?.consultas) || 0;

    const ejercicios =
        Number(progreso?.ejercicios) || 0;

    const quizzesRealizados =
        Number(
            progreso?.quizzes_realizados
        ) || 0;

    const quizzesAprobados =
        Number(
            progreso?.quizzes_aprobados
        ) || 0;

    const nivelesCompletados =
        Array.isArray(
            progreso?.niveles_completados
        )
            ? progreso.niveles_completados.length
            : 0;

    const proyectosDesbloqueados =
        Array.isArray(
            progreso?.proyectos_desbloqueados
        )
            ? progreso
                .proyectos_desbloqueados
                .length
            : 0;

    if (numeroConsultas) {
        numeroConsultas.textContent =
            consultas;
    }

    if (numeroEjercicios) {
        numeroEjercicios.textContent =
            ejercicios;
    }

    if (numeroQuizzesRealizados) {
        numeroQuizzesRealizados.textContent =
            quizzesRealizados;
    }

    if (numeroQuizzesAprobados) {
        numeroQuizzesAprobados.textContent =
            quizzesAprobados;
    }

    if (numeroNivelesCompletados) {
        numeroNivelesCompletados.textContent =
            nivelesCompletados;
    }

    if (numeroProyectosDesbloqueados) {
        numeroProyectosDesbloqueados.textContent =
            proyectosDesbloqueados;
    }

    if (perfilConsultas) {
        perfilConsultas.textContent =
            consultas;
    }

    if (perfilQuizzes) {
        perfilQuizzes.textContent =
            quizzesRealizados;
    }

    if (perfilProgreso) {
        perfilProgreso.textContent =
            `${
                limitarPorcentaje(
                    progreso?.porcentaje_general
                )
            }%`;
    }

    if (perfilNivel) {
        perfilNivel.textContent =
            progreso?.nivel_actual || 1;
    }
}


/* =================================================
   ACTUALIZAR TODO EL PANEL
================================================= */

function actualizarPanelCompleto(
    progreso,
    clase = null
) {
    if (!progreso) {
        return;
    }

    progresoActual = progreso;
    claseActualDatos = clase;

    actualizarProgresoGeneral(
        progreso
    );

    actualizarResumenDashboard(
        progreso,
        clase
    );

    actualizarRutaAprendizaje(
        progreso,
        clase
    );

    actualizarProgresoNivel(
        progreso
    );

    actualizarProyectoNivel(
        progreso,
        clase
    );

    actualizarEstadisticas(
        progreso
    );

    renderizarEtiquetas(
        listaTemas,
        progreso.temas_estudiados,
        "Aún no has estudiado temas."
    );

    renderizarEtiquetas(
        listaTemasAprobados,
        progreso.temas_aprobados,
        "Todavía no has aprobado temas.",
        "approved-topic"
    );

    renderizarEtiquetas(
        listaTemasRepasar,
        progreso.temas_por_repasar,
        "No tienes temas pendientes de repaso.",
        "review-topic"
    );
}


/* =================================================
   CARGAR PROGRESO
================================================= */

async function cargarProgreso() {
    try {
        const response = await fetch(
            RUTAS.progreso
        );

        const data = await leerRespuesta(
            response
        );

        if (!response.ok || !data.ok) {
            throw new Error(
                data.respuesta
                || "No se pudo cargar el progreso."
            );
        }

        actualizarPanelCompleto(
            data.progreso,
            data.clase_actual
        );

    } catch (error) {
        console.error(
            "Error al cargar progreso:",
            error
        );

        cambiarEstado(
            "No se pudo cargar el progreso",
            "error"
        );
    }
}


/* =================================================
   CARGAR SÍLABO PARA CÁLCULOS
================================================= */

async function cargarSilaboBase() {
    try {
        const response = await fetch(
            RUTAS.silabo
        );

        const data = await leerRespuesta(
            response
        );

        if (!response.ok || !data.ok) {
            throw new Error(
                data.respuesta
                || "No se pudo cargar el sílabo."
            );
        }

        silaboActual =
            Array.isArray(data.niveles)
                ? data.niveles
                : [];

        if (progresoActual) {
            actualizarProgresoNivel(
                progresoActual
            );
        }

    } catch (error) {
        console.error(
            "Error al cargar el sílabo:",
            error
        );
    }
}
/* =================================================
   SUBIR PDF
================================================= */

async function subirPdf() {
    const archivo = pdfInput?.files?.[0];

    if (!archivo || subiendoPdf) {
        return;
    }

    if (
        !archivo.name
            .toLowerCase()
            .endsWith(".pdf")
    ) {
        agregarMensaje(
            "Solo puedes subir archivos PDF.",
            "assistant",
            {
                error: true
            }
        );

        if (pdfInput) {
            pdfInput.value = "";
        }

        return;
    }

    if (
        archivo.size
        > 12 * 1024 * 1024
    ) {
        agregarMensaje(
            "El PDF supera el tamaño máximo de 12 MB.",
            "assistant",
            {
                error: true
            }
        );

        if (pdfInput) {
            pdfInput.value = "";
        }

        return;
    }

    subiendoPdf = true;

    if (uploadButton) {
        uploadButton.disabled = true;
    }

    cambiarEstado(
        "Leyendo PDF...",
        "busy"
    );

    agregarMensaje(
        `Subiendo «${archivo.name}»...`,
        "assistant",
        {
            id: "mensaje-pdf-pendiente",
            pending: true
        }
    );

    const formData = new FormData();

    formData.append(
        "archivo",
        archivo
    );

    try {
        const response = await fetch(
            RUTAS.subirPdf,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await leerRespuesta(
            response
        );

        eliminarMensaje(
            "mensaje-pdf-pendiente"
        );

        if (!response.ok || !data.ok) {
            agregarMensaje(
                data.respuesta
                || "No se pudo cargar el PDF.",
                "assistant",
                {
                    error: true
                }
            );

            cambiarEstado(
                "No se pudo leer el PDF",
                "error"
            );

            return;
        }

        if (documentName) {
            documentName.textContent =
                data.documento
                || archivo.name;
        }

        if (documentDetails) {
            const paginas =
                Number(data.paginas) || 0;

            documentDetails.textContent =
                paginas > 0
                    ? `${paginas} página(s) disponibles`
                    : "Material listo para usar";
        }

        if (documentStatus) {
            documentStatus.hidden = false;
        }

        agregarMensaje(
            data.respuesta,
            "assistant"
        );

        cambiarEstado(
            "Material cargado"
        );

    } catch (error) {
        console.error(
            "Error al subir el PDF:",
            error
        );

        eliminarMensaje(
            "mensaje-pdf-pendiente"
        );

        agregarMensaje(
            "No se pudo subir el PDF. "
            + "Comprueba que el servidor esté ejecutándose.",
            "assistant",
            {
                error: true
            }
        );

        cambiarEstado(
            "Sin conexión",
            "error"
        );

    } finally {
        subiendoPdf = false;

        if (uploadButton) {
            uploadButton.disabled = false;
        }

        if (pdfInput) {
            pdfInput.value = "";
        }
    }
}


/* =================================================
   EVENTOS DEL PDF
================================================= */

if (uploadButton && pdfInput) {
    uploadButton.addEventListener(
        "click",
        function () {
            pdfInput.click();
        }
    );

    pdfInput.addEventListener(
        "change",
        subirPdf
    );
}


/* =================================================
   HISTORIAL
================================================= */

async function cargarHistorial() {
    if (!contenidoHistorial) {
        return;
    }

    mostrarMensajeVacio(
        contenidoHistorial,
        "Cargando historial..."
    );

    try {
        const response = await fetch(
            RUTAS.historial
        );

        const data = await leerRespuesta(
            response
        );

        if (!response.ok || !data.ok) {
            throw new Error(
                data.respuesta
                || "No se pudo cargar el historial."
            );
        }

        limpiarElemento(
            contenidoHistorial
        );

        const historial =
            Array.isArray(data.historial)
                ? data.historial
                : [];

        if (historial.length === 0) {
            mostrarMensajeVacio(
                contenidoHistorial,
                "No hay conversaciones guardadas todavía."
            );

            return;
        }

        historial.forEach(
            (conversacion) => {
                const item = crearElemento(
                    "article",
                    "history-item"
                );

                const fecha = crearElemento(
                    "p",
                    "history-date",
                    conversacion.fecha
                    || "Sin fecha"
                );

                const pregunta = crearElemento(
                    "p",
                    "history-question",
                    `Tú: ${
                        conversacion.pregunta
                        || "Sin pregunta"
                    }`
                );

                const respuesta = crearElemento(
                    "p",
                    "history-answer",
                    `IA: ${
                        conversacion.respuesta
                        || "Sin respuesta"
                    }`
                );

                item.append(
                    fecha,
                    pregunta,
                    respuesta
                );

                contenidoHistorial.appendChild(
                    item
                );
            }
        );

    } catch (error) {
        console.error(
            "Error al cargar historial:",
            error
        );

        mostrarMensajeVacio(
            contenidoHistorial,
            "No se pudo cargar el historial."
        );
    }
}


/* =================================================
   LIMPIAR HISTORIAL
================================================= */

async function eliminarHistorial() {
    const confirmar = window.confirm(
        "¿Seguro que deseas eliminar todo "
        + "tu historial de conversaciones?"
    );

    if (!confirmar) {
        return;
    }

    try {
        cambiarEstado(
            "Eliminando historial...",
            "busy"
        );

        const response = await fetch(
            RUTAS.limpiarHistorial,
            {
                method: "POST"
            }
        );

        const data = await leerRespuesta(
            response
        );

        if (!response.ok || !data.ok) {
            throw new Error(
                data.respuesta
                || "No se pudo eliminar el historial."
            );
        }

        await cargarHistorial();

        cambiarEstado(
            "Historial eliminado"
        );

    } catch (error) {
        console.error(
            "Error al limpiar historial:",
            error
        );

        window.alert(
            error.message
            || "No se pudo eliminar el historial."
        );

        cambiarEstado(
            "No se pudo eliminar",
            "error"
        );
    }
}


/* =================================================
   REINICIAR PROGRESO
================================================= */

async function reiniciarProgreso() {
    const confirmar = window.confirm(
        "¿Seguro que deseas reiniciar tu progreso? "
        + "Se eliminarán temas aprobados, quizzes, "
        + "niveles y proyectos desbloqueados."
    );

    if (!confirmar) {
        return;
    }

    try {
        cambiarEstado(
            "Reiniciando progreso...",
            "busy"
        );

        const response = await fetch(
            RUTAS.reiniciarProgreso,
            {
                method: "POST"
            }
        );

        const data = await leerRespuesta(
            response
        );

        if (!response.ok || !data.ok) {
            throw new Error(
                data.respuesta
                || "No se pudo reiniciar el progreso."
            );
        }

        quizActual = null;

        if (data.progreso) {
            actualizarPanelCompleto(
                data.progreso,
                data.clase_actual
            );
        } else {
            await cargarProgreso();
        }

        agregarMensaje(
            "Tu progreso fue reiniciado. "
            + "Puedes comenzar nuevamente desde el primer tema.",
            "assistant"
        );

        cambiarEstado(
            "Progreso reiniciado"
        );

    } catch (error) {
        console.error(
            "Error al reiniciar progreso:",
            error
        );

        window.alert(
            error.message
            || "No se pudo reiniciar el progreso."
        );

        cambiarEstado(
            "No se pudo reiniciar",
            "error"
        );
    }
}


/* =================================================
   CARGAR SÍLABO EN EL MODAL
================================================= */

async function cargarSilaboModal() {
    if (!contenidoSilabo) {
        return;
    }

    mostrarMensajeVacio(
        contenidoSilabo,
        "Cargando ruta de aprendizaje..."
    );

    try {
        const response = await fetch(
            RUTAS.silabo
        );

        const data = await leerRespuesta(
            response
        );

        if (!response.ok || !data.ok) {
            throw new Error(
                data.respuesta
                || "No se pudo cargar el sílabo."
            );
        }

        silaboActual =
            Array.isArray(data.niveles)
                ? data.niveles
                : [];

        limpiarElemento(
            contenidoSilabo
        );

        if (silaboActual.length === 0) {
            mostrarMensajeVacio(
                contenidoSilabo,
                "No hay niveles disponibles."
            );

            return;
        }

        silaboActual.forEach(
            (nivel) => {
                const tarjeta = crearElemento(
                    "article",
                    "syllabus-item"
                );

                if (nivel.completado) {
                    tarjeta.classList.add(
                        "completed"
                    );
                }

                if (!nivel.desbloqueado) {
                    tarjeta.classList.add(
                        "locked"
                    );
                }

                const encabezado = crearElemento(
                    "div",
                    "syllabus-item-header"
                );

                const informacion =
                    crearElemento("div");

                const etiqueta = crearElemento(
                    "p",
                    "syllabus-level",
                    `NIVEL ${nivel.numero}`
                );

                const titulo = crearElemento(
                    "h3",
                    "",
                    nivel.nombre
                );

                informacion.append(
                    etiqueta,
                    titulo
                );

                const estado = crearElemento(
                    "span",
                    "syllabus-status",
                    nivel.completado
                        ? "Completado"
                        : nivel.desbloqueado
                            ? "Disponible"
                            : "Bloqueado"
                );

                encabezado.append(
                    informacion,
                    estado
                );

                const descripcion = crearElemento(
                    "p",
                    "syllabus-description",
                    nivel.descripcion
                );

                const lista = crearElemento(
                    "ul",
                    "syllabus-topics"
                );

                const temas =
                    Array.isArray(nivel.temas)
                        ? nivel.temas
                        : [];

                temas.forEach(
                    (tema) => {
                        const item = crearElemento(
                            "li",
                            "",
                            tema
                        );

                        lista.appendChild(item);
                    }
                );

                const proyecto = crearElemento(
                    "p",
                    "syllabus-project",
                    `Proyecto: ${nivel.proyecto}`
                );

                tarjeta.append(
                    encabezado,
                    descripcion,
                    lista,
                    proyecto
                );

                contenidoSilabo.appendChild(
                    tarjeta
                );
            }
        );

        if (progresoActual) {
            actualizarProgresoNivel(
                progresoActual
            );
        }

    } catch (error) {
        console.error(
            "Error al cargar el sílabo:",
            error
        );

        mostrarMensajeVacio(
            contenidoSilabo,
            "No se pudo cargar el sílabo."
        );
    }
}


/* =================================================
   CARGAR PROYECTOS
================================================= */

async function cargarProyectos() {
    if (!contenidoProyectos) {
        return;
    }

    mostrarMensajeVacio(
        contenidoProyectos,
        "Cargando proyectos..."
    );

    try {
        const response = await fetch(
            RUTAS.proyectoActual
        );

        const data = await leerRespuesta(
            response
        );

        limpiarElemento(
            contenidoProyectos
        );

        if (!response.ok || !data.ok) {
            mostrarMensajeVacio(
                contenidoProyectos,
                data.respuesta
                || "Todavía no has desbloqueado proyectos."
            );

            return;
        }

        const proyectos =
            Array.isArray(data.proyectos)
                ? data.proyectos
                : [];

        if (proyectos.length === 0) {
            mostrarMensajeVacio(
                contenidoProyectos,
                "Todavía no has desbloqueado proyectos."
            );

            return;
        }

        proyectos.forEach(
            (proyecto, indice) => {
                const tarjeta = crearElemento(
                    "article",
                    "project-item"
                );

                const numero = crearElemento(
                    "span",
                    "project-number",
                    indice + 1
                );

                const informacion =
                    crearElemento("div");

                const titulo = crearElemento(
                    "h3",
                    "",
                    proyecto
                );

                const descripcion = crearElemento(
                    "p",
                    "",
                    "Proyecto desbloqueado al completar "
                    + "el nivel correspondiente."
                );

                informacion.append(
                    titulo,
                    descripcion
                );

                tarjeta.append(
                    numero,
                    informacion
                );

                contenidoProyectos.appendChild(
                    tarjeta
                );
            }
        );

    } catch (error) {
        console.error(
            "Error al cargar proyectos:",
            error
        );

        mostrarMensajeVacio(
            contenidoProyectos,
            "No se pudieron cargar los proyectos."
        );
    }
}


/* =================================================
   ABRIR PROYECTO ACTUAL
================================================= */

async function abrirProyectoActual() {
    abrirModal(
        modalProyectos
    );

    await cargarProyectos();
}


/* =================================================
   EVENTOS DEL PROGRESO Y PROYECTOS
================================================= */

if (btnReiniciarProgreso) {
    btnReiniciarProgreso.addEventListener(
        "click",
        reiniciarProgreso
    );
}

if (btnAbrirProyecto) {
    btnAbrirProyecto.addEventListener(
        "click",
        abrirProyectoActual
    );
}

if (btnProyectoNivel) {
    btnProyectoNivel.addEventListener(
        "click",
        abrirProyectoActual
    );
}


/* =================================================
   EVENTOS DE MODALES
================================================= */

if (btnVerHistorial) {
    btnVerHistorial.addEventListener(
        "click",
        async function () {
            abrirModal(
                modalHistorial
            );

            await cargarHistorial();
        }
    );
}

if (cerrarHistorial) {
    cerrarHistorial.addEventListener(
        "click",
        function () {
            cerrarModal(
                modalHistorial
            );
        }
    );
}

if (limpiarHistorial) {
    limpiarHistorial.addEventListener(
        "click",
        eliminarHistorial
    );
}

if (btnVerSilabo) {
    btnVerSilabo.addEventListener(
        "click",
        async function () {
            abrirModal(
                modalSilabo
            );

            await cargarSilaboModal();
        }
    );
}

if (cerrarSilabo) {
    cerrarSilabo.addEventListener(
        "click",
        function () {
            cerrarModal(
                modalSilabo
            );
        }
    );
}

if (btnVerProyectos) {
    btnVerProyectos.addEventListener(
        "click",
        async function () {
            abrirModal(
                modalProyectos
            );

            await cargarProyectos();
        }
    );
}

if (cerrarProyectos) {
    cerrarProyectos.addEventListener(
        "click",
        function () {
            cerrarModal(
                modalProyectos
            );
        }
    );
}

if (btnVerPerfil) {
    btnVerPerfil.addEventListener(
        "click",
        function () {
            abrirModal(
                modalPerfil
            );
        }
    );
}

if (cerrarPerfil) {
    cerrarPerfil.addEventListener(
        "click",
        function () {
            cerrarModal(
                modalPerfil
            );
        }
    );
}
/* =================================================
   OBTENER TEMA DEL QUIZ
================================================= */

function obtenerTemaParaQuiz() {
    if (
        claseActualDatos
        && claseActualDatos.tema
    ) {
        return claseActualDatos.tema;
    }

    if (
        progresoActual
        && progresoActual.tema_actual
        && progresoActual.tema_actual
            !== "Curso completado"
    ) {
        return progresoActual.tema_actual;
    }

    return "";
}


/* =================================================
   GENERAR QUIZ
================================================= */

async function generarQuiz() {
    if (generandoQuiz) {
        return;
    }

    const tema = obtenerTemaParaQuiz();

    if (!tema) {
        window.alert(
            "No hay un tema actual disponible para evaluar."
        );

        return;
    }

    generandoQuiz = true;

    if (btnGenerarQuiz) {
        btnGenerarQuiz.disabled = true;
    }

    abrirModal(modalQuiz);

    mostrarMensajeVacio(
        contenidoQuiz,
        `Generando un quiz sobre ${tema}...`
    );

    cambiarEstado(
        "Generando evaluación...",
        "busy"
    );

    try {
        const response = await fetch(
            RUTAS.generarQuiz,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    tema
                })
            }
        );

        const data = await leerRespuesta(
            response
        );

        if (!response.ok || !data.ok) {
            throw new Error(
                data.respuesta
                || "No se pudo generar el quiz."
            );
        }

        quizActual = data.quiz;

        mostrarQuiz(
            quizActual
        );

        cambiarEstado(
            "Quiz listo"
        );

    } catch (error) {
        console.error(
            "Error al generar quiz:",
            error
        );

        mostrarMensajeVacio(
            contenidoQuiz,
            error.message
            || "No se pudo generar el quiz."
        );

        cambiarEstado(
            "No se pudo generar el quiz",
            "error"
        );

    } finally {
        generandoQuiz = false;

        if (btnGenerarQuiz) {
            btnGenerarQuiz.disabled = false;
        }
    }
}


/* =================================================
   MOSTRAR QUIZ
================================================= */

function mostrarQuiz(quiz) {
    if (
        !contenidoQuiz
        || !quiz
        || !Array.isArray(quiz.preguntas)
    ) {
        return;
    }

    limpiarElemento(
        contenidoQuiz
    );

    const tema = crearElemento(
        "p",
        "quiz-topic",
        `Tema: ${quiz.tema}`
    );

    contenidoQuiz.appendChild(
        tema
    );

    const formulario = crearElemento(
        "form"
    );

    formulario.id = "formulario-quiz";

    quiz.preguntas.forEach(
        (pregunta, indice) => {
            const tarjeta = crearElemento(
                "fieldset",
                "quiz-question"
            );

            tarjeta.dataset.indice =
                String(indice);

            const titulo = crearElemento(
                "legend",
                "",
                `${indice + 1}. ${pregunta.pregunta}`
            );

            tarjeta.appendChild(
                titulo
            );

            ["A", "B", "C"].forEach(
                (letra) => {
                    const opcion = crearElemento(
                        "label",
                        "quiz-option"
                    );

                    const radio = document.createElement(
                        "input"
                    );

                    radio.type = "radio";
                    radio.name =
                        `pregunta-${indice}`;
                    radio.value = letra;

                    const texto = crearElemento(
                        "span"
                    );

                    const letraFuerte =
                        crearElemento(
                            "strong",
                            "",
                            `${letra}. `
                        );

                    texto.appendChild(
                        letraFuerte
                    );

                    texto.append(
                        pregunta.opciones[letra]
                    );

                    opcion.append(
                        radio,
                        texto
                    );

                    tarjeta.appendChild(
                        opcion
                    );
                }
            );

            formulario.appendChild(
                tarjeta
            );
        }
    );

    const botonRevisar = crearElemento(
        "button",
        "quiz-submit-button",
        "Revisar respuestas"
    );

    botonRevisar.id =
        "btn-revisar-quiz";

    botonRevisar.type =
        "submit";

    const resultado = crearElemento(
        "div"
    );

    resultado.id =
        "resultado-quiz";

    formulario.append(
        botonRevisar,
        resultado
    );

    formulario.addEventListener(
        "submit",
        async function (event) {
            event.preventDefault();

            await revisarQuiz();
        }
    );

    contenidoQuiz.appendChild(
        formulario
    );
}


/* =================================================
   MARCAR PREGUNTAS
================================================= */

function marcarPreguntasQuiz() {
    if (!quizActual) {
        return;
    }

    quizActual.preguntas.forEach(
        (pregunta, indice) => {
            const tarjeta =
                document.querySelector(
                    `.quiz-question[data-indice="${indice}"]`
                );

            if (!tarjeta) {
                return;
            }

            tarjeta.classList.remove(
                "correct-answer",
                "wrong-answer",
                "unanswered"
            );

            const seleccionada =
                tarjeta.querySelector(
                    `input[name="pregunta-${indice}"]:checked`
                );

            if (!seleccionada) {
                tarjeta.classList.add(
                    "unanswered"
                );

            } else if (
                seleccionada.value
                === pregunta.correcta
            ) {
                tarjeta.classList.add(
                    "correct-answer"
                );

            } else {
                tarjeta.classList.add(
                    "wrong-answer"
                );
            }

            tarjeta
                .querySelectorAll("input")
                .forEach((input) => {
                    input.disabled = true;
                });
        }
    );
}


/* =================================================
   REVISAR QUIZ
================================================= */

async function revisarQuiz() {
    if (!quizActual) {
        return;
    }

    let correctas = 0;
    let preguntasSinResponder = 0;

    const errores = [];
    const partesARepasar = [];

    quizActual.preguntas.forEach(
        (pregunta, indice) => {
            const seleccionada =
                document.querySelector(
                    `input[name="pregunta-${indice}"]:checked`
                );

            if (!seleccionada) {
                preguntasSinResponder += 1;

                errores.push(
                    `Pregunta ${indice + 1}: `
                    + "no seleccionaste una respuesta."
                );

                if (
                    pregunta.parte_a_repasar
                    && !partesARepasar.includes(
                        pregunta.parte_a_repasar
                    )
                ) {
                    partesARepasar.push(
                        pregunta.parte_a_repasar
                    );
                }

                return;
            }

            if (
                seleccionada.value
                === pregunta.correcta
            ) {
                correctas += 1;

            } else {
                errores.push(
                    `Pregunta ${indice + 1}: `
                    + `la respuesta correcta era `
                    + `${pregunta.correcta}. `
                    + `${pregunta.explicacion}`
                );

                if (
                    pregunta.parte_a_repasar
                    && !partesARepasar.includes(
                        pregunta.parte_a_repasar
                    )
                ) {
                    partesARepasar.push(
                        pregunta.parte_a_repasar
                    );
                }
            }
        }
    );

    const resultadoContenedor =
        document.getElementById(
            "resultado-quiz"
        );

    if (!resultadoContenedor) {
        return;
    }

    if (preguntasSinResponder > 0) {
        limpiarElemento(
            resultadoContenedor
        );

        const aviso = crearElemento(
            "div",
            "quiz-result quiz-warning",
            `Debes responder todas las preguntas. `
            + `Te faltan ${preguntasSinResponder}.`
        );

        resultadoContenedor.appendChild(
            aviso
        );

        return;
    }

    const boton =
        document.getElementById(
            "btn-revisar-quiz"
        );

    if (boton) {
        boton.disabled = true;

        boton.textContent =
            "Guardando resultado...";
    }

    marcarPreguntasQuiz();

    try {
        const resultadoGuardado =
            await guardarResultadoQuiz(
                quizActual.tema,
                correctas,
                quizActual.preguntas.length,
                partesARepasar
            );

        mostrarResultadoQuiz(
            resultadoGuardado,
            correctas,
            partesARepasar,
            errores
        );

    } catch (error) {
        console.error(
            "Error al guardar el quiz:",
            error
        );

        limpiarElemento(
            resultadoContenedor
        );

        const aviso = crearElemento(
            "div",
            "quiz-result quiz-failed",
            error.message
            || "No se pudo guardar el resultado."
        );

        resultadoContenedor.appendChild(
            aviso
        );

        if (boton) {
            boton.disabled = false;

            boton.textContent =
                "Revisar respuestas";
        }
    }
}


/* =================================================
   GUARDAR RESULTADO DEL QUIZ
================================================= */

async function guardarResultadoQuiz(
    tema,
    correctas,
    total,
    partesARepasar
) {
    const response = await fetch(
        RUTAS.guardarResultadoQuiz,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                tema,
                correctas,
                total,
                partes_a_repasar:
                    partesARepasar
            })
        }
    );

    const data = await leerRespuesta(
        response
    );

    if (!response.ok || !data.ok) {
        throw new Error(
            data.respuesta
            || "No se pudo guardar el resultado."
        );
    }

    if (data.progreso) {
        actualizarPanelCompleto(
            data.progreso,
            data.siguiente_clase
        );
    } else {
        await cargarProgreso();
    }

    return data;
}


/* =================================================
   MOSTRAR RESULTADO DEL QUIZ
================================================= */

function mostrarResultadoQuiz(
    resultadoGuardado,
    correctas,
    partesARepasar,
    errores
) {
    const resultadoContenedor =
        document.getElementById(
            "resultado-quiz"
        );

    if (!resultadoContenedor) {
        return;
    }

    limpiarElemento(
        resultadoContenedor
    );

    const resultado = crearElemento(
        "div",
        resultadoGuardado.aprobado
            ? "quiz-result quiz-approved"
            : "quiz-result quiz-failed"
    );

    const titulo = crearElemento(
        "h3",
        "",
        resultadoGuardado.aprobado
            ? "Tema aprobado"
            : "Debes reforzar el tema"
    );

    const nota = crearElemento(
        "p",
        "",
        `Obtuviste ${correctas} de `
        + `${quizActual.preguntas.length} `
        + `respuestas correctas `
        + `(${resultadoGuardado.porcentaje}%).`
    );

    resultado.append(
        titulo,
        nota
    );

    if (resultadoGuardado.aprobado) {
        const mensaje = crearElemento(
            "p",
            "",
            "Superaste la nota mínima del 80%. "
            + "El siguiente tema fue desbloqueado."
        );

        resultado.appendChild(
            mensaje
        );

        if (
            resultadoGuardado
                .siguiente_clase
                ?.tema
        ) {
            const siguiente = crearElemento(
                "p",
                "next-topic-message",
                `Siguiente tema: ${
                    resultadoGuardado
                        .siguiente_clase
                        .tema
                }`
            );

            resultado.appendChild(
                siguiente
            );
        }

        cambiarEstado(
            "Tema aprobado"
        );

    } else {
        const mensaje = crearElemento(
            "p",
            "",
            "Necesitas al menos 80% para aprobar. "
            + "Repasa los siguientes puntos:"
        );

        resultado.appendChild(
            mensaje
        );

        const lista = crearElemento(
            "ul"
        );

        partesARepasar.forEach(
            (parte) => {
                const item = crearElemento(
                    "li",
                    "",
                    parte
                );

                lista.appendChild(item);
            }
        );

        resultado.appendChild(
            lista
        );

        const detalles = crearElemento(
            "div",
            "quiz-error-details"
        );

        errores.forEach(
            (error) => {
                const parrafo = crearElemento(
                    "p",
                    "",
                    error
                );

                detalles.appendChild(
                    parrafo
                );
            }
        );

        resultado.appendChild(
            detalles
        );

        cambiarEstado(
            "Tema pendiente de repaso"
        );
    }

    const botonFinal = crearElemento(
        "button",
        "quiz-submit-button",
        resultadoGuardado.aprobado
            ? "Continuar aprendiendo"
            : "Cerrar y repasar"
    );

    botonFinal.type = "button";

    botonFinal.addEventListener(
        "click",
        async function () {
            cerrarModal(
                modalQuiz
            );

            if (
                resultadoGuardado.aprobado
            ) {
                await continuarClase();

            } else {
                await repasarTemaActual();
            }
        }
    );

    resultado.appendChild(
        botonFinal
    );

    resultadoContenedor.appendChild(
        resultado
    );
}


/* =================================================
   EVENTOS DEL QUIZ
================================================= */

if (btnGenerarQuiz) {
    btnGenerarQuiz.addEventListener(
        "click",
        generarQuiz
    );
}

if (cerrarQuiz) {
    cerrarQuiz.addEventListener(
        "click",
        function () {
            cerrarModal(
                modalQuiz
            );
        }
    );
}
/* =================================================
   CERRAR MODALES AL HACER CLIC FUERA
================================================= */

document
    .querySelectorAll(".history-modal")
    .forEach((modal) => {
        modal.addEventListener(
            "click",
            function (event) {
                if (event.target === modal) {
                    cerrarModal(modal);
                }
            }
        );
    });


/* =================================================
   CERRAR MODALES CON ESCAPE
================================================= */

document.addEventListener(
    "keydown",
    function (event) {
        if (event.key !== "Escape") {
            return;
        }

        document
            .querySelectorAll(
                ".history-modal:not(.hidden)"
            )
            .forEach((modal) => {
                cerrarModal(modal);
            });
    }
);


/* =================================================
   ACTUALIZAR PERFIL
================================================= */

function actualizarPerfilUsuario() {
    if (!progresoActual) {
        return;
    }

    if (perfilConsultas) {
        perfilConsultas.textContent =
            Number(
                progresoActual.consultas
            ) || 0;
    }

    if (perfilQuizzes) {
        perfilQuizzes.textContent =
            Number(
                progresoActual.quizzes_realizados
            ) || 0;
    }

    if (perfilProgreso) {
        perfilProgreso.textContent =
            `${
                limitarPorcentaje(
                    progresoActual.porcentaje_general
                )
            }%`;
    }

    if (perfilNivel) {
        perfilNivel.textContent =
            progresoActual.nivel_actual || 1;
    }
}


/* =================================================
   ACTUALIZAR PROYECTO AL ABRIR PERFIL
================================================= */

if (btnVerPerfil) {
    btnVerPerfil.addEventListener(
        "click",
        function () {
            actualizarPerfilUsuario();
        }
    );
}


/* =================================================
   PREPARAR BOTONES DE TEMAS POR REPASAR
================================================= */

function prepararTemasRepaso() {
    if (!listaTemasRepasar) {
        return;
    }

    listaTemasRepasar.addEventListener(
        "click",
        async function (event) {
            const etiqueta =
                event.target.closest(
                    ".topic-tag"
                );

            if (!etiqueta) {
                return;
            }

            const tema =
                etiqueta.textContent.trim();

            if (!tema) {
                return;
            }

            cerrarModal(modalPerfil);

            const pregunta =
                `Necesito repasar "${tema}". `
                + "Explícamelo desde cero, "
                + "con un ejemplo diferente "
                + "y un ejercicio sencillo.";

            await enviarPregunta(
                pregunta
            );
        }
    );
}


/* =================================================
   CONTROL DE ERRORES GLOBALES
================================================= */

window.addEventListener(
    "error",
    function (event) {
        console.error(
            "Error global de JavaScript:",
            event.error || event.message
        );
    }
);


window.addEventListener(
    "unhandledrejection",
    function (event) {
        console.error(
            "Promesa rechazada:",
            event.reason
        );
    }
);


/* =================================================
   COMPROBAR SESIÓN
================================================= */

async function comprobarSesion() {
    try {
        const response = await fetch(
            RUTAS.progreso,
            {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            }
        );

        if (response.status === 401) {
            window.location.href = "/login";

            return false;
        }

        return true;

    } catch (error) {
        console.error(
            "No se pudo comprobar la sesión:",
            error
        );

        return true;
    }
}


/* =================================================
   INICIALIZAR DATOS
================================================= */

async function cargarDatosIniciales() {
    cambiarEstado(
        "Cargando tu progreso...",
        "busy"
    );

    await cargarSilaboBase();
    await cargarProgreso();

    actualizarPerfilUsuario();

    cambiarEstado(
        "Listo para ayudarte"
    );
}


/* =================================================
   INICIALIZACIÓN PRINCIPAL
================================================= */

async function inicializarAplicacion() {
    ajustarTextarea();

    prepararBotonesPrompt();
    prepararTemasRepaso();

    const sesionActiva =
        await comprobarSesion();

    if (!sesionActiva) {
        return;
    }

    await cargarDatosIniciales();

    if (questionInput) {
        questionInput.focus();
    }
}


/* =================================================
   EJECUTAR AL CARGAR EL DOCUMENTO
================================================= */

document.addEventListener(
    "DOMContentLoaded",
    inicializarAplicacion
);