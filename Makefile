# Override the arch with `make ARCH=i386`
ARCH    ?= $(shell flatpak --default-arch)
REPO    ?= repo
FB_ARGS ?= --user --install-deps-from=flathub

all: ${REPO}
	./build.sh "${ARCH}" "${REPO}" "${EXPORT_ARGS}" "${FB_ARGS}" "${SUBJECT}"


${REPO}:
	ostree  init --mode=archive-z2 --repo=${REPO}
