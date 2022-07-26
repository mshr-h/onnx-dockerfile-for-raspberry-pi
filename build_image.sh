#!/bin/bash
PWD=`pwd`
dirs=`ls -d -1 3.*-*-*`
for dname in $dirs; do
  docker build . --file $dname/Dockerfile.arm32v7 --tag mshr-h/onnx-raspberry-pi-3:$dname
done
