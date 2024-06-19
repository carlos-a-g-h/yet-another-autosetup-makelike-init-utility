#!/bin/bash

FILE_SRC="main.py"
FILE_OUT="yetup"
DIR_OUT="the-output"

mkdir the-output

python3 -m nuitka \
	--onefile \
	--onefile-no-compression \
	--follow-imports \
	"$FILE_SRC" \
	--output-dir="$DIR_OUT" \
	--output-filename="$FILE_OUT"

ls "$DIR_OUT"
