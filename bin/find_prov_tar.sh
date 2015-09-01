#!/bin/sh

USR=`mktemp -d`

tar -C $USR -xf $1
bin/find_prov.sh $USR
rm -rf $USR
