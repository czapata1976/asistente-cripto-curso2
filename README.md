# Asistente Cripto Multiagente

Sistema multiagente desplegable para **aprender criptomonedas desde cero**: enruta
cada solicitud al flujo adecuado, ejecuta trabajo real con herramientas, delega
en dos especialistas distintos y deja un registro auditable de cada ejecución.

Tarea final del Curso 2. Este repositorio parte del asistente cripto del curso y
lo extiende con las piezas que faltaban para cumplir la pauta completa.

---

## 1. Qué resuelve y para quién

**Usuarios.** Personas que están aprendiendo sobre criptoactivos y necesitan
resolver dudas concretas sin recibir consejos de inversión: calcular cuánto
ganaron o perdieron, entender un concepto del manual, saber el precio de mercado
hoy, o armar un plan de aportes periódicos de práctica.

**Qué no hace.** No da recomendaciones de inversión, no opera con dinero real, no
registra compras reales y no inventa datos cuando no tiene evidencia: si el
manual no cubre la pregunta, lo dice.

**Alcance.** Cinco flujos sobre un corpus cerrado (el manual
`criptomonedas-desde-cero.md`, 2.631 líneas). El servicio es de **solo lectura**:
la única acción con efecto, registrar una compra simulada, está deshabilitada en
la API por diseño.

---

## 2. Arquitectura

```mermaid
flowchart TD
    U[Usuario] -->|POST /consulta<br/>Bearer token| R[Router]
    R -->|charla| C[conversacion]
    R -->|cálculo o acción| H[herramienta<br/>ciclo ReAct]
    R -->|concepto| D[delegacion_a2a]
    R -->|precio| M[mcp]
    R -->|plan de aportes| P[plan]

    H --> T[(tools locales)]
    D -->|A2A JSON-RPC| E1[Especialista LangGraph<br/>RAG sobre el manual]
    M -->|MCP| E2[Servidor MCP CoinGecko]
    P -->|A2A JSON-RPC| E3[Especialista n8n<br/>plan DCA]

    C --> J[Juez]
    H --> J
    D --> J
    M --> J
    P --> J
    J --> RESP[Respuesta]
    RESP --> REG[(Registro JSONL)]
```

El **mismo agente** cumple los roles de router y worker: clasifica la solicitud y
después ejecuta el trabajo del flujo elegido.

| Componente | Archivo | Rol |
|---|---|---|
| Grafo | `main.py` | `START → router → rama → juez → END` |
| Router | `nodes/router.py` | Clasificación con salida estructurada (`Literal` cerrado) |
| ReAct | `nodes/herramienta.py` | Bucle `bind_tools` con tope `MAX_ITERACIONES = 5` |
| A2A obligatorio | `nodes/delegacion.py` | Encargo al especialista LangGraph |
| A2A adicional | `nodes/plan.py` | Encargo al especialista n8n |
| MCP | `nodes/mcp.py` | Precio en vivo desde CoinGecko |
| RAG | `nodes/rag.py` | Recuperación con umbral de similitud `0.65` |
| Juez | `nodes/juez.py` | Filtro determinista + revisión LLM |
| API | `servidor.py` | `POST /consulta`, `POST /rag`, `GET /registro/{id}`, `/salud` |
| Especialista 1 | `servidor_especialista.py` | LangGraph en el puerto 2024 |
| Especialista 2 | `n8n/a2a-plan-dca.json` | Workflow n8n con webhook A2A |

---

## 3. Los flujos

