#!/bin/sh

set -e

rm -rf sdk
xdg-app-builder --ccache --require-changes --repo=repo --subject="Nightly build of org.freedesktop.Sdk, `date`" ${EXPORT_ARGS-} sdk org.freedesktop.Sdk.json
