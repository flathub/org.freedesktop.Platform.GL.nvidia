#!/bin/sh
smart install --urls $@ 2>&1 >/dev/null |  sed "s#file:///#/#"
