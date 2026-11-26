#!/bin/sh
# Arranque de n8n en Cloud Run.
#
# Tareas:
#   1. Importar el workflow si todavía no está en la base de datos.
#   2. Publicarlo, para que el webhook exista.
#   3. Arrancar n8n en primer plano.
#
# La comprobación previa es importante: importar en cada arranque duplicaría el
# workflow (uno nuevo por cada instancia y por cada reinicio en frío).
set -e

WORKFLOW_ID="a2a-plan-dca"
WORKFLOW_FILE="/home/node/workflow.json"

echo "n8n: comprobando si el workflow '$WORKFLOW_ID' ya existe..."

# `n8n list:workflow` imprime "ID|Name". Si el comando falla (por ejemplo, en
# el primer arranque la base todavía no responde), se asume que no existe y se
# intenta importar: es idempotente porque usa el mismo id.
if n8n list:workflow 2>/dev/null | grep -q "$WORKFLOW_ID"; then
    echo "n8n: workflow ya presente, no se reimporta."
else
    echo "n8n: importando workflow desde $WORKFLOW_FILE..."
    n8n import:workflow --input="$WORKFLOW_FILE"
    echo "n8n: workflow importado."
fi

# Publicar es lo que hace que el webhook quede expuesto. En n8n 2.x el comando
# se llama `publish:workflow`; en versiones anteriores era `update:workflow`.
# Se intenta el nuevo y se cae al antiguo para no romper con otras versiones.
if ! n8n publish:workflow --id="$WORKFLOW_ID" 2>/dev/null; then
    echo "n8n: publish:workflow no disponible, usando update:workflow."
    n8n update:workflow --id="$WORKFLOW_ID" --active=true
fi
echo "n8n: workflow publicado."

exec n8n start
