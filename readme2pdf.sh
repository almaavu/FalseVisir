#!/usr/bin/env bash

scname=$(basename -- "$(readlink -f -- "$0")")
scdir="$(dirname $(readlink -f $0))"

sudo apt install pandoc
pandoc $1 -s -o $1.pdf
