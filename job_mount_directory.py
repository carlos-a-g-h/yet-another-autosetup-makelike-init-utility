#!/usr/bin/python3.9

from pathlib import Path
from typing import Mapping

from utils import util_verif_str
from utils import util_subproc

_JOBNAME="mount-dir"

def job(
		dirpath_orig:Path,
		dirpath_dest:Path,
		strict:bool=False
	)->bool:

	print(
		"→ Mounting a directory" "\n"
		"\t" f"From: {dirpath_orig}" "\n"
		"\t" f"To: {dirpath_dest}" "\n"
	)

	if not dirpath_orig.is_dir():
		return False

	dirpath_dest.mkdir(exist_ok=True,parents=True)

	if util_subproc([
		"mountpoint",str(dirpath_dest)
	]):
		return False

	ok=util_subproc([
		"mount","--bind",
		str(dirpath_orig),
		str(dirpath_dest)
	])
	if not strict:
		return ok

	if not ok:
		return False

	return (
		util_subproc([
			"mountpoint",str(dirpath_dest)
		])
	)

def main(arguments:Mapping)->bool:

	# mount-dir:
	#   origin: Path
	#   dest: Path
	#   strict: true / false

	arg_origin=util_verif_str(
		arguments.get("orig")
	)
	if not arg_origin:
		return False

	arg_dest=util_verif_str(
		arguments.get("dest")
	)
	if not arg_dest:
		return False

	return (
		job(
			Path(arg_origin),
			Path(arg_dest)
		)
	)
