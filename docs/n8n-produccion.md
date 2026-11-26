# El flujo de n8n en producción

Cómo hacer que la rama `plan` funcione en el servicio desplegado, y qué se
corrigió para que el fallo actual sea diagnosticable.

## Por qué falla hoy en GCP

El contenedor del agente **no lleva `.env`** (está en `.dockerignore`, y debe
estarlo: contiene claves). Por eso `settings.n8n_webhook_url` vale `""` y
`pedir_plan()` abortaba antes de intentar conectarse.

El mensaje que veía el usuario era engañoso:

> «No pude contactar al planificador. Intenta de nuevo en unos minutos.»

Eso describe un fallo transitorio, y aquí no lo es: falta configuración. Al
reintentar nunca iba a funcionar.

Y aunque se hubiera definido la variable, apuntaba a
`http://127.0.0.1:5678/webhook/a2a-plan`. Dentro de Cloud Run, `127.0.0.1` es el
**propio contenedor del agente**, donde no hay ningún n8n escuchando. En local
funciona porque n8n y el agente comparten la máquina; en la nube son procesos
separados y necesitan una URL real.

## Qué se corrigió en el código

| Archivo | Cambio |
|---|---|
| `services/n8n_cliente.py` | Excepciones propias: `N8NNoConfigurado` (falta la variable) y `N8NInalcanzable` (hay URL pero no responde). Se distingue `HTTP 401` de un fallo de red. |
| `nodes/plan.py` | Si falta configuración, la traza dice `n8n_no_configurado` y el mensaje es honesto: «El planificador de aportes no está habilitado en este despliegue». No promete un reintento inútil. |
| `config.py` | Nueva variable `N8N_CLOUD_RUN_IAM`, misma que ya usaba el especialista LangGraph. |
| `services/n8n_cliente.py` | Si `N8N_CLOUD_RUN_IAM=1`, pide un ID token de Google para la audiencia del servicio. Así n8n **puede ser privado** y no hay que inventar una clave compartida. |
| `servidor.py` → `/salud` | Publica `especialistas.n8n_configurado` y `n8n_con_iam`. Es el primer sitio donde mirar cuando la rama responde «no disponible». |

Con eso, el diagnóstico en producción pasa a ser de una línea:

```powershell
Invoke-RestMethod 'https://agente-cripto-uai-201930158969.southamerica-west1.run.app/salud'
```

```json
"especialistas": { "langgraph_configurado": true, "n8n_configurado": false, "n8n_con_iam": false }
```

## Qué hace falta para que funcione

n8n necesita **tres cosas que hoy no existen en GCP**: un lugar donde correr,
una base de datos persistente y una URL que el agente alcance.

### 1. Base de datos para n8n

Ya tienes Supabase. n8n guarda ahí sus workflows, credenciales y ejecuciones.
Usa una **conexión directa o en modo sesión** (puerto `5432`), no el pooler de
transacciones (puerto `6543`): ese modo no soporta sesiones persistentes y las
migraciones de n8n fallan a mitad.

Necesitas sacar de tu cadena de conexión:

| Variable de n8n | Valor |
|---|---|
| `DB_TYPE` | `postgresdb` |
| `DB_POSTGRESDB_HOST` | host de Supabase |
| `DB_POSTGRESDB_PORT` | `5432` |
| `DB_POSTGRESDB_DATABASE` | `postgres` |
| `DB_POSTGRESDB_USER` | usuario de Supabase |
| `DB_POSTGRESDB_PASSWORD` | contraseña de Supabase |
| `DB_POSTGRESDB_SCHEMA` | `n8n` (aislado del esquema `cripto` que ya usas) |
| `DB_POSTGRESDB_SSL_ENABLED` | `true` |

### 2. Secreto de cifrado

n8n cifra con `N8N_ENCRYPTION_KEY` las credenciales que guarda. Si cambia entre
arranques, esas credenciales dejan de leerse. Va en Secret Manager, no en el
repositorio:

```powershell
# Genera una clave y guárdala una sola vez.
python -c "import secrets; print(secrets.token_urlsafe(32))" | Out-File clave.txt
gcloud secrets create cripto-n8n-encryption --data-file=clave.txt
Remove-Item clave.txt
```

### 3. Desplegar n8n en Cloud Run, privado

