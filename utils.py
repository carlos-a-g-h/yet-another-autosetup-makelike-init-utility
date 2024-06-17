#!/usr/bin/python3.9

from pathlib import Path

from subprocess import run as sub_run
from subprocess import PIPE as sub_PIPE
from time import sleep as time_sleep
from typing import Optional,Union,Mapping

from yaml import Loader as yaml_Loader
from yaml import load as yaml_load


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

def util_subproc(command:list)->bool:

	time_sleep(0.1)

	print(
		"\nRunning command:\n$",
		command
	)

	proc=sub_run(
		command,
		stderr=sub_PIPE,
		stdout=sub_PIPE
	)
	rc:int=proc.returncode

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

	return (rc==0)