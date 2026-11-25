# Asistente cripto multiagente

Asistente educativo en español para principiantes. Calcula ganancias y pérdidas,
explica conceptos desde la guía del curso y consulta precios mediante CoinGecko MCP.

- **Agente principal** (`main.py`, `servidor.py`). Clasifica la solicitud, ejecuta el
  ciclo ReAct para cálculos y pasa la respuesta por un juez. La API es de solo lectura.
- **Especialista cripto** (`especialista.py`). Corre en otro proceso, expone A2A
  de forma nativa mediante LangGraph y recupera fragmentos de la guía desde Supabase con pgvector.
  Devuelve una respuesta con fuentes o indica que faltan evidencias.

```text
POST /consulta → router del agente principal
                  ├─ cálculo → herramientas ReAct
                  ├─ conceptos → A2A → especialista → guía en Supabase
                  ├─ precio → CoinGecko MCP
                  └─ conversación
                → juez → respuesta y trazas
```

## Arranque local

Desde esta carpeta, con Python 3.11 o 3.12 y PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Completa `GOOGLE_API_KEY`, `GOOGLE_MODEL`, `SUPABASE_DB_URL` y
`CRIPTO_API_TOKEN` en el archivo local. Usa la URI del pooler de Supabase
en modo transacción con TLS. Aplica la migración de `supabase/migrations/`
antes de cargar la guía. Coloca el PDF `Criptoactivos_Basico.pdf` en la
carpeta padre o ajusta la ruta del comando al archivo que tengas. Desde la
raíz del repositorio, ejecuta:

```powershell
python cargar_guia_supabase.py "..\Criptoactivos_Basico.pdf"
```

La carga envía los fragmentos a Gemini para generar los embeddings y guarda
el texto, el archivo, la página y los vectores en `cripto.fragmentos`.

La carga inicial del proyecto `agente-cripto` indexó **170 fragmentos de
65 páginas** con `gemini-embedding-001` (3.072 dimensiones). Para reproducir
la prueba, inicia el especialista A2A y el chat, ingresa como `usuario` y
pregunta «¿Qué es una stablecoin y cómo mantiene su paridad?».
En **Ver ejecución**, comprueba que la ruta sea `rag`, que la delegación
tenga un ID de tarea y que la respuesta muestre citas del PDF. La prueba
local recuperó las páginas 36, 40 y 41. El detalle muestra extractos y
puntuaciones de similitud.

`MCP_URL` configura CoinGecko. `ESPECIALISTA_A2A_URL` apunta al servidor LangGraph.
`ESPECIALISTA_API_TOKEN` se configura si ese servidor requiere clave.

Abre dos terminales con el entorno activado y ejecuta:

```powershell
# Terminal 1. Especialista A2A, puerto 2024.
$env:PYTHONIOENCODING = 'utf-8'
langgraph dev --no-browser --allow-blocking
```

```powershell
# Terminal 2. API del agente principal, puerto 8000.
python -m uvicorn servidor:app --host 127.0.0.1 --port 8000
```

También puedes ejecutar `python main.py` para usar la consola original. La consola
conserva el historial de la sesión y permite escribir en el portafolio simulado local.

## Pruebas de demostración

En otra terminal, desde esta carpeta:

```powershell
$env:CRIPTO_API_TOKEN = Read-Host 'Token de prueba'
function Consultar-Cripto($mensaje) {
    $body = @{ mensaje = $mensaje } | ConvertTo-Json -Compress
    Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:8000/consulta' `
        -Headers @{ Authorization = "Bearer $env:CRIPTO_API_TOKEN" } `
        -ContentType 'application/json; charset=utf-8' `
        -Body ([Text.Encoding]::UTF8.GetBytes($body)) | ConvertTo-Json -Depth 10
}

Consultar-Cripto 'Compré 0,5 BTC a USD 40000 y hoy cada BTC vale USD 50000. ¿Cuánto gané?'
Consultar-Cripto '¿Qué es una billetera de criptomonedas?'
Consultar-Cripto 'Registra una compra simulada de 1 BTC a 40000 USD.'
```

| Prueba | Evidencia esperada |
|---|---|
| Cálculo | Ruta `herramienta`, observación de USD 5000 de ganancia y decisión de terminar en `herramientas`. |
| Concepto | Ruta `rag`, encargo, ID de tarea y respuesta del especialista en `delegacion`. La respuesta final usa ese resultado y conserva las fuentes en `fuentes`. |
| Acción bloqueada | La compra simulada desde HTTP se rechaza. El registro local queda intacto. |
| Autenticación | Repite el POST con un token incorrecto. La API devuelve HTTP 401. |
| Fallo | Detén el especialista y repite la pregunta educativa. La traza muestra `fallo_a2a` y el principal indica que no pudo consultarlo. |
| Registro | Busca el `solicitud_id` de la respuesta en la terminal del principal para ver ruta, estado y traza. |

Para entregar al docente, despliega el agente principal con HTTPS y configura
`ESPECIALISTA_A2A_URL` con la dirección accesible desde ese servicio. Mantén el
especialista en una red privada o protegido por autenticación. `langgraph dev` es
el arranque local de desarrollo. Documenta la URL de revisión y comparte el token
de prueba por el canal privado que indica la pauta.

## Chat web

Configura dos contraseñas distintas en el archivo local `.env` con
`WEB_USER_PASSWORD` y `WEB_ADMIN_PASSWORD`. Usa `WEB_SESSION_SECRET` con
un valor aleatorio privado para conservar las sesiones entre reinicios
y compartir la firma entre procesos del mismo servicio. Reinicia el
servidor y abre [el chat local](http://127.0.0.1:8000/app).

- **usuario** puede crear y retomar conversaciones del mismo navegador.
- **admin** puede ver, retomar y eliminar las conversaciones guardadas.
- **Ver ejecución** muestra la ruta, el ciclo ReAct o el intercambio A2A,
  las fuentes y el ID de la solicitud.

El historial usa SQLite en `datos/historial_web.sqlite3`. Configura
`WEB_HISTORY_DB` sobre un volumen persistente para conservar conversaciones
al redesplegar. Usa HTTPS en el servicio desplegado y configura
`WEB_SECURE_COOKIE=1` si el proxy no informa el esquema a Uvicorn.
La API `POST /consulta` también sigue disponible mediante su token Bearer.
