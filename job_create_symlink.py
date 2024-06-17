#!/usr/bin/python3.9

from pathlib import Path
from typing import Mapping

from utils import util_verif_str
from utils import util_verif_bool

_JOBNAME="create-link"

def job(
		path_orig:Path,
		path_dest:Path,
		link_indir:bool,
		quiet:bool=False,
	)->bool:

	path_dest_ok=path_dest

	if link_indir:
		if path_dest.exists():
			if not path_dest.is_dir():
				return False

		path_dest_ok=path_dest.joinpath(path_orig.name)
		if path_dest_ok.exists():
			return False

	if not quiet:
		print(
			"→ Creating symlink" "\n"
			"\t" f"From: {path_orig}" "\n"
			"\t" f"To: {path_dest_ok}" "\n"
		)

	if not path_orig.exists():
		return False

	if path_dest_ok.is_symlink():
		return False

	path_dest_ok.parent.mkdir(
		exist_ok=True,
		parents=True
	)

	try:
		path_dest_ok.symlink_to(
			path_orig
		)
	except Exception as exc:
		print(
			"Failed to create symlink:",
			exc
		)
		return False

	return (
		path_dest_ok.is_symlink()
	)

def main(
		arguments:Mapping
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
		Path(arg_orig).absolute(),
		Path(arg_dest).absolute(),
		arg_indir
	)

