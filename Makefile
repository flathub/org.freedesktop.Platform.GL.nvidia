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
SUBST_FILES=org.freedesktop.Sdk.json org.freedesktop.GlxInfo.json os-release org.freedesktop.Sdk.appdata.xml org.freedesktop.Platform.appdata.xml org.freedesktop.Platform.GL.mesa-git.json
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

gl-drivers: gl-drivers-${ARCH}

gl-drivers-${ARCH}:

gl-drivers-i386: gl-drivers-i386-nvidia

gl-drivers-x86_64: gl-drivers-x86_64-nvidia

gl-drivers-i386-nvidia: nvidia-i386-375-26

gl-drivers-x86_64-nvidia: nvidia-x86_64-375-26 nvidia-x86_64-370-28 nvidia-x86_64-340-101 nvidia-x86_64-304-134

nvidia-%:
	sed -e 's/@@SDK_BRANCH@@/${SDK_BRANCH}/g'				\
	    -e 's/@@SDK_RUNTIME_VERSION@@/${SDK_RUNTIME_VERSION}/g'		\
	    -e 's/@@NVIDIA_VERSION@@/${NVIDIA_VERSION}/g'					\
	    -e 's/@@NVIDIA_SHA256@@/${NVIDIA_SHA256}/g'					\
	    -e 's/@@NVIDIA_SIZE@@/${NVIDIA_SIZE}/g'					\
	    -e 's%@@NVIDIA_URL@@%${NVIDIA_URL}%g'					\
	    -e 's%@@NVIDIA_OLD@@%${NVIDIA_OLD}%g'					\
	      org.freedesktop.Platform.GL.nvidia.json.in > org.freedesktop.Platform.GL.nvidia.json.tmp && mv org.freedesktop.Platform.GL.nvidia.json.tmp org.freedesktop.Platform.GL.nvidia.json || exit 1;
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
	    --subject="build of , org.freedesktop.Platform.GL.nvidia `date`" \
	    ${EXPORT_ARGS} nv org.freedesktop.Platform.GL.nvidia.json


nvidia-i386-375-26: NVIDIA_VERSION=375-26
nvidia-i386-375-26: NVIDIA_SHA256=7c79cfaae5512f34ff14cf0fe76632c7c720600d4bbae71d90ff73f1674e617b
nvidia-i386-375-26: NVIDIA_SIZE=44541069
nvidia-i386-375-26: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/375.26/NVIDIA-Linux-x86-375.26.run

nvidia-x86_64-375-26: NVIDIA_VERSION=375-26
nvidia-x86_64-375-26: NVIDIA_SHA256=9cc4abadd47165a17a4f9475e90e91d1b63de63fcc28c4e2e30e10dee845b4b2
nvidia-x86_64-375-26: NVIDIA_SIZE=42693150
nvidia-x86_64-375-26: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/375.26/NVIDIA-Linux-x86_64-375.26-no-compat32.run

nvidia-x86_64-370-28: NVIDIA_VERSION=370-28
nvidia-x86_64-370-28: NVIDIA_SHA256=f498bcf4ddf05725792bd4a1ca9720a88ade81de27bd27f2f3c313723f11444c
nvidia-x86_64-370-28: NVIDIA_SIZE=43511970
nvidia-x86_64-370-28: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/370.28/NVIDIA-Linux-x86_64-370.28-no-compat32.run

nvidia-x86_64-340-101: NVIDIA_VERSION=340-101
nvidia-x86_64-340-101: NVIDIA_SHA256=5ef62e073ba18d4ca745dcaa53c5fbf3d1de4b84cc1739a6cc3f7f746a77c752
nvidia-x86_64-340-101: NVIDIA_SIZE=38664384
nvidia-x86_64-340-101: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/340.101/NVIDIA-Linux-x86_64-340.101-no-compat32.run
nvidia-x86_64-340-101: NVIDIA_OLD=old-

nvidia-x86_64-304-134: NVIDIA_VERSION=304-134
nvidia-x86_64-304-134: NVIDIA_SHA256=42213765cd28078314657d3c1ba382584f09e5e57598240596021f4f76c0c443
nvidia-x86_64-304-134: NVIDIA_SIZE=42217254
nvidia-x86_64-304-134: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/304.134/NVIDIA-Linux-x86_64-304.134-no-compat32.run
nvidia-x86_64-304-134: NVIDIA_OLD=old-

mesa-git:
	$(call subst-metadata)
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
		--subject="build of org.freedesktop.Platform.GL.mesa-git, `date`" \
		${EXPORT_ARGS} mesa org.freedesktop.Platform.GL.mesa-git.json


runtimes: ${REPO} $(patsubst %,%.in,$(SUBST_FILES))
	$(call subst-metadata)
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
		--subject="build of org.freedesktop.Sdk, `date`" \
		${EXPORT_ARGS} sdk org.freedesktop.Sdk.json

${REPO}:
	ostree  init --mode=archive-z2 --repo=${REPO}