| Solicitud de ejemplo | Ruta | Trabajo que ejecuta | Resultado esperado |
|---|---|---|---|
| «Compré 0,5 BTC a USD 40000 y hoy vale USD 50000. ¿Cuánto gané?» | `herramienta` | ReAct: llama `calcular_ganancia`, recibe la observación y responde | Ganancia USD 5.000,00 (+25,00%) |
| «¿Cuántos pesos chilenos son 100 dólares?» | `herramienta` | ReAct: `convertir_a_pesos` con tasa fija declarada | 95.000 CLP |
| «Registra una compra simulada de 1 BTC a 40000 USD» | `herramienta` | Detecta la acción de escritura y **la bloquea** | Mensaje de acción no autorizada; portafolio intacto |
| «¿Qué es una billetera de criptomonedas?» | `rag` | A2A al especialista LangGraph, que recupera del manual | Respuesta con fuentes y similitud |
| «¿Cuál es la receta del pastel de choclo?» | `rag` o `conversacion` | Sin evidencia suficiente: no llama al generador | «No tengo esa información en el material disponible» |
| «¿Cuánto vale bitcoin hoy?» | `mcp` | Decide criptos, llama al MCP de CoinGecko, redacta con el dato | Precio real, sin inventar |
| «Quiero comprar 50 USD de bitcoin cada semana durante 12 semanas» | `plan` | A2A al especialista n8n, que calcula el plan | Tabla de 12 compras y total USD 600,00 |
| «Hola, ¿qué puedes hacer?» | `conversacion` | Charla con historial | Presentación del asistente |

Cada respuesta incluye `ruta`, `traza`, `solicitud_id` y la evidencia del flujo
(`herramientas`, `mcp`, `fuentes`, `delegacion`, `delegacion_n8n`).

---

## 4. Entorno y ejecución local

Probado con **Python 3.12** en Windows. La versión 3.14 no sirve: algunas
dependencias fijadas no tienen wheel para ella.

```powershell
cd asistente-cripto
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Completa `GOOGLE_API_KEY` en `.env` (gratis en
<https://aistudio.google.com/apikey>). Genera también `CRIPTO_API_TOKEN`,
`WEB_USER_PASSWORD`, `WEB_ADMIN_PASSWORD` y `WEB_SESSION_SECRET` con valores
aleatorios, por ejemplo:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Índice del manual

```powershell
python cargar_guia.py --revisar   # cuenta fragmentos sin llamar a Gemini
python cargar_guia.py             # genera embeddings e indexa (386 fragmentos)
```

El corpus por defecto es `criptomonedas-desde-cero.md`, versionado en el
repositorio. También acepta un PDF: `python cargar_guia.py ruta/manual.pdf`.

### Levantar los servicios

Tres terminales con el entorno activado:

```powershell
# 1. Especialista LangGraph (A2A obligatorio), puerto 2024
python -m uvicorn servidor_especialista:app --host 127.0.0.1 --port 2024

# 2. Especialista n8n (A2A adicional), puerto 5678
npx --yes n8n import:workflow --input=n8n/a2a-plan-dca.json
npx n8n start

# 3. Agente principal, puerto 8000
python -m uvicorn servidor:app --host 127.0.0.1 --port 8000
```

Para comprobar que el workflow de n8n responde A2A antes de seguir:

```powershell
python scripts\probar_n8n.py
```

Abre <http://127.0.0.1:8000/app> para el chat web, o usa la API:

```powershell
$token = (Select-String -Path .env -Pattern '^CRIPTO_API_TOKEN=(.+)$').Matches.Groups[1].Value
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/consulta' `
  -Headers @{ Authorization = "Bearer $token" } -ContentType 'application/json' `
  -Body '{"mensaje":"¿Qué es una stablecoin?"}' | ConvertTo-Json -Depth 8
```

> n8n es **opcional**. Si `N8N_WEBHOOK_URL` está vacío, la rama `plan` responde
> con un mensaje controlado y el resto del agente funciona igual.

### Base de datos opcional (pgvector)

El backend por defecto es SQLite y no necesita servidor de base de datos. Para usar
Postgres con pgvector hay un `docker-compose.yml` listo:

```powershell
docker compose up -d
# en .env: RAG_BACKEND=postgres y SUPABASE_DB_URL=postgresql://cripto:cripto@127.0.0.1:5433/cripto
python cargar_guia.py
```

