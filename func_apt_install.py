#!/usr/bin/python3.9

from pathlib import Path
from typing import Mapping

from utils import util_verif_str
from utils import util_subproc

_JOBNAME="apt-install"

def job_type1(
		path_target:Path,
	)->bool:

	print(
		"→ Installing local package(s) using APT" "\n"
		"\t" f"Path: {path_target}" "\n"
	)

	full_command=["apt","install","-yy"]

	if path_target.is_file():

		if not path_target.suffix.lower()==".deb":
			return False
		if not path_target.stat().st_size>0:
			return False

		full_command.append(
			path_target.absolute()
		)

	if path_target.is_dir():

		at_least_one=False
		for fse in path_target.iterdir():
			if not fse.is_file():
				continue
			if not fse.suffix.lower()==".deb":
				continue
			if not fse.stat().st_size>0:
				continue

			if not at_least_one:
				at_least_one=True
			print(
				"\t" f"Detected: {fse.name}\n"
			)
			full_command.append(
				fse.absolute()
			)
	
		if not at_least_one:
			return False

	return (
		util_subproc(
			full_command,
			announce=False
		)
	)

def job_type2(names_raw:str)->bool:

	print(
		"→ Installing package(s) using APT" "\n"
	)

	full_command=["apt","install","-yy"]

	for name in names_raw.split():
		name_ok=util_verif_str(name)
		if not name_ok:
			continue

		print(
			"\t" f"Detected: {name_ok}\n"
		)

		full_command.append(name_ok)

	return (
		util_subproc(
			full_command,
			announce=False
		)
	)

def main(arguments:Mapping)->bool:

	# - apt-install:
	#     path: Path
	#     names: String

	arg_path_str=util_verif_str(
		arguments.get("path")
	)
	gave_path=isinstance(arg_path_str,str)

	arg_names=util_verif_str(
		arguments.get("names")
	)
	gave_names=isinstance(arg_names,str)

	if gave_path and (not gave_names):

		return (
			job_type1(
				Path(arg_path_str)
			)
		)

	if (not gave_path) and gave_names:

		return (
			job_type2(
				arg_names
			)
		)

	return False
