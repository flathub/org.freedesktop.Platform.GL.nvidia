all:
	gcc -o nvidia-extract -Wall -DNVIDIA_VERSION='"'$(subst -,.,${NVIDIA_VERSION})'"' nvidia-extract.c $(CFLAGS) ${LDFLAGS} -larchive -lz -llzma -lzstd
