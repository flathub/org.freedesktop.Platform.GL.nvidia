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
SUBST_FILES=org.freedesktop.Sdk.json org.freedesktop.GlxInfo.json os-release issue issue.net org.freedesktop.Sdk.appdata.xml org.freedesktop.Platform.appdata.xml org.freedesktop.Platform.GL.mesa-git.json org.freedesktop.Platform.GL.mesa-17.json
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

gl-drivers-i386-nvidia: \
	nvidia-i386-375-39 nvidia-i386-375-26 nvidia-i386-370-28 \
	nvidia-i386-367-57 nvidia-i386-340-102 nvidia-i386-340-101 \
	nvidia-i386-304-135 nvidia-i386-304-134

gl-drivers-x86_64-nvidia: \
	nvidia-x86_64-375-39 nvidia-x86_64-375-26 nvidia-x86_64-370-28 \
	nvidia-x86_64-367-57 nvidia-x86_64-340-102 nvidia-x86_64-340-101 \
	nvidia-x86_64-304-135 nvidia-x86_64-304-134

# Ensure the NVidia builds don't run in parallel
.NOTPARALLEL:

nvidia-%:
	sed -e 's/@@SDK_BRANCH@@/${SDK_BRANCH}/g'				\
	    -e 's/@@SDK_RUNTIME_VERSION@@/${SDK_RUNTIME_VERSION}/g'		\
	    -e 's/@@NVIDIA_VERSION@@/${NVIDIA_VERSION}/g'					\
	    -e 's/@@NVIDIA_SHA256@@/${NVIDIA_SHA256}/g'					\
	    -e 's/@@NVIDIA_SIZE@@/${NVIDIA_SIZE}/g'					\
	    -e 's%@@NVIDIA_URL@@%${NVIDIA_URL}%g'					\
	      org.freedesktop.Platform.GL.nvidia.json.in > org.freedesktop.Platform.GL.nvidia.json.tmp && mv org.freedesktop.Platform.GL.nvidia.json.tmp org.freedesktop.Platform.GL.nvidia-${NVIDIA_VERSION}.json || exit 1;
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
	    --subject="build of , org.freedesktop.Platform.GL.nvidia `date`" \
	    ${EXPORT_ARGS} nv org.freedesktop.Platform.GL.nvidia-${NVIDIA_VERSION}.json

nvidia-i386-375-39: NVIDIA_VERSION=378-13
nvidia-i386-375-39: NVIDIA_SHA256=05e62a6098aac7373438ee381072253a861d56522f74948c2b714e20e69a46b1
nvidia-i386-375-39: NVIDIA_SIZE=44397547
nvidia-i386-375-39: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/378.13/NVIDIA-Linux-x86-378.13.run

nvidia-i386-375-39: NVIDIA_VERSION=375-39
nvidia-i386-375-39: NVIDIA_SHA256=7f33f6572c5c5c57df71531749c7339309a2097918375685ea8018826cf19456
nvidia-i386-375-39: NVIDIA_SIZE=44434734
nvidia-i386-375-39: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/375.39/NVIDIA-Linux-x86-375.39.run

nvidia-i386-375-26: NVIDIA_VERSION=375-26
nvidia-i386-375-26: NVIDIA_SHA256=7c79cfaae5512f34ff14cf0fe76632c7c720600d4bbae71d90ff73f1674e617b
nvidia-i386-375-26: NVIDIA_SIZE=44541069
nvidia-i386-375-26: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/375.26/NVIDIA-Linux-x86-375.26.run

nvidia-i386-370-28: NVIDIA_VERSION=370-28
nvidia-i386-370-28: NVIDIA_SHA256=6323254ccf2a75d7ced1374a76ca56778689d0d8a9819e4ee5378ea3347b9835
nvidia-i386-370-28: NVIDIA_SIZE=44189522
nvidia-i386-370-28: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/370.28/NVIDIA-Linux-x86-370.28.run

nvidia-i386-367-57: NVIDIA_VERSION=367-57
nvidia-i386-367-57: NVIDIA_SHA256=43d4e926f71ac6c581018badf467458709822e97a7564ed9f1b521b7b63d88bb
nvidia-i386-367-57: NVIDIA_SIZE=44731570
nvidia-i386-367-57: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/367.57/NVIDIA-Linux-x86-367.57.run

nvidia-i386-340-102: NVIDIA_VERSION=340-102
nvidia-i386-340-102: NVIDIA_SHA256=61b13d5dae0f6f5d788a4d8c4c98e8d971d19cb90b606058060d007946248828
nvidia-i386-340-102: NVIDIA_SIZE=38779756
nvidia-i386-340-102: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/340.102/NVIDIA-Linux-x86-340.102.run

nvidia-i386-340-101: NVIDIA_VERSION=340-101
nvidia-i386-340-101: NVIDIA_SHA256=5f5eda9c3d9bf53b56ef4f546dd1be5317eed46df425edbdd2c34023fb9eb062
nvidia-i386-340-101: NVIDIA_SIZE=38932143
nvidia-i386-340-101: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/340.101/NVIDIA-Linux-x86-340.101.run

nvidia-i386-304-135: NVIDIA_VERSION=304-135
nvidia-i386-304-135: NVIDIA_SHA256=5cb0a191ddca7b4c72b3c26cd57b7d719878ce628d24b5b026a0e5c8d3a00d93
nvidia-i386-304-135: NVIDIA_SIZE=41202842
nvidia-i386-304-135: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/304.135/NVIDIA-Linux-x86-304.135.run

