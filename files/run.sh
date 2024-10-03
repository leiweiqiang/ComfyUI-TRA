#!/bin/bash
# docker run -d --runtime=nvidia --restart always --gpus device=3 --name relighting-nuke-1 \
#  -v /home/exx/workspace/relighting/workspace:/root/workspace \
#  leiweiqiang/relighting-nuke:latest
docker run -d \
    --name relighting \
    -e SSH_REMOTE_PORT=22022 \
    -e COMFYUI_REMOTE_PORT=22188 \
    -e JUPYTER_REMOTE_PORT=22888 \
    -v /home/exx/workspace/relighting/workspace/ComfyUI/input:/ComfyUI/input \
    -v /home/exx/workspace/relighting/workspace/ComfyUI/output:/ComfyUI/output \
    --runtime=nvidia \
    --restart always \
    --gpus device=3 \
    leiweiqiang/relighting-nuke:latest
