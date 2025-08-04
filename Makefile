# Override the arch with `make ARCH=i386`
ARCH            ?= $(shell flatpak --default-arch)
REPO            ?= repo
FB_ARGS         ?= --user --install-deps-from=flathub --disable-rofiles-fuse
DRIVER_VERSIONS ?= $(shell . ./versions.sh && printf -- '%s' "$${DRIVER_VERSIONS}")

all:
	env DRIVER_VERSIONS="${DRIVER_VERSIONS}" ./build.sh "${ARCH}" "${REPO}" "${EXPORT_ARGS}" "${FB_ARGS}" "${SUBJECT}"
