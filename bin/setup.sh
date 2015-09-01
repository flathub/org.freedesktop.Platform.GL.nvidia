#!/bin/sh

mkdir -p packages/noarch
mkdir -p packages/x86_64

bin/setup_root.sh $1
bin/build.sh smart channel -y --add mydb type=rpm-sys name="RPM Database"
bin/build.sh smart channel -y --add noarch type=rpm-dir name="RPM Database" path=/app/packages/RPMS/noarch
bin/build.sh smart channel -y --add x86_64 type=rpm-dir name="RPM Database" path=/app/packages/RPMS/x86_64/
