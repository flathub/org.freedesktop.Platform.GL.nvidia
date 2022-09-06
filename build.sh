#!/usr/bin/env bash

source ./versions.sh

ARCH=$1
REPO=$2
EXPORT_ARGS=$3
FB_ARGS=$4
SUBJECT=${5:-"org.freedesktop.Platform.GL.nvidia `git rev-parse HEAD`"}

set -e
set -x

SDK_BRANCH=1.4
SDK_RUNTIME_VERSION=21.08

for VER in $DRIVER_VERSIONS; do
    F="data/nvidia-$VER-$ARCH.data"
    if [ ! -f $F ]; then
        echo WARNING, no data file for $VER $ARCH
        continue
    fi
    NVIDIA_VERSION=$(echo $VER | sed "s/\./-/;s/\./-/")
    EXTRA_DATA=$(cat $F)
    NVIDIA_URL=$(cat $F | sed "s/:[^:]*:[^:]*:[^:]*://")
    if test "${ARCH}" = "i386" ; then \
        REF=org.freedesktop.Platform.GL32.nvidia
	ARCH=x86_64
    else
	REF=org.freedesktop.Platform.GL.nvidia
    fi

    rm -f org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json
    sed -e "s/@@SDK_BRANCH@@/${SDK_BRANCH}/g"			\
        -e "s/@@SDK_RUNTIME_VERSION@@/${SDK_RUNTIME_VERSION}/g"	\
        -e "s/@@NVIDIA_VERSION@@/${NVIDIA_VERSION}/g"		\
        -e "s=@@EXTRA_DATA@@=${EXTRA_DATA}=g" \
        -e "s=@@NVIDIA_URL@@=${NVIDIA_URL}=g" \
        -e "s=@@REF@@=${REF}=g" }
        org.freedesktop.Platform.GL.nvidia.json.in > ${REF}-$NVIDIA_VERSION.json

    flatpak-builder -v --force-clean --ccache --sandbox --delete-build-dirs \
                    --arch=${ARCH} --repo=${REPO} \
                    --subject="${SUBJECT}" \
                    ${FB_ARGS} ${EXPORT_ARGS} builddir ${REF}-$NVIDIA_VERSION.json


    rm org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json
done
