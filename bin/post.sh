#!/bin/sh
touch -d @0 /usr/share/fonts
touch -d @0 /usr/share/fonts/*
fc-cache -fs
