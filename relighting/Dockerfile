FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04
RUN apt-get update && apt-get install -y \
    nano \
    vim \
    htop \
    tmux \
    openssh-server \
    supervisor \
    sudo \
    git \
    cmake \
    build-essential \
    curl \
    tar \
    gzip \
    unzip \
    zip \
    pkg-config \
    autoconf \
    automake \
    libtool \
    pkg-config \
    autoconf-archive \
    && rm -rf /var/lib/apt/lists/*
# Clone vcpkg repository
RUN git clone https://github.com/microsoft/vcpkg.git /vcpkg

# Set working directory
WORKDIR /vcpkg

# Bootstrap vcpkg
RUN ./bootstrap-vcpkg.sh

# Install OpenImageIO and dependencies via vcpkg
RUN ./vcpkg install openimageio[tools,opencolorio,pybind11]

# Create symlink to make OpenImageIO available in Python's site-packages
RUN ln -s /vcpkg/installed/x64-linux/lib/python3.11/site-packages/OpenImageIO/OpenImageIO.cpython-311-x86_64-linux-gnu.so /usr/local/lib/python3.11/dist-packages/OpenImageIO.so

# RUN mkdir /var/run/sshd
# RUN echo 'root:tratra' | chpasswd
# RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
# RUN mkdir -p /app
# COPY ./runpod.txt /etc
# COPY ./start.sh /app
# COPY ./frp /frp
# WORKDIR /root/workspace
# RUN chmod +x /app/start.sh
# EXPOSE 22
# ENTRYPOINT ["bash", "/app/start.sh"]

# SSH configuration and key generation

COPY ./workspace/ComfyUI /ComfyUI
RUN pip install -r /ComfyUI/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/ComfyUI_essentials/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/was-node-suite-comfyui/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/ComfyUI-Easy-Use/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/ComfyUI-Inspire-Pack/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/ComfyUI-Inspyrenet-Rembg/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/ComfyUI-TRA/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/ComfyUI-KJNodes/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/ComfyUI-Manager/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/ComfyUI-VideoHelperSuite/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/efficiency-nodes-comfyui/requirements.txt
RUN pip install -r /ComfyUI/custom_nodes/rgthree-comfy/requirements.txt

RUN mkdir /var/run/sshd
RUN echo 'root:tratra' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
RUN mkdir -p /etc/ssh \
    && /usr/bin/ssh-keygen -A \
    && chmod 600 /etc/ssh/ssh_host_* \
    && chmod 644 /etc/ssh/ssh_host_*.pub

# Remove input and output directories from ComfyUI
RUN rm -rf /ComfyUI/input /ComfyUI/output

# SSH configuration, FRP setup, and supervisor
RUN mkdir -p /app
COPY ./runpod.txt /etc
COPY ./frp /frp
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chmod +x /frp/update_frpc_config.sh

WORKDIR /root/
EXPOSE 22
EXPOSE 8188
EXPOSE 8888

# Add a startup script to create symbolic links for input and output directories
# CMD ["/bin/bash", "-c", "ln -s /input /ComfyUI/input && ln -s /output /ComfyUI/output && /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]
CMD ["/bin/bash", "-c", "/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]

