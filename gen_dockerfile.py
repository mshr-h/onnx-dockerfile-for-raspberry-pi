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
    cmake \
    curl \
    libtool \
    unzip \
    zlib1g-dev

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install numpy

# Clone protobuf repo
WORKDIR /code
RUN git clone https://github.com/protocolbuffers/protobuf protobuf

# Install protobuf from source
WORKDIR /code/protobuf
RUN git checkout v21.4 && \
  git submodule update --init --recursive
RUN ./autogen.sh && \
  ./configure --with-zlib && \
  make -j$(nproc) && \
  make install && \
  sudo ldconfig

# Clone onnx repo
WORKDIR /code
RUN git clone --single-branch --branch main--recursive $https://github.com/onnx/onnx onnx

# Start the basic build
WORKDIR /code/onnx
RUN CMAKE_ARGS=-DONNX_USE_LITE_PROTO=ON python3 setup.py bdist_wheel

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
