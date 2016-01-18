#!/bin/bash

BUILD=`pwd`/build
CHROOT=$BUILD/chroot
ROOT=$BUILD/root
VAR=$BUILD/var
SRC=`pwd`

XDG_APP_HELPER=`which xdg-app-helper 2> /dev/null`
LINUX_USER_CHROOT=`which linux-user-chroot 2> /dev/null`

declare -x LC_ALL=en_US.utf8
declare -x HOME=/app/buildhome
unset CFLAGS
unset CXXFLAGS
unset LDFLAGS
unset FFLAGS
unset ACLOCAL_FLAGS
unset ACLOCAL_PATH
unset CPLUS_INCLUDE_PATH
unset C_INCLUDE_PATH
unset GI_TYPELIB_PATH
unset INSTALL
unset LDFLAGS
unset LD_LIBRARY_PATH
unset PERL5LIB
unset PKG_CONFIG_PATH
unset PYTHONPATH
unset XDG_CONFIG_DIRS
unset XDG_DATA_DIRS
declare -x PATH="/usr/bin:/app/packages/bin"
if test -d buildhome/.ccache; then
    declare -x PATH="/app/buildhome/bin/ccache:$PATH"
fi

echo "builduser:x:`id  -u`:`id -u`:Build user:/app/packages:/sbin/nologin" >> $ROOT/usr/etc/passwd
echo "builduser:x:`id  -g`:" >> $ROOT/usr/etc/group

rc=1
if test "x${XDG_APP_HELPER}" != "x"; then
    $XDG_APP_HELPER -w -W -E -a $SRC -v $VAR $ROOT/usr env PATH="$PATH" /app/bin/cd.sh "$@"
    rc=$?;
elif test "x${LINUX_USER_CHROOT}" != "x"; then
    $LINUX_USER_CHROOT --unshare-ipc --unshare-pid --unshare-net --mount-bind /dev /dev --mount-proc /proc --mount-bind $ROOT/usr /usr --mount-bind $VAR /var --mount-bind $SRC /app --chdir /app $CHROOT "$@"
    rc=$?;
else
    echo "No containment helper found"
fi

cp -a $BUILD/passwd.orig $ROOT/usr/etc/passwd
cp -a $BUILD/group.orig $ROOT/usr/etc/group

exit $rc
