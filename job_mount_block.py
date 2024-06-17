#!/usr/bin/python3.9

from pathlib import Path
from typing import Any,Mapping,Optional

from utils import util_verif_str
from utils import util_subproc

_JOBNAME="mount-blk"

def job(
		filepath:Path,
		dirpath:Path,
		mode:Optional[str]=None,
		isloop:bool=False,
		scrict:bool=False
	)->bool:

	print(
		"→ Mounting a file (or block device)" "\n"
		"\t" f"File: {filepath}" "\n"
		"\t" f"Dir: {dirpath}" "\n"
	)

	if not filepath.is_file():
		return False

	dirpath.mkdir(exist_ok=True,parents=True)

	if util_subproc([
		"mountpoint",str(dirpath)
	]):
		return False

	mount_command=["mount"]
	if mode=="rw" or mode=="ro" or isloop:
		mount_command.append("-o")
		if mode=="rw" or mode=="ro":
			mount_command.append(mode)
		if isloop:
			mount_command.append("loop")

	mount_command.extend([
		str(filepath),
		str(dirpath)
	])

	if not util_subproc(mount_command):
		return False

	return (
		util_subproc([
			"mountpoint",str(dirpath)
		])
	)

def main(arguments:Mapping)->bool:

	# mount-block:
	#   file: Path
	#   dest: Path
	#   mode: ro / rw / None
	#   isloop: true / false
	#   strict: true / false

	arg_file=util_verif_str(
		arguments.get("file")
	)
	if not arg_file:
		return False

	arg_dest=util_verif_str(
		arguments.get("dest")
	)
	if not arg_dest:
		return False

	arg_mode=util_verif_str(
		arguments.get("mode")
	)
	if isinstance(arg_mode,str):
		if not (arg_mode=="ro" or arg_mode=="rw"):
			arg_mode=None

	arg_isloop:Any=arguments.get("isloop",False)
	if not isinstance(arg_isloop,bool):
		arg_isloop=False

	return (
		job(
			Path(arg_file),
			Path(arg_dest),
			mode=arg_mode,
			isloop=arg_isloop
		)
	)

