all:
	gcc -o nvidia-extract -Wall -DNVIDIA_VERSION='"'$(subst -,.,${NVIDIA_VERSION})'"' -DNVIDIA_ARCH='"'${NVIDIA_ARCH}'"' nvidia-extract.c $(CFLAGS) ${LDFLAGS} -larchive -lz -llzma -lzstd
