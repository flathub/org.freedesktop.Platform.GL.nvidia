SPECS="$@"
export LC_ALL=C
rm -rf /tmp/dep
mkdir -p /tmp/dep

# Generate mapping package name => package name + full version + arch
for spec in $SPECS; do
   export spec
   bash -c "`rpmspec -q $spec --qf 'echo packages/RPMS/%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm > /tmp/dep/%{NAME}.pkg;'`";
done

ALL_SOURCES=

for spec in $SPECS; do
    SPEC_DEPENDENCIES=

    SOURCES=`rpmspec -P $spec | grep "^Source.*:" | awk '{ print $2 }' /dev/stdin`
    for i in $SOURCES; do
        if [ -e  specs/`basename $i` ]; then
            echo "packages/SOURCES/`basename $i`: specs/`basename $i`";
            echo -e "\tcp -f specs/`basename $i` packages/SOURCES/\n";
        else
            echo "packages/SOURCES/`basename $i`:";
            echo -e "\twget -P packages/SOURCES/ $i\n";
            ALL_SOURCES="$ALL_SOURCES packages/SOURCES/`basename $i`";
        fi
        SPEC_DEPENDENCIES="$SPEC_DEPENDENCIES packages/SOURCES/`basename $i`";
    done

    PATCHES=`rpmspec -P $spec | grep "^Patch.*:" | awk '{ print $2 }' /dev/stdin`
    SPEC_PATCHES=
    for i in $PATCHES; do
        echo "packages/SOURCES/`basename $i`: specs/`basename $i`";
        echo -e "\tcp -f specs/`basename $i` packages/SOURCES/\n";
        SPEC_DEPENDENCIES="$SPEC_DEPENDENCIES packages/SOURCES/`basename $i`";
    done

    PACKAGES=`rpmspec -q ${spec} --qf 'packages/RPMS/%{ARCH}/%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm '`
    BUILDREQS=`rpmspec -q ${spec} --buildrequires`
    BRS=""
    for br in $BUILDREQS; do
        BRS="$BRS `cat /tmp/dep/${br}.pkg`"
    done
    echo "$PACKAGES: $spec $BRS \$(SDK_BASE_IMAGE) $SPEC_DEPENDENCIES"
    echo "	-echo Building $spec"
    echo "	bin/setup.sh \$(SDK_BASE_IMAGE)"
    if [ "x${BRS}" != "x" ]; then
        echo "	bin/build.sh smart install -y $BRS"
    fi
    echo "	bin/build.sh rpmbuild --clean -bb $spec"
    echo "	bin/clear_root.sh"
    echo
    echo "`basename ${spec} .spec`: $PACKAGES"
    echo
    echo "only-`basename ${spec} .spec`: "
    echo "	-echo Building only $spec"
    echo "	bin/setup.sh \$(SDK_BASE_IMAGE)"
    if [ "x${BRS}" != "x" ]; then
        echo "	bin/build.sh smart install -y $BRS"
    fi
    echo "	bin/build.sh rpmbuild --clean -bb $spec"
    echo "	bin/clear_root.sh"
    echo
done

echo -e "sources: $ALL_SOURCES"
