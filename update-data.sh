#!/bin/bash

source ./versions.sh

set -e

for VER in $DRIVER_VERSIONS; do
    for ARCH in x86_64 i386; do
        F="data/nvidia-$VER-$ARCH.data"
        if [ -f $F ]; then continue; fi

        if [ $ARCH == x86_64 ]; then
            NVIDIA_ARCH=x86_64
            SUFFIX=-no-compat32
        else
            NVIDIA_ARCH=x86
            SUFFIX=
        fi

        MAJOR_VER=(${VER//./ }[0])

        # Nvidia dropped 32bit support after 390 series but 64bit contains
        # 32bit compat libs
        if [ $ARCH == i386 ] && [ $MAJOR_VER -gt 390 ]; then
            NVIDIA_ARCH=x86_64
        fi

        echo Generating $F

        rm -f dl
        if [[ $TESLA_VERSIONS == *$VER* ]]; then
            URL=http://us.download.nvidia.com/tesla/${VER}/NVIDIA-Linux-${NVIDIA_ARCH}-${VER}.run
            if ! curl -f -o dl $URL; then
                echo "Unable to find URL for version $VER, arch $ARCH"
                echo $URL
                exit 1
            fi
        elif [[ $VULKAN_VERSIONS == *$VER* ]]; then
            VULKAN_VER=${VER//./}
            URL=https://developer.nvidia.com/vulkan-beta-${VULKAN_VER}-linux
            if ! curl -f -L -o dl $URL; then
                echo "Unable to find URL for version $VER, arch $ARCH"
                exit 1
            fi
        else
            URL=https://us.download.nvidia.com/XFree86/Linux-${NVIDIA_ARCH}/${VER}/NVIDIA-Linux-${NVIDIA_ARCH}-${VER}${SUFFIX}.run
            if ! curl -f -o dl $URL; then
                URL=https://download.nvidia.com/XFree86/Linux-${NVIDIA_ARCH}/${VER}/NVIDIA-Linux-${NVIDIA_ARCH}-${VER}${SUFFIX}.run
                if ! curl -f -o dl $URL; then
                    echo "Unable to find URL for version $VER, arch $ARCH"
                    exit 1
                fi
            fi
        fi
        SHA256=$(sha256sum dl | awk "{print \$1}")
        SIZE=$(stat -c%s dl)
        rm -f dl

        echo :$SHA256:$SIZE::$URL > $F
        git add $F
    done
done