---

## 5. Configuración

Todas las variables se leen en `config.py`. Los valores secretos **nunca** están
en el repositorio: `.env` está en `.gitignore`.

| Variable | Función |
|---|---|
| `GOOGLE_API_KEY` | Credencial de Gemini. Obligatoria. |
| `GOOGLE_MODEL` | Identificador del modelo de chat. |
| `GEMINI_EMBEDDING_MODEL` | Modelo de embeddings del RAG. |
| `CRIPTO_API_TOKEN` | Clave Bearer de `POST /consulta` y `POST /rag`. |
| `ESPECIALISTA_A2A_URL` | URL del especialista LangGraph. |
| `ESPECIALISTA_API_TOKEN` | Clave opcional para ese especialista. |
| `ESPECIALISTA_CLOUD_RUN_IAM` | `1` usa identidad IAM entre servicios de Cloud Run. |
| `N8N_WEBHOOK_URL` | Webhook del workflow A2A de n8n. Vacío lo deshabilita. |
| `MCP_URL` | Servidor MCP de CoinGecko. |
| `RAG_BACKEND` | `sqlite` (local) o `postgres` (pgvector). |
| `RAG_CORPUS` | Documento a indexar. |
| `RAG_SQLITE_PATH` | Archivo del índice local. |
| `SUPABASE_DB_URL` | Cadena de conexión, solo con `RAG_BACKEND=postgres`. |
| `REGISTRO_PATH` | Archivo JSONL del registro de ejecuciones. |
| `WEB_USER_PASSWORD` / `WEB_ADMIN_PASSWORD` | Contraseñas del chat web (deben ser distintas). |
| `WEB_SESSION_SECRET` | Firma de las cookies de sesión. |
| `WEB_SECURE_COOKIE` | `1` fuerza cookies `Secure` detrás de HTTPS. |
| `WEB_HISTORY_POSTGRES` | `1` guarda el historial en Postgres en vez de SQLite. |
| `WEB_HISTORY_DB` | Ruta del SQLite de historial. |
| `DEBUG` | `1` activa trazas de depuración. |

---

## 6. Datos de ejemplo

- **Consultas de prueba:** `evals/casos.jsonl` (11 casos con resultado esperado).
- **Corpus autorizado:** `criptomonedas-desde-cero.md`, material del curso,
  versionado en el repositorio.
- **Portafolio simulado:** `datos/portafolio.json`, se crea solo si se ejecuta la
  acción de escritura (deshabilitada en la API).
- **Conversaciones:** `datos/historial_web.sqlite3`, generado por el chat web.

---

## 7. Pruebas y evidencias

### 7.1 Todo lo automatizable, en un comando

```powershell
.\scripts\probar_todo.ps1
```

El script comprueba qué servicios están levantados, ejecuta las cuatro suites en
orden y termina con una tabla resumen. Si no tienes n8n corriendo, usa
`-SinN8n`: esos casos se marcan omitidos en vez de fallidos. Para una verificación
rápida sin red ni servicios, `-SoloUnitarias`.

También se pueden ejecutar por separado:

```powershell
python -m unittest discover -s tests          # 9 pruebas unitarias
python -m evals.ejecutar                      # 12 casos del agente
python evidencias/pruebas_base.py             # 20 pruebas de la base
python scripts/metricas.py                    # métricas del registro
```

Resultados de la última corrida registrada en este repositorio:

| Conjunto | Resultado |
|---|---|
| Tests unitarios | **9/9** |
| Casos de evaluación | **12/12** |
| Pruebas de evidencias | **20/20** |

Los informes quedan en `evals/resultados/` y `evidencias/` en Markdown (legible) y
JSON (con las respuestas completas sin recortar).

### 7.2 Cómo se demuestra cada criterio de la base

