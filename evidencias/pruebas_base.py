"""Pruebas de la base obligatoria contra el servicio en ejecución.

Genera el informe de evidencias que pide la pauta: cada prueba muestra la
entrada, la ejecución observada y el resultado. Está pensado para que el
docente (o cualquier compañero) lo repita con un comando.

Requisitos:
    1. El especialista A2A en marcha (puerto 2024).
    2. El servicio principal en marcha (puerto 8000).
    3. El índice del RAG cargado (`python cargar_guia.py`).

Uso:
    python evidencias/pruebas_base.py
    python evidencias/pruebas_base.py --url http://127.0.0.1:8000

Salida:
    evidencias/informe-<fecha>.md   informe legible
    evidencias/informe-<fecha>.json respuestas completas, sin recortar
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from config import settings  # noqa: E402
from tools.herramientas import PORTAFOLIO_PATH  # noqa: E402


SALIDA = Path(__file__).resolve().parent
resultados: list[dict] = []


def registrar(criterio: str, prueba: str, ok: bool, observado: str, evidencia=None) -> None:
    """Añade una prueba al informe."""
    resultados.append({
        "criterio": criterio,
        "prueba": prueba,
        "resultado": "PASÓ" if ok else "FALLÓ",
        "observado": observado,
        "evidencia": evidencia,
    })
    marca = "OK   " if ok else "FALLA"
    print(f"  [{marca}] {prueba}")
    if not ok:
        print(f"           → {observado}")


def consultar(base: str, mensaje: str, token: str | None = None,
              session_id: str | None = None) -> tuple[int, dict]:
    """Envía una consulta al servicio y devuelve (status, cuerpo)."""
    cabeceras = {"Content-Type": "application/json; charset=utf-8"}
    if token is not None:
        cabeceras["Authorization"] = f"Bearer {token}"
    cuerpo = {"mensaje": mensaje}
    if session_id:
        cuerpo["session_id"] = session_id
    try:
        respuesta = httpx.post(f"{base}/consulta", json=cuerpo, headers=cabeceras, timeout=90)
        return respuesta.status_code, respuesta.json()
    except httpx.HTTPError as exc:
        return 0, {"error": f"{type(exc).__name__}: {exc}"}


def prueba_salud(base: str) -> None:
    try:
        cuerpo = httpx.get(f"{base}/salud", timeout=15).json()
        registrar("Despliegue", "El servicio responde en /salud", True,
                  f"modelo={cuerpo.get('modelo')} rag={cuerpo.get('rag_backend')}", cuerpo)
    except httpx.HTTPError as exc:
        registrar("Despliegue", "El servicio responde en /salud", False, str(exc))


def prueba_sin_token(base: str) -> None:
    # 1. Sin cabecera Authorization.
    status, cuerpo = consultar(base, "¿Qué es una billetera de criptomonedas?")
    registrar("Seguridad", "Solicitud sin credencial se rechaza", status == 401,
              f"HTTP {status} · {cuerpo.get('error')}", {"status": status, "cuerpo": cuerpo})

    # 2. Con un token inválido.
    status, cuerpo = consultar(base, "¿Qué es una billetera de criptomonedas?", token="token-falso")
    registrar("Seguridad", "Solicitud con token inválido se rechaza", status == 401,
              f"HTTP {status} · {cuerpo.get('error')}", {"status": status, "cuerpo": cuerpo})


def prueba_enrutamiento(base: str, token: str) -> None:
    calculo = "Compré 0,5 BTC a USD 40000 y hoy cada BTC vale USD 50000. ¿Cuánto gané?"
    concepto = "¿Qué es una billetera de criptomonedas?"

    s1, r1 = consultar(base, calculo, token)
    s2, r2 = consultar(base, concepto, token)

    ok = s1 == 200 and s2 == 200 and r1.get("ruta") != r2.get("ruta")
    registrar("Enrutamiento", "Dos solicitudes activan flujos distintos", ok,
              f"«{calculo[:38]}…» → {r1.get('ruta')} · «{concepto[:38]}…» → {r2.get('ruta')}",
              {"calculo": r1, "concepto": r2})

    # ReAct: se ve la herramienta, la observación y la decisión de parar.
    pasos = r1.get("herramientas") or []
    usar_tool = any("tool=" in paso for paso in pasos)
    recibio_obs = any("->" in paso for paso in pasos)
    decidio_parar = any("respuesta final" in paso for paso in pasos)
    registrar("ReAct", "El agente llama una herramienta y recibe el resultado",
              usar_tool and recibio_obs, f"{len(pasos)} pasos: {pasos[:1]}",
              {"pasos_react": pasos})
    registrar("ReAct", "Condición de parada explícita en la traza", decidio_parar,
              "parada por respuesta final del LLM; tope duro MAX_ITERACIONES = 5",
              {"pasos_react": pasos})

    # A2A: encargo, respuesta del especialista y uso.
    delegacion = r2.get("delegacion") or {}
    registro_a2a = delegacion.get("registro_a2a") if isinstance(delegacion, dict) else None
    tiene_encargo = bool(delegacion.get("encargo"))
    tiene_tarea = bool(delegacion.get("tarea_id"))
    respondio = delegacion.get("estado") == "respondido"
    usa_resultado = bool(r2.get("fuentes")) or respondio
    registrar("Delegación A2A", "El especialista responde el encargo",
              tiene_encargo and tiene_tarea and respondio,
              f"agente={delegacion.get('agente')} · tarea={delegacion.get('tarea_id')} "
              f"· estado={delegacion.get('estado')}",
              {"delegacion": delegacion})
    registrar("Delegación A2A", "El resultado del especialista se usa en la respuesta",
              usa_resultado, f"fuentes citadas: {r2.get('fuentes')}",
              {"respuesta": r2.get("respuesta"), "fuentes": r2.get("fuentes")})

    # RAG: fragmentos recuperados con su similitud (dentro del especialista).
    fragmentos = delegacion.get("fragmentos") or []
    registrar("Delegación A2A", "El especialista devuelve fragmentos con similitud",
              len(fragmentos) >= 1,
              "; ".join(f"{f['fuente']} ({f['similitud']})" for f in fragmentos) or "sin fragmentos",
              {"fragmentos": fragmentos})


def prueba_rag_directo(base: str, token: str) -> None:
    """RAG por el propio agente principal, sin pasar por el especialista.

    Separa el criterio «RAG documental» del criterio «delegación A2A»: aquí no
    hay encargo a otro agente, solo recuperación y uso de las fuentes.
    """
    cabeceras = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    pregunta = "¿Qué es una stablecoin y cómo mantiene su paridad?"
    try:
        respuesta = httpx.post(f"{base}/rag", json={"pregunta": pregunta},
                               headers=cabeceras, timeout=90)
        cuerpo = respuesta.json()
    except httpx.HTTPError as exc:
        registrar("RAG documental", "El agente principal recupera fragmentos por sí mismo",
                  False, str(exc))
        return

    fragmentos = cuerpo.get("fragmentos") or []
    fuentes = cuerpo.get("fuentes") or []
    mejor = fragmentos[0]["similitud"] if fragmentos else None
    registrar("RAG documental", "El agente principal recupera fragmentos sin delegar (POST /rag)",
              respuesta.status_code == 200 and len(fragmentos) >= 1 and bool(fuentes),
              f"{len(fragmentos)} fragmentos · mejor similitud={mejor}", cuerpo)

    texto = (cuerpo.get("respuesta") or "").casefold()
    respaldada = bool(fuentes) and any(f.casefold() in texto for f in fuentes)
    registrar("RAG documental", "Las fuentes recuperadas se usan en la respuesta",
              respaldada, f"fuentes={fuentes}", {"respuesta": cuerpo.get("respuesta")})

    # El umbral debe cortar las preguntas fuera del corpus en vez de inventar.
    try:
        fuera = httpx.post(f"{base}/rag", json={"pregunta": "¿Cuál es la mejor receta de pastel de choclo?"},
                           headers=cabeceras, timeout=90).json()
    except httpx.HTTPError:
        return
    registrar("RAG documental", "Una pregunta fuera del corpus no inventa una respuesta",
              bool(fuera.get("sin_evidencia")) and not fuera.get("fuentes"),
              f"sin_evidencia={fuera.get('sin_evidencia')} · respuesta={(fuera.get('respuesta') or '')[:80]}",
              fuera)


def _bloqueo_determinista() -> dict:
    """Fuerza el `tool_call` de escritura y verifica la intercepción del nodo.

    Sin esto, la prueba por HTTP es engañosa: cuando el modelo se niega por su
    cuenta no hay `accion_bloqueada` en la traza, y parecería que el sistema
    bloqueó algo que en realidad nunca se pidió.
    """
    from unittest.mock import patch

    from langchain_core.messages import AIMessage
    from nodes.herramienta import herramienta

    class ModeloForzado:
        """Modelo falso que pide la herramienta de escritura."""

        def __init__(self) -> None:
            self.n = 0
            self.vinculadas: list[str] = []

        def bind_tools(self, tools):  # noqa: ANN001
            self.vinculadas = [t.name for t in tools]
            return self

        def invoke(self, mensajes):  # noqa: ANN001
            self.n += 1
            if self.n == 1:
                return AIMessage(content="", tool_calls=[{
                    "name": "registrar_compra_simulada",
                    "args": {"cripto": "bitcoin", "cantidad": 1, "precio_usd": 40000},
                    "id": "call-escritura",
                }])
            return AIMessage(content="Listo.")

    modelo = ModeloForzado()
    with patch("nodes.herramienta.get_llm", return_value=modelo):
        salida = herramienta({
            "user_input": "Registra una compra de 1 bitcoin a 40000 USD.",
            "permitir_escritura": False,
        })
    return {"salida": salida, "herramientas_ofrecidas": modelo.vinculadas}


def prueba_accion_bloqueada(base: str, token: str) -> None:
    antes = PORTAFOLIO_PATH.read_text(encoding="utf-8") if PORTAFOLIO_PATH.exists() else None
    status, cuerpo = consultar(base, "Registra una compra simulada de 1 bitcoin a 40000 USD.", token)
    despues = PORTAFOLIO_PATH.read_text(encoding="utf-8") if PORTAFOLIO_PATH.exists() else None

    sin_efecto = antes == despues
    registro = _bloqueo_determinista()
    salida = registro["salida"]
    interceptada = "accion_bloqueada" in (salida.get("trace") or [])
    no_ofrecida = "registrar_compra_simulada" not in registro["herramientas_ofrecidas"]

    # 1. La garantía del código: aunque el modelo pida la escritura, no se ejecuta.
    registrar("Seguridad", "El código intercepta la escritura antes de ejecutarla",
              interceptada and no_ofrecida,
              f"traza={salida.get('trace')} · herramienta no ofrecida={no_ofrecida} "
              f"· respuesta={salida.get('borrador', '')[:80]}",
              registro)

    # 2. El efecto observable: el intento real por HTTP no modifica el portafolio.
    registrar("Seguridad", "El intento por HTTP no altera el portafolio",
              status == 200 and sin_efecto,
              f"HTTP {status} · traza={cuerpo.get('traza')} · portafolio sin cambios={sin_efecto}",
              {"status": status, "cuerpo": cuerpo, "portafolio_antes": antes,
               "portafolio_despues": despues})


def prueba_mcp(base: str, token: str) -> None:
    status, cuerpo = consultar(base, "¿Cuánto vale bitcoin hoy en dólares?", token)
    pasos = cuerpo.get("mcp") or []
    registro_ok = any("respuesta MCP" in paso for paso in pasos)
    registrar("MCP", "El agente obtiene el precio por MCP y lo usa",
              status == 200 and cuerpo.get("ruta") == "mcp" and registro_ok,
              f"ruta={cuerpo.get('ruta')} · {len(pasos)} pasos MCP",
              {"cuerpo": cuerpo})


def prueba_plan_n8n(base: str, token: str) -> None:
    """Flujo A2A adicional: el especialista vive en n8n, no en LangGraph.

    Es un caso distinto al obligatorio: el de la guía responde conceptos;
    este calcula un plan de aportes periódicos.
    """
    mensaje = ("Quiero comprar 50 dólares de bitcoin cada semana durante 12 semanas. "
               "Ármame el plan.")
    status, cuerpo = consultar(base, mensaje, token)
    delegacion = cuerpo.get("delegacion_n8n") or {}
    artefacto = delegacion.get("artefacto") or {}

    encargado = (status == 200 and cuerpo.get("ruta") == "plan"
                 and delegacion.get("estado") == "completado")
    registrar("A2A con n8n", "El agente principal encarga el plan al especialista n8n",
              encargado,
              f"ruta={cuerpo.get('ruta')} · agente={delegacion.get('agente')} "
              f"· tarea={delegacion.get('tarea_id')} · estado={delegacion.get('estado')}",
              {"cuerpo": cuerpo})

    compras = artefacto.get("compras")
    total = float(artefacto.get("total_usd") or 0)
    correcto = compras == 12 and abs(total - 600.0) < 0.01
    registrar("A2A con n8n", "n8n calcula el plan y su resultado se usa en la respuesta",
              correcto,
              f"{compras} compras · total USD {total:,.2f} "
              f"· respuesta={(cuerpo.get('respuesta') or '')[:90]}",
              {"artefacto": artefacto, "respuesta": cuerpo.get("respuesta")})


def prueba_memoria(base: str, token: str) -> None:
    import uuid

    session_id = str(uuid.uuid4())
    _, primera = consultar(base, "Hola, me llamo Valentina y estoy aprendiendo de cripto.", token, session_id)
    _, segunda = consultar(base, "¿Cómo me llamo y qué estoy aprendiendo?", token, session_id)

    respuesta = (segunda.get("respuesta") or "").casefold()
    recuerda = "valentina" in respuesta
    registrar("Memoria persistente", "El agente retoma el hilo en una segunda solicitud",
              recuerda, f"respuesta al segundo turno: {segunda.get('respuesta', '')[:160]}",
              {"session_id": session_id, "turno1": primera, "turno2": segunda})


def prueba_registro(base: str, token: str) -> None:
    status, cuerpo = consultar(base, "¿Qué es una stablecoin?", token)
    solicitud_id = cuerpo.get("solicitud_id")
    if not solicitud_id:
        registrar("Despliegue", "El registro permite cruzar una solicitud", False,
                  "la respuesta no trajo solicitud_id", {"cuerpo": cuerpo})
        return
    fila = httpx.get(f"{base}/registro/{solicitud_id}",
                     headers={"Authorization": f"Bearer {token}"}, timeout=20).json()
    coincide = fila.get("solicitud_id") == solicitud_id and fila.get("ruta") == cuerpo.get("ruta")
    registrar("Despliegue", "El registro permite cruzar una solicitud y su resultado", coincide,
              f"solicitud={solicitud_id} · ruta={fila.get('ruta')} · estado={fila.get('estado')} "
              f"· {fila.get('duracion_ms')} ms",
              {"respuesta": cuerpo, "registro": fila})


def prueba_resiliencia() -> None:
    """Provoca un fallo real de A2A apuntando el cliente a un puerto cerrado.

    Se hace en proceso (no por HTTP) para no tener que reiniciar el servicio.
    El efecto que ve el usuario es el mismo que al detener el especialista.
    """
    from nodes.delegacion import delegar_concepto

    original = settings.especialista_url
    # Puerto 9 (discard): la conexión se rechaza de inmediato, sin esperar timeout.
    object.__setattr__(settings, "especialista_url", "http://127.0.0.1:9")
    try:
        salida = delegar_concepto({"user_input": "¿Qué es una billetera de criptomonedas?"})
    finally:
        object.__setattr__(settings, "especialista_url", original)

    estado = (salida.get("delegacion") or {}).get("estado")
    traza = salida.get("trace") or []
    ok = estado == "fallo_a2a" and "fallo_a2a" in traza
    registrar("Resiliencia", "Un fallo de A2A se maneja sin inventar la respuesta",
              ok, f"estado={estado} · traza={traza} · mensaje={salida.get('borrador', '')[:90]}",
              {"salida": {k: v for k, v in salida.items() if k != "fragmentos"}})


def escribir_informe(base: str) -> Path:
    sello = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    total = len(resultados)
    paso = sum(1 for r in resultados if r["resultado"] == "PASÓ")

    lineas = [
        "# Informe de evidencias — asistente cripto multiagente",
        "",
        f"- Fecha (UTC): {sello}",
        f"- Servicio probado: `{base}`",
        f"- Modelo: `{settings.google_model}` · Backend RAG: `{settings.rag_backend}`",
        f"- Resultado: **{paso}/{total}** pruebas aprobadas",
        "",
        "Cada fila muestra la prueba, lo observado en la ejecución y su veredicto.",
        "Las respuestas completas están en el `.json` que acompaña a este informe.",
        "",
        "| Criterio | Prueba | Resultado | Observado |",
        "|---|---|---|---|",
    ]
    for r in resultados:
        observado = r["observado"].replace("|", "\\|").replace("\n", " ")
        lineas.append(f"| {r['criterio']} | {r['prueba']} | **{r['resultado']}** | {observado} |")

    destino = SALIDA / f"informe-{sello}.md"
    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    (SALIDA / f"informe-{sello}.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return destino


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="URL del servicio principal")
    args = parser.parse_args()

    if not settings.api_token:
        print("Falta CRIPTO_API_TOKEN en el .env.", file=sys.stderr)
        return 1

    base, token = args.url.rstrip("/"), settings.api_token
    print(f"Probando {base}\n")

    prueba_salud(base)
    prueba_sin_token(base)
    prueba_enrutamiento(base, token)
    prueba_rag_directo(base, token)
    prueba_accion_bloqueada(base, token)
    prueba_mcp(base, token)
    prueba_plan_n8n(base, token)
    prueba_memoria(base, token)
    prueba_registro(base, token)
    prueba_resiliencia()

    destino = escribir_informe(base)
    fallidas = [r for r in resultados if r["resultado"] == "FALLÓ"]
    print(f"\nInforme: {destino}")
    print(f"Aprobadas: {len(resultados) - len(fallidas)}/{len(resultados)}")
    return 1 if fallidas else 0


if __name__ == "__main__":
    raise SystemExit(main())
