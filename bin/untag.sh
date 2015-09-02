#!/bin/sh

export REPO=$1
export NAME=$2
export ARCH=$3
export VERSION=$4
export TAG=$5

COMMIT_ARGS="--repo=${REPO}"
if [ "x${GPG_KEY}" != "x" ]; then
    COMMIT_ARGS="${COMMIT_ARGS} --gpg-sign=${GPG_KEY}"
fi
if [ "x${GPG_HOME}" != "x" ]; then
    COMMIT_ARGS="${COMMIT_ARGS} --gpg-homedir=${GPG_HOME}"
fi

for ORIG_BRANCH in `(cd ${REPO}/refs/heads/; echo  runtime/${NAME}${TAG}*/${ARCH}/${VERSION})`; do
    export NEW_BRANCH=`echo ${ORIG_BRANCH} | sed s/${TAG}//`;
    export COMMITMSG=`ostree show --repo=${REPO} ${ORIG_BRANCH} | tail -n +4 | head -n 1 | sed -e 's/^[ \t]*//'`

    ostree commit ${COMMIT_ARGS} --tree=ref=${ORIG_BRANCH} -b ${NEW_BRANCH} -s "${COMMITMSG}"
done
