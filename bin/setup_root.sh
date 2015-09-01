#!/bin/sh

if test -L build; then
    mkdir -p `readlink -f build`
else
    mkdir -p build
fi

BUILD=`pwd`/build
CHROOT=$BUILD/chroot
ROOT=$BUILD/root
VAR=$BUILD/var
IMAGE=`readlink -f $1`

rm -rf $ROOT $VAR $CHROOT
mkdir -p $ROOT $VAR $CHROOT

mkdir -p $CHROOT/var $CHROOT/usr $CHROOT/tmp $CHROOT/app $CHROOT/proc $CHROOT/dev
ln -s usr/lib $CHROOT/lib
ln -s usr/bin $CHROOT/bin
ln -s usr/sbin $CHROOT/sbin
ln -s /usr/etc $CHROOT/etc

(cd $ROOT; tar xvf $IMAGE > /dev/null; mv etc usr; mkdir -p $VAR/lib; mv var/lib/rpm $VAR/lib)

cp -a $ROOT/usr/etc/passwd $BUILD/passwd.orig
cp -a $ROOT/usr/etc/group $BUILD/group.orig
