#!/bin/sh

export REPO=$1
export NAME=$2
export ARCH=$3
export VERSION=$4
export TAG=$5

OSTREE_ARGS="--repo=${REPO}"
GPG_ARGS=""
if [ "x${GPG_HOME}" != "x" ]; then
    GPG_ARGS="${COMMIT_ARGS} --gpg-homedir=${GPG_HOME}"
fi

for ORIG_BRANCH in `(cd ${REPO}/refs/heads/; echo  runtime/${NAME}${TAG}*/${ARCH}/${VERSION})`; do
    export NEW_BRANCH=`echo ${ORIG_BRANCH} | sed s/${TAG}//`;
    export COMMITMSG=`ostree show --repo=${REPO} ${ORIG_BRANCH} | tail -n +4 | head -n 1 | sed -e 's/^[ \t]*//'`

    if [ "x${GPG_KEY}" != "x" ]; then
        ostree gpg-sign ${OSTREE_ARGS} ${GPG_ARGS} "${ORIG_BRANCH}" "${GPG_KEY}"
    fi

    mkdir -p `dirname ${REPO}/refs/heads/${NEW_BRANCH}`
    touch ${REPO}/refs/heads/${NEW_BRANCH}
    ostree reset ${OSTREE_ARGS} ${NEW_BRANCH} ${ORIG_BRANCH}
done
