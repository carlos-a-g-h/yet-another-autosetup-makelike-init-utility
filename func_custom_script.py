#!/usr/bin/python3.9

from pathlib import Path
from secrets import token_hex
from typing import Mapping,Optional

from utils import util_subproc
from utils import util_verif_str

_JOBNAME="custom-script"

def job(
		content:str,
		path_basedir:Path,
		varname:Optional[str]
	)->bool:

	print(
		"→ Running a custom script" "\n"
	)

	tmp_scr=Path(f"/tmp/script.{token_hex(16)}.sh")

	#varname_ok="CONFIG_FILE_WORKING_DIRECTORY"
	#if isinstance(varname,str):
	#	varname_ok=varname

	varname_ok={
		True:varname,
		False:"CONFIG_FILE_WORKING_DIRECTORY"
	}[isinstance(varname,str)]

	try:
		tmp_scr.parent.mkdir(exist_ok=True,parents=True)
		tmp_scr.write_text(
			"#!/usr/bin/bash" "\n"
			f"""export {varname_ok}="{path_basedir.absolute()}";""" "\n"
			f"""{content}"""
		)
		#print(
		#	"Written script\n{",
		#	tmp_scr.read_text(),"\n}"
		#)
	except Exception as exc:
		print(exc)
		return False


	ok=util_subproc([
		"bash",
		str(tmp_scr)
	])

	tmp_scr.unlink()

	return ok

def main(
		arguments:Mapping,
		path_basedir:Path
	)->bool:

	# custom-script:
	#   content:|
	#     ...

	content=util_verif_str(arguments.get("content"))
	if not isinstance(content,str):
		return False

	varname=util_verif_str(arguments.get("cfwd-as"))

	return (
		job(
			content,
			path_basedir,
			varname
		)
	)
