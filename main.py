#!/usr/bin/python3.9

from pathlib import Path
from typing import Mapping,Optional

from utils import util_yaml_reader
from utils import util_verif_bool
from utils import util_verif_str
from utils import util_subproc

from func_custom_script import main as runjob_custom_script
from func_custom_script import _JOBNAME as _SYMBOL_JOBNAME_CUSTOM_SCRIPT

from func_write_file import main as runjob_write_file
from func_write_file import _JOBNAME as _SYMBOL_JOBNAME_WRITE_FILE

from func_create_symlink import main as runjob_create_symlink
from func_create_symlink import _JOBNAME as _SYMBOL_JOBNAME_CREATE_SYMLINK

from func_mount_block import main as runjob_mount_block
from func_mount_block import _JOBNAME as _SYMBOL_JOBNAME_MOUNT_BLOCK

from func_mount_directory import main as runjob_mount_directory
from func_mount_directory import _JOBNAME as _SYMBOL_JOBNAME_MOUNT_DIR

from func_mount_volume import main as runjob_mount_volume
from func_mount_volume import _JOBNAME as _SYMBOL_JOBNAME_MOUNT_VOLUME

from func_apt_install import main as runjob_apt_install
from func_apt_install import _JOBNAME as _SYMBOL_JOBNAME_APTINSTALL

from func_new_application import main as runjob_new_application
from func_new_application import _JOBNAME as _SYMBOL_JOBNAME_NEW_APP

_SYMBOL_TIME_SETTINGS="time-settings"
_SYMBOL_JOBLIST="joblist"

_KNOWN_JOBS=(
	_SYMBOL_JOBNAME_CUSTOM_SCRIPT,
	_SYMBOL_JOBNAME_WRITE_FILE,
	_SYMBOL_JOBNAME_CREATE_SYMLINK,
	_SYMBOL_JOBNAME_MOUNT_BLOCK,
	_SYMBOL_JOBNAME_MOUNT_DIR,
	_SYMBOL_JOBNAME_MOUNT_VOLUME,
	_SYMBOL_JOBNAME_APTINSTALL,
	_SYMBOL_JOBNAME_NEW_APP,
)

def runner_timesetup(data_time:Mapping):

	print("\n[ Time Settings ]")

	arg_timezone=util_verif_str(data_time.get("timezone"))
	if isinstance(arg_timezone,str):
		util_subproc([
			"timedatectl","set-timezone",arg_timezone
		])

def runner_joblist(
		data_joblist:list,
		path_programdir:Path,
		#target_tag:Optional[str]=None
	):

	print("\n[ Jobs List ]")

	#spec_tag=False
	#if isinstance(target_tag,str):
	#	spec_tag=True

	for step in data_joblist:
		if not isinstance(step,Mapping):
			continue
		if not len(step)==1:
			continue
		mainkey=list(step.keys())[0]
		if mainkey not in _KNOWN_JOBS:
			continue

		ok=False

		tag=util_verif_str(
			step.get(mainkey,{}).get("tag")
		)

		crucial=util_verif_bool(
			step.get(mainkey,{}).get("crucial",False)
		)

		hidden=util_verif_bool(
			step.get(mainkey,{}).get("hidden",False)
		)

		headline=(
			f"Job {mainkey}" "\n"
			"\t" f"crucial: {crucial}" "\n"
			"\t" f"hidden: {hidden}"
		)
		if isinstance(tag,str):
			headline=(
				f"{headline}" "\n"
				"\t" f"tag: {tag}"
			)

		if hidden:
			continue

		#print(headline)
		#if hidden and (not spec_tag):
		#	continue

		#if spec_tag:
		#	if not target_tag==tag:
		#		continue

		if mainkey==_SYMBOL_JOBNAME_CUSTOM_SCRIPT:
			ok=runjob_custom_script(step.get(mainkey),path_programdir)

		if mainkey==_SYMBOL_JOBNAME_WRITE_FILE:
			ok=runjob_write_file(step.get(mainkey))

		if mainkey==_SYMBOL_JOBNAME_CREATE_SYMLINK:
			ok=runjob_create_symlink(step.get(mainkey))

		if mainkey==_SYMBOL_JOBNAME_MOUNT_BLOCK:
			ok=runjob_mount_block(step.get(mainkey))

		if mainkey==_SYMBOL_JOBNAME_MOUNT_DIR:
			ok=runjob_mount_directory(step.get(mainkey))

		if mainkey==_SYMBOL_JOBNAME_MOUNT_VOLUME:
			ok=runjob_mount_volume(step.get(mainkey))

		if mainkey==_SYMBOL_JOBNAME_APTINSTALL:
			ok=runjob_apt_install(step.get(mainkey))

		if mainkey==_SYMBOL_JOBNAME_NEW_APP:
			ok=runjob_new_application(step.get(mainkey))

		if not ok:

			if crucial:
				print(
					"\nJob failed! Cannot go any further\n"
				)
				break

			print("\nJob failed!\n")

			continue

		print("\nJob Finished!\n")

