# n8n como servicio de Cloud Run.
#
# Por qué una imagen propia en vez de `n8nio/n8n` a secas: Cloud Run crea
# contenedores nuevos con frecuencia y su disco es efímero. La definición del
# workflow tiene que estar disponible sin intervención manual, así que la
# imagen lleva el JSON dentro y un entrypoint lo importa la primera vez.
#
# La persistencia NO vive en el contenedor: n8n guarda workflows, credenciales
# y ejecuciones en Postgres (DB_TYPE=postgresdb). Sin eso, cada arranque en frío
# perdería el workflow y el webhook dejaría de existir.
#
# Build (el contexto es esta misma carpeta `n8n/`, porque solo necesita el
# workflow y el entrypoint):
#   docker build -t cripto-n8n n8n/
#   gcloud builds submit n8n/ --tag=<region>-docker.pkg.dev/<proyecto>/<repo>/cripto-n8n
#
# La versión se fija para que el workflow y el motor no se desincronicen: el
# JSON usa nodos con `typeVersion` concretos.

FROM n8nio/n8n:2.49.6

# El usuario `node` ya viene en la imagen oficial; se mantiene para no correr
# como root, que Cloud Run no permite de todos modos.
USER node
WORKDIR /home/node

COPY --chown=node:node a2a-plan-dca.json /home/node/workflow.json
COPY --chown=node:node entrypoint.sh /home/node/entrypoint.sh
RUN chmod +x /home/node/entrypoint.sh

# Cloud Run solo enruta al puerto que se declara en el servicio (`--port`).
ENV N8N_PORT=5678 \
    N8N_LISTEN_ADDRESS=0.0.0.0 \
    N8N_DIAGNOSTICS_ENABLED=false \
    N8N_RUNNERS_MODE=internal \
    N8N_BLOCK_ENV_ACCESS_IN_NODE=false \
    N8N_PROXY_HOPS=1

EXPOSE 5678
ENTRYPOINT ["/home/node/entrypoint.sh"]
