#!/bin/sh

DRIVER=$1
REPO=$2

EXTRACT_DIR=`mktemp -d /tmp/nvidia-extract.XXXXXXXXXX`
rm -rf $EXTRACT_DIR
$1 -x --target $EXTRACT_DIR

BASE=`basename $EXTRACT_DIR/libGL.so.*.*`
VERSION=${BASE#libGL.so.}

IMAGE_DIR=`mktemp -d /tmp/nvidia-image.XXXXXXXXXX`

mkdir -p $IMAGE_DIR/files
mkdir -p $IMAGE_DIR/files/tls

for i in libEGL.so libGLESv1_CM.so libGLESv2.so libGL.so libnvidia-cfg.so libnvidia-eglcore.so libnvidia-fbc.so libnvidia-glcore.so libnvidia-glsi.so libnvidia-gtk3.so libnvidia-ifr.so libnvidia-ml.so libnvidia-tls.so tls/libnvidia-tls.so; do
    mv $EXTRACT_DIR/$i.$VERSION $IMAGE_DIR/files/`dirname $i`
    ln -s `basename $i.$VERSION` $IMAGE_DIR/files/$i.1
done
ln -s libGLESv2.so.$VERSION $IMAGE_DIR/files/libGLESv2.so.2
ln -s libnvidia-gtk3.so.$VERSION $IMAGE_DIR/files/libnvidia-gtk3.so

rm -rf $EXTRACT_DIR

cat <<EOF >$IMAGE_DIR/metadata
[Runtime]
name=org.freedesktop.Platform.GL/x86_64/1.4
EOF

if [ ! -d ${REPO} ] ; then
    ostree  init --mode=archive-z2 --repo=${REPO}
fi
ostree commit --repo=${REPO} --owner-uid=0 --owner-gid=0 --no-xattrs --branch=runtime/org.freedesktop.Platform.GL/x86_64/1.4  -s "Nvidia driver ${VERSION}" $IMAGE_DIR

rm -rf $IMAGE_DIR
