all: repo org.freedesktop.Sdk.json
	rm -rf sdk
	xdg-app-builder --ccache --require-changes --repo=repo --subject="build of org.freedesktop.Sdk, `date`" ${EXPORT_ARGS} sdk org.freedesktop.Sdk.json
	rm -rf sdk

repo:
	ostree  init --mode=archive-z2 --repo=repo