def runner(
		data:Mapping,
		path_programdir:Path
	):

	# print(data)

	if _SYMBOL_TIME_SETTINGS in data.keys():
		if not isinstance(data[_SYMBOL_TIME_SETTINGS],Mapping):
			print(f"YAML Mapping expected in '{_SYMBOL_TIME_SETTINGS}'")
			return

		runner_timesetup(data[_SYMBOL_TIME_SETTINGS])

	if _SYMBOL_JOBLIST in data.keys():
		if not isinstance(data[_SYMBOL_JOBLIST],list):
			print(f"YAML List expected in '{_SYMBOL_JOBLIST}'")
			return

		runner_joblist(
			data[_SYMBOL_JOBLIST],
			path_programdir
		)

def command_run(path_config:Path)->int:

	the_custom_config=util_yaml_reader(path_config)

	if the_custom_config is None:
		print("Failed to read the custom config")
		return 1
	if len(the_custom_config)==0:
		print("Custom config not valid")
		return 1

	runner(
		the_custom_config,
		Path(sys_argv[0]).parent,
	)

	return 0

def command_help()->int:

	print(

		"\n"
		"# Config file structure (in YAML btw):" "\n\n"

		f"{_SYMBOL_TIME_SETTINGS}:" "\n"
			"\t" "timezone:" "\n"
			"\t\t" "# Any valid timezone listed in timedatectl" "\n"
			"\t\t" "# timedatectl (and systemd) must be installed in order for this to work" "\n"

		"\n"

		f"{_SYMBOL_JOBLIST}:" "\n"
		"\t" "# List of jobs to perform sequentially" "\n"
		"\t" f"# There are {len(_KNOWN_JOBS)} types of jobs:" "\n"

		"\n"

		"\t" f"- {_SYMBOL_JOBNAME_WRITE_FILE}: # Writes content to a text file" "\n"
		"\t\t" "dest: # Absolute path to a file" "\n"
		"\t\t" "content: # Text that you want to write" "\n"

		"\n"

		"\t" f"- {_SYMBOL_JOBNAME_CREATE_SYMLINK}: # Create symbolic link (absolute paths only)" "\n"
		"\t\t" "orig: # (Mandatory) Absolute path to a real file or directory" "\n"
		"\t\t" "dest: # (Mandatory) Absolute path to the destination path for the symlink" "\n"
		"\t\t" "indir: # Wether the destination path is a directory and the symlink has to be created as a child of that directory"

		"\n"

		"\t" f"- {_SYMBOL_JOBNAME_CUSTOM_SCRIPT}: # Run a custom bash script" "\n"
		"\t\t" "content: # A bash script (multiline recommended), nonzero exit status will be trated as a failure" "\n"

		"\n"

		"\t" f"- {_SYMBOL_JOBNAME_MOUNT_BLOCK}: # Mount a file or block device" "\n"
		"\t\t" "file: # (Mandatory) Absolute path to the block device file" "\n"
		"\t\t" "dest: # (Mandatory) Absolute path to the destination directory" "\n"
		"\t\t" "mode: # Mount mode (rw, ro). Leaving it blank means auto" "\n"

		"\n"

		"\t" f"- {_SYMBOL_JOBNAME_MOUNT_DIR}: # Bind mount of a directory (non-recursive)" "\n"
		"\t\t" "orig: # Absolute path to the directory that you want to mount" "\n"
		"\t\t" "dest: # Absolute path to the destination directory" "\n"

		"\n"

		"\t" f"- {_SYMBOL_JOBNAME_MOUNT_VOLUME}: # Mount a volume by its UUID" "\n"
		"\t\t" "uuid: # (Mandatory) UUID of the volume (partition) that you want to mount" "\n"
		"\t\t" "dest: # (Mandatory) Absolute path to the destination directory" "\n"
		"\t\t" "mode: # Mount mode (rw, ro). Leaving it blank means auto" "\n"

		"\n"

		"\t" f"- {_SYMBOL_JOBNAME_APTINSTALL}:" "\n"
			"\t\t" "# Install packages from remote sources OR local .DEB packages using APT" "\n"
			"\t\t" "# NOTE: You cannot do both things in the same job, you have to choose what to do" "\n"
		"\t\t" "path: # Path to a package or a directory (non-recursive)" "\n"
		"\t\t" "names: # Names of packages separated by a single space" "\n"

		"\n"

		"\t" f"- {_SYMBOL_JOBNAME_NEW_APP}: # Creates (or overwrites) a .DESKTOP file in /usr/share/applications" "\n"
		"\t\t" "stem: # Filename without the extension" "\n"
		"\t\t" "name: # (Mandatory) .DESKTOP Name" "\n"
		"\t\t" "exec: # (Mandatory) .DESKTOP Exec" "\n"
		"\t\t" "categories: # .DESKTOP Categories (Mandatory)" "\n"
		"\t\t" "comment: # .DESKTOP Comment" "\n"
		"\t\t" "terminal: # .DESKTOP Terminal (Bool, defaults to false)" "\n"
		"\t\t" "icon: # .DESKTOP Icon" "\n"
		"\t\t" "mimetype: # .DESKTOP MymeType" "\n"
		"\t\t" "snotify: # .DESKTOP StartupNotify (Bool, defaults to false)" "\n"
		"\t\t" "path-icon:" "\n"
			"\t\t\t" "# Image file path that will be copied to /usr/share/icons/" "\n"
			"\t\t\t" "# The filename will be the icon name + the file extension from the given path" "\n"
		"\t\t" "path-link:" "\n"
			"\t\t\t" "# Path to a new symlink" "\n"
			"\t\t\t" "# The path has to be a directory" "\n"

		"\n"

		"\t" "# Think of the jobs as functions: You can reuse any of the available jobs with different parameters as much as you want to match your specific needs" "\n\n"

		"\t" "# Additional fields for jobs:" "\n\n"

		"\t" "# 'tag' field: You can add the 'tag' field to any job to identify it at runtime, this is good for debugging and testing" "\n"
		"\t" "# 'crucial' field: Jobs marked as crucial will cancel the entire workflow in case of failure" "\n"
		"\t" "# 'hidden' field: Hidden jobs will be skipped when running the joblist"

		"\n"
	)

	return 0

if __name__=="__main__":

	from sys import argv as sys_argv
	from sys import exit as sys_exit

	if len(sys_argv)==1:

		print(
			"\n"
			"Usage" "\n"
			"-----" "\n"
			f"$ {Path(sys_argv[0]).name} [Command] (Args)" "\n\n"
			"Commands" "\n"
			"--------" "\n"
			"help → Shows the config file reference (it has no args)" "\n"
			"run → Runs a config file" "\n"
		)

		sys_exit(0)

	if sys_argv[1]=="help":

		sys_exit(
			command_help()
		)

	if sys_argv[1]=="run":

		if not len(sys_argv)>2:
			print("Missing: Config file path")
			sys_exit(1)

		sys_exit(
			command_run(
				Path(sys_argv[2])
			)
		)

	print("Unknown command")

	sys_exit(1)
