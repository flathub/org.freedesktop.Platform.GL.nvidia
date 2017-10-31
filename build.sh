#!/bin/bash

source ./versions.sh

ARCH=$1
EXTRA_ARGS=$2

set -e
set -x

SDK_BRANCH=1.4
SDK_RUNTIME_VERSION=1.6

for VER in $DRIVER_VERSIONS; do
    F="data/nvidia-$VER-$ARCH.data"
    if [ ! -f $F ]; then
        echo WARNING, no data file for $VER $ARCH
        continue
    fi
    NVIDIA_VERSION=$(echo $VER | sed "s/\./-/")
    EXTRA_DATA=$(cat $F)
    rm -f org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json
    sed -e "s/@@SDK_BRANCH@@/${SDK_BRANCH}/g"			\
        -e "s/@@SDK_RUNTIME_VERSION@@/${SDK_RUNTIME_VERSION}/g"	\
        -e "s/@@NVIDIA_VERSION@@/${NVIDIA_VERSION}/g"		\
        -e "s=@@EXTRA_DATA@@=${EXTRA_DATA}=g" \
        org.freedesktop.Platform.GL.nvidia.json.in > org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json

    flatpak-builder -v --force-clean --ccache --sandbox --delete-build-dirs \
                    --user --install-deps-from=flathub \
                    --arch=${ARCH} \
                    --repo=repo --subject="build of, org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION `date`" \
                    ${EXTRA_ARGS} builddir org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json
    rm org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json
done
