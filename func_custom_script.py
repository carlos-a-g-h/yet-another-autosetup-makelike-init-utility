#!/usr/bin/python3.9

from pathlib import Path
from secrets import token_hex
from typing import Mapping

from utils import util_subproc
from utils import util_verif_str

_JOBNAME="custom-script"

def job(content:str)->bool:

	print(
		"→ Running a custom script" "\n"
	)

	tmp_scr=Path(f"/tmp/script.{token_hex(16)}.sh")

	try:
		tmp_scr.parent.mkdir(exist_ok=True,parents=True)
		tmp_scr.write_text(content)
	except Exception as exc:
		print(exc)
		return False

	ok=util_subproc([
		"bash",
		str(tmp_scr)
	])

	tmp_scr.unlink()

	return ok

def main(arguments:Mapping)->bool:

	# custom-script:
	#   content:|
	#     ...

	content=util_verif_str(arguments.get("content"))
	if not isinstance(content,str):
		return False

	return (
		job(content)
	)
