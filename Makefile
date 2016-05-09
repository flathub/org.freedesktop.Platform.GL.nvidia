all: repo org.freedesktop.Sdk.json
	flatpak-builder --force-clean --ccache --require-changes --repo=repo --subject="build of org.freedesktop.Sdk, `date`" ${EXPORT_ARGS} sdk org.freedesktop.Sdk.json
	rm -rf sdk

repo:
	ostree  init --mode=archive-z2 --repo=repo
