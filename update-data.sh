#!/usr/bin/env bash

source ./versions.sh

set -e

for VER in ${DRIVER_VERSIONS}; do
    for ARCH in x86_64 i386 aarch64; do
        F="data/nvidia-${VER}-${ARCH}.data"
        if [ -f ${F} ]; then continue; fi

        # Parse version string
        MAJOR_VER=${VER%%.*}
        ### Check for build as part of VER
        if [ ${VER#*.} == ${VER##*.} ]; then
            MINOR_VER=${VER##*.}
        else
            partial=${VER#*.}
            MINOR_VER=${partial%%.*}
            BUILD=${VER##*.}
        fi

        # Additional URL parameters
        if [ ${ARCH} == x86_64 ]; then
            NVIDIA_ARCH=x86_64
            if [ ${MAJOR_VER} -lt 470 ]; then
                SUFFIX=-no-compat32
            else
                SUFFIX=
            fi
        elif [ ${ARCH} == aarch64 ]; then
            NVIDIA_ARCH=aarch64
            SUFFIX=
        else
            NVIDIA_ARCH=x86
            SUFFIX=
        fi

        # Nvidia dropped 32bit support after 390 series but 64bit contains
        # 32bit compat libs
        if [ ${ARCH} == i386 ] && [ ${MAJOR_VER} -gt 390 ]; then
            NVIDIA_ARCH=x86_64
        fi

        if [ ${ARCH} == aarch64 ]; then
            if [ ${MAJOR_VER} -lt 470 ]; then
                continue
            elif [[ ${TESLA_VERSIONS} == *${VER}* ]]; then
                continue
            elif [[ ${VULKAN_VERSIONS} == *${VER}* ]]; then
                continue
            else
                if [ ${VER} == 510.39.01 ]; then
                    continue
                elif [ ${VER} == 495.46 ]; then
                    continue
                elif [ ${VER} == 470.94 ]; then
                    continue
                fi
            fi
        fi

        echo "Generating ${F}"

        # Setup URL string and download driver
        rm -f dl
        if [[ ${TESLA_VERSIONS} == *${VER}* ]]; then
            if [ ${MAJOR_VER} -eq 410 ] && [ ${MINOR_VER} -eq 129 ]; then
                URL=https://us.download.nvidia.com/tesla/${VER}/NVIDIA-Linux-${NVIDIA_ARCH}-${VER}-diagnostic.run
            elif [ ${MAJOR_VER} -eq 418 ] && [ ${MINOR_VER} -ge 87 ] && [ ${MINOR_VER} -lt 116 ]; then
                URL=https://us.download.nvidia.com/tesla/${MAJOR_VER}.${MINOR_VER}/NVIDIA-Linux-${NVIDIA_ARCH}-${VER}.run
            else
                URL=https://us.download.nvidia.com/tesla/${VER}/NVIDIA-Linux-${NVIDIA_ARCH}-${VER}.run
            fi
            if ! curl -f -o dl ${URL}; then
                echo "Unable to find URL for version ${VER}, arch ${ARCH}"
                echo ${URL}
                exit 1
            fi
        elif [[ ${VULKAN_VERSIONS} == *${VER}* ]]; then
            VULKAN_VER=${VER//./}
            URL=https://developer.nvidia.com/downloads/vulkan-beta-${VULKAN_VER}-linux
            if ! curl -f -L -o dl ${URL}; then
                echo "Unable to find URL for version ${VER}, arch ${ARCH}"
                exit 1
            fi
        else
            URL=https://us.download.nvidia.com/XFree86/Linux-${NVIDIA_ARCH}/${VER}/NVIDIA-Linux-${NVIDIA_ARCH}-${VER}${SUFFIX}.run
            if ! curl -f -o dl ${URL}; then
                URL=https://download.nvidia.com/XFree86/Linux-${NVIDIA_ARCH}/${VER}/NVIDIA-Linux-${NVIDIA_ARCH}-${VER}${SUFFIX}.run
                if ! curl -f -o dl ${URL}; then
                    echo "Unable to find URL for version ${VER}, arch ${ARCH}"
                    exit 1
                fi
            fi
        fi

        # Create output `.data` file and add it to git
        SHA256=$(sha256sum dl | awk "{print \$1}")
        SIZE=$(stat -c%s dl)
        rm -f dl

        echo :${SHA256}:${SIZE}::${URL} > ${F}

        git add ${F}
    done
done
