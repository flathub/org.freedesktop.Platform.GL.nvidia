# Override the arch with `make ARCH=i386`
ARCH   ?= $(shell flatpak --default-arch)
REPO   ?= repo

# SDK Versions setup here
#
# SDK_BRANCH:          The version (branch) of runtime and sdk to produce
# SDK_RUNTIME_VERSION: The org.freedesktop.BaseSdk and platform version to build against
#
SDK_BRANCH=1.4
SDK_RUNTIME_VERSION=1.4

# Canned recipe for generating metadata
SUBST_FILES=org.freedesktop.Sdk.json org.freedesktop.GlxInfo.json os-release org.freedesktop.Sdk.appdata.xml org.freedesktop.Platform.appdata.xml
define subst-metadata
	@echo -n "Generating files: ${SUBST_FILES}... ";
	@for file in ${SUBST_FILES}; do 					\
	  file_source=$${file}.in; 						\
	  sed -e 's/@@SDK_ARCH@@/${ARCH}/g' 					\
	      -e 's/@@SDK_BRANCH@@/${SDK_BRANCH}/g' 				\
	      -e 's/@@SDK_RUNTIME_VERSION@@/${SDK_RUNTIME_VERSION}/g' 		\
	      $$file_source > $$file.tmp && mv $$file.tmp $$file || exit 1;	\
	done
	@echo "Done.";
endef

all: runtimes

extra: glxinfo gl-drivers-${ARCH}

glxinfo: ${REPO} $(patsubst %,%.in,$(SUBST_FILES))
	$(call subst-metadata)
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
	    --subject="build of org.freedesktop.GlxInfo, `date`" \
	    ${EXPORT_ARGS} glxinfo org.freedesktop.GlxInfo.json

gl-drivers-${ARCH}:

gl-drivers-x86_64: org.freedesktop.Platform.GL.nvidia.json.in
	sed -e 's/@@SDK_BRANCH@@/${SDK_BRANCH}/g'				\
	    -e 's/@@SDK_RUNTIME_VERSION@@/${SDK_RUNTIME_VERSION}/g'		\
	    -e 's/@@NVIDIA_VERSION@@/375-26/g'					\
	    -e 's/@@NVIDIA_SHA256@@/9cc4abadd47165a17a4f9475e90e91d1b63de63fcc28c4e2e30e10dee845b4b2/g'					\
	    -e 's/@@NVIDIA_SIZE@@/42693150/g'					\
	    -e 's%@@NVIDIA_URL@@%http://http.download.nvidia.com/XFree86/Linux-x86_64/375.26/NVIDIA-Linux-x86_64-375.26-no-compat32.run%g'					\
	      org.freedesktop.Platform.GL.nvidia.json.in > org.freedesktop.Platform.GL.nvidia.json.tmp && mv org.freedesktop.Platform.GL.nvidia.json.tmp org.freedesktop.Platform.GL.nvidia.json || exit 1;
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
	    --subject="build of , org.freedesktop.Platform.GL.nvidia `date`" \
	    ${EXPORT_ARGS} nv org.freedesktop.Platform.GL.nvidia.json

runtimes: ${REPO} $(patsubst %,%.in,$(SUBST_FILES))
	$(call subst-metadata)
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
		--subject="build of org.freedesktop.Sdk, `date`" \
		${EXPORT_ARGS} sdk org.freedesktop.Sdk.json

${REPO}:
	ostree  init --mode=archive-z2 --repo=${REPO}
