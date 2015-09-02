NULL=

SDK_BASE_IMAGE=$(IMAGEDIR)/freedesktop-contents-sdk-$(ARCH)-$(BASE_HASH).tar.gz
PLATFORM_BASE_IMAGE=$(IMAGEDIR)/freedesktop-contents-platform-$(ARCH)-$(BASE_HASH).tar.gz
NOARCH=packages/RPMS/noarch

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

packages/platform-packages: $(NOARCH)/$(NAME)-platform-$(VERSION)-1.sdk.noarch.rpm $(NOARCH)/freedesktop-platform-base-0.1-1.sdk.noarch.rpm
	bin/setup.sh $(SDK_BASE_IMAGE)
	rm -f packages/platform-packages
	bin/build.sh bin/list_packages.sh $(NAME)-platform > packages/platform-packages
	bin/clear_root.sh

$(NAME)-$(VERSION)-platform.tar.gz $(NAME)-$(VERSION)-platform-rpmdb.tar.gz: packages/platform-packages $(NOARCH)/$(NAME)-platform-$(VERSION)-1.sdk.noarch.rpm $(PLATFORM_BASE_IMAGE)
	-echo building $(NAME)-platform
	bin/setup_root.sh $(PLATFORM_BASE_IMAGE)
	bin/build.sh rpm -Uvh `cat packages/platform-packages`
	bin/build.sh bin/post.sh
	rm -rf $(NAME)-$(VERSION)-platform.tar.gz $(NAME)-$(VERSION)-platform-rpmdb.tar.gz
	tar --transform 's,^build/root/usr,files,S' -czf $(NAME)-$(VERSION)-platform.tar.gz build/root/usr --owner=root
	tar --transform 's,^build/var,files,S' -czf $(NAME)-$(VERSION)-platform-rpmdb.tar.gz build/var/lib/rpm --owner=root
	bin/clear_root.sh

$(NAME)-$(VERSION)-sdk.tar.gz $(NAME)-$(VERSION)-sdk-rpmdb.tar.gz: $(NOARCH)/$(NAME)-sdk-$(VERSION)-1.sdk.noarch.rpm
	bin/setup.sh $(SDK_BASE_IMAGE)
	bin/build.sh smart install -y  $(NOARCH)/$(NAME)-sdk-$(VERSION)-1.sdk.noarch.rpm
	bin/build.sh bin/post.sh
	rm -rf $(NAME)-$(VERSION)-sdk.tar.gz $(NAME)-$(VERSION)-sdk-rpmdb.tar.gz
	tar --transform 's,^build/root/usr,files,S' -czf $(NAME)-$(VERSION)-sdk.tar.gz build/root/usr --owner=root
	tar --transform 's,^build/var,files,S' -czf $(NAME)-$(VERSION)-sdk-rpmdb.tar.gz build/var/lib/rpm --owner=root
	bin/clear_root.sh

$(NAME)-$(VERSION)-debug.tar.gz $(NAME)-$(VERSION)-debug-src.tar.gz: $(NOARCH)/$(NAME)-debug-$(VERSION)-1.sdk.noarch.rpm
	bin/setup.sh $(SDK_BASE_IMAGE)
	bin/build.sh smart install -y  $(NOARCH)/$(NAME)-debug-$(VERSION)-1.sdk.noarch.rpm
	rm -rf $(NAME)-$(VERSION)-debug.tar.gz $(NAME)-$(VERSION)-debug-src.tar.gz
	tar --transform 's,^build/root/usr/lib/debug,files,S' -czf $(NAME)-$(VERSION)-debug.tar.gz build/root/usr/lib/debug --owner=root
	tar --transform 's,^build/root/usr/src/debug,files,S' -czf $(NAME)-$(VERSION)-debug-src.tar.gz build/root/usr/src/debug --owner=root
	bin/clear_root.sh

repo:
	ostree  init --mode=archive-z2 --repo=repo

commit-platform: repo $(NAME)-$(VERSION)-platform.tar.gz  $(NAME)-$(VERSION)-platform-rpmdb.tar.gz
	bin/commit.sh repo $(NAME)-$(VERSION)-platform.tar.gz $(NAME)-$(VERSION)-platform-rpmdb.tar.gz metadata.platform $(ID).Platform$(EXTRA_NAME) $(ARCH) $(VERSION)

commit-sdk: repo $(NAME)-$(VERSION)-sdk.tar.gz $(NAME)-$(VERSION)-sdk-rpmdb.tar.gz
	bin/commit.sh repo $(NAME)-$(VERSION)-sdk.tar.gz $(NAME)-$(VERSION)-sdk-rpmdb.tar.gz metadata.sdk $(ID).Sdk$(EXTRA_NAME) $(ARCH) $(VERSION)

commit-debug: repo $(NAME)-$(VERSION)-debug.tar.gz $(NAME)-$(VERSION)-debug-src.tar.gz
	bin/simple-commit.sh repo $(NAME)-$(VERSION)-debug.tar.gz $(ID).Debug$(EXTRA_NAME) $(ARCH) $(VERSION)
	bin/simple-commit.sh repo $(NAME)-$(VERSION)-debug-src.tar.gz $(ID).DebugSrc$(EXTRA_NAME) $(ARCH) $(VERSION)

commit: commit-sdk commit-platform commit-debug
	echo done

untag:
	./untag.sh repo $(ID).Platform $(ARCH) $(VERSION) $(EXTRA_NAME)
	./untag.sh repo $(ID).Sdk $(ARCH) $(VERSION) $(EXTRA_NAME)
	./untag.sh repo $(ID).Debug $(ARCH) $(VERSION) $(EXTRA_NAME)
	./untag.sh repo $(ID).DebugSrc $(ARCH) $(VERSION) $(EXTRA_NAME)
