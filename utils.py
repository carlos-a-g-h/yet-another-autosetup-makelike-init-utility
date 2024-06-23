#!/usr/bin/python3.9

from pathlib import Path

from subprocess import run as sub_run
from subprocess import PIPE as sub_PIPE
from time import sleep as time_sleep
from typing import Optional,Union,Mapping

from yaml import Loader as yaml_Loader
from yaml import load as yaml_load

def util_path_fixer(
		given_path:Path,
		base_path:Path
	)->Path:

	if given_path.is_absolute():
		return given_path

	return base_path.joinpath(given_path)

def util_yaml_reader(
		filepath:Path
	)->Optional[Union[list,Mapping]]:

	if not filepath.is_file():
		return None

	data:Optional[Union[list,Mapping]]=None
	try:
		data=yaml_load(
			filepath.read_text(),
			Loader=yaml_Loader
		)
	except Exception as e:
		print(e)
		return None

	return data

def util_verif_str(
		data:Optional[str],
		lowerit:bool=False
	)->Optional[str]:

	if not isinstance(data,str):
		return None

	data_ok=data.strip()
	if len(data_ok)==0:
		return None

	return data_ok

def util_verif_bool(
		data:Optional[Union[str,bool,int]],
		fallback:Optional[bool]=None
	)->Optional[bool]:

	if not isinstance(data,(str,bool,int)):
		return fallback

	if isinstance(data,int):
		if data==0:
			return False
		if data==1:
			return True
		return fallback

	if isinstance(data,str):
		data_ok=util_verif_str(data,True)
		if not isinstance(data_ok,str):
			return fallback

		if data_ok=="false":
			return False
		if data_ok=="true":
			return True

		return fallback

	return data

def util_create_symlink(
		path_orig:Path,
		path_dest:Path,
		link_indir:bool
	)->bool:

	path_dest_ok=path_dest

	if link_indir:
		if path_dest.exists():
			if not path_dest.is_dir():
				return False

		path_dest_ok=path_dest.joinpath(path_orig.name)
		if path_dest_ok.exists():
			return False

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

def util_subproc(
		command:list,
		announce:bool=True,
	)->bool:

	time_sleep(0.1)

	if announce:
		print(
			"Running command:\n$",
			command
		)

	proc=sub_run(
		command,
		stderr=sub_PIPE,
		stdout=sub_PIPE
	)
	rc:int=proc.returncode

	if announce:
		print("Script output {")

	stdout_ok:Optional[str]=util_verif_str(
		proc.stdout.decode()
	)
	if isinstance(stdout_ok,str):
		print(stdout_ok)

	stderr_ok:Optional[str]=util_verif_str(
		proc.stderr.decode()
	)
	if isinstance(stderr_ok,str):
		print(stderr_ok)

	if announce:
		print("} End of Script output")

	return (rc==0)