| Criterio | Cómo verlo |
|---|---|
| **Enrutamiento** | Los dos primeros casos de `evidencias/pruebas_base.py`: la misma API responde por `herramienta` y por `rag`, con trabajo distinto en cada una. |
| **Ciclo ReAct** | En la respuesta de la consulta de ganancia, mira `herramientas`: aparece la llamada `tool=calcular_ganancia args=… -> observación`, y luego la parada «respuesta final del LLM». El tope duro es `MAX_ITERACIONES = 5`. |
| **Delegación A2A** | En la consulta de concepto, mira `delegacion`: trae `agente`, `encargo`, `tarea_id` y `estado`. Las `fuentes` de la respuesta salen de ese artefacto. |
| **Seguridad** | `POST /consulta` sin cabecera o con token inválido devuelve **401**. El bloqueo de escritura se demuestra en `tests/test_seguridad.py`, que fuerza el `tool_call` con un modelo falso: el nodo lo intercepta antes de ejecutar y la herramienta ni siquiera se le ofrece al modelo. |
| **Resiliencia** | La última prueba de `pruebas_base.py` apunta el cliente A2A a un puerto cerrado: el flujo devuelve `fallo_a2a` con un mensaje claro, sin inventar la respuesta ni reintentar en bucle. Hay además un test para el límite de cuota de Gemini (`ModelRateLimitError`), que cae a un cálculo local determinista. |
| **Despliegue** | Cada respuesta trae `solicitud_id`; `GET /registro/{solicitud_id}` devuelve la línea del registro con ruta, estado, traza y latencia. |

### 7.3 Ampliaciones y su prueba

| Ampliación | Puntos | Prueba |
|---|---|---|
| **RAG documental** | +0,5 | `POST /rag` recupera fragmentos **sin delegar en otro agente** y devuelve `fuentes` y `fragmentos` con su similitud. Una pregunta fuera del corpus devuelve `sin_evidencia: true`. |
| **MCP** | +0,5 | «¿Cuánto vale bitcoin hoy?» → ruta `mcp`; el campo `mcp` muestra la decisión y la llamada real a CoinGecko. |
| **Memoria persistente** | +0,5 | Dos `POST /consulta` con el mismo `session_id`: el segundo turno recuerda el nombre dado en el primero. También por el chat web. |
| **Evaluación versionada** | +0,5 | `evals/casos.jsonl` + `python -m evals.ejecutar`. |
| **Observabilidad** | +0,5 | `python scripts/metricas.py --comparar antes.jsonl despues.jsonl`. Ver 7.4. |
| **A2A con n8n** | +1,0 | «Quiero comprar 50 USD de bitcoin cada semana durante 12 semanas» → ruta `plan`; el campo `delegacion_n8n` trae `encargo`, `tarea_id`, `estado` y el artefacto calculado en n8n. |

### 7.4 Comparación antes/después (observabilidad)

Mismo conjunto de 11 entradas, ejecutado con y sin el juez LLM:

```powershell
python -m evals.ejecutar --sin-juez --sin-dependencias
Move-Item datos/registros/ejecuciones.jsonl datos/registros/antes.jsonl
python -m evals.ejecutar --sin-dependencias
Move-Item datos/registros/ejecuciones.jsonl datos/registros/despues.jsonl
python scripts/metricas.py --comparar datos/registros/antes.jsonl datos/registros/despues.jsonl
```

Resultado medido:

| Métrica | Sin juez | Con juez | Δ |
|---|---|---|---|
| Casos aprobados | 11/11 | 11/11 | 0 |
| p50 de latencia | 10.100 ms | 17.855 ms | +77% |
| Tokens de entrada | 9.640 | 15.581 | +62% |
| Llamadas al modelo por consulta | 2,09 | 3,09 | +1,00 |

