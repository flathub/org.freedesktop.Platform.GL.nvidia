#!/bin/sh

REPO=$1
TAR=$2
NAME=$3
ARCH=$4
VERSION=$5

REV=`git rev-parse HEAD`

rm -rf build/commit
mkdir -p build/commit
echo "extracting ${TAR}"
tar xf ${TAR} -C build/commit

COMMIT_ARGS="--repo=${REPO} --owner-uid=0 --owner-gid=0 --no-xattrs"
if [ "x${GPG_KEY}" != "x" ]; then
    COMMIT_ARGS="${COMMIT_ARGS} --gpg-sign=${GPG_KEY}"
fi
if [ "x${GPG_HOME}" != "x" ]; then
    COMMIT_ARGS="${COMMIT_ARGS} --gpg-homedir=${GPG_HOME}"
fi

echo "commiting runtime/${NAME}/${ARCH}/${VERSION}"
ostree commit ${COMMIT_ARGS} --branch=runtime/${NAME}/${ARCH}/${VERSION}  -s "build of ${REV}" build/commit

echo "commiting summary"
ostree summary -u --repo=${REPO}

rm -rf build/commit
