#!/bin/sh

REPO=$1
TAR=$2
TAR_VAR=$3
METADATA=$4
NAME=$5
ARCH=$6
VERSION=$7

REV=`git rev-parse HEAD`

rm -rf build/commit
mkdir -p build/commit
rm -rf build/commit-locales
mkdir -p build/commit-locales
echo "extracting ${TAR}"
tar xf ${TAR} -C build/commit
cp ${METADATA} build/commit/metadata

COMMIT_ARGS="--repo=${REPO} --owner-uid=0 --owner-gid=0 --no-xattrs"
if [ "x${GPG_KEY}" != "x" ]; then
    COMMIT_ARGS="${COMMIT_ARGS} --gpg-sign=${GPG_KEY}"
fi
if [ "x${GPG_HOME}" != "x" ]; then
    COMMIT_ARGS="${COMMIT_ARGS} --gpg-homedir=${GPG_HOME}"
fi

echo "extracting locales"
for F in build/commit/files/share/locale/*; do
    BASENAME=`basename $F`
    LOCALE=`basename $F | sed s/[@_].*//`
    if [ ${BASENAME} != "en_US" ]; then
        mkdir -p build/commit-locales/$LOCALE/files/share
        mkdir -p build/commit/files/share/runtime/locale/$LOCALE/share/$BASENAME
        mv $F build/commit-locales/$LOCALE/files/share
        ln -s ../runtime/locale/$LOCALE/share/$BASENAME $F
    fi
done
for F in build/commit/files/lib/locale/*; do
    BASENAME=`basename $F`
    LOCALE=`basename $F | sed s/[@_].*//`
    if [ ${BASENAME} != "en_US" ]; then
        mkdir -p build/commit-locales/$LOCALE/files/lib
        mkdir -p build/commit/files/share/runtime/locale/$LOCALE/lib/$BASENAME
        mv $F build/commit-locales/$LOCALE/files/lib
        ln -s ../../share/runtime/locale/$LOCALE/lib/$BASENAME $F
    fi
done

echo "commiting runtime/${NAME}/${ARCH}/${VERSION}"
ostree commit ${COMMIT_ARGS} --branch=runtime/${NAME}/${ARCH}/${VERSION}  -s "build of ${REV}" build/commit

for F in build/commit-locales/*; do
    LOCALE=`basename $F`
    echo "commiting runtime/${NAME}.Locale.$LOCALE/${ARCH}/${VERSION}"
    ostree commit ${COMMIT_ARGS} --branch=runtime/${NAME}.Locale.$LOCALE/${ARCH}/${VERSION} -s "build of ${REV}" $F
done

rm -rf build/commit
mkdir -p build/commit
echo "extracting ${TAR_VAR}"
tar xf ${TAR_VAR} -C build/commit
echo "commiting runtime/${NAME}.Var/${ARCH}/${VERSION}"
ostree commit ${COMMIT_ARGS} --branch=runtime/${NAME}.Var/${ARCH}/${VERSION}  -s "build of ${REV}" build/commit

if [ "x${DELTAS}" != "x" ]; then
    echo "commiting generating deltas"
    ostree static-delta generate --repo=${REPO} --min-fallback-size 1 --empty runtime/${NAME}/x86_64/$VERSION
    ostree static-delta generate --repo=${REPO} --min-fallback-size 1 --empty runtime/${NAME}.Var/x86_64/$VERSION
fi

echo "commiting summary"
ostree summary -u --repo=${REPO}

rm -rf build/commit build/commit-locales

echo "syncing"
sync
