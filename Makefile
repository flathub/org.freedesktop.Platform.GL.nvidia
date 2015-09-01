srcdir = $(CURDIR)
builddir = $(CURDIR)

FREEDESKTOP_VERSION=1.0
ARCH=x86_64
IMAGEDIR=freedesktop-sdk-base/images/$(ARCH)
NOARCH=packages/RPMS/noarch
BASE_HASH=cda42b256f1691e750bce3a421a4fe6536115ac3

EXTRA_NAME=
DELTAS=
GPG_KEY=
GPG_HOME=

SDK_BASE_IMAGE=$(IMAGEDIR)/freedesktop-contents-sdk-$(ARCH)-$(BASE_HASH).tar.gz
PLATFORM_BASE_IMAGE=$(IMAGEDIR)/freedesktop-contents-platform-$(ARCH)-$(BASE_HASH).tar.gz

$(SDK_BASE_IMAGE) $(PLATFORM_BASE_IMAGE) images:
	if test ! -d freedesktop-sdk-base; then \
		git clone git://anongit.freedesktop.org/xdg-app/freedesktop-sdk-base;\
	fi
	(cd  freedesktop-sdk-base && \
	 git fetch origin && \
	 git checkout $(BASE_HASH) && \
	 make)

NULL=

ALL_SPECS = $(wildcard specs/*.spec)

deps: rpm-dependencies.P

rpm-dependencies.P: $(ALL_SPECS) bin/makedeps.sh $(SDK_BASE_IMAGE)
	bin/setup.sh $(SDK_BASE_IMAGE)
	bin/build.sh bin/makedeps.sh $(ALL_SPECS) > rpm-dependencies.P
	bin/clear_root.sh

packages/base_provides: $(PLATFORM_BASE_IMAGE)
	bin/find_prov_tar.sh $(PLATFORM_BASE_IMAGE) > packages/base_provides

packages/base_sdk_provides: $(SDK_BASE_IMAGE)
	bin/find_prov_tar.sh $(SDK_BASE_IMAGE) > packages/base_sdk_provides

$(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm:	packages/base_provides

$(NOARCH)/freedesktop-sdk-base-0.1-1.sdk.noarch.rpm:	packages/base_sdk_provides


-include rpm-dependencies.P
