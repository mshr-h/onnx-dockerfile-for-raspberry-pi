base_images = [
    "3.10-bullseye-build", "3.10-buster-build", "3.7-bullseye-build",
    "3.7-buster-build", "3.8-bullseye-build", "3.8-buster-build",
    "3.9-bullseye-build", "3.9-buster-build"
]

template = r"""FROM balenalib/raspberrypi3-python:{}

#Enforces cross-compilation through Qemu
RUN [ "cross-build-start" ]

RUN apt update && apt install -y \
    autoconf \
    automake \
    build-essential \
    curl \
    libtool \
    protobuf-compiler \
    libprotobuf-dev \
    unzip \
    zlib1g-dev

# Install CMake from source
WORKDIR /code
RUN git clone https://github.com/Kitware/CMake && \
    cd CMake && \
    git checkout v3.24.0 && \
    ./bootstrap && make && make install && \
    cd .. && \
    rm -rf CMake

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install numpy protobuf

# Clone onnx repo
WORKDIR /code
RUN git clone --single-branch --branch main --recursive https://github.com/onnx/onnx onnx

# Start the basic build
WORKDIR /code/onnx
RUN CMAKE_ARGS="-DONNX_USE_PROTOBUF_SHARED_LIBS=ON" python3 setup.py bdist_wheel

# print output path
RUN realpath /code/onnx/dist/onnx-*.whl

RUN [ "cross-build-end" ]
"""

if __name__ == "__main__":
    print("Start generating Dockerfile.arm32v7")
    for i in base_images:
        fname = "{}/Dockerfile.arm32v7".format(i)
        print("  Generating {}".format(fname))
        with open(fname, mode="w") as f:
            f.write(template.format(i))