**Conclusión honesta:** el juez añade exactamente una llamada al modelo por
consulta y casi duplica la latencia, sin mejorar la tasa de aprobación en este
conjunto. Se mantiene porque el filtro determinista de secretos cubre lo
anticipado y el juez cubre lo que no lo está; pero la medición deja claro que, si
el costo importa, desactivarlo es una decisión defendible con estos números en la
mano.

---

## 8. Despliegue

El `Dockerfile` sirve cualquier plataforma que ejecute contenedores. El servicio
necesita los dos especialistas accesibles: el de LangGraph y, si se usa la
ampliación, el de n8n.

```powershell
docker build -t asistente-cripto .
docker run -p 8080:8080 --env-file .env asistente-cripto
```

Variables mínimas en el entorno del despliegue: `GOOGLE_API_KEY`,
`CRIPTO_API_TOKEN`, `ESPECIALISTA_A2A_URL`, `RAG_BACKEND`, `MCP_URL` y las del chat
web.

### Despliegue en Google Cloud Run

El proyecto **agente-cripto-uai** tiene ID `animated-spider-434900-a4` y
número `201930158969`. Cloud Build, Artifact Registry y los dos servicios
funcionan en Santiago (`southamerica-west1`). El especialista
`cripto-especialista` es privado; el servicio `agente-cripto-uai` ofrece
el [chat web](https://agente-cripto-uai-201930158969.southamerica-west1.run.app/app).

El activador `deploy-agente-cripto-main` escucha pushes a `main` desde la
conexión GitLab de segunda generación. Usa `cloudbuild.yaml` para ejecutar
las pruebas, construir y publicar la imagen, y actualizar primero el
especialista y luego el chat. Cloud Run obtiene las credenciales desde
Secret Manager y guarda las conversaciones en Supabase.

`.gitlab-ci.yml` ejecuta pruebas. Su despliegue alternativo se habilita
con `DEPLOY_FROM_GITLAB=1` y Workload Identity Federation. Para usar el
activador de Cloud Build, deja esa variable sin definir.

**Credenciales de prueba:** se entregan por correo a los profesores. No están en
este repositorio, ni en la documentación, ni en las evidencias.

---

## 9. Estructura del repositorio

```text
.
├── main.py                  grafo del agente
├── servidor.py              API HTTP + registro
├── servidor_especialista.py especialista A2A (LangGraph)
├── especialista.py          grafo del especialista
├── config.py                única lectura de variables de entorno
├── llm.py                   creación diferida del modelo
├── cargar_guia.py           indexación del corpus (PDF o Markdown)
├── nodes/                   un archivo por nodo del grafo
├── prompts/                 prompts por nodo
├── services/                a2a, mcp, rag (sqlite/postgres), memoria, registro, telemetría
├── tools/                   herramientas del ciclo ReAct
├── web/                     chat y login
├── tests/                   pruebas unitarias
├── evals/                   casos versionados + runner
├── evidencias/              pruebas de la base + informes
├── scripts/metricas.py      métricas y comparación
├── n8n/                     workflow A2A exportado
└── supabase/migrations/     esquema para el backend pgvector
```

---

## 10. Limitaciones conocidas

- **Depende de Gemini.** Sin `GOOGLE_API_KEY` ningún flujo con modelo funciona;
  solo el cálculo local de respaldo.
- **El router es un LLM.** Puede clasificar de forma distinta entre corridas; los
  casos de evaluación usan expectativas tolerantes donde el límite es ambiguo.
- **El RAG local es fuerza bruta.** Compara el vector de la consulta contra todos
  los fragmentos en Python. Con 386 fragmentos es instantáneo; con millones haría
  falta pgvector o un índice ANN.
- **El juez LLM no está justificado por las métricas** en el conjunto actual (ver
  7.4). Es una decisión de defensa en profundidad, no de calidad medida.
- **La acción de escritura solo existe en la consola local**, no en la API.
- **n8n no corre en el despliegue de Render** por defecto: es un servicio aparte y
  hay que levantarlo donde el agente principal pueda alcanzarlo.
