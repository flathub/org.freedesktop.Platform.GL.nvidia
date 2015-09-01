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

all: freedesktop-platform.tar.gz

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

packages/freedesktop-platform-packages: $(NOARCH)/freedesktop-platform-0.1-1.sdk.noarch.rpm $(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm
	bin/setup.sh $(SDK_BASE_IMAGE)
	rm -f packages/freedesktop-platform-packages
	bin/build.sh bin/list_packages.sh freedesktop-platform > packages/freedesktop-platform-packages
	bin/clear_root.sh

freedesktop-platform.tar.gz freedesktop-platform-rpmdb.tar.gz: packages/freedesktop-platform-packages $(NOARCH)/freedesktop-platform-0.1-1.sdk.noarch.rpm $(PLATFORM_BASE_IMAGE)
	-echo building freedesktop-platform
	bin/setup_root.sh $(PLATFORM_BASE_IMAGE)
	bin/build.sh rpm -Uvh `cat packages/freedesktop-platform-packages`
	bin/build.sh bin/post.sh
	tar --transform 's,^build/root/usr,files,S' -czf freedesktop-platform.tar.gz build/root/usr --owner=root
	tar --transform 's,^build/var,files,S' -czf freedesktop-platform-rpmdb.tar.gz build/var/lib/rpm --owner=root
	bin/clear_root.sh

freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz: $(NOARCH)/freedesktop-sdk-0.1-1.sdk.noarch.rpm
	bin/setup.sh $(SDK_BASE_IMAGE)
	bin/build.sh smart install -y  $(NOARCH)/freedesktop-sdk-0.1-1.sdk.noarch.rpm
	bin/build.sh bin/post.sh
	rm -rf freedesktop-sdk.tar.gz freedesktop-sdk-rpmdb.tar.gz
	tar --transform 's,^build/root/usr,files,S' -czf freedesktop-sdk.tar.gz build/root/usr --owner=root
	tar --transform 's,^build/var,files,S' -czf freedesktop-sdk-rpmdb.tar.gz build/var/lib/rpm --owner=root
	bin/clear_root.sh

freedesktop-debug.tar.gz freedesktop-debug-src.tar.gz: $(NOARCH)/freedesktop-debug-0.1-1.sdk.noarch.rpm
	bin/setup.sh $(SDK_BASE_IMAGE)
	bin/build.sh smart install -y  $(NOARCH)/freedesktop-debug-0.1-1.sdk.noarch.rpm
	rm -rf freedesktop-debug.tar.gz freedesktop-debug-src.tar.gz
	tar --transform 's,^build/root/usr/lib/debug,files,S' -czf freedesktop-debug.tar.gz build/root/usr/lib/debug --owner=root
	tar --transform 's,^build/root/usr/src/debug,files,S' -czf freedesktop-debug-src.tar.gz build/root/usr/src/debug --owner=root
	bin/clear_root.sh

repo:
	ostree  init --mode=archive-z2 --repo=repo

-include rpm-dependencies.P
