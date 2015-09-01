#!/bin/sh

USR=`mktemp -d`

tar -C $USR -xf $1

export LC_ALL=C
for i in $USR/bin/*; do
    j=`basename $i`
    echo -n "/usr/bin/$j /bin/$j /sbin/$j "
done

for lib in $USR/lib/*.so*; do
    if [ -f $lib ]; then
        chmod a+x $lib
        echo "$lib" | /usr/lib/rpm/find-provides | tr '\n' ' ';
    fi
done
if [ -d $USR/lib/perl5 ]; then
    find $USR/lib/perl5/ -type f | /usr/lib/rpm/perl.prov | tr '\n' ' '
fi
if [ -d $USR/lib/pkgconfig/ ]; then
    find $USR/lib/pkgconfig/ -type f -or -type l | /usr/lib/rpm/pkgconfigdeps.sh -P | tr '\n' ' '
fi

rm -rf $USR
