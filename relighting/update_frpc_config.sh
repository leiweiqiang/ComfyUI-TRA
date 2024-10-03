#!/bin/bash

SSH_REMOTE_PORT=${SSH_REMOTE_PORT:-25022}
COMFYUI_REMOTE_PORT=${COMFYUI_REMOTE_PORT:-25188}
JUPYTER_REMOTE_PORT=${JUPYTER_REMOTE_PORT:-25888}
SERVICE_NAME=${HOSTNAME}

FRPC_CONFIG="/frp/frpc.toml"

if [ ! -f "$FRPC_CONFIG" ]; then
    echo "Error: $FRPC_CONFIG does not exist."
    exit 1
fi

sed -i "s/name = \"ssh\"/name = \"$SERVICE_NAME-ssh\"/" "$FRPC_CONFIG"
sed -i "s/name = \"comfyui\"/name = \"$SERVICE_NAME-comfyui\"/" "$FRPC_CONFIG"
sed -i "s/name = \"jupyter-notebook\"/name = \"$SERVICE_NAME-jupyter-notebook\"/" "$FRPC_CONFIG"

sed -i "s/remotePort = 22/remotePort = $SSH_REMOTE_PORT/" "$FRPC_CONFIG"
sed -i "s/remotePort = 8188/remotePort = $COMFYUI_REMOTE_PORT/" "$FRPC_CONFIG"
sed -i "s/remotePort = 8888/remotePort = $JUPYTER_REMOTE_PORT/" "$FRPC_CONFIG"
