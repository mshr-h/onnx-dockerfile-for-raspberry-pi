# Build ONNX Python wheel package for Raspberry Pi 3

This repository provides [ONNX](https://github.com/onnx/onnx) build dockerfile for Arm32v7l (Raspberry Pi 3).

Currently we support the following conbination of software versions.

- Python 3.7-3/10
- Debian Bullseye/Buster

We provide pre-build docker images below.

- [mshrh/onnx-raspberry-pi-3](https://hub.docker.com/r/mshrh/onnx-raspberry-pi-3)

You can pull it with the command below.

```bash
docker pull mshrh/onnx-raspberry-pi-3
```

Or you can manually build image from Dockerfile by following instruction.

## Build instruction

1. Install DockerCE on your machine by following the instruction
    - [https://docs.docker.com/install/](https://docs.docker.com/install/)

2. Clone this repository

```sh
git clone https://github.com/mshr-h/onnx-dockerfile-for-raspberry-pi
cd onnx-dockerfile-for-raspberry-pi
```

3. Move to a folder where you want to build for and run docker build

```sh
cd 3.7-bullseye-build # Debian bullseye with Python 3.7
docker build -t onnx-arm32v7 -f Dockerfile.arm32v7 .
```

4. Note the fullpath of the `.whl` file

5. Copy the Python wheel file from the docker image

```sh
docker create -ti --name onnx_temp onnx-arm32v7 bash
docker cp onnx_temp:/code/onnx/dist/onnx-1.6.0-cp35-cp35m-linux_armv7l.whl .
docker rm -fv onnx_temp
```

6. Copy wheel file(`onnx-1.6.0-cp35-cp35m-linux_armv7l.whl`) to the Raspberry Pi 3 or other ARM device

7. Install the ONNX wheel file

```sh
sudo apt update
sudo apt install -y python3 python3-pip
pip install onnx-1.6.0-cp35-cp35m-linux_armv7l.whl
```
