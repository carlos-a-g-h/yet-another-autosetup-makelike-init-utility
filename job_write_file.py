#!/usr/bin/python3.9

from pathlib import Path
from typing import Mapping

from utils import util_verif_str

_JOBNAME="write-file"

def job(
		path_dest:Path,
		content:str,
	):

	print(
		"→ Writing to a file" "\n"
		"\t" f"To: {path_dest}" "\n"
	)

	path_dest.parent.mkdir(exist_ok=True,parents=True)

	if path_dest.exists():
		if not path_dest.is_file():
			return False

	try:
		if path_dest.is_file():
			path_dest.unlink()

		path_dest.write_text(
			content.strip()
		)
	except Exception as exc:
		print(
			"\tError while writing to the file:",
			exc
		)
		return False

	return True

def main(arguments:Mapping)->bool:

	# write-file:
	#   dest: Path
	#   content: |
	#     ...

	path_dest_str=util_verif_str(
		arguments.get("dest")
	)
	if not path_dest_str:
		return False

	content=util_verif_str(arguments.get("content"))
	if not isinstance(content,str):
		return False

	return (
		job(
			Path(path_dest_str).absolute(),
			content
		)
	)