```powershell
$proyecto = 'animated-spider-434900-a4'
$region   = 'southamerica-west1'
$imagen   = "$region-docker.pkg.dev/$proyecto/cloud-run-source-deploy/cripto-n8n"

# Construye desde la carpeta n8n/ (contexto pequeño: solo el workflow y el entrypoint)
gcloud builds submit n8n/ --project=$proyecto --region=$region --tag=$imagen

gcloud run deploy cripto-n8n `
  --project=$proyecto --region=$region `
  --image=$imagen `
  --port=5678 `
  --no-allow-unauthenticated `
  --memory=1Gi --cpu=1 --timeout=300 `
  --set-env-vars="DB_TYPE=postgresdb,DB_POSTGRESDB_HOST=<host>,DB_POSTGRESDB_PORT=5432,DB_POSTGRESDB_DATABASE=postgres,DB_POSTGRESDB_USER=<usuario>,DB_POSTGRESDB_SCHEMA=n8n,DB_POSTGRESDB_SSL_ENABLED=true,N8N_HOST=0.0.0.0,N8N_PROTOCOL=https" `
  --set-secrets="DB_POSTGRESDB_PASSWORD=cripto-supabase:latest,N8N_ENCRYPTION_KEY=cripto-n8n-encryption:latest"
```

`--no-allow-unauthenticated` es lo correcto aquí: el webhook no queda abierto a
internet y el agente lo invoca con identidad de servicio. Es el mismo esquema
que ya usa `cripto-especialista`.

### 4. Permitir que el agente invoque a n8n

```powershell
gcloud run services add-iam-policy-binding cripto-n8n `
  --project=$proyecto --region=$region `
  --member="serviceAccount:<cuenta-del-servicio-agente>" `
  --role=roles/run.invoker
```

La cuenta del agente es la que ya usa `agente-cripto-uai` (en el pipeline es
`GCP_CHAT_SERVICE_ACCOUNT`). El especialista LangGraph la tiene como invoker, así
que puedes copiar el mismo miembro.

### 5. Decirle al agente dónde está n8n

```powershell
$urlN8n = gcloud run services describe cripto-n8n `
  --project=$proyecto --region=$region --format='value(status.url)'

gcloud run services update agente-cripto-uai `
  --project=$proyecto --region=$region `
  --update-env-vars="N8N_WEBHOOK_URL=$urlN8n/webhook/a2a-plan,N8N_CLOUD_RUN_IAM=1"
```

Esto es un `update`, no un `deploy`: **no reconstruye la imagen** ni interrumpe
el servicio más que unos segundos, así que no compite con el activador de Cloud
Build.

## Verificación

```powershell
$base = 'https://agente-cripto-uai-201930158969.southamerica-west1.run.app'

# 1. El agente debe reportar el planificador configurado.
Invoke-RestMethod "$base/salud"
#    -> especialistas.n8n_configurado = true, n8n_con_iam = true

# 2. La rama plan debe responder y traer la delegación.
$token = '<CRIPTO_API_TOKEN>'
Invoke-RestMethod -Method Post "$base/consulta" `
  -Headers @{ Authorization = "Bearer $token" } -ContentType 'application/json' `
  -Body '{"mensaje":"Quiero comprar 50 USD de bitcoin cada semana durante 12 semanas. Ármame el plan."}' |
  ConvertTo-Json -Depth 8
#    -> ruta = plan, delegacion_n8n.estado = completado, artefacto.compras = 12
```

Si `n8n_configurado` sigue en `false`, la variable no llegó al contenedor. Si
está en `true` pero `delegacion_n8n.estado` es `fallo_n8n`, revisa los logs de
`cripto-n8n`: lo normal es que el workflow no se haya publicado (el entrypoint
lo intenta en cada arranque) o que la base de datos haya rechazado la conexión.

## Costos y límites que conviene saber

- **n8n no escala a cero gratis.** Con `--no-allow-unauthenticated` y
  `--memory=1Gi`, un servicio con instancias mínimas en cero arranca en frío en
  cada periodo de inactividad, y la primera consulta de plan tardará decenas de
  segundos. Si molesta, fija `--min-instances=1` y asume el costo.
- **Cloud Run no garantiza disco.** Por eso todo lo persistente va a Postgres.
  El `N8N_ENCRYPTION_KEY` es lo único que, si se pierde, obliga a volver a crear
  las credenciales de n8n.
- **El editor de n8n queda privado.** Para abrirlo hay que usar
  `gcloud run services proxy cripto-n8n --region=southamerica-west1` y entrar por
  `http://localhost:8080`. Es intencional: el editor no debe ser público.
- **Alternativa más barata si no quieres operar n8n en GCP:** correr n8n en otra
  plataforma con HTTPS y la misma base Postgres, y apuntar `N8N_WEBHOOK_URL` ahí
  sin `N8N_CLOUD_RUN_IAM`. El código soporta ambos modos.
