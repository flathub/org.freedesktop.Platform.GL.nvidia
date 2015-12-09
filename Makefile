NAME=freedesktop
ID=org.freedesktop
VERSION=1.2
ARCH=x86_64
IMAGEDIR=freedesktop-sdk-base/images/$(ARCH)
BASE_HASH=52853d3961aeba5e24cfb251422c2d0842340039

EXTRA_NAME=
DELTAS=
GPG_KEY=
GPG_HOME=

all: $(NAME)-$(VERSION)-platform.tar.gz $(NAME)-$(VERSION)-sdk.tar.gz

debug: $(NAME)-$(VERSION)-debug.tar.gz

ALL_SPECS = $(wildcard specs/*.spec)

include Makefile.inc
-include rpm-dependencies.P

$(SDK_BASE_IMAGE) $(PLATFORM_BASE_IMAGE) images:
	if test ! -d freedesktop-sdk-base; then \
		git clone git://anongit.freedesktop.org/xdg-app/freedesktop-sdk-base;\
	fi
	(cd  freedesktop-sdk-base && \
	 git fetch origin && \
	 git checkout $(BASE_HASH) && \
	 make)
