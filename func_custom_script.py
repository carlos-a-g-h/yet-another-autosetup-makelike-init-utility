#!/usr/bin/python3.9

from pathlib import Path
from secrets import token_hex
from typing import Mapping

from utils import util_subproc
from utils import util_verif_str

_JOBNAME="custom-script"

def job(
		content:str,
		path_programdir:Path
	)->bool:

	print(
		"→ Running a custom script" "\n"
	)

	tmp_scr=path_programdir.joinpath(
		f"tmp.{token_hex(16)}.sh"
	)

	tmp_scr.write_text(content)

	ok=util_subproc([
		"bash",
		str(tmp_scr)
	])

	tmp_scr.unlink()

	return ok

def main(
		arguments:Mapping,
		path_programdir:Path
	)->bool:

	# custom-script:
	#   content:|
	#     ...

	content=util_verif_str(arguments.get("content"))
	if not isinstance(content,str):
		return False

	return (
		job(
			content,
			path_programdir
		)
	)
