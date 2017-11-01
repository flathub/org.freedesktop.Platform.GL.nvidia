# Override the arch with `make ARCH=i386`
ARCH   ?= $(shell flatpak --default-arch)
REPO   ?= repo

all: ${REPO}
	./build.sh "${ARCH}" "${REPO}" "${EXPORT_ARGS}"


${REPO}:
	ostree  init --mode=archive-z2 --repo=${REPO}
