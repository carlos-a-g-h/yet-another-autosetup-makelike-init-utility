#!/usr/bin/python3.9

from pathlib import Path
from typing import Mapping,Optional

from utils import util_verif_str
from utils import util_verif_bool
from utils import util_create_symlink

_JOBNAME="new-app"

def job(
		stem:str,
		app_name:str,app_exec:str,app_categories:str,
		app_comment:Optional[str],
		app_terminal:bool,
		app_icon:Optional[str],
		app_mimetype:Optional[str],
		app_snotify:Optional[str],
		app_path_icon:Optional[str],
		app_path_link:Optional[str],
	)->bool:

	filepath=Path(
		f"/usr/share/applications/{stem}.desktop"
	)

	print(
		"→ Creating app" "\n"
		"\t" f"Filename: {filepath.stem}" "\n"
		"\t" f"App Name: {app_name}" "\n"
	)

	if filepath.exists():
		if not filepath.is_file():
			return False
		try:
			filepath.unlink()
		except Exception as e:
			print(e)
			return False

	content=(
		"[Desktop Entry]" "\n"
		"Version=1.0" "\n"
		"Type=Application" "\n"
		"Name=" f"""{app_name}""" "\n"
		"Exec=" f"""{app_exec}""" "\n"
		"Categories=" f"""{app_categories}"""
	)

	if isinstance(app_comment,str):
		content=(
			f"{content}" "\n"
			"Comment=" f"""{app_comment}"""
		)

	next={True:"true",False:"false"}[app_terminal]

	content=(
		f"{content}" "\n"
		f"Terminal={next}"
	)

	has_icon=isinstance(app_icon,str)

	if has_icon:
		content=(
			f"{content}" "\n"
			"Icon=" f"""{app_icon}"""
		)

	if isinstance(app_mimetype,str):
		content=(
			f"{content}" "\n"
			"MimeType=" f"""{app_mimetype}"""
		)

	next={True:"true",False:"false"}[app_snotify]

	content=(
		f"{content}" "\n"
		f"StartupNotify={next}"
	)

	try:
		filepath.write_text(content)
	except Exception as e:
		print(e)
		return False

	if isinstance(app_path_link,str):
		dirpath_link=Path(app_path_link)
		if not util_create_symlink(filepath,dirpath_link,True):
			print(
				"WARNING: Failed to create the link for the app"
			)

	if has_icon:
		if isinstance(app_path_icon,str):
			app_path_icon_pl=Path(app_path_icon)
			wutt=(
				not app_path_icon_pl.is_file()
			)
			if wutt:
				print(
					"WARNING: Failed to copy icon file" "\n"
					"\t" "The given path is not a file" "\n"
				)

			if not wutt:
				wutt=(
					app_path_icon_pl.stat().st_size>1024*1024*5
				)
				if wutt:
					print(
						"WARNING: Failed to copy icon file" "\n"
						"\t" "The file is too big (>5MB)" "\n"
					)

			if not wutt:
				try:
					Path(
						f"/usr/share/icons/{app_icon}{app_path_icon_pl.suffix}"
					).write_bytes(
						app_path_icon_pl.read_bytes()
					)
				except Exception as exc:
					print(
						"WARNING: Failed to copy icon file" "\n",
						exc
					)

	return True


def main(arguments:Mapping)->bool:

	arg_stem=util_verif_str(
		arguments.get("stem")
	)
	if not isinstance(arg_stem,str):
		return False

	arg_name=util_verif_str(
		arguments.get("name")
	)
	if not isinstance(arg_name,str):
		return False

	arg_exec=util_verif_str(
		arguments.get("exec")
	)
	if not isinstance(arg_exec,str):
		return False

	arg_categories=util_verif_str(
		arguments.get("categories")
	)
	if not isinstance(arg_categories,str):
		return False

	arg_comment=util_verif_str(
		arguments.get("comment")
	)

	arg_terminal=util_verif_bool(
		arguments.get("terminal"),
		fallback=False
	)

	arg_icon=util_verif_str(
		arguments.get("icon")
	)

	arg_mimetype=util_verif_str(
		arguments.get("mimetype")
	)

	arg_snotify=util_verif_bool(
		arguments.get("snotify"),
		fallback=False
	)

	arg_path_icon=util_verif_str(
		arguments.get("path-icon")
	)

	arg_path_link=util_verif_str(
		arguments.get("path-link")
	)

	return (
		job(
			arg_stem,
			arg_name,arg_exec,arg_categories,
			arg_comment,arg_terminal,arg_icon,arg_mimetype,arg_snotify,
			arg_path_icon,arg_path_link
		)
	)
