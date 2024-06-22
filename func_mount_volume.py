#!/usr/bin/python3.9

from pathlib import Path
from typing import Mapping,Optional

from utils import util_path_fixer
from utils import util_subproc
from utils import util_verif_str

_JOBNAME="mount-vol"

def job(
		uuid:str,
		dirpath:Path,
		mode:Optional[str]=None,
		strict:bool=False
	)->bool:

	print(
		"→ Mounting a volume" "\n"
		"\t" f"UUID: {dirpath}" "\n"
		"\t" f"Dir: {dirpath}" "\n"
	)

	dirpath.mkdir(exist_ok=True,parents=True)

	if util_subproc([
		"mountpoint",str(dirpath)
	]):
		return False

	if not util_subproc([
		"blkid","-U",uuid
	]):
		return False

	mount_command=["mount"]
	if isinstance(mode,str):
		if mode=="rw" or mode=="ro":
			mount_command.extend(["-o",mode])

	mount_command.extend([
		"-U",uuid,str(dirpath)
	])

	ok=util_subproc(mount_command)
	if not strict:
		return ok

	if not ok:
		return False

	return (
		util_subproc([
			"mountpoint",str(dirpath)
		])
	)

def main(
		arguments:Mapping,
		path_basedir:Path
	)->bool:

	# mount-volume:
	#   uuid: String
	#   dest: Path
	#   mode: ro / rw / None
	#   strict: true / false

	arg_uuid=util_verif_str(
		arguments.get("uuid")
	)
	if not arg_uuid:
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

	return (
		job(
			arg_uuid,
			util_path_fixer(
				Path(arg_dest),
				path_basedir
			),
			mode=arg_mode
		)
	)

