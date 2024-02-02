#!/usr/bin/env bash

# shellcheck disable=SC1091
source ./versions.sh

ARCH=$1
REPO=$2
EXPORT_ARGS=$3
FB_ARGS=$4
SUBJECT=$5

set -e
set -x

EXT_PREFIX='org.freedesktop.Platform.GL.nvidia'
SDK_BRANCH=1.4
SDK_RUNTIME_VERSION=23.08

for VER in $DRIVER_VERSIONS; do
    if test "${ARCH}" = 'x86_64'; then
        # If we're building the x86_64 driver, we also build the i386 driver.
        # Note: The i386 driver has to be built first, otherwise the x86_64 repo would get overwritten by it.
        TARGET_ARCHES="i386 ${ARCH}"
    else
        TARGET_ARCHES=${ARCH}
    fi

    for TARGET_ARCH in ${TARGET_ARCHES}; do
        F="data/nvidia-${VER}-${TARGET_ARCH}.data"
        if [ ! -f "${F}" ]; then
            echo "WARNING: No data file for ${VER} ${TARGET_ARCH}"
            continue
        fi

        echo "Packaging ${TARGET_ARCH} NVIDIA driver version ${VER} on ${ARCH} host..."

        NVIDIA_VERSION=$(echo "${VER}" | tr '.' '-')
        NVIDIA_SHA256=$(awk -F ':' '{print $2}' "${F}")
        NVIDIA_URL=$(awk -F '::' '{print $2}' "${F}")

        if test -z "${SUBJECT}"; then
            SUBJECT="${VER}"
            if test -d '.git'; then
                SUBJECT="${SUBJECT} ($(git rev-parse --short HEAD))"
            fi
        fi

        sed -e "s/@@EXT_PREFIX@@/${EXT_PREFIX}/g" \
            -e "s/@@SDK_BRANCH@@/${SDK_BRANCH}/g" \
            -e "s/@@SDK_RUNTIME_VERSION@@/${SDK_RUNTIME_VERSION}/g" \
            -e "s/@@NVIDIA_VERSION@@/${NVIDIA_VERSION}/g" \
            -e "s=@@NVIDIA_URL@@=${NVIDIA_URL}=g" \
            -e "s/@@NVIDIA_ARCH@@/${TARGET_ARCH}/g" \
            -e "s/@@NVIDIA_SHA256@@/${NVIDIA_SHA256}/g" \
            "${EXT_PREFIX}.json.in" > "${EXT_PREFIX}-${NVIDIA_VERSION}.json"

        flatpak-builder -v --force-clean --ccache --sandbox --delete-build-dirs \
                        --arch="${ARCH}" \
                        --repo="${REPO}" \
                        --subject="${SUBJECT}" \
                        ${FB_ARGS} ${EXPORT_ARGS} builddir "${EXT_PREFIX}-${NVIDIA_VERSION}.json"

        if test "${TARGET_ARCH}" = 'i386'; then
            flatpak build-commit-from ${EXPORT_ARGS} \
                    --src-ref="runtime/${EXT_PREFIX}-${NVIDIA_VERSION}/${ARCH}/${SDK_BRANCH}" \
                    "${REPO}" \
                    "runtime/org.freedesktop.Platform.GL32.nvidia-${NVIDIA_VERSION}/${ARCH}/${SDK_BRANCH}"
        fi
        rm "${EXT_PREFIX}-${NVIDIA_VERSION}.json"
    done
done
