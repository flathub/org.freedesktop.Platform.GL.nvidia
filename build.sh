#!/usr/bin/env bash

source ./versions.sh

ARCH=$1
REPO=$2
EXPORT_ARGS=$3
FB_ARGS=$4
SUBJECT=${5:-"org.freedesktop.Platform.GL.nvidia `git rev-parse HEAD`"}

set -e
set -x

for VER in $DRIVER_VERSIONS; do
    F="data/nvidia-$VER-$ARCH.data"
    if [ ! -f $F ]; then
        echo WARNING, no data file for $VER $ARCH
        continue
    fi
    NVIDIA_VERSION=$(echo $VER | sed "s/\./-/;s/\./-/")
    NVIDIA_SHA256=$(cat $F | pcregrep -o1 "^:([^:]*):")
    NVIDIA_URL=$(cat $F | sed "s/:[^:]*:[^:]*:[^:]*://")
    rm -f org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json
    sed -e "s/@@NVIDIA_VERSION@@/${NVIDIA_VERSION}/g"		\
        -e "s=@@NVIDIA_URL@@=${NVIDIA_URL}=g" \
        -e "s=@@NVIDIA_SHA256@@=${NVIDIA_SHA256}=g" \
        org.freedesktop.Platform.GL.nvidia.json.in > org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json

    flatpak-builder -v --force-clean --ccache --sandbox --delete-build-dirs \
                    --arch=${ARCH} --repo=${REPO} \
                    --subject="${SUBJECT}" \
                    ${FB_ARGS} ${EXPORT_ARGS} builddir org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json

    if test "${ARCH}" = "i386" ; then \
        flatpak build-commit-from  ${EXPORT_ARGS} --src-ref=runtime/org.freedesktop.Platform.GL.nvidia-${NVIDIA_VERSION}/${ARCH}/${SDK_BRANCH} ${REPO} runtime/org.freedesktop.Platform.GL32.nvidia-${NVIDIA_VERSION}/x86_64/${SDK_BRANCH} ;
    fi

    rm org.freedesktop.Platform.GL.nvidia-$NVIDIA_VERSION.json
done