nvidia-i386-304-134: NVIDIA_VERSION=304-134
nvidia-i386-304-134: NVIDIA_SHA256=84f7891af131bb9f9a8a34401dfef4288218019406dfa4ae57b6d52b14e81c9d
nvidia-i386-304-134: NVIDIA_SIZE=41201159
nvidia-i386-304-134: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86/304.134/NVIDIA-Linux-x86-304.134.run

nvidia-x86_64-375-39: NVIDIA_VERSION=378-13
nvidia-x86_64-375-39: NVIDIA_SHA256=a97a2ab047759a0b2c4abab5601e6f027230d355615ee745e24e738ee21cf5da
nvidia-x86_64-375-39: NVIDIA_SIZE=42773114
nvidia-x86_64-375-39: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/378.13/NVIDIA-Linux-x86_64-378.13-no-compat32.run

nvidia-x86_64-375-39: NVIDIA_VERSION=375-39
nvidia-x86_64-375-39: NVIDIA_SHA256=95a3221292f357fbd77697b9bb78d1694def5761202f695ef2065c61efb2ddd8
nvidia-x86_64-375-39: NVIDIA_SIZE=43736902
nvidia-x86_64-375-39: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/375.39/NVIDIA-Linux-x86_64-375.39-no-compat32.run

nvidia-x86_64-375-26: NVIDIA_VERSION=375-26
nvidia-x86_64-375-26: NVIDIA_SHA256=9cc4abadd47165a17a4f9475e90e91d1b63de63fcc28c4e2e30e10dee845b4b2
nvidia-x86_64-375-26: NVIDIA_SIZE=42693150
nvidia-x86_64-375-26: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/375.26/NVIDIA-Linux-x86_64-375.26-no-compat32.run

nvidia-x86_64-370-28: NVIDIA_VERSION=370-28
nvidia-x86_64-370-28: NVIDIA_SHA256=f498bcf4ddf05725792bd4a1ca9720a88ade81de27bd27f2f3c313723f11444c
nvidia-x86_64-370-28: NVIDIA_SIZE=43511970
nvidia-x86_64-370-28: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/370.28/NVIDIA-Linux-x86_64-370.28-no-compat32.run

nvidia-x86_64-367-57: NVIDIA_VERSION=367-57
nvidia-x86_64-367-57: NVIDIA_SHA256=b94a8ab6a1da464b44ba9bbb25e1e220441ae8340221de3bd159df00445dd6e4
nvidia-x86_64-367-57: NVIDIA_SIZE=42984178
nvidia-x86_64-367-57: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/367.57/NVIDIA-Linux-x86_64-367.57-no-compat32.run

nvidia-x86_64-340-102: NVIDIA_VERSION=340-102
nvidia-x86_64-340-102: NVIDIA_SHA256=6a36bd9a0033769ecd11ce2aa60aeb41b50b20616c43fd19c55e027c451f585e
nvidia-x86_64-340-102: NVIDIA_SIZE=38598444
nvidia-x86_64-340-102: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/340.102/NVIDIA-Linux-x86_64-340.102-no-compat32.run

nvidia-x86_64-340-101: NVIDIA_VERSION=340-101
nvidia-x86_64-340-101: NVIDIA_SHA256=5ef62e073ba18d4ca745dcaa53c5fbf3d1de4b84cc1739a6cc3f7f746a77c752
nvidia-x86_64-340-101: NVIDIA_SIZE=38664384
nvidia-x86_64-340-101: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/340.101/NVIDIA-Linux-x86_64-340.101-no-compat32.run

nvidia-x86_64-304-135: NVIDIA_VERSION=304-135
nvidia-x86_64-304-135: NVIDIA_SHA256=352f4a4d5ef692b26383e2cf9ec866f6973f905d53eb6bc9f2161b6ba2afae5a
nvidia-x86_64-304-135: NVIDIA_SIZE=42205949
nvidia-x86_64-304-135: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/304.135/NVIDIA-Linux-x86_64-304.135-no-compat32.run

nvidia-x86_64-304-134: NVIDIA_VERSION=304-134
nvidia-x86_64-304-134: NVIDIA_SHA256=42213765cd28078314657d3c1ba382584f09e5e57598240596021f4f76c0c443
nvidia-x86_64-304-134: NVIDIA_SIZE=42217254
nvidia-x86_64-304-134: NVIDIA_URL=http://http.download.nvidia.com/XFree86/Linux-x86_64/304.134/NVIDIA-Linux-x86_64-304.134-no-compat32.run

mesa-git:
	$(call subst-metadata)
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
		--subject="build of org.freedesktop.Platform.GL.mesa-git, `date`" \
		${EXPORT_ARGS} mesa org.freedesktop.Platform.GL.mesa-git.json

mesa-17:
	$(call subst-metadata)
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
		--subject="build of org.freedesktop.Platform.GL.mesa-17, `date`" \
		${EXPORT_ARGS} mesa org.freedesktop.Platform.GL.mesa-17.json


runtimes: ${REPO} $(patsubst %,%.in,$(SUBST_FILES))
	$(call subst-metadata)
	flatpak-builder --force-clean --ccache --require-changes --repo=${REPO} --arch=${ARCH} \
		--subject="build of org.freedesktop.Sdk, `date`" \
		${EXPORT_ARGS} sdk org.freedesktop.Sdk.json

${REPO}:
	ostree  init --mode=archive-z2 --repo=${REPO}
