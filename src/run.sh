Run() {
	IsExistCmd() { type "$1" > /dev/null 2>&1; }
	Install() { ! IsExistCmd "$1" && sudo apt -y install "$1"; }
	IsExistPkg() { dpkg -l | grep "$1" > /dev/null 2>&1; }
	InstallPkg() { ! IsExistPkg "$1" && sudo apt -y install "$1"; }
	RunBatch() { gimp --no-interface --console-messages --no-data --no-splash --batch-interpreter python-fu-eval --batch - < "$1"; }
	Install gimp
	InstallPkg gimp-python
	RunBatch "$(cd $(dirname $0); pwd)/save_xcf.py"
}
Run "$@"
