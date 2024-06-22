#!/usr/bin/python3.9

from pathlib import Path
from typing import Mapping

from utils import util_verif_str
from utils import util_verif_bool
from utils import util_create_symlink
from utils import util_path_fixer

_JOBNAME="create-link"

def job(
		path_orig:Path,
		path_dest:Path,
		link_indir:bool,
	)->bool:

	print(
		"→ Creating symlink" "\n"
		"\t" f"From: {path_orig}" "\n"
		"\t" f"To: {path_dest}" "\n"
	)

	return (
		util_create_symlink(
			path_orig,path_dest,
			link_indir
		)
	)

def main(
		arguments:Mapping,
		path_basedir:Path
	)->bool:

	# link-path:
	#   orig: Path
	#   dest: Path

	arg_orig=util_verif_str(
		arguments.get("orig")
	)
	if not arg_orig:
		return False

	arg_dest=util_verif_str(
		arguments.get("dest")
	)
	if not arg_dest:
		return False

	arg_indir=util_verif_bool(
		arguments.get("indir"),
		fallback=False
	)

	return job(
		util_path_fixer(
			Path(arg_orig),
			path_basedir
		),
		util_path_fixer(
			Path(arg_dest),
			path_basedir
		),
		arg_indir
	)

