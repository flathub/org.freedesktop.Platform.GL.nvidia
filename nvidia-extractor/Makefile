all:
	gcc -o nvidia-extract -Wall -DNVIDIA_VERSION='"'$(subst -,.,${NVIDIA_VERSION})'"' -DARCH='"'${ARCH}'"' nvidia-extract.c ${CFLAGS} ${LDFLAGS} -larchive -lz -llzma -lzstd
